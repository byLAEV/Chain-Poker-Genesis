#!/usr/bin/env python3
import tempfile, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
path=ROOT/"Storage"/"API"/"storage_api.py"
spec=importlib.util.spec_from_file_location("node_core_storage_api",path)
module=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(module)

def main():
    with tempfile.TemporaryDirectory() as root:
        api=module.StorageAPI(root)
        created=api.create("public","api-object",b"data",mirror=False)
        assert created["storage_class"]=="public"
        assert api.exists("public","api-object")
        data,_=api.read("public","api-object")
        assert data==b"data"
        updated=api.update("public","api-object",b"new",mirror=False)
        assert updated["version"]==2
        assert updated["created_at"]==created["created_at"]
        assert updated["updated_at"]!=created["updated_at"]
        assert api.verify("public","api-object")["verification_result"]=="VALID"
        assert api.delete("public","api-object")
    print("Node Core Storage API tests: PASS")

if __name__=="__main__": main()
