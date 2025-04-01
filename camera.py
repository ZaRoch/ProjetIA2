import cv2

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur : impossible d'accéder à la caméra.")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Erreur : échec de la capture de l'image.")
        return None

    return frame
