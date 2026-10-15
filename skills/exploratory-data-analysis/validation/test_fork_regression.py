"""Regression tests for the reviewed portable fork; synthetic local files only."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import _common

@pytest.mark.parametrize('script,prefix', [('eda_analyzer.py', []), ('capability_manifest.py', ['inspect'])])
def test_force_cannot_replace_original_json(script, prefix):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / 'study.json'
        data = b'{"values": [1, 2, 3]}'
        raw.write_bytes(data)
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS / script), *prefix, 'study.json', '--root', str(root), '--output', 'study.json', '--force'], capture_output=True, text=True)
        assert result.returncode == 2
        assert raw.read_bytes() == data
        assert 'original input' in result.stderr

@pytest.mark.parametrize('operation', ['input', 'output', 'root'])
def test_directory_alias_is_rejected_before_resolution(operation):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        actual = root / 'real'
        actual.mkdir()
        (actual / 'study.csv').write_text('value\n1\n2\n', encoding='utf-8')
        link = root / 'alias'
        if os.name == 'nt':
            import _winapi
            _winapi.CreateJunction(str(actual), str(link))
        else:
            link.symlink_to(actual, target_is_directory=True)
        with pytest.raises(_common.CliError, match='symlink or junction'):
            if operation == 'input':
                _common.checked_input_file('alias/study.csv', root=root)
            elif operation == 'output':
                _common.checked_output_file('alias/report.json', root=root, suffixes={'.json'})
            else:
                _common.checked_root(link)
        assert (actual / 'study.csv').read_text() == 'value\n1\n2\n'

def test_existing_output_requires_force_and_preserves_raw_input():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / 'study.json'
        raw.write_text('{"values": [1, 2, 3]}', encoding='utf-8')
        before = raw.read_bytes()
        report = root / 'report.json'
        report.write_text('{"old": true}', encoding='utf-8')
        command = [sys.executable, '-B', str(SCRIPTS / 'eda_analyzer.py'), 'study.json', '--root', str(root), '--output', 'report.json']
        result = subprocess.run(command, capture_output=True, text=True)
        assert result.returncode == 2
        assert json.loads(report.read_text()) == {'old': True}
        result = subprocess.run(command + ['--force'], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert raw.read_bytes() == before
        assert 'analysis' in json.loads(report.read_text())
