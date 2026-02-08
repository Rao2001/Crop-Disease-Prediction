# Crop Disease Prediction & Analysis App

This project uses Deep Learning to detect crop diseases from leaf images. It includes a training notebook and a modern Streamlit web application for easy usage.

## 🛠️ Technology Stack & Design Decisions

Here is a breakdown of the technologies used and why they were chosen:

### 1. **Core Logic: Python & TensorFlow**
*   **What used**: We used **Python** as the main language and **TensorFlow/Keras** for building the AI model.
*   **Why**:
    *   **Python** is the industry standard for Data Science and Machine Learning.
    *   **Convolutional Neural Networks (CNNs)** in TensorFlow are highly effective for image classification tasks like identifying patterns of disease on leaves.
    *   **Keras** (built into TensorFlow) provides a simple, high-level API to build complex neural networks quickly.

### 2. **User Interface: Streamlit**
*   **What used**: **Streamlit** was selected to build the web interface (`app.py`).
*   **Why**:
    *   **Speed**: Streamlit allows us to turn Python scripts into shareable web apps in minutes, not weeks.
    *   **Data-Centric**: It is designed specifically for data science projects, handling heavy computations (like model inference) efficiently.
    *   **Interactivity**: It provides built-in widgets (file uploaders, buttons) that work seamlessly with Python logic.

### 3. **Image Processing: OpenCV & Pillow (PIL)**
*   **What used**: **NuPy**, **OpenCV** (in notebook), and **Pillow** (in app) for image manipulation.
*   **Why**:
    *   The model expects inputs in a very specific format (256x256 pixels, RGB color). These tools let us resize and normalize user uploads to match this format perfectly before prediction.

### 4. **Data Management: Mock Database**
*   **What used**: A Python dictionary-based structure in `utils.py`.
*   **Why**:
    *   To provide instant "Treatment" and "Description" info without needing a complex SQL database setup for this MVP (Minimum Viable Product). This keeps the app lightweight and easy to run anywhere.

---

## 🚀 How to Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Train the Model**:
    *   Open `crop_disease_prediction.ipynb`.
    *   Point it to your dataset.
    *   Run all cells to generate `models/crop_disease_model.h5`.

3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

---

## 📂 Project Structure

*   `app.py`: The main entry point for the web application.
*   `prediction.py`: Handles the loading of the AI model and processing images.
*   `utils.py`: Contains helper functions and the disease information database.
*   `crop_disease_prediction.ipynb`: The research notebook used to create and train the model.
*   `models/`: Directory where the trained model is saved.
