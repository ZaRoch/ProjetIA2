import face_recognition
import pickle
import numpy as np

def extract_face_descriptor(image):
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None

def serialize_descriptor(descriptor):
    return pickle.dumps(descriptor)

def deserialize_descriptor(blob):
    return pickle.loads(blob)

def compare_faces(known_descriptors, descriptor, seuil=0.6):
    distances = face_recognition.face_distance(known_descriptors, descriptor)
    min_distance = np.min(distances)
    return min_distance < seuil, min_distance
