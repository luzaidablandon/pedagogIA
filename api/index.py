import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

app = FastAPI()

# Configuración con las llaves de entorno de Vercel
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@app.get("/")
async def home():
    # Retornamos un HTML simple para probar la conexión
    return HTMLResponse(content="<h1>PedagogIA activa</h1><p>Usa /api/preguntar?q=tu_pregunta</p>")

@app.get("/api/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        # 1. Búsqueda de contexto
        search = tavily.search(query=q, max_results=2)
        context = "\n".join([r['content'] for r in search['results']])
        
        # 2. Configuración del modelo con el nombre técnico EXACTO
        # Usamos 'gemini-1.5-flash' sin prefijos raros, la librería se encarga
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Actúa como PedagogIA. Contexto: {context}. Pregunta: {q}. Responde de forma ejecutiva."
        
        # 3. Generación
        response = model.generate_content(prompt)
        return {"respuesta": response.text}
        
    except Exception as e:
        # Si falla el 1.5, intentamos con el Pro como respaldo automático
        try:
            model_backup = genai.GenerativeModel('gemini-pro')
            response = model_backup.generate_content(q)
            return {"respuesta": response.text, "nota": "Usado modelo de respaldo"}
        except:
            return {"error": f"Fallo total de modelos: {str(e)}"}
