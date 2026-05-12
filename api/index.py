import os
from fastapi import FastAPI, Query
import google.generativeai as genai
from tavily import TavilyClient

app = FastAPI()

# Configuración de las llaves que pusiste en Vercel
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@app.get("/")
def home():
    return {"proyecto": "PedagogIA", "estado": "Cerebro conectado"}

@app.get("/preguntar")
async def preguntar(q: str = Query(..., description="La pregunta para la IA")):
    try:
        # 1. El Investigador (Tavily) busca en la web
        busqueda = tavily.search(query=q, max_results=3)
        contexto = "\n".join([resultado['content'] for resultado in busqueda['results']])
        
        # 2. El Cerebro (Gemini) procesa la info
      model = genai.GenerativeModel('gemini-pro') # Usamos flash por ser más rápido y gratuito
        
        prompt_instrucciones = f"""
        Eres PedagogIA, una asistente experta en educación e Inteligencia Artificial.
        Tu estilo es minimalista, ejecutivo y profesional.
        
        CONTEXTO ACTUALIZADO DE LA WEB:
        {contexto}
        
        PREGUNTA DEL USUARIO:
        {q}
        
        INSTRUCCIONES:
        1. Responde de forma directa y clara.
        2. Usa bullet points para facilitar la lectura.
        3. Si la información viene de la web, menciónalo brevemente.
        """
        
        response = model.generate_content(prompt_instrucciones)
        
        return {
            "respuesta": response.text,
            "fuentes": [r['url'] for r in busqueda['results']]
        }
    except Exception as e:
        return {"error": str(e)}
