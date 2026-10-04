from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, io, tarfile, sys
BASE=Path(__file__).resolve().parents[2]/"Storage"/"Kubo"
sys.path.insert(0,str(BASE))
from kubo_installer import KuboInstaller, KuboInstallationError
from kubo_paths import KuboPathManager

def test_path_traversal_rejected():
    with TemporaryDirectory() as root:
        package=Path(root)/"evil.tar.gz"
        with tarfile.open(package,"w:gz") as t:
            data=b"evil"
            info=tarfile.TarInfo("../../escape")
            info.size=len(data); t.addfile(info,io.BytesIO(data))
        try:
            KuboInstaller(path_manager=KuboPathManager(root))._extract_safe(package,Path(root)/"stage")
        except KuboInstallationError: pass
        else: raise AssertionError("archive traversal accepted")

def test_wrong_extension_rejected():
    with TemporaryDirectory() as root:
        package=Path(root)/"pkg.zip"; package.write_bytes(b"x")
        try: KuboInstaller(path_manager=KuboPathManager(root))._extract_safe(package,Path(root)/"stage")
        except KuboInstallationError: pass
        else: raise AssertionError("wrong package accepted")
