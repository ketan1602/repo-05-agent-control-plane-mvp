from __future__ import annotations

from pathlib import Path

import yaml


class PolicyEngine:
    def __init__(self, policies_dir: str = "policies") -> None:
        self._dir = Path(policies_dir)
        self._current_version: str = "v1"
        self._cache: dict[str, dict] = {}

    def load_policy(self, version: str) -> dict:
        if version in self._cache:
            return self._cache[version]
        path = self._dir / f"supply_chain_{version}.yaml"
        if not path.exists():
            raise FileNotFoundError(f"Policy file not found: {path}")
        with path.open() as f:
            policy = yaml.safe_load(f)
        self._cache[version] = policy
        return policy

    def current_version(self) -> str:
        return self._current_version

    def set_current_version(self, version: str) -> dict:
        policy = self.load_policy(version)
        self._current_version = version
        return policy

    def available_versions(self) -> list[str]:
        return sorted(
            p.stem.replace("supply_chain_", "")
            for p in self._dir.glob("supply_chain_*.yaml")
        )

    def current_policy(self) -> dict:
        return self.load_policy(self._current_version)
