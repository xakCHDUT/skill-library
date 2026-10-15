"""Exercise the skill's full-precision CI setting for small-unit outcomes."""
import numpy as np
import pingouin as pg
from scipy import stats

def test_small_unit_confidence_interval_retains_precision():
    a = np.array([10, 11, 13, 14, 15, 17, 19, 22], dtype=float) * 1e-6
    b = np.array([1, 3, 5, 8, 9, 12, 18, 25, 31], dtype=float) * 1e-6
    old = pg.options.get('round.column.CI95')
    try:
        pg.options['round.column.CI95'] = None
        ci = pg.ttest(a, b, correction=True)['CI95'].iloc[0]
        expected = stats.ttest_ind(a, b, equal_var=False).confidence_interval()
        np.testing.assert_allclose(ci, [expected.low, expected.high], atol=1e-18, rtol=1e-12)
        assert ci[0] < 0 < ci[1]
        assert ci[1] - ci[0] > 0
    finally:
        pg.options['round.column.CI95'] = old
