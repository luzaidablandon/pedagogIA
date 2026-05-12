import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

app = FastAPI()

# Configuración inicial
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@app.get("/")
async def home():
    # Retornamos la interfaz visual que ya teníamos
    return HTMLResponse(content=html_content)

@app.get("/api/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        # 1. Obtener contexto con Tavily
        search = tavily.search(query=q, max_results=2)
        context = "\n".join([r['content'] for r in search['results']])
        
        # 2. DETECCIÓN AUTOMÁTICA DE MODELO (Solución al 404)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Seleccionamos el mejor disponible (preferiblemente flash, si no el primero que haya)
        selected_model = next((m for m in available_models if 'flash' in m), available_models[0])
        
        model = genai.GenerativeModel(selected_model)
        
        # 3. Generar respuesta
        prompt = f"Eres PedagogIA. Responde breve y profesional. Contexto: {context}. Pregunta: {q}"
        response = model.generate_content(prompt)
        
        return {"respuesta": response.text}
    except Exception as e:
        return {"error": f"Error tras detección: {str(e)}"}

# Mantenemos el html_content que ya conoces
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PedagogIA</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 flex items-center justify-center min-h-screen p-4">
    <div class="max-w-lg w-full bg-white p-8 shadow-2xl rounded-3xl">
        <h1 class="text-3xl font-light mb-2 text-slate-800">Pedagog<span class="font-bold text-blue-600">IA</span></h1>
        <input type="text" id="q" placeholder="Escribe tu consulta..." class="w-full p-4 bg-slate-50 border-none rounded-2xl mb-4 focus:ring-2 focus:ring-blue-500">
        <button onclick="enviar()" id="btn" class="w-full bg-blue-600 text-white p-4 rounded-2xl hover:bg-blue-700 transition-all">Consultar</button>
        <div id="res" class="mt-6 text-slate-600 text-sm whitespace-pre-wrap"></div>
    </div>
    <script>
        async function enviar() {
            const q = document.getElementById('q').value;
            const res = document.getElementById('res');
            if(!q) return;
            res.innerHTML = "🔄 Buscando modelo compatible y procesando...";
            const response = await fetch(`/api/preguntar?q=${encodeURIComponent(q)}`);
            const data = await response.json();
            res.innerHTML = data.respuesta || data.error;
        }
    </script>
</body>
</html>
"""
