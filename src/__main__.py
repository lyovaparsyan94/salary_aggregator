import asyncio

from bot.telegram_handler import TelegramHandler
from config import configs
from db.client import ClientMongoDB
from repository.db_repository import MongoDBRepository
from services.aggregator import aggregate_salaries


def main():
    repository: MongoDBRepository = MongoDBRepository()
    client: ClientMongoDB = ClientMongoDB(
        mongo_uri=configs.PRIVATE_CONFIGS.MONGO_URI,
        metadata_path=configs.DIR_CONFIG.COLLECTION_METADATA_DIR,
        bson_path=configs.DIR_CONFIG.BSON_COLLECTION_DIR,
        db_repository=repository,
        configs=configs
    )

    bot: TelegramHandler = TelegramHandler(
        repository=repository,
        configs=configs,
        client=client,
        job=aggregate_salaries
    )

    bot.run_bot()
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    loop.create_task(bot.run_bot())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == "__main__":
    main()
