import os
import json
import cv2
import numpy as np
import sqlite3
from scipy.spatial.distance import cosine
import time
from datetime import datetime, timedelta
import insightface
import pandas as pd

# Initialize the ArcFace model from InsightFace
model = insightface.app.FaceAnalysis(providers=['CPUExecutionProvider'])
model.prepare(ctx_id=0)

# Database setup
conn = sqlite3.connect('attendance_system.db')
cursor = conn.cursor()

def save_final_attendance_to_directory():
    """
    Save the final attendance to the Attendance directory structure based on date and class.
    """
    # Define the root folder for attendance
    root_folder = 'Attendance'
    os.makedirs(root_folder, exist_ok=True)  # Ensure the root folder exists

    # Query the database to fetch all attendance records
    cursor.execute("SELECT class_id, reg_number, student_name, date, status FROM final_attendance")
    records = cursor.fetchall()

    # Process the records into a DataFrame
    attendance_data = pd.DataFrame(records, columns=['class_id', 'reg_number', 'student_name', 'date', 'status'])

    # Create a directory for each date and class
    for date, date_group in attendance_data.groupby('date'):
        date_str = date.split(" ")[0]  # Extract only the date part (YYYY-MM-DD)
        date_folder = os.path.join(root_folder, date_str)  # Create folder under 'Attendance' for the date

        # Ensure the date folder exists
        os.makedirs(date_folder, exist_ok=True)

        # Save records for each class in separate files
        for class_id, class_group in date_group.groupby('class_id'):
            class_file = os.path.join(date_folder, f"class{class_id}.xlsx")  # File for the specific class
            class_group.to_excel(class_file, index=False)  # Save as Excel
            print(f"Attendance saved to {class_file}")

def load_student_embeddings():
    """
    Load all stored student embeddings and return as a dictionary.
    """
    embeddings_dict = {}
    embeddings_folder = 'student_info/embeddings/'
    for student_id in os.listdir(embeddings_folder):
        student_path = os.path.join(embeddings_folder, student_id)
        student_embeddings = []
        for embedding_file in os.listdir(student_path):
            if embedding_file.endswith('.json'):
                with open(os.path.join(student_path, embedding_file), 'r') as f:
                    data = json.load(f)
                    student_embeddings.append(np.array(data['embedding']))
        embeddings_dict[student_id] = student_embeddings
    return embeddings_dict

def reinitialize_temp_attendance(class_id):
    """
    Reinitialize the temporary attendance table for the next class.
    All attendance columns are reset to 0 for all students.
    """
    cursor.execute("DELETE FROM temporary_attendance")
    cursor.execute("SELECT reg_number, name FROM students")
    students = cursor.fetchall()
    for student in students:
        student_id, student_name = student
        cursor.execute('''
            INSERT INTO temporary_attendance (student_reg_id, student_name, timestamp_status1, timestamp_status2,
                                              timestamp_status3, timestamp_status4, timestamp_status5, timestamp_status6, class_id)
            VALUES (?, ?, 0, 0, 0, 0, 0, 0, ?)
        ''', (student_id, student_name, class_id))
    conn.commit()
    print(f"Temporary attendance table reinitialized for Class ID {class_id}.")

def update_attendance_for_interval(embeddings_dict, interval):
    """
    Captures attendance for the current 10-minute interval.
    Updates only the specific column in the temporary_attendance table.
    """
    cap = cv2.VideoCapture(0)
    recognized_students = []
    try:
        print(f"Capturing attendance for interval {interval}...")
        start_time = time.time()
        while time.time() - start_time < 60:  # Run for 1 minutes (60 seconds)
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame. Retrying...")
                continue
            
            faces = model.get(frame)
            for face in faces:
                live_embedding = face.embedding
                recognized = "Unknown"
                best_similarity = -1
                for student_id, stored_embeddings in embeddings_dict.items():
                    for stored_embedding in stored_embeddings:
                        similarity = 1 - cosine(live_embedding, stored_embedding)
                        if similarity > best_similarity:
                            best_similarity = similarity
                            recognized = student_id if similarity >= 0.5 else "Unknown"
                
                if recognized != "Unknown" and recognized not in recognized_students:
                    recognized_students.append(recognized)
                    cursor.execute(f'''
                        UPDATE temporary_attendance
                        SET timestamp_status{interval} = 1
                        WHERE student_reg_id = ?
                    ''', (recognized,))
                    conn.commit()
                    print(f"Marked present: {recognized} in interval {interval}")
            
            cv2.imshow("Attendance Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    cursor.execute(f'''
        UPDATE temporary_attendance
        SET timestamp_status{interval} = 0
        WHERE timestamp_status{interval} IS NULL
    ''')
    conn.commit()
    print(f"Attendance for interval {interval} finalized.")

def finalize_attendance():
    """
    Finalize attendance for the current hour and store it in the final_attendance table.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT * FROM temporary_attendance")
    records = cursor.fetchall()
    for record in records:
        class_id, reg_number, student_name, *statuses = record
        total_present = sum(int(status) for status in statuses)
        final_status = "Present" if total_present >= 4 else "Absent"
        cursor.execute('''
            INSERT INTO final_attendance (reg_number, student_name, class_id, status, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (reg_number, student_name, class_id, final_status, current_time))
    conn.commit()
    print("Final attendance for the hour has been recorded.")
    save_final_attendance_to_directory()
    
    # Reinitialize the `final_attendance` table
    cursor.execute("DELETE FROM final_attendance")
    conn.commit()
    print("Final attendance table has been reset.")
    
    # Reset the `temporary_attendance` table for the next hour
    cursor.execute("SELECT MAX(class_id) FROM temporary_attendance")
    last_class_id = cursor.fetchone()[0] or 0  # If no class_id exists, default to 0
    next_class_id = last_class_id + 1

def manage_hourly_attendance():
    """
    Manages attendance for each hour. Takes attendance 6 times at 10-minute intervals.
    Finalizes attendance at the end of the hour and resets for the next class.
    """
    embeddings_dict = load_student_embeddings()
    current_hour = datetime.now().hour
    class_id = 1

    while True:
        current_time = datetime.now().replace(second=0,microsecond=0)
        if current_time.hour != current_hour:
            finalize_attendance()
            class_id += 1
            reinitialize_temp_attendance(class_id)
            current_hour = current_time.hour
            print(f"Moved to Class ID {class_id} for hour {current_hour}.")
        
        for interval in range(1, 7):
            update_attendance_for_interval(embeddings_dict, interval)


if __name__ == "__main__":
    reinitialize_temp_attendance(1)
    manage_hourly_attendance()
    # finalize_attendance()