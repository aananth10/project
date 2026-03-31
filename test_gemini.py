import google.generativeai as genai

api_key = "AIzaSyDykMhGW70WIH3pjIM8lUOGlXw_BHwtqo8"
genai.configure(api_key=api_key)

print("--- SUPPORTED MODELS ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print("ERROR:", e)
