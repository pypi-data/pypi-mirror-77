from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CustomEntityRequestRegistryFields:
    """  """

    entity_registry_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        entity_registry_id = self.entity_registry_id

        return {
            "entityRegistryId": entity_registry_id,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> CustomEntityRequestRegistryFields:
        entity_registry_id = d.get("entityRegistryId")

        return CustomEntityRequestRegistryFields(entity_registry_id=entity_registry_id,)
