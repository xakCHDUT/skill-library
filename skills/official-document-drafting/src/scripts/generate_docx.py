#!/usr/bin/env python3
"""Export official-document Markdown using the bundled, standard-library runtime."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from docgen.cli import main
if __name__ == '__main__':
    raise SystemExit(main())
