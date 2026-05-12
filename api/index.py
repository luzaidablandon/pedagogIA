import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

app = FastAPI()

# Configuración de APIs
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

genai.configure(api_key=GEMINI_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PedagogIA | Consultor</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 flex items-center justify-center min-h-screen p-4">
    <div class="max-w-lg w-full bg-white p-8 shadow-2xl rounded-3xl border border-slate-100">
        <h1 class="text-4xl font-light text-slate-800 mb-2">Pedagog<span class="font-bold text-indigo-600">IA</span></h1>
        <p class="text-xs text-slate-400 mb-8 uppercase tracking-[0.2em]">Inteligencia Educativa en Tiempo Real</p>
        
        <div class="space-y-4">
            <input type="text" id="q" placeholder="¿Qué quieres investigar hoy?" 
                   class="w-full p-4 bg-slate-50 border-none rounded-2xl focus:ring-2 focus:ring-indigo-500 transition-all outline-none">
            
            <button onclick="enviar()" id="btn" class="w-full bg-slate-900 text-white p-4 rounded-2xl font-medium hover:bg-indigo-600 transition-all shadow-lg shadow-indigo-100">
                Consultar al Cerebro
            </button>
        </div>
        
        <div id="res" class="mt-8 text-slate-600 leading-relaxed text-sm whitespace-pre-wrap max-h-64 overflow-y-auto p-2"></div>
    </div>

    <script>
        async function enviar() {
            const q = document.getElementById('q').value;
            const res = document.getElementById('res');
            const btn = document.getElementById('btn');
            if(!q) return;
            
            btn.disabled = true;
            btn.innerHTML = "Procesando...";
            res.innerHTML = "🔍 Investigando fuentes y sintetizando respuesta...";
            
            try {
                const response = await fetch(`/preguntar?q=${encodeURIComponent(q)}`);
                const data = await response.json();
                res.innerHTML = data.respuesta || data.error;
            } catch (e) {
                res.innerHTML = "❌ Error de conexión con el servidor.";
            } finally {
                btn.disabled = false;
                btn.innerHTML = "Consultar al Cerebro";
            }
        }
    </script>
</body>
</html>
"""

@app.get("/")
@app.get("/api")
async def home():
    return HTMLResponse(content=html_content)

@app.get("/preguntar")
@app.get("/api/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        # 1. Búsqueda con Tavily
        search = tavily.search(query=q, max_results=2)
        context = "\n".join([r['content'] for r in search['results']])
        
        # 2. Selección dinámica del modelo (Para evitar el 404)
        # Intentamos con el nombre estándar de la versión 1.5
        model_name = 'gemini-1.5-flash'
        
        model = genai.GenerativeModel(model_name=model_name)
        
        prompt = f"""
        Eres PedagogIA.
        Contexto: {context}
        Usuario pregunta: {q}
        Responde de forma ejecutiva, profesional y en español.
        """
        
        response = model.generate_content(prompt)
        return {"respuesta": response.text}
        
    except Exception as e:
        return {"error": f"Error técnico: {str(e)}"}
