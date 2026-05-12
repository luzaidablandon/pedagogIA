import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

# IMPORTACIONES MODULARES
from api.interface import get_html_content
from api.agente import procesar_consulta_institucional

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@app.get("/")
async def home():
    return HTMLResponse(content=get_html_content())

@app.get("/api/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        # 1. Búsqueda oficial (Seguridad de fuente)
        search = tavily.search(query=f"site:sena.edu.co {q}", max_results=2)
        contexto = "\\n".join([r['content'] for r in search['results']])
        
        # 2. Selección de modelo
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        selected_model = next((m for m in available_models if 'flash' in m), available_models[0])
        
        # 3. Procesamiento en el módulo Agente
        respuesta = procesar_consulta_institucional(q, contexto, selected_model)
        
        return {
            "respuesta": respuesta,
            "fuente": search['results'][0]['url'] if search['results'] else "Guía Metodológica Oficial"
        }
    except Exception as e:
        return {"error": str(e)}
