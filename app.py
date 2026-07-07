from flask import Flask, send_from_directory
from config import Config
import os
from models import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Tạo thư mục tự động
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(Config.BASE_DIR, 'instance'), exist_ok=True)
    
    # Khởi tạo DB nếu chưa có
    if not os.path.exists(Config.DB_PATH):
        init_db()

    # Đăng ký các Blueprints từ thư mục routes
    from routes.auth import auth_bp
    from routes.dashboard import dash_bp
    from routes.api import api_bp
    from routes.orders import orders_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(orders_bp)

    # Route hiển thị ảnh Bill
    @app.route('/uploads/bills/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    