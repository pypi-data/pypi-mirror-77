# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Generates adversarial neighbors.

This file provides the class(es) and the corresponding functional interface(s)
for generating adversarial neighbors.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

from absl import logging
from neural_structured_learning.lib import abstract_gen_neighbor as abs_gen
from neural_structured_learning.lib import utils
import tensorflow as tf


def _apply_feature_constraints(feature, min_value, max_value):
  """Constrains `feature` to be between `min_value` and `max_value`."""
  if min_value is not None:
    feature = tf.math.maximum(feature, min_value)
  if max_value is not None:
    feature = tf.math.minimum(feature, max_value)
  return feature


class _GenAdvNeighbor(abs_gen.GenNeighbor):
  """Class for generating adversarial neighbors based on gradient-based methods.

  The core of this class implements the projected gradient descent (PGD)
  operation:
  ```
  adv_neighbor = input_features
  iterations = 10  # Number of iterations to run PGD.
  for _ in range(iterations):
    grad = gradient(adv_neighbor)
    adv_neighbor = adv_neighbor + adv_step_size * grad
    adv_neighbor = project(adv_neighbor)
  ```
  where `adv_step_size` is the step size (analogous to learning rate) for
  searching/calculating adversarial neighbor, `gradient(x)` calculates the
  gradient of the model at `x`, and `project(v)` projects the vector `v` onto
  the epsilon ball.

  Attributes:
    labeled_loss: a scalar (`tf.float32`) tensor calculated from true labels (or
      supervisions).
    adv_config: a `nsl.configs.AdvNeighborConfig` object.
    raise_invalid_gradient: (optional) a Boolean flag indicating whether to
      raise an error when gradients cannot be computed on some input features.
      There are three cases where gradients cannot be computed:  (1) The feature
        is a `tf.SparseTensor`. (2) The feature is in a non-differentiable
        `tf.DType`, like string or integer. (3) The feature is not involved in
        loss computation.  If set to False, those input without gradient will be
        ignored silently and not perturbed. (default=False)
    pgd_model_fn: the model function. Takes in the input_features and produces a
      prediction. This is required for PGD with more than one step.
    pgd_loss_fn: the loss function. Calculates loss between prediction and
      ground truth.
  """

  def __init__(self,
               labeled_loss,
               adv_config,
               raise_invalid_gradient=False,
               gradient_tape=None,
               pgd_model_fn=None,
               pgd_loss_fn=None):
    self._labeled_loss = labeled_loss
    self._adv_config = adv_config
    self._raise_invalid_gradient = raise_invalid_gradient
    self._gradient_tape = gradient_tape
    self._pgd_model_fn = pgd_model_fn
    self._pgd_loss_fn = pgd_loss_fn

  def _compute_gradient(self, loss, dense_features, gradient_tape=None):
    """Computes the gradient given a loss and dense features."""
    feature_values = list(dense_features.values())
    if gradient_tape is None:
      grads = tf.gradients(loss, feature_values)
    else:
      grads = gradient_tape.gradient(loss, feature_values)

    # The order of elements returned by .values() and .keys() are guaranteed
    # corresponding to each other.
    keyed_grads = dict(zip(dense_features.keys(), grads))

    invalid_grads, valid_grads = self._split_dict(keyed_grads,
                                                  lambda grad: grad is None)
    # Two cases that grad can be invalid (None):
    # (1) The feature is not differentiable, like strings or integers.
    # (2) The feature is not involved in loss computation.
    if invalid_grads:
      if self._raise_invalid_gradient:
        raise ValueError('Cannot perturb features ' + str(invalid_grads.keys()))
      logging.log_first_n(logging.WARNING, 'Cannot perturb features %s', 1,
                          invalid_grads.keys())

    # Guards against numerical errors. If the gradient is malformed (inf, -inf,
    # or NaN) on a dimension, replace it with 0, which has the effect of not
    # perturbing the original sample along that perticular dimension.
    return tf.nest.map_structure(
        lambda g: tf.where(tf.math.is_finite(g), g, tf.zeros_like(g)),
        valid_grads)

  # The _compose_as_dict and _decompose_as functions are similar to
  # tf.nest.{flatten, pack_sequence_as} except that the composed representation
  # is a dictionary of (name, value) pairs instead of a list of values. The
  # names are needed for joining values from different inputs (e.g. input
  # features and feature masks) with possibly missing values (e.g. no mask for
  # some features).
  def _compose_as_dict(self, inputs):
    if isinstance(inputs, collections.Mapping):
      return inputs
    elif isinstance(inputs, (tuple, list)):
      return dict(enumerate(inputs))  # index -> value
    else:
      return {'': inputs} if inputs is not None else {}

  def _decompose_as(self, structure, values):
    if isinstance(structure, collections.Mapping):
      return values
    elif isinstance(structure, (tuple, list)):
      return [values[index] for index in range(len(structure))]
    else:
      return values[''] if structure is not None else None

  def _split_dict(self, dictionary, predicate_fn):
    """Splits `dictionary` into 2 by bool(predicate_fn(key, value))."""
    positives, negatives = {}, {}
    for key, value in dictionary.items():
      if predicate_fn(value):
        positives[key] = value
      else:
        negatives[key] = value
    return positives, negatives

  def gen_neighbor(self, input_features, pgd_labels=None):
    """Generates adversarial neighbors and the corresponding weights.

    This function perturbs only *dense* tensors to generate adversarial
    neighbors. No perturbation will be applied on sparse tensors  (e.g., string
    or int). Therefore, in the generated adversarial neighbors, the values of
    these sparse tensors will be kept the same as the input_features. In other
    words, if input_features is a dictionary mapping feature names to tensors,
    the dense features will be perturbed and the values of sparse features will
    remain the same.

    Arguments:
      input_features: a dense (float32) tensor, a list of dense tensors, or a
        dictionary of feature names and dense tensors. The shape of the
        tensor(s) should be either:
        (a) pointwise samples: [batch_size, feat_len], or
        (b) sequence samples: [batch_size, seq_len, feat_len]
      pgd_labels: the labels corresponding to each input. This should have shape
        `[batch_size, 1]`. This is required for PGD-generated adversaries, and
        unused otherwise.

    Returns:
      adv_neighbor: the perturbed example, with the same shape and structure as
        input_features
      adv_weight: a dense (float32) tensor with shape of [batch_size, 1],
        representing the weight for each neighbor

    Raises:
      ValueError: if some of the `input_features` cannot be perturbed due to
        (a) it is a `tf.SparseTensor`,
        (b) it has a non-differentiable type like string or integer, or
        (c) it is not involved in loss computation.
        This error is suppressed if `raise_invalid_gradient` is set to False
        (which is the default).
    """
    loss = self._labeled_loss
    gradient_tape = self._gradient_tape

    # Composes both features and feature_masks to dictionaries, so that the
    # feature_masks can be looked up by key.
    features = self._compose_as_dict(input_features)
    dense_original_features, sparse_original_features = self._split_dict(
        features, lambda feature: isinstance(feature, tf.Tensor))
    feature_masks = self._compose_as_dict(self._adv_config.feature_mask)
    feature_min = self._compose_as_dict(self._adv_config.clip_value_min)
    feature_max = self._compose_as_dict(self._adv_config.clip_value_max)
    if sparse_original_features:
      sparse_keys = str(sparse_original_features.keys())
      if self._raise_invalid_gradient:
        raise ValueError('Cannot perturb non-Tensor input: ' + sparse_keys)
      logging.log_first_n(logging.WARNING,
                          'Cannot perturb non-Tensor input: %s', 1, sparse_keys)
    dense_features = dense_original_features
    for t in range(self._adv_config.pgd_iterations):
      keyed_grads = self._compute_gradient(loss, dense_features, gradient_tape)
      masked_grads = {
          key: utils.apply_feature_mask(grad, feature_masks.get(key, None))
          for key, grad in keyed_grads.items()
      }

      unit_perturbations = utils.maximize_within_unit_norm(
          masked_grads, self._adv_config.adv_grad_norm)
      perturbations = tf.nest.map_structure(
          lambda t: t * self._adv_config.adv_step_size, unit_perturbations)
      # Clip perturbations into epsilon ball here. Note that this ball is
      # centered around the original input point.
      diff = {}
      bounded_diff = {}
      for key, perturb in perturbations.items():
        # Only include features for which perturbation occurred. There is
        # nothing to project for features without perturbations.
        diff[key] = dense_features[key] + perturb - dense_original_features[key]
      if self._adv_config.pgd_epsilon is not None:
        bounded_diff = utils.project_to_ball(diff, self._adv_config.pgd_epsilon,
                                             self._adv_config.adv_grad_norm)
      else:
        bounded_diff = diff
      # Backfill the rest of the dense features.
      for key, feature in dense_features.items():
        if key not in bounded_diff:
          bounded_diff[key] = feature - dense_original_features[key]
      adv_neighbor = dict(sparse_original_features)
      for key, feature in dense_original_features.items():
        adv_neighbor[key] = tf.stop_gradient(
            _apply_feature_constraints(
                feature +
                bounded_diff[key] if key in perturbations else feature,
                feature_min.get(key, None), feature_max.get(key, None)))

      # Update for the next iteration.
      if t < self._adv_config.pgd_iterations - 1:
        inputs_t = self._decompose_as(input_features, adv_neighbor)
        # Compute the new loss to calculate gradients with.
        features = self._compose_as_dict(inputs_t)
        dense_features, _ = self._split_dict(
            features, lambda feature: isinstance(feature, tf.Tensor))
        if gradient_tape is not None:
          with gradient_tape:
            # Gradient calculated against dense features only.
            gradient_tape.watch(dense_features)
            loss = self._pgd_loss_fn(pgd_labels, self._pgd_model_fn(inputs_t))
        else:
          loss = self._pgd_loss_fn(pgd_labels, self._pgd_model_fn(inputs_t))

    # Converts the perturbed examples back to their original structure.
    adv_neighbor = self._decompose_as(input_features, adv_neighbor)

    batch_size = tf.shape(list(features.values())[0])[0]
    adv_weight = tf.ones([batch_size, 1])

    return adv_neighbor, adv_weight


def gen_adv_neighbor(input_features,
                     labeled_loss,
                     config,
                     raise_invalid_gradient=False,
                     gradient_tape=None,
                     pgd_model_fn=None,
                     pgd_loss_fn=None,
                     pgd_labels=None):
  """Generates adversarial neighbors for the given input and loss.

  This function implements the following operation:
  `adv_neighbor = input_features + adv_step_size * gradient`
  where `adv_step_size` is the step size (analogous to learning rate) for
  searching/calculating adversarial neighbor.

  Arguments:
    input_features: a dense (float32) tensor, a list of dense tensors, or a
      dictionary of feature names and dense tensors. The shape of the tensor(s)
      should be either:
      (a) pointwise samples: `[batch_size, feat_len]`, or
      (b) sequence samples: `[batch_size, seq_len, feat_len]`. Note that only
        dense (`float`) tensors in `input_features` will be perturbed and all
        other features (`int`, `string`, or `SparseTensor`) will be kept as-is
        in the returning `adv_neighbor`.
    labeled_loss: A scalar tensor of floating point type calculated from true
      labels (or supervisions).
    config: A `nsl.configs.AdvNeighborConfig` object containing the following
      hyperparameters for generating adversarial samples.
      - 'feature_mask': mask (with 0-1 values) applied on the graident.
      - 'adv_step_size': step size to find the adversarial sample.
      - 'adv_grad_norm': type of tensor norm to normalize the gradient.
    raise_invalid_gradient: (optional) A Boolean flag indicating whether to
      raise an error when gradients cannot be computed on any input feature.
      There are three cases where this error may happen: (1) The feature is a
        `SparseTensor`. (2) The feature has a non-differentiable `dtype`, like
        string or integer. (3) The feature is not involved in loss computation.
        If set to `False` (default), those inputs without gradient will be
        ignored silently and not perturbed.
    gradient_tape: A `tf.GradientTape` object watching the calculation from
      `input_features` to `labeled_loss`. Can be omitted if running in graph
      mode.
    pgd_model_fn: The model to generate adversaries for. Generates predictions
      for a given set of inputs, in the shape of `input_features`.
    pgd_loss_fn: The loss function. Takes samples of labels and a model
      predictions.
    pgd_labels: labels for the input features. This should have shape
      `[batch_size, 1]`. Required to generate adversaries with PGD, unused
      otherwise.

  Returns:
    adv_neighbor: The perturbed example, with the same shape and structure as
      `input_features`.
    adv_weight: A dense `Tensor` with shape of `[batch_size, 1]`,
      representing the weight for each neighbor.

  Raises:
    ValueError: In case of `raise_invalid_gradient` is set and some of the input
      features cannot be perturbed. See `raise_invalid_gradient` for situations
      where this can happen.
  """
  adv_helper = _GenAdvNeighbor(
      labeled_loss,
      config,
      raise_invalid_gradient,
      gradient_tape,
      pgd_model_fn=pgd_model_fn,
      pgd_loss_fn=pgd_loss_fn)
  return adv_helper.gen_neighbor(input_features, pgd_labels)
