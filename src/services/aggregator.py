from datetime import datetime, timedelta
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

        # Создание словаря с датами и значениями из результата агрегации
        salaries_dict = {item['_id']: item['total_salary'] for item in result}

        # Создание списка всех дат в указанном диапазоне
        current_date = dt_from
        labels = []
        dataset = []

        while current_date <= dt_upto:
            if group_type == "day":
                formatted_date = current_date.strftime("%Y-%m-%dT00:00:00")
                labels.append(formatted_date)
                dataset.append(salaries_dict.get(formatted_date, 0))
                current_date += timedelta(days=1)
            elif group_type == "hour":
                formatted_date = current_date.strftime("%Y-%m-%dT%H:00:00")
                labels.append(formatted_date)
                dataset.append(salaries_dict.get(formatted_date, 0))
                current_date += timedelta(hours=1)
            elif group_type == "month":
                formatted_date = current_date.strftime("%Y-%m-01T00:00:00")
                labels.append(formatted_date)
                dataset.append(salaries_dict.get(formatted_date, 0))
                current_date += timedelta(days=1)
                current_date = (current_date.replace(day=1) + timedelta(days=31)).replace(day=1)
            else:
                break

        return {"dataset": dataset, "labels": labels}
    except Exception as e:
        print(f"Error: {e}")
        return {"dataset": [], "labels": []}
