from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CustomEntityBaseRequest:
    """  """

    aliases: Optional[List[str]] = None
    custom_fields: Optional[Dict[Any, Any]] = None
    fields: Optional[Dict[Any, Any]] = None
    folder_id: Optional[str] = None
    name: Optional[str] = None
    schema_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        if self.aliases is None:
            aliases = None
        else:
            aliases = self.aliases

        custom_fields = self.custom_fields
        fields = self.fields
        folder_id = self.folder_id
        name = self.name
        schema_id = self.schema_id

        return {
            "aliases": aliases,
            "customFields": custom_fields,
            "fields": fields,
            "folderId": folder_id,
            "name": name,
            "schemaId": schema_id,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> CustomEntityBaseRequest:
        aliases = d.get("aliases")

        custom_fields = d.get("customFields")

        fields = d.get("fields")

        folder_id = d.get("folderId")

        name = d.get("name")

        schema_id = d.get("schemaId")

        return CustomEntityBaseRequest(
            aliases=aliases,
            custom_fields=custom_fields,
            fields=fields,
            folder_id=folder_id,
            name=name,
            schema_id=schema_id,
        )
