from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from utils import SmartBotUtils
import os

# States for conversation
ASKING, SUMMARIZING, REWRITING, IDEAS, EXPLAINING, TRANSLATING, DOCUMENT = range(7)

utils = SmartBotUtils()

# Main menu keyboard
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("💬 Ask Question", callback_data='ask')],
        [InlineKeyboardButton("📝 Summarize Text", callback_data='summarize')],
        [InlineKeyboardButton("✍️ Rewrite Text", callback_data='rewrite')],
        [InlineKeyboardButton("💡 Generate Ideas", callback_data='ideas')],
        [InlineKeyboardButton("📚 Explain Topic", callback_data='explain')],
        [InlineKeyboardButton("🌐 Translate Text", callback_data='translate')],
        [InlineKeyboardButton("📄 Analyze Document", callback_data='document')],
    ]
    return InlineKeyboardMarkup(keyboard)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🤖 **Welcome to SmartBot!**\n\n"
        "Your AI-powered assistant is ready to help you with:\n\n"
        "💬 **Ask Questions** - Get answers to general questions\n"
        "📝 **Summarize Text** - Send long text and receive a short summary\n"
        "✍️ **Rewrite Text** - Make messages clearer and professional\n"
        "💡 **Generate Ideas** - Get creative ideas for any topic\n"
        "📚 **Explain Topics** - Understand difficult topics simply\n"
        "🌐 **Translate Text** - Translate between languages\n"
        "📄 **Analyze Documents** - Upload PDF or text files for analysis\n\n"
        "Please choose an option below:"
    )
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )
    return ConversationHandler.END

# Button click handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    action = query.data
    messages = {
        'ask': "💬 Please send me your question:",
        'summarize': "📝 Please send me the text you want to summarize:",
        'rewrite': "✍️ Please send me the text you want to rewrite:",
        'ideas': "💡 Please tell me the topic you need ideas for:",
        'explain': "📚 Please tell me the topic you want explained:",
        'translate': "🌐 Please send me the text to translate (format: 'en:Hello world' or text then ask in reply):",
        'document': "📄 Please upload a PDF or text file to analyze:"
    }
    
    await query.edit_message_text(
        messages.get(action, "Please choose an option:"),
        reply_markup=None
    )
    
    # Set the action state
    if action == 'ask':
        return ASKING
    elif action == 'summarize':
        return SUMMARIZING
    elif action == 'rewrite':
        return REWRITING
    elif action == 'ideas':
        return IDEAS
    elif action == 'explain':
        return EXPLAINING
    elif action == 'translate':
        return TRANSLATING
    elif action == 'document':
        return DOCUMENT

# Ask question handler
async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.reply_text("🤔 Thinking...")
    response = utils.ask_question(question)
    await update.message.reply_text(response)
    return ConversationHandler.END

# Summarize handler
async def summarize_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if len(text) < 50:
        await update.message.reply_text("⚠️ Please send a longer text to summarize (at least 50 characters).")
        return SUMMARIZING
    
    await update.message.reply_text("📝 Summarizing...")
    response = utils.summarize_text(text)
    await update.message.reply_text(f"📝 **Summary:**\n{response}", parse_mode='Markdown')
    return ConversationHandler.END

# Rewrite handler
async def rewrite_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text("✍️ Rewriting...")
    response = utils.rewrite_text(text)
    await update.message.reply_text(f"✍️ **Rewritten Text:**\n{response}", parse_mode='Markdown')
    return ConversationHandler.END

# Ideas handler
async def generate_ideas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    await update.message.reply_text("💡 Generating ideas...")
    response = utils.generate_ideas(topic)
    await update.message.reply_text(f"💡 **Ideas for {topic}:**\n{response}", parse_mode='Markdown')
    return ConversationHandler.END

# Explain handler
async def explain_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    await update.message.reply_text("📚 Researching and explaining...")
    response = utils.explain_topic(topic)
    await update.message.reply_text(f"📚 **Explanation:**\n{response}", parse_mode='Markdown')
    return ConversationHandler.END

# Translate handler
async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Check if text contains language specification
    if ':' in text and len(text.split(':')) >= 2:
        parts = text.split(':', 1)
        target_lang = parts[0].strip()
        text_to_translate = parts[1].strip()
    else:
        await update.message.reply_text(
            "⚠️ Please specify the target language and text.\n"
            "Example: Spanish:Hello, how are you?"
        )
        return TRANSLATING
    
    await update.message.reply_text("🌐 Translating...")
    response = utils.translate_text(text_to_translate, target_lang)
    await update.message.reply_text(f"🌐 **Translation ({target_lang}):**\n{response}", parse_mode='Markdown')
    return ConversationHandler.END

# Document handler
async def analyze_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    
    if document:
        # Check file size (limit to 5MB)
        if document.file_size > 5 * 1024 * 1024:
            await update.message.reply_text("⚠️ File too large. Please upload a file under 5MB.")
            return DOCUMENT
        
        # Check file type
        file_name = document.file_name
        allowed_extensions = ['.pdf', '.txt']
        if not any(file_name.lower().endswith(ext) for ext in allowed_extensions):
            await update.message.reply_text("⚠️ Please upload a PDF or TXT file.")
            return DOCUMENT
        
        await update.message.reply_text("📄 Analyzing document... This may take a moment.")
        
        try:
            file = await document.get_file()
            file_content = await file.download_as_bytearray()
            
            response = utils.analyze_document(bytes(file_content), file_name)
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"⚠️ Error analyzing document: {str(e)}")
        return ConversationHandler.END
    
    await update.message.reply_text("⚠️ Please upload a document file.")
    return DOCUMENT

# Cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled. Type /start to begin again.")
    return ConversationHandler.END

# Fallback handler for unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Unknown command. Please use /start to see available options."
    )
