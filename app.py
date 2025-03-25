from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Получение всех задач из базы данных
def get_all_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = [{"id": row[0], "text": row[1]} for row in cursor.fetchall()]
    conn.close()
    return tasks

# Добавление задачи в базу данных
def add_task_to_db(text):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (text) VALUES (?)", (text,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

# Удаление задачи из базы данных
def delete_task_from_db(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Маршрут для отображения index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# API: Получение всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = get_all_tasks()
    return jsonify(tasks)

# API: Добавление новой задачи
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400
    text = data["text"]
    task_id = add_task_to_db(text)
    return jsonify({"id": task_id, "text": text}), 201

# API: Удаление задачи
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    delete_task_from_db(task_id)
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    init_db()  # Инициализируем базу данных при запуске
    app.run(host='0.0.0.0', port=5000, debug=True)
