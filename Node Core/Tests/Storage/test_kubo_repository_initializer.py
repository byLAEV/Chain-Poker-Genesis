from pathlib import Path
from tempfile import TemporaryDirectory
import json, os, sys

BASE=Path(__file__).resolve().parents[2]/"Storage"/"Kubo"
sys.path.insert(0,str(BASE))
from kubo_repository_initializer import KuboRepositoryInitializer, KuboRepositoryError
from kubo_paths import KuboPathManager

def test_init_uses_explicit_ipfs_path():
    with TemporaryDirectory() as root:
        root=Path(root)
        exe=root/"fake-ipfs"
        exe.write_text("#!/bin/sh\nmkdir -p \"$IPFS_PATH\"\nprintf '{\"Identity\":{\"PeerID\":\"peer-test\"}}' > \"$IPFS_PATH/config\"\nprintf '1\\n' > \"$IPFS_PATH/version\"\n")
        os.chmod(exe,0o755)
        paths=KuboPathManager(root).paths("v0.43.1")
        result=KuboRepositoryInitializer().initialize(executable=exe,paths=paths,version="v0.43.1")
        assert result["repository_initialized"] is True
        assert result["ipfs_path"] == str(paths.repository)
        assert (paths.repository/"config").is_file()

def test_existing_repository_is_not_reinitialized():
    with TemporaryDirectory() as root:
        root=Path(root)
        paths=KuboPathManager(root).paths("v0.43.1")
        paths.repository.mkdir(parents=True)
        (paths.repository/"config").write_text("{}")
        try:
            KuboRepositoryInitializer().initialize(executable="/missing",paths=paths,version="v0.43.1")
        except KuboRepositoryError:
            pass
        else:
            raise AssertionError("existing repository accepted for reinitialization")

def test_invalid_repository_rejected():
    with TemporaryDirectory() as root:
        root=Path(root)
        exe=root/"fake-ipfs"
        exe.write_text("#!/bin/sh\nmkdir -p \"$IPFS_PATH\"\nprintf '{}' > \"$IPFS_PATH/config\"\nprintf '1\\n' > \"$IPFS_PATH/version\"\n")
        os.chmod(exe,0o755)
        paths=KuboPathManager(root).paths("v0.43.1")
        try:
            KuboRepositoryInitializer().initialize(executable=exe,paths=paths,version="v0.43.1")
        except KuboRepositoryError:
            pass
        else:
            raise AssertionError("invalid repository accepted")
