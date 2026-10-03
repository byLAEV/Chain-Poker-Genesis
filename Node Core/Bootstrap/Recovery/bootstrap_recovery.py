#!/usr/bin/env python3
"""Public bootstrap recovery entry point."""
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from bootstrap_recovery_impl import recover
__all__=["recover"]
