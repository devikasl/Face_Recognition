import streamlit as st
from PIL import Image
import numpy as np
from keras.models import load_model

def main():
    st.title("Parkinson's Disease Prediction")

    # File uploader for an image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load the image from the uploaded file
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Add two buttons for prediction types
        if st.button("Predict Spiral"):
            model_path = r"C:\Users\91859\Desktop\parkinson/model.h5"  
            model = load_model(model_path)
            class_labels = ["Healthy", "Parkinson's Disease"]

            # Preprocess the image
            img_array = np.array(image.resize((128, 128))) / 255.0
            img_tensor = np.expand_dims(img_array, axis=0)

            # Predict using the model
            prediction = model.predict(img_tensor)

            # Get the predicted class index
            predicted_class_index = np.argmax(prediction[0])

            # Display prediction result
            st.success(f"The image is predicted to be {class_labels[predicted_class_index]}.")

        if st.button("Predict Wave"):
            model_path = r"C:\Users\91859\Desktop\parkinson/classifier.h5"  # Update with your actual model path for Wave
            model = load_model(model_path)
            class_labels = ["Healthy", "Parkinson's Disease"]

            # Preprocess the image
            img_array = np.array(image.resize((128, 128))) / 255.0
            img_tensor = np.expand_dims(img_array, axis=0)

            # Predict using the model
            prediction = model.predict(img_tensor)

            # Get the predicted class index
            predicted_class_index = np.argmax(prediction[0])

            # Display prediction result
            st.success(f"The image is predicted to be {class_labels[predicted_class_index]}.")

if __name__ == "__main__":
    main()
