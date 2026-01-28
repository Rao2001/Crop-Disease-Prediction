import base64

def get_disease_info(disease_name):
    """
    Simulates an API call to get detailed info about a disease.
    In a real app, this would fetch from a database or external API.
    """
    # Mock database
    disease_db = {
        # Apple
        "Apple___Apple_scab": {
            "description": "Apple scab is a fungal disease caused by *Venturia inaequalis*. It affects leaves and fruit, causing dark, scabby lesions.",
            "treatment": "Apply fungicides like captan or sulfur. Remove and destroy infected leaves to prevent spread.",
            "severity": "Moderate"
        },
        "Apple___Black_rot": {
            "description": "Black rot is a fungal disease caused by *Botryosphaeria obtusa*. It causes purple spots on leaves and rot on fruit.",
            "treatment": "Prune dead wood and remove mummified fruit. Apply fungicides during the growing season.",
            "severity": "High"
        },
        "Apple___Cedar_apple_rust": {
            "description": "A fungal disease requiring juniper/cedar trees as alternate hosts. Causes yellow-orange spots on apple leaves.",
            "treatment": "Remove nearby wild cedar/juniper trees. Apply fungicides at the pink bud stage.",
            "severity": "Low to Moderate"
        },
        "Apple___healthy": {
            "description": "The apple plant appears healthy.",
            "treatment": "Continue regular care, watering, and monitoring.",
            "severity": "None"
        },

        # Blueberry
        "Blueberry___healthy": {
            "description": "The blueberry plant appears healthy.",
            "treatment": "Maintain acidic soil (pH 4.5-5.5) and proper irrigation.",
            "severity": "None"
        },

        # Cherry
        "Cherry_(including_sour)___Powdery_mildew": {
            "description": "A fungal disease causing a white, powdery growth on leaves and fruit. Leaves may curl or drop early.",
            "treatment": "Prune for good air circulation. Apply fungicides or sulfur sprays at first sign.",
            "severity": "Moderate"
        },
        "Cherry_(including_sour)___healthy": {
            "description": "The cherry plant appears healthy.",
            "treatment": "Ensure good air circulation and regular watering.",
            "severity": "None"
        },

        # Corn
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
            "description": "Fungal disease causing rectangular gray to tan lesions on leaves. Can severely reduce yield.",
            "treatment": "Use resistant hybrids. Rotate crops and till bacteria-infected debris.",
            "severity": "High"
        },
        "Corn_(maize)___Common_rust_": {
            "description": "Fungal disease causing reddish-brown pustules on leaves. Often favored by cool, moist weather.",
            "treatment": "Plant resistant varieties. Fungicides may be needed in severe cases.",
            "severity": "Moderate"
        },
        "Corn_(maize)___Northern_Leaf_Blight": {
            "description": "Fungal disease causing large, cigar-shaped grey-green lesions on leaves.",
            "treatment": "Use resistant varieties and crop rotation. Apply fungicides if infection is early.",
            "severity": "Moderate to High"
        },
        "Corn_(maize)___healthy": {
            "description": "The corn plant appears healthy.",
            "treatment": "Maintain nitrogen levels and proper spacing.",
            "severity": "None"
        },

        # Grape
        "Grape___Black_rot": {
            "description": "Fungal disease causing brown spots on leaves and shriveling/blackening of grapes (mummies).",
            "treatment": "Remove mummified fruit from vines. Apply protectant fungicides.",
            "severity": "High"
        },
        "Grape___Esca_(Black_Measles)": {
            "description": "Fungal trunk disease causing 'tiger striping' on leaves and spotting on berries.",
            "treatment": "Avoid pruning wounds during wet weather. Remove infected parts of the vine.",
            "severity": "High"
        },
        "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
            "description": "Fungal disease causing irregular brown spots on leaves.",
            "treatment": "Apply fungicides suitable for grape leaf spot diseases.",
            "severity": "Moderate"
        },
        "Grape___healthy": {
            "description": "The grape vine appears healthy.",
            "treatment": "Prune regularly and manage canopy for airflow.",
            "severity": "None"
        },

        # Orange
        "Orange___Haunglongbing_(Citrus_greening)": {
            "description": "A serious bacterial disease spread by psyllids. Causes yellowing leaves ('blotchy mottle') and misshapen, bitter fruit.",
            "treatment": "There is no cure. Inspect for psyllids and remove infected trees immediately.",
            "severity": "Critical"
        },

        # Peach
        "Peach___Bacterial_spot": {
            "description": "Bacterial disease causing small water-soaked spots on leaves and holes ('shot-hole' effect).",
            "treatment": "Plant resistant varieties. Copper sprays can help reduce population.",
            "severity": "Moderate"
        },
        "Peach___healthy": {
            "description": "The peach tree appears healthy.",
            "treatment": "Regular pruning and fertilization.",
            "severity": "None"
        },

        # Pepper
        "Pepper,_bell___Bacterial_spot": {
            "description": "Bacterial disease causing small, dark, water-soaked spots on leaves and fruit.",
            "treatment": "Use disease-free seeds. Copper sprays may suppress spread.",
            "severity": "Moderate"
        },
        "Pepper,_bell___healthy": {
            "description": "The bell pepper plant appears healthy.",
            "treatment": "Consistent watering and calcium checks to prevent blossom end rot.",
            "severity": "None"
        },

        # Potato
        "Potato___Early_blight": {
            "description": "Fungal disease causing dark brown concentric rings ('bullseye') on leaves.",
            "treatment": "Rotate crops. Apply fungicides when spots first appear.",
            "severity": "Moderate"
        },
        "Potato___Late_blight": {
            "description": "Serious fungal-like disease causing large, dark, water-soaked spots on leaves and tuber rot. Caused the Irish Potato Famine.",
            "treatment": "Destroy infected plants immediately. Apply preventive fungicides regularly.",
            "severity": "Critical"
        },
        "Potato___healthy": {
            "description": "The potato plant appears healthy.",
            "treatment": "Ensure soil is hilled around stems.",
            "severity": "None"
        },

        # Raspberry
        "Raspberry___healthy": {
            "description": "The raspberry plant appears healthy.",
            "treatment": "Prune old canes after fruiting.",
            "severity": "None"
        },

        # Soybean
        "Soybean___healthy": {
            "description": "The soybean plant appears healthy.",
            "treatment": "Monitor for pests like aphids.",
            "severity": "None"
        },

        # Squash
        "Squash___Powdery_mildew": {
            "description": "Fungal disease leaving white powdery spots on leaves and stems.",
            "treatment": "Apply neem oil or sulfur fungicides. Improve air circulation.",
            "severity": "Moderate"
        },

        # Strawberry
        "Strawberry___Leaf_scorch": {
            "description": "Fungal disease causing purple blotches on leaves that turn brown.",
            "treatment": "Remove infected leaves. Apply fungicides if severe.",
            "severity": "Moderate"
        },
        "Strawberry___healthy": {
            "description": "The strawberry plant appears healthy.",
            "treatment": "Mulch to keep berries off soil.",
            "severity": "None"
        },

        # Tomato
        "Tomato___Bacterial_spot": {
            "description": "Bacterial disease causing small, water-soaked spots that turn dark/brown on leaves and fruit.",
            "treatment": "Use copper-based bactericides. Minimize overhead watering.",
            "severity": "Moderate"
        },
        "Tomato___Early_blight": {
            "description": "Fungal disease causing 'bullseye' pattern spots on lower leaves first.",
            "treatment": "Mulch to prevent soil splash. Apply fungicides and remove lower leaves.",
            "severity": "Moderate"
        },
        "Tomato___Late_blight": {
            "description": "Aggressive disease causing large, dark, greasy-looking spots on leaves and stems.",
            "treatment": "Remove and destroy infected plants immediately to save the crop.",
            "severity": "Critical"
        },
        "Tomato___Leaf_Mold": {
            "description": "Fungal disease causing yellow spots on upper leaf surface and olive-green mold on the underside.",
            "treatment": "Reduce humidity and increase airflow (pruning).",
            "severity": "Moderate"
        },
        "Tomato___Septoria_leaf_spot": {
            "description": "Fungal disease causing many small circular spots with dark borders and light centers.",
            "treatment": "Remove lower leaves. Apply fungicides like chlorothalonil.",
            "severity": "Moderate"
        },
        "Tomato___Spider_mites Two-spotted_spider_mite": {
            "description": "Tiny pests that suck sap, causing yellow stippling on leaves and fine webbing.",
            "treatment": "Spray with strong water stream or insecticidal soap/neem oil.",
            "severity": "Moderate"
        },
        "Tomato___Target_Spot": {
            "description": "Fungal disease causing brown necroses with concentric rings on leaves and fruit.",
            "treatment": "Apply fungicides and improve air circulation.",
            "severity": "Moderate"
        },
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
            "description": "Viral disease transmitted by whiteflies. Causes leaves to curl upward and yellow edges.",
            "treatment": "Control whiteflies. Remove infected plants immediately. Use resistant varieties.",
            "severity": "High"
        },
        "Tomato___Tomato_mosaic_virus": {
            "description": "Viral disease causing mottled (light/dark green) patterns on leaves and stunted growth.",
            "treatment": "Sterilize tools. Wash hands (smokers can transmit TMV). Remove infected plants.",
            "severity": "High"
        },
        "Tomato___healthy": {
            "description": "The tomato plant appears healthy.",
            "treatment": "Regular watering, pruning suckers, and staking.",
            "severity": "None"
        },

        "default": {
            "description": "Detailed information for this specific disease is currently unavailable in our database.",
            "treatment": "Consult a local agricultural extension expert for diagnosis and treatment plans.",
            "severity": "Unknown"
        }
    }
    
    return disease_db.get(disease_name, disease_db["default"])

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
