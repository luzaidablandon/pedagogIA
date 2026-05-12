import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient

app = FastAPI()

# Configuración de clientes
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
except Exception as e:
    print(f"Error de configuración: {e}")

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PedagogIA</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 flex items-center justify-center min-h-screen p-4">
    <div class="max-w-lg w-full bg-white p-8 shadow-2xl rounded-3xl border border-gray-100">
        <h1 class="text-3xl font-light text-gray-800 mb-2">Pedagog<span class="font-bold text-blue-600">IA</span></h1>
        <p class="text-[10px] text-gray-400 mb-8 uppercase tracking-widest">Plataforma de Consulta Inteligente</p>
        
        <input type="text" id="q" placeholder="¿Qué deseas investigar hoy?" 
               class="w-full p-4 bg-gray-50 border-none rounded-2xl mb-4 focus:ring-2 focus:ring-blue-500 outline-none">
        
        <button onclick="enviar()" id="btn" class="w-full bg-blue-600 text-white p-4 rounded-2xl font-medium hover:bg-blue-700 transition-all shadow-lg shadow-blue-100">
            Consultar al Cerebro
        </button>
        
        <div id="res" class="mt-8 text-gray-600 text-sm whitespace-pre-wrap leading-relaxed"></div>
    </div>

    <script>
        async function enviar() {
            const q = document.getElementById('q').value;
            const res = document.getElementById('res');
            const btn = document.getElementById('btn');
            if(!q) return;
            
            btn.disabled = true;
            res.innerHTML = "🔍 Buscando y analizando...";
            
            try {
                const response = await fetch(`/api/preguntar?q=${encodeURIComponent(q)}`);
                const data = await response.json();
                res.innerHTML = data.respuesta || data.error;
            } catch (e) {
                res.innerHTML = "❌ Error al conectar con el servidor.";
            } finally {
                btn.disabled = false;
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
        # Búsqueda de información
        search = tavily.search(query=q, max_results=2)
        context = "\\n".join([r['content'] for r in search['results']])
        
        # Uso del modelo estable
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Eres PedagogIA. Responde de forma profesional y corta. Contexto: {context}. Pregunta: {q}"
        response = model.generate_content(prompt)
        
        return {"respuesta": response.text}
    except Exception as e:
        return {"error": f"Lo siento, hubo un problema técnico: {str(e)}"}
