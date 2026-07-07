from flask import Blueprint, render_template, redirect, url_for
from database import get_db
from routes.auth import is_admin

dash_bp = Blueprint('dashboard', __name__)

@dash_bp.route('/')
@dash_bp.route('/dashboard')
def index():
    if not is_admin(): return redirect(url_for('auth.login'))
    
    conn = get_db()
    total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    pending_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 0").fetchone()[0]
    approved_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 1").fetchone()[0]
    total_codes = conn.execute("SELECT COUNT(*) FROM event_codes").fetchone()[0]
    
    recent_orders = conn.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()
    
    return render_template('dashboard.html', 
                           total=total_orders, pending=pending_orders, 
                           approved=approved_orders, codes=total_codes, 
                           orders=recent_orders)
                           