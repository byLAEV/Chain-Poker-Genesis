from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from storage_engine import LocalStore

class LocalStorageProvider:
    provider_type = "LOCAL"
    def __init__(self, node_root): self.store = LocalStore(node_root)
    def put(self, object_class, object_id, data): return self.store.put(object_class, object_id, data)
    def get(self, object_class, object_id): return self.store.get(object_class, object_id)
    def exists(self, object_class, object_id): return self.store.exists(object_class, object_id)
    def delete(self, object_class, object_id): return self.store.delete(object_class, object_id)
    def verify(self, object_class, object_id, expected_hash): return self.store.verify(object_class, object_id, expected_hash)
    def status(self): return {"provider_type": self.provider_type, "status": "READY"}
