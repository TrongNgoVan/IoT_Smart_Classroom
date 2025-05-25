import sqlite3

# Kết nối hoặc tạo cơ sở dữ liệu
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Tạo bảng với cột mới 'attendance_time'
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    attendance_score REAL DEFAULT 0.0,
    attendance_status TEXT CHECK(attendance_status IN ('Đã Điểm Danh', 'Chưa Điểm Danh')) NOT NULL,
    attendance_time TEXT DEFAULT NULL
)
''')

print("Table created or updated successfully.")

# Thêm dữ liệu mẫu
students_to_insert = [
    ('B21DCCN726', 'VanTrong', 0.0, 'Chưa Điểm Danh', None),
    ('B21DCKH334', 'VanThu', 0.0, 'Chưa Điểm Danh', None),
    ('B21DCCN728', 'LeThanh', 0.0, 'Chưa Điểm Danh', None),
    ('B21DCKH335', 'PhamHoang', 0.0, 'Chưa Điểm Danh', None),
    ('B21DCCN729', 'SonTung', 0.0, 'Chưa Điểm Danh', None),
    ('B21DCKH336', 'NooPhuocThinh', 0.0, 'Chưa Điểm Danh', None)
]

# Chèn dữ liệu vào bảng
conn.executemany('''
INSERT OR IGNORE INTO students (student_code, name, attendance_score, attendance_status, attendance_time)
VALUES (?, ?, ?, ?, ?)
''', students_to_insert)

conn.commit()
print("Inserted initial students successfully.")

# Truy vấn và hiển thị dữ liệu
cursor.execute('SELECT * FROM students')
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
