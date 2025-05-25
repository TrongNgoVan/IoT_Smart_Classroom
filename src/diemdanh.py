import sqlite3

import sqlite3
from datetime import datetime

# Kết nối đến SQLite và cập nhật trạng thái điểm danh
def update_attendance(student_name):
    try:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        # Kiểm tra xem tên có trong CSDL không
        cursor.execute('SELECT attendance_score, attendance_status FROM students WHERE name = ?', (student_name,))
        result = cursor.fetchone()

        if result:
            current_score, current_status = result

            # Nếu trạng thái là "Chưa Điểm Danh", cập nhật điểm chuyên cần, trạng thái và thời gian điểm danh
            if current_status == "Chưa Điểm Danh":
                new_score = current_score + 1
                attendance_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Lấy thời gian hiện tại

                cursor.execute('''
                    UPDATE students 
                    SET attendance_score = ?, attendance_status = 'Đã Điểm Danh', attendance_time = ?
                    WHERE name = ?
                ''', (new_score, attendance_time, student_name))
                conn.commit()

                print(f"Updated {student_name}: Attendance score = {new_score}, Status = Đã Điểm Danh, Time = {attendance_time}")
            else:
                print(f"{student_name} đã được điểm danh.")
        else:
            print(f"Không tìm thấy {student_name} trong CSDL.")

    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
    finally:
        conn.close()

