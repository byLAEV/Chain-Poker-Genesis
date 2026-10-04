import io,json
from contextlib import redirect_stdout
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"CLI"))
from node_cli import NodeCLI

class Config:
    def __init__(self): self.data={"decentralized_storage":{"status":"READY","mode":"LOCAL"}}
    def get(self): return self.data
    def set_storage_mode(self,mode,readiness=None):
        assert mode=="DUAL_STORAGE" and readiness["dual_storage_ready"] is True
        self.data["decentralized_storage"]={"status":"DUAL_STORAGE_READY","mode":mode}
        return self.data

class Coherence:
    def verify_all(self): return {"dual_storage_ready":True}

class Node:
    def __init__(self): self.configuration=Config(); self.storage_coherence=Coherence()

def run(node,args):
    out=io.StringIO()
    with redirect_stdout(out): code=NodeCLI(node).run(args)
    return code,json.loads(out.getvalue())

def test_storage_mode_get_and_set():
    n=Node()
    code,result=run(n,["storage","mode","get"])
    assert code==0 and result["mode"]=="LOCAL"
    code,result=run(n,["storage","mode","set","DUAL_STORAGE"])
    assert code==0 and result["mode"]=="DUAL_STORAGE"
