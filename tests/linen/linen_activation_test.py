# Copyright 2023 The Flax Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for flax.linen.activation."""

import jax
import jax.numpy as jnp
from absl.testing import absltest
from jax import random
from jax._src.test_util import JaxTestCase

from flax import linen as nn

# Parse absl flags test_srcdir and test_tmpdir.
jax.config.parse_flags_with_absl()


class ActivationTest(JaxTestCase):
  def test_prelu(self):
    rng = random.key(0)
    key, skey_1, skey_2 = jax.random.split(rng, 3)
    x = jax.random.uniform(skey_1, (4, 6, 5)) - 0.5
    act = nn.PReLU()
    y, params = act.init_with_output(skey_2, x)
    expected_y = jnp.where(x < 0, x*act.negative_slope_init, x)
    init_negative_slope = params['params']['negative_slope']
    expected_negative_slope = jnp.array(act.negative_slope_init, dtype=jnp.float32)

    self.assertEqual(y.shape, x.shape)
    self.assertArraysAllClose(expected_y, y)
    self.assertArraysEqual(init_negative_slope, expected_negative_slope)


if __name__ == '__main__':
  absltest.main()
