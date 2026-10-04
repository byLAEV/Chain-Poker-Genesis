#!/usr/bin/env python3
"""Kubo local RPC health checks; no synchronization or protocol logic."""
from __future__ import annotations
import json, urllib.request, urllib.error

class KuboHealthError(RuntimeError): pass

class KuboHealthManager:
    def __init__(self, api_url="http://127.0.0.1:5001", timeout=3.0):
        self.api_url=api_url.rstrip("/")
        self.timeout=timeout

    def check(self, *, expected_ipfs_path: str|None=None)->dict:
        try:
            ident=self._post("/api/v0/id")
            version=self._post("/api/v0/version")
        except (OSError, urllib.error.URLError, json.JSONDecodeError, KuboHealthError) as exc:
            return {"health_state":"UNHEALTHY","reason":str(exc)}
        if not ident.get("ID"):
            return {"health_state":"UNHEALTHY","reason":"Kubo API returned no PeerID"}
        reported=version.get("Version")
        if not reported:
            return {"health_state":"UNHEALTHY","reason":"Kubo API returned no version"}
        return {"health_state":"HEALTHY","peer_id":ident["ID"],"version":reported}

    def require_healthy(self, **kwargs)->dict:
        result=self.check(**kwargs)
        if result.get("health_state")!="HEALTHY":
            raise KuboHealthError(result.get("reason","Kubo is unhealthy"))
        return result

    def _post(self,path):
        req=urllib.request.Request(self.api_url+path,data=b"",method="POST")
        try:
            with urllib.request.urlopen(req,timeout=self.timeout) as response:
                return json.loads(response.read(1024*1024).decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise KuboHealthError(f"Kubo API HTTP {exc.code}") from exc
