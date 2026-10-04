#!/usr/bin/env python3
"""Managed Linux Kubo daemon process lifecycle."""
from __future__ import annotations
import json, os, signal, subprocess
from pathlib import Path

class KuboProcessError(RuntimeError): pass

class KuboProcessManager:
    def __init__(self, paths):
        self.paths=paths
        self.paths.runtime.mkdir(parents=True,exist_ok=True)
        self.paths.logs.mkdir(parents=True,exist_ok=True)
        self.pid_path=self.paths.runtime/"kubo.pid"
        self.process_meta=self.paths.runtime/"process.json"

    def start(self, executable: str|Path, *, version: str) -> int:
        executable=Path(executable).resolve()
        if not executable.is_file() or not os.access(executable,os.X_OK):
            raise KuboProcessError("Kubo executable is unavailable")
        if not (self.paths.repository/"config").is_file():
            raise KuboProcessError("Kubo repository is not initialized")
        existing=self._running_pid()
        if existing is not None:
            raise KuboProcessError(f"Kubo is already running with PID {existing}")
        env=os.environ.copy(); env["IPFS_PATH"]=str(self.paths.ipfs_path)
        log_path=self.paths.logs/"kubo.log"
        log=log_path.open("ab")
        try:
            proc=subprocess.Popen(
                [str(executable),"daemon"],
                stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                cwd=str(self.paths.repository), env=env, start_new_session=True
            )
        except OSError as exc:
            log.close()
            raise KuboProcessError("unable to start Kubo daemon") from exc
        self.pid_path.write_text(str(proc.pid)+"\n",encoding="utf-8")
        self.process_meta.write_text(json.dumps({
            "pid":proc.pid,"version":version,"executable_path":str(executable),
            "ipfs_path":str(self.paths.ipfs_path),"log_path":str(log_path)
        },indent=2)+"\n",encoding="utf-8")
        log.close()
        return proc.pid

    def stop(self, timeout: float=15.0) -> bool:
        pid=self._running_pid()
        if pid is None:
            self._clear_runtime()
            return False
        try: os.kill(pid,signal.SIGTERM)
        except ProcessLookupError:
            self._clear_runtime(); return False
        import time
        deadline=time.monotonic()+timeout
        while time.monotonic()<deadline:
            if not self._pid_exists(pid):
                self._clear_runtime(); return True
            time.sleep(.2)
        try: os.kill(pid,signal.SIGKILL)
        except ProcessLookupError: pass
        self._clear_runtime()
        return True

    def is_running(self)->bool:
        return self._running_pid() is not None

    def _running_pid(self):
        if not self.pid_path.is_file(): return None
        try: pid=int(self.pid_path.read_text().strip())
        except ValueError: return None
        if pid<=1 or not self._pid_exists(pid):
            self._clear_runtime()
            return None
        return pid

    @staticmethod
    def _pid_exists(pid):
        try: os.kill(pid,0); return True
        except ProcessLookupError: return False
        except PermissionError: return True

    def _clear_runtime(self):
        for p in (self.pid_path,self.process_meta):
            try:p.unlink()
            except FileNotFoundError:pass
