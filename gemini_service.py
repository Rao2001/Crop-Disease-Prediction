import google.generativeai as genai
import time
import json

def configure_gemini(api_key):
    """
    Configures the Gemini API and tests the connection.
    Returns (True, None) if valid, (False, error_message) otherwise.
    """
    if not api_key:
        return False, "API Key is empty"
    try:
        genai.configure(api_key=api_key)
        
        # Test the key with a lightweight call
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content("Test connection")
        return True, None
    except Exception as e:
        return False, str(e)

def analyze_image_with_gemini(image, api_key):
    """
    Analyzes an image using Gemini 1.5 Pro/Flash to identify crop diseases.
    Returns a structured dictionary with the analysis results.
    """
    try:
        # Ensure we are configured (double check)
        genai.configure(api_key=api_key)
        
        # Use Gemini Flash Latest for best stability and free tier compatibility
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = """
        You are an expert plant pathologist and agricultural consultant.
        Analyze the provided image of a plant/leaf.

        1. **Identify the Plant**: What specific crop is this?
        2. **Identify the Condition**: Is it healthy? If not, what specific disease, pest, or deficiency is present? 
           Be precise (e.g., "Tomato Early Blight" rather than just "Blight").
        3. **Confidence**: Estimate your confidence level (0-100%).
        4. **Detailed Findings**: Describe the visual symptoms you see (spots, colors, patterns).
        5. **Recommended Treatment**: 
           - Organic/Cultural controls.
           - Chemical controls (if necessary, with safety warnings).
        6. **Prevention**: How to prevent this in the future.

        Output your response ONLY in valid JSON format with the following keys:
        {
            "plant_name": "...",
            "disease_name": "...",
            "status": "Healthy" or "Diseased",
            "confidence": 95,
            "description": "...",
            "treatment": "...",
            "prevention": "..."
        }
        Do not wrap the JSON in markdown code blocks. Just return the raw JSON string.
        """
        
        # Pass image directly (PIL Image)
        response = model.generate_content([prompt, image])
        
        # Clean up response text in case it has markdown format
        text_response = response.text.strip()
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
            
        return json.loads(text_response)
        
    except Exception as e:
        # Fallback error structure
        return {
            "error": str(e),
            "disease_name": "Analysis Failed",
            "confidence": 0,
            "treatment": "Please check your API key or internet connection."
        }

def get_chat_response(history, user_input, disease_context):
    """
    Handles chat interaction with the AI Agronomist.
    """
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        chat = model.start_chat(history=[])
        
        # We manually structure context since we aren't maintaining stateful chat object in this simple function
        # Better approach: Pass previous history as context in a single prompt
        
        full_prompt = f"Context: User is asking about a plant diagnosed with {disease_context}.\n"
        
        for msg in history:
            full_prompt += f"{msg['role'].title()}: {msg['content']}\n"
            
        full_prompt += f"User: {user_input}\nAssistant:"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
