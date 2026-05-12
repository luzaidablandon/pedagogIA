from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "PedagogIA está en línea y lista para el siguiente paso"}