"""Independent deterministic synthetic tasks, with numeric and file invariants."""
from pathlib import Path
import csv, hashlib, importlib.metadata, json, math, os, subprocess, sys
library = Path(__file__).resolve().parents[2]
root = Path.cwd() / 'work/research-synthetic'
root.mkdir(parents=True, exist_ok=True)
area = root / 'synthetic-task'
area.mkdir(exist_ok=True)
os.environ.update(PYTHONDONTWRITEBYTECODE='1', MPLBACKEND='Agg', MPLCONFIGDIR=str(root / 'mpl-cache'))
eda = library / 'skills/exploratory-data-analysis/scripts'
checks = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append({'name': name, 'passed': True})
def cli(script, *arguments, output=None, expected=0):
    command = [sys.executable, '-B', '-S', str(eda / script), *arguments, '--root', str(area)]
    if output:
        command += ['--output', output]
        if expected == 0:
            command += ['--force']
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    check('cli:' + script + ':' + str(output or expected), result.returncode == expected)
    if expected == 0 and output and output.endswith('.json'):
        return json.loads((area / output).read_text(encoding='utf-8'))
    return result

raw = area / 'study.csv'
rows = []
for i in range(12):
    rows.append([f'synthetic-person-{i if i != 6 else 0}', 'A' if i < 6 else 'B', 'train' if i < 6 else 'test', f'2026-01-{i+1:02}', '' if i == 4 else 'NA' if i == 9 else 1000 if i == 11 else i+1])
with raw.open('w', encoding='utf-8', newline='') as stream:
    writer = csv.writer(stream)
    writer.writerow(['subject', 'group', 'split', 'date', 'measurement'])
    writer.writerows(rows)
before = hashlib.sha256(raw.read_bytes()).hexdigest()
profile = cli('tabular_profile.py', 'study.csv', '--missing-token', 'NA', output='profile.json')['analysis']
check('profile-scans-12-synthetic-rows', profile['rows_scanned'] == 12)
check('profile-does-not-truncate-small-input', not profile['row_limit_reached'])
numeric = profile['columns'][-1]
check('two-explicit-missing-values-counted', numeric['missing_count'] == 2)
check('numeric-mean-and-median-recomputed', math.isclose(numeric['numeric_aggregates']['mean'], 105.1) and numeric['numeric_aggregates']['median'] == 6.5)
check('profile-preserves-raw-identifiers', 'synthetic-person' not in json.dumps(profile))
audit = cli('missingness_leakage_audit.py', 'study.csv', '--missing-token', 'NA', '--entity-column', 'subject', '--group-column', 'group', '--split-column', 'split', '--time-column', 'date', output='audit.json')['analysis']
check('detects-one-cross-split-subject', audit['leakage_audit']['entity_tokens_in_multiple_splits'] == 1)
distribution = cli('distribution_sensitivity.py', 'study.csv', '--column', 'measurement', '--missing-token', 'NA', output='distribution.json')['analysis']
check('flags-planted-outlier-without-removal', distribution['columns'][0]['outlier_sensitivity']['outside_iqr_fence_count_in_sample'] == 1)
cli('eda_analyzer.py', 'study.csv', '--missing-token', 'NA', output='report.md')
cli('report_scaffold.py', '--input', 'study.csv', '--analysis-date', '2026-10-15', output='scaffold.md')
check('eda-does-not-change-source', hashlib.sha256(raw.read_bytes()).hexdigest() == before)
cap = cli('tabular_profile.py', 'study.csv', '--max-rows', '5', output='prefix.json')['analysis']
check('prefix-cap-explicit', cap['rows_scanned'] == 5 and cap['row_limit_reached'])
(area / 'broken.csv').write_text('x,y\n1,2,3\n', encoding='utf-8')
cli('tabular_profile.py', 'broken.csv', expected=2)
cli('tabular_profile.py', 'missing.csv', expected=2)
(area / 'invalid.json').write_text('{"x": NaN}', encoding='utf-8')
cli('eda_analyzer.py', 'invalid.json', expected=2)
json_raw = area / 'raw.json'
json_raw.write_text('{"values": [1, 2, 3]}', encoding='utf-8')
json_before = json_raw.read_bytes()
cli('eda_analyzer.py', 'raw.json', '--force', output='raw.json', expected=2)
check('force-never-overwrites-raw-json', json_raw.read_bytes() == json_before)

import numpy as np
import pandas as pd
import pingouin as pg
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.power import tt_ind_solve_power
import matplotlib.pyplot as plt
sys.path.insert(0, str(library / 'skills/statistical-analysis/scripts'))
import assumption_checks as ac
a = np.array([10, 11, 13, 14, 15, 17, 19, 22], dtype=float)
b = np.array([1, 3, 5, 8, 9, 12, 18, 25, 31], dtype=float)
pg.options['round.column.CI95'] = None
result = pg.ttest(a, b, correction=True)
delta = float(a.mean() - b.mean())
variance_a, variance_b = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
se = math.sqrt(variance_a + variance_b)
df = (variance_a + variance_b)**2 / (variance_a**2/(len(a)-1) + variance_b**2/(len(b)-1))
t = delta / se
p = float(2 * stats.t.sf(abs(t), df))
ci = delta + np.array([-1, 1]) * stats.t.ppf(.975, df) * se
check('welch-t-recomputed-from-means-variances', math.isclose(float(result['T'].iloc[0]), t, rel_tol=1e-12))
check('welch-p-and-df-match-independent-calculation', math.isclose(float(result['p_val'].iloc[0]), p, rel_tol=1e-12) and math.isclose(float(result['dof'].iloc[0]), df, rel_tol=1e-12))
check('welch-ci-matches-independent-calculation', bool(np.allclose(result['CI95'].iloc[0], ci, atol=1e-12)))
pooled_sd = math.sqrt(((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2))
d = float(pg.compute_effsize(a, b, eftype='cohen'))
check('signed-effect-size-recomputed', math.isclose(d, delta/pooled_sd, rel_tol=1e-12))
normality = ac.check_normality(np.r_[a, np.nan, np.nan], plot=False)
check('missing-observations-counted', normality['n_missing'] == 2 and normality['n'] == len(a))
for invalid in ([1, 2], [1, np.inf, 3], [np.nan, np.nan, np.nan], [3, 3, 3]):
    try:
        ac.check_normality(invalid, plot=False)
    except ValueError:
        pass
    else:
        raise AssertionError('invalid normality input accepted')
checks.append({'name': 'undersized-infinite-missing-constant-inputs-rejected', 'passed': True})
x = np.linspace(-2, 2, 60)
design = sm.add_constant(x)
noise = np.sin(np.arange(60) * 1.17)
noise = noise - design @ np.linalg.lstsq(design, noise, rcond=None)[0]
y = 2 + 3 * x + noise
model = sm.OLS(y, design).fit()
check('ols-recovers-designed-intercept-and-slope', bool(np.allclose(model.params, [2, 3], atol=1e-12)))
old_show = plt.show
plt.show = lambda: plt.savefig(area / 'ols-diagnostics.png', dpi=150)
try:
    diag = ac.check_regression_diagnostics(model, plot=True)
finally:
    plt.show = old_show
check('diagnostics-do-not-claim-independent-observations', diag['autocorrelation']['ok'] is None and diag['autocorrelation']['statistic'] is None)
check('diagnostic-figure-created-and-closed', (area / 'ols-diagnostics.png').stat().st_size > 10000 and not plt.get_fignums())
n = math.ceil(tt_ind_solve_power(effect_size=.5, alpha=.05, power=.8, ratio=1))
check('planning-sample-size-rounds-up-to-64-per-arm', n == 64)
versions = {name: importlib.metadata.version(name) for name in ['numpy', 'pandas', 'scipy', 'statsmodels', 'pingouin', 'matplotlib', 'h5py', 'biopython', 'pillow', 'tifffile', 'polars']}
report = {'synthetic_data_only': True, 'network_calls': 0, 'checks': checks, 'passed': len(checks), 'versions': versions, 'statistical_results': {'mean_difference': delta, 'welch_t': t, 'degrees_of_freedom': df, 'p_value': p, 'ci95': ci.tolist(), 'signed_cohen_d': d, 'planned_n_per_group': n}, 'eda_profile': {'rows_scanned': profile['rows_scanned'], 'numeric_column': numeric}}
(root / 'synthetic-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
print(json.dumps({'passed': len(checks), 'statistical_results': report['statistical_results'], 'numeric_profile': numeric}, ensure_ascii=False))
