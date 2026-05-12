import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

# IMPORTAMOS NUESTRA INTERFAZ
from api.interface import get_html_content

app = FastAPI()

# Configuración de Clientes
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@app.get("/")
async def home():
    # LLAMAMOS A LA FUNCIÓN DEL MÓDULO INTERFACE
    return HTMLResponse(content=get_html_content())

@app.get("/api/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        # Búsqueda oficial SENA
        search = tavily.search(query=f"site:sena.edu.co {q}", max_results=2)
        contexto = "\\n".join([r['content'] for r in search['results']])
        fuente = search['results'][0]['url'] if search['results'] else "Portal SENA"

        # Modelo Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt_inst = f"Actúa como asistente del SENA. Usa este contexto: {contexto}. Pregunta: {q}"
        
        response = model.generate_content(prompt_inst)
        return {"respuesta": response.text, "fuente": fuente}
    except Exception as e:
        return {"error": str(e)}
