import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

app = FastAPI()

# Configuración de Clientes
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# PROMPT INSTITUCIONAL BLINDADO
SYSTEM_PROMPT = """
Eres PedagogIA, el Asistente Institucional del SENA. 
RESTRICCIONES CRÍTICAS:
- Solo usa dominios *.sena.edu.co o sitios oficiales del SENA.
- Rechaza Wikipedia, blogs o foros.
- Si no hay información oficial, indica que no hay datos verificables.
- Tono profesional, pedagógico y neutral.
- Para labores administrativas (actas, notificaciones), sigue la estructura formal del SENA.
"""

@app.get("/api/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        # Búsqueda dinámica filtrada por dominios SENA
        # Prioriza la guía metodológica y comunidad de instructores
        search_query = f"site:sena.edu.co {q}"
        search = tavily.search(query=search_query, search_depth="advanced", max_results=3)
        
        contexto_web = "\\n".join([f"Fuente [{r['url']}]: {r['content']}" for r in search['results']])
        
        # Selección automática del mejor modelo Gemini disponible
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        selected_model = next((m for m in available_models if 'flash' in m), available_models[0])
        model = genai.GenerativeModel(selected_model)
        
        full_prompt = f"{SYSTEM_PROMPT}\\n\\nCONTEXTO OFICIAL RECUPERADO:\\n{contexto_web}\\n\\nCONSULTA: {q}"
        response = model.generate_content(full_prompt)
        
        return {
            "respuesta": response.text,
            "fuentes": [r['url'] for r in search['results']]
        }
    except Exception as e:
        return {"error": f"Error en consulta institucional: {str(e)}"}
