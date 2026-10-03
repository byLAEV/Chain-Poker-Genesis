#!/usr/bin/env python3
"""Protocol-neutral storage classification and operation policy."""

class StoragePolicyError(Exception): pass

class StoragePolicy:
    version = "1.0.0"
    RULES = {
        "temporary": {"distributable": False, "requires_encryption_for_distribution": False, "deletable": True},
        "public": {"distributable": True, "requires_encryption_for_distribution": False, "deletable": True},
        "private": {"distributable": True, "requires_encryption_for_distribution": True, "deletable": True},
        "restricted": {"distributable": True, "requires_encryption_for_distribution": True, "deletable": True},
        "personal": {"distributable": False, "requires_encryption_for_distribution": False, "deletable": True},
    }

    def rule(self, object_class):
        try: return dict(self.RULES[object_class])
        except KeyError as exc: raise StoragePolicyError("unsupported storage class") from exc

    def validate_write(self, object_class, *, mirror, encrypted):
        rule = self.rule(object_class)
        if mirror and not rule["distributable"]:
            raise StoragePolicyError(f"{object_class} objects cannot be distributed")
        if mirror and rule["requires_encryption_for_distribution"] and not encrypted:
            raise StoragePolicyError(f"{object_class} distribution requires encrypted bytes")
        return {
            "policy_version": self.version,
            "distribution_allowed": rule["distributable"],
            "encryption_required_for_distribution": rule["requires_encryption_for_distribution"],
        }

    def validate_delete(self, object_class):
        self.rule(object_class)
        return True

    def all_rules(self):
        return {k: dict(v) for k, v in self.RULES.items()}
