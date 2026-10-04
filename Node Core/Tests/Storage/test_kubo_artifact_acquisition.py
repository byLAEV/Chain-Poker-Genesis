from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, io, sys
BASE=Path(__file__).resolve().parents[2]/"Storage"/"Kubo"
sys.path.insert(0,str(BASE))
from kubo_release_source import OfficialKuboReleaseSource
from kubo_artifact_acquirer import KuboArtifactAcquirer, KuboDownloadError

class Resp:
    def __init__(self,data): self.data=io.BytesIO(data)
    def read(self,n=-1): return self.data.read(n)
    def close(self): pass

def test_source_urls():
    class Source(OfficialKuboReleaseSource):
        def __init__(self):
            self.calls=[]
        def _get_bytes(self,url):
            self.calls.append(url)
            if url.endswith("/dist.json"): return b'{"ok":true}'
            return b"v0.43.1\nv0.42.0\n"
    s=Source()
    assert s.latest_stable_version()=="v0.43.1"
    a=s.artifact("v0.43.1",os_name="linux",architecture="amd64")
    assert a.filename=="kubo_v0.43.1_linux-amd64.tar.gz"

def test_verified_download():
    payload=b"verified kubo test package"
    digest=hashlib.sha512(payload).hexdigest()
    with TemporaryDirectory() as root:
        acq=KuboArtifactAcquirer(opener=lambda url,timeout: Resp(payload))
        from kubo_release_source import KuboArtifact
        a=KuboArtifact("v0.43.1","linux","amd64","kubo_v0.43.1_linux-amd64.tar.gz","https://dist.ipfs.tech/kubo/v0.43.1/x","https://dist.ipfs.tech/kubo/v0.43.1/x.sha512")
        p=acq.acquire(a,Path(root)/"incoming",digest)
        assert p.read_bytes()==payload
        verified=acq.promote_verified(p,Path(root)/"verified")
        assert verified.is_file()

def test_bad_integrity_rejected():
    with TemporaryDirectory() as root:
        acq=KuboArtifactAcquirer(opener=lambda url,timeout: Resp(b"bad"))
        from kubo_release_source import KuboArtifact
        a=KuboArtifact("v0.43.1","linux","amd64","pkg.tar.gz","https://dist.ipfs.tech/kubo/v0.43.1/x","https://dist.ipfs.tech/kubo/v0.43.1/x.sha512")
        try: acq.acquire(a,Path(root),"0"*128)
        except KuboDownloadError: pass
        else: raise AssertionError("integrity mismatch accepted")
