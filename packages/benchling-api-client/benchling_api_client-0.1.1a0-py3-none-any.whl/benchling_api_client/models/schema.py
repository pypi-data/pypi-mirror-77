from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .schema_field import SchemaField


@dataclass
class Schema:
    """  """

    id: Optional[str] = None
    name: Optional[str] = None
    field_definitions: Optional[List[SchemaField]] = None
    type: Optional[str] = None
    prefix: Optional[str] = None
    registry_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        if self.field_definitions is None:
            field_definitions = None
        else:
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        type = self.type
        prefix = self.prefix
        registry_id = self.registry_id

        return {
            "id": id,
            "name": name,
            "fieldDefinitions": field_definitions,
            "type": type,
            "prefix": prefix,
            "registryId": registry_id,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Schema:
        id = d.get("id")

        name = d.get("name")

        field_definitions = []
        for field_definitions_item_data in d.get("fieldDefinitions") or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = d.get("type")

        prefix = d.get("prefix")

        registry_id = d.get("registryId")

        return Schema(
            id=id, name=name, field_definitions=field_definitions, type=type, prefix=prefix, registry_id=registry_id,
        )
