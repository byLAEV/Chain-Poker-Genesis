"""secp256k1 provider backed by coincurve."""
class CoincurveProvider:
    name="coincurve"
    version="2d11b1160c75ae8fd94fe8fe3f226aec176bf9bf"
    def __init__(self):
        try: import coincurve
        except ImportError as e: raise RuntimeError("coincurve dependency is required") from e
        self._cc=coincurve
    def capabilities(self): return ("sign","verify","public_key")
    def sign(self,message,private_key): return self._cc.PrivateKey(private_key).sign(message)
    def verify(self,signature,message,public_key): return self._cc.PublicKey(public_key).verify(signature,message)
    def public_key(self,private_key): return self._cc.PrivateKey(private_key).public_key.format(compressed=True)
