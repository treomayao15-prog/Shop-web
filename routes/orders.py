from flask import Blueprint, redirect, url_for
from database import get_db
from routes.auth import is_admin
import telebot
from config import Config

orders_bp = Blueprint('orders', __name__)
bot = telebot.TeleBot(Config.BOT_TOKEN)

@orders_bp.route('/action/order/<int:order_id>/<action>')
def action_order(order_id, action):
    if not is_admin(): return redirect(url_for('auth.login'))
    
    conn = get_db()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    
    if order:
        new_status = 1 if action == 'approve' else 2
        conn.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        conn.commit()
        
        # Báo về Telegram
        msg = "✅ Đơn của bạn đã được duyệt!\nBây giờ bạn có thể dùng lệnh /guima [Mã_Sự_Kiện]" if new_status == 1 else "❌ Đơn của bạn đã bị từ chối."
        try:
            bot.send_message(order['telegram_id'], msg)
        except: pass

    conn.close()
    return redirect(url_for('dashboard.index'))
    