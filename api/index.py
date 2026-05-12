import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

# Importante: No cambiamos nada de lo que ya te funciona
app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PedagogIA</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 flex items-center justify-center min-h-screen">
    <div class="max-w-md w-full bg-white p-8 shadow-xl rounded-2xl border border-gray-100">
        <h1 class="text-3xl font-light text-gray-800 mb-2">Pedagog<span class="font-bold text-blue-600">IA</span></h1>
        <p class="text-xs text-gray-400 mb-6 uppercase tracking-tighter">Consultoría en tiempo real</p>
        
        <input type="text" id="q" placeholder="Ej: Tendencias IA 2026..." 
               class="w-full p-3 border border-gray-200 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500">
        
        <button onclick="enviar()" class="w-full bg-black text-white p-3 rounded-lg font-semibold hover:bg-gray-800 transition-all">
            Consultar al Cerebro
        </button>
        
        <div id="res" class="mt-6 text-gray-700 leading-relaxed text-sm whitespace-pre-wrap"></div>
    </div>

    <script>
        async function enviar() {
            const q = document.getElementById('q').value;
            const res = document.getElementById('res');
            if(!q) return;
            
            res.innerHTML = "🔄 Investigando en la red y procesando...";
            try {
                // Usamos la ruta completa para evitar el 404
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

# Usamos la ruta raíz "/" y también "/api" por si Vercel se confunde
@app.get("/")
@app.get("/api")
async def home():
    return HTMLResponse(content=html_content)

@app.get("/preguntar")
@app.get("/api/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        search = tavily.search(query=q, max_results=2)
        context = "\\n".join([r['content'] for r in search['results']])
        
        # EL NOMBRE CLAVE: models/gemini-1.5-flash
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        prompt = f"Eres PedagogIA, experta en educación e IA. Contexto: {context}. Pregunta: {q}. Responde de forma ejecutiva y profesional."
        
        response = model.generate_content(prompt)
        return {"respuesta": response.text}
    except Exception as e:
        return {"error": f"Error en el cerebro: {str(e)}"}
