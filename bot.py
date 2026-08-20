import logging
import os
from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, filters
from dotenv import load_dotenv
import handlers

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot"""
    # Get bot token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables")
        return
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Conversation handler for all features
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', handlers.start),
            CommandHandler('help', handlers.start)
        ],
        states={
            handlers.ASKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.ask_question)],
            handlers.SUMMARIZING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.summarize_text)],
            handlers.REWRITING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.rewrite_text)],
            handlers.IDEAS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.generate_ideas)],
            handlers.EXPLAINING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.explain_topic)],
            handlers.TRANSLATING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.translate_text)],
            handlers.DOCUMENT: [MessageHandler(filters.Document.ALL, handlers.analyze_document)],
        },
        fallbacks=[
            CommandHandler('cancel', handlers.cancel),
            CommandHandler('start', handlers.start)
        ],
        per_message=False
    )
    
    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handlers.button_handler))
    
    # Add handler for unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, handlers.unknown))
    
    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
