from firebase_config import db

try:
    # Intenta escribir un documento de prueba
    doc_ref = db.collection("test").document("conexion")
    doc_ref.set({"status": "ok", "mensaje": "Conexión exitosa"})
    print("✅ Firebase conectado correctamente")
except Exception as e:
    print(f"❌ Error de conexión: {e}")