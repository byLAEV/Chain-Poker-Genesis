import importlib.util,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("node_core",ROOT/"node_core.py"); mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; sys.modules[spec.name]=mod; spec.loader.exec_module(mod)
class NodeCoreReferenceTests(unittest.TestCase):
    def test_boot_initialize_activate(self):
        n=mod.NodeCore(); self.assertEqual(n.initialize()["state"],"INITIALIZED"); self.assertEqual(n.activate(),"ACTIVE")
    def test_crypto(self):
        n=mod.NodeCore(); self.assertEqual(len(n.crypto.hash(b"test")),64); self.assertEqual(len(n.crypto.merkle([b"a",b"b"])),64)
    def test_time_chain(self):
        n=mod.NodeCore(); a=n.time.record(1); b=n.time.record(2); self.assertEqual(b.sequence,a.sequence+1); self.assertNotEqual(a.previous_hash,b.previous_hash)
    def test_security(self):
        n=mod.NodeCore(); self.assertFalse(n.security.validate_path("../escape").allowed); self.assertFalse(n.security.validate_path("CPG/x").allowed)
if __name__=="__main__": unittest.main()
