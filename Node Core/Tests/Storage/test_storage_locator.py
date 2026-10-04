#!/usr/bin/env python3
import tempfile, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"Storage"/"Storage Manager"))
sys.path.insert(0,str(ROOT/"Storage"/"Object Registry"))
sys.path.insert(0,str(ROOT/"Storage"/"Providers"))
from storage_manager import StorageManager
from storage_locator import StorageLocator

def main():
    with tempfile.TemporaryDirectory() as temp:
        StorageManager(temp).put_json("public","locator-record-0001",{"status":"VALID"},mirror=False)
        location=StorageLocator(temp).locate("locator-record-0001")
        assert location["logical_path"]
        assert location["location"]==location["logical_path"]
        assert location["storage_class"]=="public"
        assert location["state"]=="PRESENT"
        assert location["version"]==1
    print("Node Core Storage locator tests: PASS")

if __name__=="__main__": main()
