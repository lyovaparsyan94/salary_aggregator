import json
from abc import ABC, abstractmethod
from typing import Any

import bson


class DB_Repository(ABC):
    @abstractmethod
    def get_metadata(self, metadata: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def load_bson(self, bson_path: str) -> list[dict[str, Any]]:
        raise NotImplementedError


class MongoDBRepository(DB_Repository):
    def get_metadata(self, metadata: str) -> dict[str, Any]:
        with open(metadata) as file:
            metadata: dict[str, Any] = json.load(file)
        return metadata

    def load_bson(self, bson_path: str) -> list[dict[str, Any]]:
        with open(bson_path, 'rb') as file:
            data: list[dict[str, Any]] = bson.decode_all(file.read())
        return data
