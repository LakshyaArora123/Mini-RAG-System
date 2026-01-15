from qdrant_client.models import PayloadSchemaType
from backend.qdrant_client import client, COLLECTION

def ensure_payload_indexes():
    existing = client.get_collection(COLLECTION).payload_schema

    if "source" not in existing:
        client.create_payload_index(
            collection_name=COLLECTION,
            field_name="source",
            field_schema=PayloadSchemaType.KEYWORD
        )
