import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

app = FastAPI()

# Configuración de APIs
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PedagogIA | v3</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 flex items-center justify-center min-h-screen p-4">
    <div class="max-w-lg w-full bg-white p-8 shadow-2xl rounded-3xl border border-slate-100">
        <h1 class="text-4xl font-light text-slate-800 mb-2">Pedagog<span class="font-bold text-indigo-600">IA</span></h1>
        <p class="text-xs text-slate-400 mb-8 uppercase tracking-[0.2em]">Cerebro: Gemini 3 Flash</p>
        
        <input type="text" id="q" placeholder="¿En qué puedo ayudarte?" 
               class="w-full p-4 bg-slate-50 border-none rounded-2xl mb-4 focus:ring-2 focus:ring-indigo-500 outline-none">
        
        <button onclick="enviar()" id="btn" class="w-full bg-black text-white p-4 rounded-2xl font-medium hover:bg-indigo-600 transition-all">
            Consultar
        </button>
        
        <div id="res" class="mt-8 text-slate-600 text-sm whitespace-pre-wrap"></div>
    </div>

    <script>
        async function enviar() {
            const q = document.getElementById('q').value;
            const res = document.getElementById('res');
            if(!q) return;
            res.innerHTML = "🔍 Procesando con Gemini 3...";
            try {
                const response = await fetch(`/preguntar?q=${encodeURIComponent(q)}`);
                const data = await response.json();
                res.innerHTML = data.respuesta || data.error;
            } catch (e) {
                res.innerHTML = "❌ Error de conexión.";
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
        # Búsqueda en tiempo real
        search = tavily.search(query=q, max_results=2)
        context = "\\n".join([r['content'] for r in search['results']])
        
        # USAMOS EL MODELO QUE APARECE EN TU PANEL: gemini-3-flash
        model = genai.GenerativeModel('gemini-3-flash')
        
        prompt = f"Eres PedagogIA. Contexto: {context}. Pregunta: {q}. Responde de forma ejecutiva."
        
        response = model.generate_content(prompt)
        return {"respuesta": response.text}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}
