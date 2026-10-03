"""OpenPGP provider backed by GPGME Python bindings."""
class GPGMEProvider:
    name="gpgme"
    version="a4b0c9f6e285c0a56b758f73cc4ee38c0b3e5c46"
    def __init__(self):
        try: import gpg
        except ImportError as e: raise RuntimeError("GPGME Python binding is required") from e
        self._gpg=gpg
        self.context=gpg.Context()
    def capabilities(self): return ("key_lookup","sign","verify","encrypt","decrypt")
    def find_key(self,pattern): return self.context.keylist(pattern=pattern).__next__()
