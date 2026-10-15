"""Portable regression checks. Use a disposable environment with nbformat/nbclient/ipykernel."""
import argparse
import copy
import json
import math
import os
from pathlib import Path
import random
import statistics
import subprocess
import sys
import tempfile
import warnings

import nbformat
from nbclient import NotebookClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kernel', default='python3')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    skill = Path(__file__).resolve().parents[1]
    cli = skill / 'scripts/new_notebook.py'
    checks = []
    def check(name, condition):
        checks.append({'name': name, 'passed': bool(condition)})
        if not condition:
            raise AssertionError(name)
    with tempfile.TemporaryDirectory(prefix='notebook-validation-') as temp:
        cwd = Path(temp)
        def run(*arguments):
            env = dict(os.environ, PYTHONIOENCODING='gbk')
            return subprocess.run([sys.executable, str(cli), *arguments], cwd=cwd,
                                  env=env, capture_output=True, text=True, encoding='utf-8')
        for kind in ('experiment', 'tutorial'):
            output = cwd / (kind + '-中文-🧪.ipynb')
            result = run('--kind', kind, '--title', '中文实验🧪', '--out', str(output))
            check(kind + ': Unicode paths succeed with GBK parent environment', result.returncode == 0 and output.exists())
            with warnings.catch_warnings():
                warnings.simplefilter('error')
                notebook = nbformat.read(output, as_version=4)
                nbformat.validate(notebook)
            check(kind + ': schema and explicit unique cell IDs', len({c.id for c in notebook.cells}) == len(notebook.cells))
            check(kind + ': Unicode title retained', '中文实验🧪' in notebook.cells[0].source)
            clean = copy.deepcopy(notebook)
            executed = NotebookClient(notebook, timeout=60, kernel_name=args.kernel,
                                      resources={'metadata': {'path': str(cwd)}}).execute()
            code = [c for c in executed.cells if c.cell_type == 'code']
            check(kind + ': all code cells execute', all(c.execution_count is not None and not any(o.output_type == 'error' for o in c.outputs) for c in code))
            # Check meaning, not merely execution: compare the template results to independent arithmetic.
            import ast
            last = ast.literal_eval(code[-1].outputs[-1].data['text/plain'])
            if kind == 'experiment':
                rng = random.Random(7)
                values = [rng.random() for _ in range(20)]
                valid = last['seed'] == 7 and math.isclose(last['mean'], statistics.fmean(values)) and math.isclose(last['range'], max(values)-min(values))
            else:
                valid = last == {'min': 0.0, 'max': 1.0}
            check(kind + ': output agrees with independent arithmetic', valid)
            second = NotebookClient(clean, timeout=60, kernel_name=args.kernel,
                                    resources={'metadata': {'path': str(cwd)}}).execute()
            check(kind + ': fresh kernel rerun is deterministic', [c.outputs for c in code] == [c.outputs for c in second.cells if c.cell_type == 'code'])
            before = output.read_bytes()
            refused = run('--title', 'replacement', '--out', str(output))
            check(kind + ': existing output preserved', refused.returncode != 0 and before == output.read_bytes())
            forced = run('--title', 'replacement', '--out', str(output), '--force')
            check(kind + ': explicit replacement succeeds', forced.returncode == 0 and 'replacement' in nbformat.read(output, as_version=4).cells[0].source)
        default = run('--title', 'Working directory')
        check('default output belongs to calling directory', default.returncode == 0 and (cwd / 'output/jupyter-notebook/working-directory.ipynb').exists())
    report = {'date': '2026-10-15', 'test_type': 'actual_cli_schema_and_isolated_kernel_execution',
              'passed': len(checks), 'failed': 0, 'checks': checks}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': len(checks), 'failed': 0}))


if __name__ == '__main__':
    main()
