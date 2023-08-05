"""
.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de>
"""

import numpy as np
import pytest

from ...fields import ScalarField
from ...grids import UnitGrid
from .. import WavePDE


@pytest.mark.parametrize("dim", [1, 2])
def test_wave_consistency(dim):
    """ test some methods of the wave model """
    eq = WavePDE()
    assert isinstance(str(eq), str)
    assert isinstance(repr(eq), str)

    grid = UnitGrid([4] * dim)
    state = eq.get_initial_condition(ScalarField.random_uniform(grid))
    field = eq.evolution_rate(state)
    assert field.grid == grid
    rhs = eq._make_pde_rhs_numba(state)
    np.testing.assert_allclose(field.data, rhs(state.data, 0))
