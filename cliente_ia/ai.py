from google import genai

client = genai.Client(api_key="AIzaSyCtsoMaZBR8xKCumdx5OASpPqSw6l5a0zA")

def preguntar(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text