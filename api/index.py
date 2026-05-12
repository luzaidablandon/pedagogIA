import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

app = FastAPI()

# Configuración de APIs
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Buscamos el HTML en la raíz del proyecto
    # En Vercel, la raíz está un nivel arriba de la carpeta 'api'
    path = os.path.join(os.path.dirname(__file__), "..", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/preguntar")
async def preguntar(q: str = Query(..., description="Consulta")):
    try:
        search = tavily.search(query=q, max_results=3)
        context = "\n".join([r['content'] for r in search['results']])
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Eres PedagogIA. Contexto: {context}. Pregunta: {q}")
        
        return {"respuesta": response.text}
    except Exception as e:
        return {"error": str(e)}
