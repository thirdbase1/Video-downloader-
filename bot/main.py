import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.config import BOT_TOKEN
from bot.handlers import handlers
from bot.logger import logger

def main():
    logger.info("Starting Video Splitter Bot...")

    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        # Register handlers
        app.add_handler(CommandHandler("start", handlers.start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.handle_url))
        app.add_handler(CallbackQueryHandler(handlers.handle_callback))

        # Add error handler
        async def error_handler(update, context):
            logger.error(f"Update {update} caused error: {context.error}")

        app.add_error_handler(error_handler)

        logger.info("Bot started and polling...")
        app.run_polling()

    except Exception as e:
        logger.critical(f"Bot crashed: {e}")
        # Restart? If deployed via service manager, let it exit.
        raise e

if __name__ == "__main__":
    main()
