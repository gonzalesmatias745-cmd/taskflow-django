from google import genai

client = genai.Client(api_key="AIzaSyCtsoMaZBR8xKCumdx5OASpPqSw6l5a0zA")
for m in client.models.list():
    print(f"model disponible: {m.name}")