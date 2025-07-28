import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('attendance_system.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_number TEXT NOT NULL UNIQUE,
    usn TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT
    )
    ''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS timetable (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_slot TEXT NOT NULL,
    monday TEXT,
    tuesday TEXT,
    wednesday TEXT,
    thursday TEXT,
    friday TEXT
)
''')

# Create the temporary_attendance table (if it doesn't exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS temporary_attendance (
    class_id INTEGER,
    student_reg_id TEXT,
    student_name TEXT,
    timestamp_status1 INTEGER,
    timestamp_status2 INTEGER,
    timestamp_status3 INTEGER,
    timestamp_status4 INTEGER,
    timestamp_status5 INTEGER,
    timestamp_status6 INTEGER,
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (student_reg_id) REFERENCES students(reg_number)
)
''')

# Create the final attendance table
cursor.execute('''
CREATE TABLE IF NOT EXISTS final_attendance (
    final_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER,
    reg_number TEXT NOT NULL,
    date TEXT NOT NULL,
    status INTEGER,
    FOREIGN KEY (class_id) REFERENCES classes (class_id),
    FOREIGN KEY (reg_number) REFERENCES students (reg_number)
);
''')
#create the users table for login credentials
cursor.execute('''
CREATE TABLE users (
    user_id VARCHAR(15),
    password VARCHAR(15)
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete!")
