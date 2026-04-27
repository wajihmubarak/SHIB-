# --- إضافة رصيد عند إكمال مهمة ---
@app.route('/api/complete-task', methods=['POST'])
def complete_task():
    if 'user_id' not in session: 
        return jsonify({"success": False, "message": "يجب تسجيل الدخول"})
    
    data = request.json
    uid = session['user_id']
    task_id = data.get('task_id') # معرف المهمة
    reward = float(data.get('reward')) # قيمة الجائزة من المهمة
    
    with get_db() as conn:
        # إضافة قيمة المهمة لرصيد المستخدم
        conn.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (reward, uid))
        # ممكن هنا نسجل إنو أتم المهمة دي عشان ما يكررها
        conn.commit()
        
        updated = conn.execute("SELECT balance FROM users WHERE id = ?", (uid)).fetchone()
        return jsonify({"success": True, "new_balance": updated['balance']})
