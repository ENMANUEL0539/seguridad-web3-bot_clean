import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Leer token desde variable de entorno
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No se encontró la variable de entorno BOT_TOKEN")

# Enlaces de tus proyectos
LINKS = {
    "Blog": "https://comfortable-joker.blogspot.com/",
    "Newsletter": "https://comfortable-joker.beehiiv.com/",
    "Comunidad": "https://comfortable-joker.beehiiv.com/p/comfortable-joker-comunity",
    "Servicios (Ko-fi)": "https://ko-fi.com/enmanuel05"
}

# Función start con menú principal
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📰 Blog", url=LINKS["Blog"])],
        [InlineKeyboardButton("📩 Newsletter", url=LINKS["Newsletter"])],
        [InlineKeyboardButton("🌐 Comunidad", url=LINKS["Comunidad"])],
        [InlineKeyboardButton("💼 Servicios", url=LINKS["Servicios (Ko-fi)"])],
        [InlineKeyboardButton("📰 Noticias Crypto/Web3", callback_data="news")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("""👋 Bienvenido a *Seguridad en la Web3 al Día*.
Elige una opción:""", reply_markup=reply_markup, parse_mode="Markdown")

# Función para mostrar noticias
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "news":
        # Ejemplo: noticias desde CoinDesk (puedes cambiar la fuente)
        try:
            res = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
            data = res.json()
            precio = data['bpi']['USD']['rate']
            msg = f"💰 *Bitcoin hoy*: {precio} USD\n\nMás noticias pronto..."
        except Exception as e:
            msg = f"No pude obtener noticias ahora. Error: {e}"

        await query.edit_message_text(text=msg, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("🤖 Bot corriendo en Render...")
    app.run_polling()

if __name__ == "__main__":
    main()
