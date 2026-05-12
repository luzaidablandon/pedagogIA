import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

# 1. ESTO DEBE ESTAR AQUÍ, SIN SANGRÍA (AL MARGEN IZQUIERDO)
app = FastAPI()

# 2. Configuración de clientes
GENAI_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

genai.configure(api_key=GENAI_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

# 3. Contenido HTML
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PedagogIA</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 flex items-center justify-center min-h-screen p-4">
    <div class="max-w-lg w-full bg-white p-8 shadow-2xl rounded-3xl border border-slate-100">
        <h1 class="text-3xl font-light text-slate-800 mb-2">Pedagog<span class="font-bold text-indigo-600">IA</span></h1>
        <p class="text-[10px] text-slate-400 mb-8 uppercase tracking-widest">Módulo de Inteligencia Artificial</p>
        <input type="text" id="q" placeholder="¿Qué deseas consultar?" class="w-full p-4 bg-slate-50 border-none rounded-2xl mb-4 outline-none focus:ring-2 focus:ring-indigo-500">
        <button onclick="enviar()" id="btn" class="w-full bg-black text-white p-4 rounded-2xl font-medium hover:bg-indigo-600 transition-all">Consultar</button>
        <div id="res" class="mt-6 text-slate-600 text-sm whitespace-pre-wrap"></div>
    </div>
    <script>
        async function enviar() {
            const q = document.getElementById('q').value;
            const res = document.getElementById('res');
            if(!q) return;
            res.innerHTML = "🔄 Procesando consulta...";
            try {
                const response = await fetch(`/api/preguntar?q=${encodeURIComponent(q)}`);
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
async def home():
    return HTMLResponse(content=html_content)

@app.get("/api/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        # Búsqueda
        search = tavily.search(query=q, max_results=2)
        context = "\\n".join([r['content'] for r in search['results']])
        
        # Selección de modelo: Usamos el nombre que viste en tu panel pero con el prefijo correcto
        # Si 'gemini-3-flash' falla, el sistema lanzará el error específico para corregirlo.
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
        prompt = f"Eres PedagogIA. Contexto: {context}. Pregunta: {q}. Responde de forma ejecutiva."
        response = model.generate_content(prompt)
        
        return {"respuesta": response.text}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}
