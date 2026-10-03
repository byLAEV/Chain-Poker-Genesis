"""libsodium provider backed by PyNaCl."""
class PyNaClProvider:
    name="pynacl"
    version="a5d50e2c9d87a64f5d69c7d42fa79f03e49d08b6"
    def __init__(self):
        try: import nacl
        except ImportError as e: raise RuntimeError("PyNaCl dependency is required") from e
        self._nacl=nacl
    def capabilities(self): return ("aead","hash","public_key","signatures","key_exchange")
