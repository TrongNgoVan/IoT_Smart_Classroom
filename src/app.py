from flask import Flask, render_template
import sqlite3

# Flask app initialization
app = Flask(__name__)

# Route để hiển thị danh sách sinh viên
@app.route('/students')
def students():
    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        
        # Lấy tất cả sinh viên
        cursor.execute("SELECT student_code ,name, attendance_score, attendance_status ,attendance_time FROM students")
        students_list = cursor.fetchall()
        conn.close()

        return render_template('students.html', students=students_list)
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        return "Error fetching student data"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
