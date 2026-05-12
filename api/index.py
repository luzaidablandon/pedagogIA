import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

app = FastAPI()

# Configuración de las llaves
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@app.get("/", response_class=HTMLResponse)
def home():
    # Buscamos el archivo index.html en la raíz del proyecto
    ruta_html = os.path.join(os.getcwd(), "index.html")
    try:
        with open(ruta_html, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <h1>PedagogIA</h1>
        <p>Error: El archivo index.html no se encuentra en la raíz.</p>
        <p>Asegúrate de que el archivo esté fuera de la carpeta 'api'.</p>
        """

@app.get("/preguntar")
async def preguntar(q: str = Query(..., description="La pregunta para la IA")):
    try:
        busqueda = tavily.search(query=q, max_results=3)
        contexto = "\n".join([resultado['content'] for resultado in busqueda['results']])
        
        model = genai.GenerativeModel('gemini-pro')
        
        prompt_instrucciones = f"Actúa como PedagogIA. Contexto: {contexto}. Pregunta: {q}"
        
        response = model.generate_content(prompt_instrucciones)
        return {"respuesta": response.text}
    except Exception as e:
        return {"error": str(e)}
