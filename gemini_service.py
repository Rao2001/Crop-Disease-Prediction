import google.generativeai as genai
import os

def configure_gemini(api_key):
    """
    Configures the Gemini API with the provided key.
    """
    if not api_key:
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        return False

def get_ai_treatment_plan(disease_name, confidence):
    """
    Generates a custom treatment plan using Gemini 1.5 Pro.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = f"""
        Act as an expert agricultural scientist. 
        
        Our automated diagnosis system has identified a potential issue in a crop.
        
        **Predicted Condition:** {disease_name}
        **Confidence Level:** {confidence}%
        
        Please provide a comprehensive management report. 
        If the 'Predicted Condition' name implies a specific disease (e.g., 'Tomato_Early_Blight'), analyze that specific disease.
        If the condition implies a healthy plant (e.g., 'Tomato_Healthy'), provide care tips to MAINTAIN this health.
        If the condition name is unclear or looks like a technical label, do your best to infer the plant and issue, but mention if you are guessing.

        Structure your response as follows:
        1.  **Diagnosis Overview**: Explain what this condition is in simple terms.
        2.  **Treatment Options**:
            *   *Organic/Cultural*: (e.g. pruning, neem oil, spacing)
            *   *Chemical*: (If applicable, with safety warnings)
        3.  **Future Prevention**: How to stop it from coming back next season.
        4.  **Safety Assessment**: Is the produce safe to eat?
        
        Keep the format clean using Markdown.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI Agronomist: {str(e)}"

def get_chat_response(history, user_input, disease_context):
    """
    Handles chat interaction with the AI Agronomist.
    history: List of previous messages
    user_input: The user's new question
    disease_context: The disease detected in the current session
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Construct a simple chat prompt with context
        # In a more advanced version, we'd use the ChatSession object from the SDK
        
        context_prompt = f"""
        Context: The user is consulting you (an expert agronomist) about a plant diagnosed with {disease_context}.
        
        User: {user_input}
        
        Answer concisely and helpfully.
        """
        
        response = model.generate_content(context_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
