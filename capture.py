import cv2
import os
import store_embeddings
import time
from face_detection import detect_faces

def create_or_get_student_folder(student_id):
    """
    Create a folder for each student if it doesn't exist.
    If the folder already exists, return the path.
    """
    folder_path = f'Student_info/Images/{student_id}'

    if not os.path.exists(folder_path):
        # Create a folder if it doesn't exist
        os.makedirs(folder_path)
        print(f"Folder created for student: {student_id}")
    else:
        print(f"Folder already exists for student: {student_id}")
        
    return folder_path

def capture_student_images(student_id, num_images_per_position=10):
    """
    Capture images for the student and store them in their folder.
    Captures specified number of images for each position.
    """
    # Get or create a folder for the student
    folder_path = create_or_get_student_folder(student_id)

    # Define positions
    positions = ["front-facing", "right-side-facing", "left-side-facing"]

    # Start the video capture
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return

    try:
        for position in positions:
            print(f"Position: {position}. Please get ready to capture {num_images_per_position} images.")
        
            for i in range(num_images_per_position):
                print(f"Capturing image {i + 1}/{num_images_per_position}. Press 's' to capture.")
                while True:
                    # Capture frame-by-frame
                    ret, frame = video_capture.read()

                    if not ret:
                        print("Failed to grab frame.")
                        break

                    # Convert to grayscale (face detection works better in grayscale)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Detect faces using MTCNN
                    boxes, _ = detect_faces(frame)
                    if boxes is not None:
                        for box in boxes:
                            x1, y1, x2, y2 = map(int, box)
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                    # Display the instructions and the video feed
                    display_text = f"Position: {position} | Press 's' to capture"
                    cv2.putText(frame, display_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.imshow("Capture Student Images", frame)

                    # Wait for the user to press 's' to save the image
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("s") or key == ord("S"):
                        # Save the captured image with the position indicated in the file name
                        img_filename = os.path.join(folder_path, f"{position}_image_{i + 1}.jpg")
                        cv2.imwrite(img_filename, frame)
                        print(f"Captured and saved: {img_filename}")
                        time.sleep(1)  # Brief pause after saving
                        break
                    elif key == ord("q"):
                        print("Quitting capture.")
                        return

    finally:
        # Release the video capture object and close windows
        video_capture.release()
        cv2.destroyAllWindows()
        print("Image capture process completed.")

if __name__ == "__main__":
    # Ask for student information (name or registration number)
    student_id = input("Enter the Student's register number: ")

    # Capture images for the student during the admission process
    capture_student_images(student_id, num_images_per_position=10)
    
    # Save embeddings to JSON file
    store_embeddings.capture_and_store_embeddings(student_id)