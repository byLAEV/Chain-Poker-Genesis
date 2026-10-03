#!/usr/bin/env python3
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[2]/"Cryptography"
sys.path.insert(0,str(BASE/"Core"))
from crypto_service import CryptoService
from crypto_core import merkle_root if False else sha256
