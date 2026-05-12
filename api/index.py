import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

app = FastAPI()

# Configuración de APIs
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# El HTML lo ponemos aquí directamente para evitar errores de lectura de archivos
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>PedagogIA</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 flex items-center justify-center min-h-screen">
    <div class="max-w-md w-full bg-white p-8 shadow-lg rounded-xl">
        <h1 class="text-2xl font-bold text-blue-600 mb-4">PedagogIA</h1>
        <input type="text" id="q" placeholder="¿Qué quieres saber?" class="w-full p-2 border rounded mb-4">
        <button onclick="enviar()" class="w-full bg-black text-white p-2 rounded">Consultar</button>
        <div id="res" class="mt-4 text-gray-600"></div>
    </div>
    <script>
        async function enviar() {
            const q = document.getElementById('q').value;
            const res = document.getElementById('res');
            res.innerHTML = "Investigando...";
            const response = await fetch(`/preguntar?q=${encodeURIComponent(q)}`);
            const data = await response.json();
            res.innerHTML = data.respuesta || data.error;
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def home():
    return HTMLResponse(content=html_content)

@app.get("/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        search = tavily.search(query=q, max_results=2)
        context = "\\n".join([r['content'] for r in search['results']])
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Eres PedagogIA. Responde breve: {q}. Contexto: {context}")
        return {"respuesta": response.text}
    except Exception as e:
        return {"error": str(e)}
