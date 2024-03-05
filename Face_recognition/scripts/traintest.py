import streamlit as st
import face_recognition
import cv2
import numpy as np
import os

# Add this global variable to store known face encodings
known_face_encodings = []
known_face_names = []  # Added to store names corresponding to known_face_encodings

def detect_faces(image_path):
    global known_face_encodings, known_face_names  # Use the global variables

    # Load the image
    image = face_recognition.load_image_file(image_path)

    # Find all face locations and face encodings in the image
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    print(f"Number of faces detected: {len(face_locations)}")  # Add this line

    # Draw rectangles around the detected faces and display names
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the face encoding with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"  # Default name if no match found

        # If a match is found, use the name from known_face_names
        if any(matches):
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw rectangles and display names with increased font size
        font_size = 1.0  # Adjust this value to increase/decrease font size
        font_thickness = 3
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), font_thickness)

        # Print matches inside the loop
        print(f"Matches: {matches}")

    return image

# ... (rest of the code remains unchanged)



def get_known_face_names():
    # Retrieve the names from known_faces_encodings.txt
    encodings_file = r"C:\Users\91859\Desktop\Face Recognition/scripts/known_faces_encodings.txt"
    
    known_face_names = []
    with open(encodings_file, "r") as file:
        for line in file:
            name, _ = line.strip().split(":")
            known_face_names.append(name)

    return known_face_names

def save_face_encoding(image_path, name, encodings_file):
    global known_face_encodings, known_face_names  # Use the global variables
    
    # Load the image
    image = face_recognition.load_image_file(image_path)

    # Find the face encoding for the image
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        print(f"No face found in the image: {image_path}")
        return

    # Assume using the first detected face encoding
    face_encoding = face_encodings[0]

    # Append the name and face encoding to the file
    with open(encodings_file, "a") as file:
        line = f"{name}:{','.join(map(str, face_encoding))}\n"
        file.write(line)
        print(f"Saved face encoding for {name}")

    # Update the global variables
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)

def main():
    global known_face_encodings, known_face_names  # Use the global variables
    
    st.title("Face Detection App")

    # Upload an image for face detection
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Convert the uploaded file to a readable path
        image_path = r"C:\Users\91859\Desktop\Face Recognition/images/{uploaded_file.name}"

        # Save the uploaded image to the specified path
        with open(image_path, "wb") as file:
            file.write(uploaded_file.getvalue())

        # Perform face detection and display the result
        result_image = detect_faces(image_path)
        st.image(result_image, caption="Detected Faces", use_column_width=True, channels="RGB")

if __name__ == "__main__":
    # Set the path for known_faces_encodings.txt
    known_faces_encodings_file = r"C:\Users\91859\Desktop\Face Recognition/scripts/known_faces_encodings.txt"

    # Save face encodings for known individuals using the same image for encoding and recognition
    save_face_encoding(r"C:\Users\91859\Desktop\Face Recognition\images\elonmusk.jpg", "Elon Musk", known_faces_encodings_file)
    save_face_encoding(r"C:\Users\91859\Desktop\Face Recognition\images\alia.jpg", "Alia", known_faces_encodings_file)
    save_face_encoding(r"C:\Users\91859\Desktop\Face Recognition\images\Devika S L.jpg", "Devika", known_faces_encodings_file)
 
    # Run the main application
    main()
