import os

class Config:
    # Bảo mật
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mat_khau_bi_mat_cua_shop_trc_2026'
    
    # Telegram Bot
    BOT_TOKEN = "ĐIỀN_TOKEN_BOT_CỦA_BẠN_VÀO_ĐÂY"
    WEB_URL = "https://ten_mien_cua_ban.com" # Thay bằng URL hosting của bạn
    
    # Đường dẫn hệ thống
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'instance', 'shop.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'bills')
    
    # Tài khoản Admin mặc định
    ADMIN_USER = "admin"
    ADMIN_PASS = "admin123"
    