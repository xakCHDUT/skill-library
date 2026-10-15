# Notebook validation

Actual validation: 2026-10-15, Windows, Python 3.12. Both templates ran top to bottom in fresh isolated kernels, including a second clean run. All 17 assertions in `results.json` passed. Format validation also passed with Python UTF-8 mode.

The scaffold needs only Python's standard library. These extra packages are for executing the validation suite, not for creating a notebook:

```sh
python -m venv .venv
# Activate this disposable environment using your shell's normal command.
python -m pip install -r validation/requirements-windows-py312.lock.txt
python -m ipykernel install --sys-prefix --name skill-validation
python validation/test_notebooks.py --kernel skill-validation --report validation/results.json
```

The lock records the validated Windows/Python 3.12 environment. Other platforms may need their own dependency resolution and validation. If you already have a suitable kernel, pass its name instead. Tests create temporary synthetic notebooks and remove them afterward; no personal notebook is used.

Checks cover Unicode paths in a GBK parent environment, title retention, strict format/cell IDs, actual execution, independent arithmetic, fresh-kernel reproducibility, preservation of existing files, explicit replacement, and output relative to the invocation directory. Jupyter emitted its standard local TCP transport and Windows event-loop notices; execution completed successfully.
