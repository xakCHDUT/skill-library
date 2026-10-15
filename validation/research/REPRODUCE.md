# Reproduce the research-skill validation

These instructions assume this public library has `skills/` and `validation/research/` directories. They do not require the private local review workspace. The immutable source file list and Git blob hashes are in `source-manifest.json`.

Use a new directory and Python 3.12. On Windows PowerShell, from this library's root:

```powershell
$LibraryRoot = (Get-Location).Path
python -m venv .validation-venv
$ValidationPython = Join-Path $LibraryRoot '.validation-venv/Scripts/python.exe'
& $ValidationPython -m pip install --index-url https://pypi.org/simple -r skills/statistical-analysis/validation/requirements-tested.txt

# Fetch only the two skills and necessary test infrastructure.
git clone --filter=blob:none --sparse https://github.com/K-Dense-AI/scientific-agent-skills.git upstream-validation
git -C upstream-validation sparse-checkout set skills/exploratory-data-analysis skills/statistical-analysis tests/exploratory-data-analysis tests/statistical-analysis tests/_contract
git -C upstream-validation checkout a1043ef544e3a100c28e70a736b6cf32554d0677
git -C upstream-validation apply (Join-Path $LibraryRoot 'validation/research/skill-changes.patch')
git -C upstream-validation apply (Join-Path $LibraryRoot 'validation/research/windows-test-compatibility.patch')

$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$env:MPLBACKEND = 'Agg'
Set-Location upstream-validation
& $ValidationPython -m pytest -q -p no:cacheprovider tests/exploratory-data-analysis
& $ValidationPython -m pytest -q -p no:cacheprovider tests/statistical-analysis
Set-Location $LibraryRoot
& $ValidationPython -m pytest -q -p no:cacheprovider skills/exploratory-data-analysis/validation
& $ValidationPython -m pytest -q -p no:cacheprovider skills/statistical-analysis/validation
```

The cone-mode sparse checkout includes root files and the immediate `tests/` files, including `tests/conftest.py` and `tests/skill-requirements.toml`. Run each skill's tests in its own process to avoid shared module-name collisions.

Expected Windows counts with the validated dependency snapshot:

- Upstream EDA suite after the two transparent Windows test fixes: 27 passed, 1 skipped because creating a direct symbolic link needs privilege on this machine.
- Upstream statistics suite: 32 passed.
- Published EDA additional regressions: 6 passed, including real Windows junction rejection for root/input/output and preservation of original JSON.
- Published statistics precision regression: 1 passed.
- Combined: 66 passed, 1 skipped. Subtests are reported separately, not added again.

`windows-test-compatibility.patch` only limits the POSIX mode assertion to POSIX and closes the test's own NumPy memory map before deleting its fixture. It does not suppress application failures. The original failing counts are retained in `validation.json`.

The dependency snapshot was tested on Windows Python 3.12; it is not a complete cross-platform lockfile. Optional Bayesian sampling was not tested. The 30 additional synthetic task checks and exact numerical results are preserved separately in each skill's `validation/synthetic-validation.json`; these are not counted as 30 extra pytest cases. From the library root, reproduce them with `python validation/research/reproduce_synthetic.py` in the same environment. The command creates only synthetic files and reports under `work/research-synthetic/` and makes no network calls.
