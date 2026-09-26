import telebot, os, fitz
from flask import Flask, request
from deep_translator import GoogleTranslator
TOKEN = os.environ.get("BOT_TOKEN", "8865686478:AAEKR-3jJ4n6FDJDuWLo30rPdHL888Ne9TA")
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)
def ترجم_صفحة_كاملة(text):
    if len(text.strip()) < 10: return text
    try:
        return GoogleTranslator(source='en', target='ar').translate(text)
    except:
        return text
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "✅ البوت شغال في Render - بدون تقطيع!\nارسل PDF")
@bot.message_handler(content_types=['document'])
def handle(m):
    try:
        bot.send_message(m.chat.id, "⏳ أترجم الصفحة كاملة...")
        data = bot.download_file(bot.get_file(m.document.file_id).file_path)
        inp = f"/tmp/{m.document.file_name}"
        open(inp, 'wb').write(data)
        doc = fitz.open(inp)
        full_ar = ""
        for i, page in enumerate(doc, 1):
            en = page.get_text().strip()
            if en:
                ar = ترجم_صفحة_كاملة(en)
                full_ar += f"\n\n--- صفحة {i} ---\n{ar}\n"
        out = f"/tmp/AR_{m.document.file_name}.txt"
        with open(out, 'w', encoding='utf-8') as f:
            f.write(full_ar)
        with open(out, 'rb') as f:
            bot.send_document(m.chat.id, f, caption="✅ مترجم بدون تقطيع")
        doc.close()
        os.remove(inp); os.remove(out)
    except Exception as e:
        bot.send_message(m.chat.id, f"خطأ: {e}")
@app.route("/")
def home(): return "Bot Running V14"
@app.route("/webhook", methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
    return "ok", 200
application = app
