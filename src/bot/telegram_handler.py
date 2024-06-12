import json
from typing import Any

from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters


class TelegramHandler:
    def __init__(self, repository: Any, client: Any, configs: Any, job: Any) -> None:
        self.repository = repository
        self.client = client
        self.configs = configs
        self.job = job

    async def start(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text('Send me JSON data to aggregate.')

    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        try:
            data: dict[str, Any] = json.loads(update.message.text)
            result: dict[str, Any] = await self.fetch_aggregation(data)
            await update.message.reply_text(json.dumps(result))
        except json.JSONDecodeError:
            await update.message.reply_text('Invalid JSON data.')

    async def fetch_aggregation(self, data: dict[str, Any]) -> dict[str, Any]:
        dt_from: str = data['dt_from']
        dt_upto: str = data['dt_upto']
        group_type: str = data['group_type']

        collection = await self.client.get_collection()  # Ensure await is used here
        result: dict[str, Any] = await self.job(dt_from, dt_upto, group_type, collection=collection)
        return result

    def run_bot(self) -> None:
        application = ApplicationBuilder().token(self.configs.PRIVATE_CONFIGS.TELEGRAM_TOKEN).build()

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        application.run_polling()
