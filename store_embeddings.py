import insightface
import os
import json
import cv2

# Initialize the ArcFace model from InsightFace library
model = insightface.app.FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
model.prepare(ctx_id=0)  # Set to -1 if running on CPU only

def create_or_Get_Student_Folder(student_id):
    """
    Ensure folders for images and embeddings exist for the student.
    """
    images_folder = f'Student_info/Images/{student_id}'
    embeddings_folder = f'Student_info/Embeddings/{student_id}'
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(embeddings_folder, exist_ok=True)
    return images_folder, embeddings_folder

def capture_and_store_embeddings(student_id):
    """
    Capture face embeddings from images in the student's folder and store them in a JSON file.
    """
    # Define paths
    images_folder, embeddings_folder = create_or_Get_Student_Folder(student_id)

    # Loop through each file in the student's image folder
    for filename in os.listdir(images_folder):
        image_path = os.path.join(images_folder, filename)
        
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing {image_path}...")

            # Load the image and detect faces
            image = cv2.imread(image_path)
            faces = model.get(image)
            
            if faces:
                # Get the first face's embedding (assuming one face per image)
                embedding = faces[0].embedding.tolist()
                
                # Define the JSON file path for each image
                embedding_file_path = os.path.join(embeddings_folder, f'{os.path.splitext(filename)[0]}_embedding.json')
                
                try:
                    # Save the embedding in the specified format
                    with open(embedding_file_path, 'w') as f:
                        json.dump({"Student_id": student_id, "embedding": embedding}, f, indent=4)
                    
                    print(f"Processed and saved embedding for: {filename}")
                except Exception as e:
                    print(f"Failed to save embedding for {filename}: {e}")
            else:
                print(f"No faces found in {filename}")
