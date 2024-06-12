from typing import Any

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


class ClientMongoDB:
    def __init__(self, mongo_uri: str, metadata_path: str, bson_path: str, db_repository: Any, configs: Any) -> None:
        self.mongo_uri = mongo_uri
        self.metadata = metadata_path
        self.bson_path = bson_path
        self.db_repository = db_repository
        self.configs = configs

    async def get_collection(self) -> AsyncIOMotorCollection:
        metadata: dict[str, Any] = self.db_repository.get_metadata(self.metadata)
        client: AsyncIOMotorClient = self.create_client()
        db_name, coll_name = metadata["indexes"][0]["ns"].split('.')
        db = client[db_name]
        collection = db[coll_name]

        document_count = await collection.count_documents({})

        if document_count == 0:
            await self.create_collection(collection, metadata, bson_path=self.bson_path)
        document_count = await collection.count_documents({}) # for checking count of document while testing
        return collection

    async def create_collection(self,
                                collection: AsyncIOMotorCollection,
                                metadata: dict[str, Any],
                                bson_path: str,
                                ) -> None:
        data: Any = self.db_repository.load_bson(bson_path)
        await collection.insert_many(data)
        await self.create_indexes(collection, metadata)

    def create_client(self) -> AsyncIOMotorClient:
        client = motor.motor_asyncio.AsyncIOMotorClient(self.configs.PRIVATE_CONFIGS.MONGO_URI)
        return client

    async def create_indexes(self, collection: AsyncIOMotorCollection, metadata: dict[str, Any]) -> None:
        indexes = metadata.get("indexes", [])
        for index in indexes:
            keys = list(index["key"].items())
            if "_id" in index["key"]:
                await collection.create_index(keys, name=index["name"])
            else:
                await collection.create_index(keys, name=index["name"], unique=True)
