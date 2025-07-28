import cv2
from facenet_pytorch import MTCNN

# Initialize MTCNN model
mtcnn = MTCNN(keep_all=True, device='cuda' if cv2.cuda.getCudaEnabledDeviceCount()>0 else 'cpu')

def detect_faces(frame):
    """
    Detect faces in a frame using MTCNN.
    Returns the bounding boxes and probabilities for the detected faces.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, probs = mtcnn.detect(rgb_frame)
    return boxes, probs