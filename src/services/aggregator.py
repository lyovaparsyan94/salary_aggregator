from datetime import datetime
from typing import Any


async def aggregate_salaries(dt_from: str, dt_upto: str, group_type: str, collection) -> dict[str, list[Any]]:
    try:
        dt_from = datetime.fromisoformat(dt_from)
        dt_upto = datetime.fromisoformat(dt_upto)

        group_format = {
            "hour": "%Y-%m-%dT%H:00:00",
            "day": "%Y-%m-%dT00:00:00",
            "month": "%Y-%m-01T00:00:00"
        }.get(group_type, "%Y-%m-01T00:00:00")

        pipeline = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": group_format,
                            "date": "$dt"
                        }
                    },
                    "total_salary": {"$sum": "$value"}
                }
            },
            {"$sort": {"_id": 1}}
        ]

        cursor = collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)

        dataset = [item['total_salary'] for item in result]
        labels = [item['_id'] for item in result]

        return {"dataset": dataset, "labels": labels}
    except Exception:
        return {"dataset": [], "labels": []}
