import google.generativeai as genai

KEY = "AIzaSyDuSu5jIRoaBNjR88TBdNnrWgXuZOaTXLg"

print(f"Testing Key with gemini-flash-latest...")

try:
    genai.configure(api_key=KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
    resp = model.generate_content("Hello")
    print("SUCCESS: Connected!")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"FAILED: {e}")
