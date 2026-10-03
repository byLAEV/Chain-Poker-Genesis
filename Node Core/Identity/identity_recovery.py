"""Identity continuity and new-life recovery decision boundary."""
from __future__ import annotations
from .identity_core import NodeLife

def recover_same_life(life:NodeLife, continuity_verified:bool):
    if life.state!="TERMINATED": raise ValueError("only terminated life can enter recovery")
    if not continuity_verified: raise ValueError("continuity not established; create a new Node Life")
    return life.transition("NODE_LIFE_RECOVERED","RECOVERED")

def requires_new_life(life:NodeLife,continuity_verified:bool)->bool:
    return life.state=="TERMINATED" and not continuity_verified
