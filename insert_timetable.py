import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('attendance_system.db')
cursor = conn.cursor()

'''
# Timetable data to be inserted
timetable_data = [
    ("09:00 - 10:00", "Class1", "Lab", "Class1", "Lab", "Class1"),
    ("10:00 - 11:00", "Class2", None, "Class2", None, "Class2"),
    ("11:00 - 11:15", "Break", None, "Break", None, "Break"),
    ("11:15 - 12:15", "Class3", "Class3", "Class3", "Class3", "Class3"),
    ("12:15 - 13:15", "Class4", "Class4", "Class4", "Class4", "Class4"),
    ("13:15 - 14:00", "Lunch", None, "Lunch", None, "Lunch"),
    ("14:00 - 15:00", "Class5", "Class5", "Class5", "Class5", "Class5"),
    ("15:00 - 16:00", "Class6", "Class6", "Class6", "Class6", "Class6")
]

# Insert timetable data into the classes table
cursor.executemany(
INSERT INTO timetable (time_slot, monday, tuesday, wednesday, thursday, friday)
VALUES (?, ?, ?, ?, ?, ?)
, timetable_data)

#print("Timetable data has been successfully inserted into the database.")
'''
'''
#insert student data
student_data = [
    (1,"SCE232CS01","1SB23CS407","Rohit"),
    (2,"SCE232CS02","1SB23CS403","Manoj"),
    (3,"SCE232CS03","1SB23CS405","Prajwal")
]
#insert student data into students table
cursor.executemany(''''''
    INSERT INTO students (id,reg_number,usn,name)
    VALUES (?,?,?,?)''''''
    , student_data
)
print("Student data insert successfully")
'''

#insert into user table
cursor.execute('''
    INSERT INTO users (user_id, password) VALUES
    ("user", "user@123")''')
# Commit the changes and close the connection
conn.commit()
conn.close()