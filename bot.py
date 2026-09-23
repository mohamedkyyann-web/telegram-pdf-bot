import telebot, os
import PyPDF2
from deep_translator import GoogleTranslator

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "أهلا يا محمد! أرسل لي ملف PDF وسأترجمه لك للعربية فوراً 📄")

@bot.message_handler(content_types=['document'])
def handle_pdf(m):
    try:
        if not m.document.file_name.lower().endswith('.pdf'):
            return
        bot.reply_to(m, "⏳ جاري الترجمة...")
        file_info = bot.get_file(m.document.file_id)
        data = bot.download_file(file_info.file_path)
        open("temp.pdf","wb").write(data)
        reader = PyPDF2.PdfReader("temp.pdf")
        text = ""
        for p in reader.pages[:10]:
            text += p.extract_text() or ""
        trans = GoogleTranslator(source='auto', target='ar').translate(text[:4000])
        open("translated.txt","w",encoding="utf-8").write(trans)
        bot.send_document(m.chat.id, open("translated.txt","rb"), caption="✅ تمت الترجمة")
    except Exception as e:
        bot.send_message(m.chat.id, f"خطأ: {e}")

bot.infinity_polling()
