from flask import Blueprint, request
import telebot
import os
from config import Config
from database import get_db

api_bp = Blueprint('api', __name__)
bot = telebot.TeleBot(Config.BOT_TOKEN)

@api_bp.route('/' + Config.BOT_TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@api_bp.route('/set_webhook')
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{Config.WEB_URL}/{Config.BOT_TOKEN}")
    return "✅ Webhook đã thiết lập! Bot đã sẵn sàng nhận lệnh.", 200

# ----- CÁC LỆNH BOT -----
@bot.message_handler(commands=['start'])
def start(message):
    conn = get_db()
    try:
        conn.execute("INSERT OR IGNORE INTO users (telegram_id, name, username) VALUES (?, ?, ?)",
                     (str(message.from_user.id), message.from_user.first_name, message.from_user.username or ""))
        conn.commit()
    except: pass
    finally: conn.close()
    bot.reply_to(message, "👋 Chào mừng bạn! Dùng /dat_trc để nạp bill. Dùng /guima [Mã] để gửi mã.")

@bot.message_handler(commands=['dat_trc'])
def dat_trc(message):
    bot.reply_to(message, f"💳 THÔNG TIN THANH TOÁN:\nNội dung CK: Donate {message.from_user.id}\n📸 Hãy gửi ảnh Bill vào đây.")

@bot.message_handler(content_types=['photo'])
def handle_bill(message):
    bot.reply_to(message, "⏳ Đang xử lý Bill...")
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    telegram_id = str(message.from_user.id)
    filename = f"{telegram_id}_{message.photo[-1].file_id}.jpg"
    bill_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    
    with open(bill_path, 'wb') as f:
        f.write(downloaded_file)
    
    conn = get_db()
    conn.execute("INSERT INTO orders (telegram_id, bill_image, status) VALUES (?, ?, 0)", (telegram_id, filename))
    conn.commit()
    conn.close()
    bot.reply_to(message, "✅ Đã nhận Bill! Vui lòng chờ Admin duyệt.")

@bot.message_handler(commands=['guima'])
def gui_ma(message):
    user_id = str(message.from_user.id)
    conn = get_db()
    order = conn.execute("SELECT id FROM orders WHERE telegram_id = ? AND status = 1", (user_id,)).fetchone()
    
    if not order:
        bot.reply_to(message, "⚠️ Bạn chưa có đơn nào được duyệt! /dat_trc trước nhé.")
        conn.close()
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        conn.execute("INSERT INTO event_codes (telegram_id, event_code) VALUES (?, ?)", (user_id, parts[1]))
        conn.commit()
        bot.reply_to(message, "✅ Gửi mã thành công lên Hệ thống!")
    else:
        bot.reply_to(message, "⚠️ Sai cú pháp! Dùng: /guima [Mã_Sự_Kiện]")
    conn.close()
    