import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # جدول المستخدمين: ID، الاسم، الرصيد
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, name TEXT, balance REAL DEFAULT 0)')
    # جدول السحوبات للأدمن
    cursor.execute('CREATE TABLE IF NOT EXISTS withdrawals (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, amount REAL, status TEXT DEFAULT "Pending")')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# جلب بيانات المستخدم
@app.route('/api/user/<user_id>')
def get_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, balance FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"name": user[0], "balance": user[1]})
    return jsonify({"error": "Not found"}), 404

# إضافة رصيد (مثلاً بعد مهمة)
@app.route('/api/add_balance', methods=['POST'])
def add_balance():
    data = request.json
    uid, amount = str(data.get('user_id')), float(data.get('amount'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, uid))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
