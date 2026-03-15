from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

import config
import validators
import database
import shortener

database.init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    if context.args:

        link_id = context.args[0]

        data = database.get_link(link_id)

        if data:

            url = data[0]

            database.add_click(link_id)

            button = [[InlineKeyboardButton("Open Link", url=url)]]

            await update.message.reply_text(
                "🔗 Click below to open link",
                reply_markup=InlineKeyboardMarkup(button)
            )

        else:

            await update.message.reply_text("Link not found.")

    else:

        await update.message.reply_text(
            "Send me any URL and I will create a short Telegram link."
        )


async def create_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    if not validators.url(url):

        await update.message.reply_text("❌ Invalid URL")
        return

    link_id = shortener.generate_id()

    database.save_link(
        link_id,
        url,
        update.message.from_user.id
    )

    short_link = f"https://t.me/{config.BOT_USERNAME}?start={link_id}"

    await update.message.reply_text(

        f"✅ Your Short Link\n\n{short_link}"

    )


async def my_urls(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    links = database.user_links(user_id)

    if not links:

        await update.message.reply_text("You have no links.")
        return

    text = "📊 Your Links\n\n"

    for link in links:

        link_id, url, clicks = link

        short = f"https://t.me/{config.BOT_USERNAME}?start={link_id}"

        text += f"{short}\nClicks: {clicks}\n\n"

    await update.message.reply_text(text)


def main():

    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("myurls", my_urls))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, create_link))

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":

    main()
