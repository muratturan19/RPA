"""Utilities for reading and processing Excel files."""

import pandas as pd
from pathlib import Path
from typing import List


def read_excel_files(files: List[Path]):
    """Placeholder Excel processing."""
    return [pd.read_excel(f) for f in files]
