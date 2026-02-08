import base64


def set_background(image_file):
    """
    Sets a background image for the Streamlit app.
    """
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    return style

def custom_css():
    """
    Returns custom CSS for the app.
    """
    return """
    <style>
        /* Main Container */
        .main {
            background-color: #f0f2f6;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #2c3e50;
            font-family: 'Helvetica Neue', sans-serif;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: #ffffff;
        }
        
        /* Success Message */
        .stSuccess {
            background-color: #d4edda;
            color: #155724;
            border-radius: 5px;
            padding: 10px;
        }
        
        /* Error Message */
        .stError {
            background-color: #f8d7da;
            color: #721c24;
            border-radius: 5px;
            padding: 10px;
        }
        
        /* Prediction Card */
        .prediction-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .metric-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        
        .confidence-score {
            font-size: 2em;
            font-weight: bold;
            color: #2e86c1;
        }
    </style>
    """
