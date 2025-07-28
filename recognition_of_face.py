import insightface
import os
import json
import cv2
import numpy as np
import sqlite3
from scipy.spatial.distance import cosine
import time

# Initialize the ArcFace model from InsightFace library
model = insightface.app.FaceAnalysis(providers=['CPUExecutionProvider'])  # Adjust provider if you have GPU support
model.prepare(ctx_id=0)  # Set to -1 if running on CPU only

# Database setup
conn = sqlite3.connect('attendance_system.db')
cursor = conn.cursor()

def load_student_embeddings():
    """
    Load all stored student embeddings and return as a dictionary.
    """
    embeddings_dict = {}
    embeddings_folder = 'student_info/embeddings/'
    
    # Loop through each student's folder
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

def update_attendance(student_id):
    """
    Insert a record into the temporary attendance table.
    """
    cursor.execute(''' 
        INSERT INTO temporary_attendance (student_reg_id, timestamp_status1, timestamp_status2, timestamp_status3,
                                          timestamp_status4, timestamp_status5, timestamp_status6) 
        VALUES (?, 1, 1, 1, 1, 1, 1)  -- Assuming present for all 6 intervals for simplicity
    ''', (student_id,))
    conn.commit()

def recognize_faces():
    """
    Open the camera, capture live frames, and recognize faces in real time.
    """
    # Load embeddings
    embeddings_dict = load_student_embeddings()
    
    # Open camera
    cap = cv2.VideoCapture(1)  # Using '1' for USB connected Webcam
    
    recognized_usns = []  # List to store recognized students
    last_attendance_check = time.time()
    attendance_check_interval = 10 * 60  # 10 minutes in seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break
        
        # Detect faces in the frame
        faces = model.get(frame)
        
        for face in faces:
            live_embedding = face.embedding  # Get live embedding
            recognized = "Unknown"
            best_similarity = -1  # Cosine similarity ranges from -1 to 1
            
            # Compare with stored embeddings
            for student_id, stored_embeddings in embeddings_dict.items():
                for stored_embedding in stored_embeddings:
                    similarity = 1 - cosine(live_embedding, stored_embedding)  # Calculate cosine similarity
                    
                    if similarity > best_similarity:
                        best_similarity = similarity
                        recognized = student_id if similarity >= 0.5 else "Unknown"  # Adjust threshold as needed
            
            # If recognized, mark attendance
            if recognized != "Unknown" and recognized not in recognized_usns:
                recognized_usns.append(recognized)
                update_attendance(recognized)
                
            # Display result on the frame
            bbox = face.bbox.astype(int)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.putText(frame, f"{recognized} ({best_similarity:.2f})", (bbox[0], bbox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Show the frame
        cv2.imshow("Real-Time Face Recognition", frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Check attendance every 10 minutes
        current_time = time.time()
        if current_time - last_attendance_check >= attendance_check_interval:
            last_attendance_check = current_time
            # Add logic here if you want to finalize attendance or handle absent students
            print("Updating attendance for all recognized students every 10 minutes")
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

# Run the face recognition
if __name__ == "__main__":
    recognize_faces()
