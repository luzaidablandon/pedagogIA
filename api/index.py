import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from tavily import TavilyClient
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

app = FastAPI()

# Configuración de Seguridad Institucional
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Cargar base de datos vectorial (si existe)
try:
    vector_db = FAISS.load_local("faiss_sena_index", embeddings, allow_dangerous_deserialization=True)
except:
    vector_db = None

# PROMPT BLINDADO - Arquitectura Senior
SYSTEM_PROMPT = """
Actúa como Asesor Institucional del SENA. 
REGLAS DE ORO:
1. SOLO responde con información de *.sena.edu.co o documentos oficiales cargados.
2. Si la información no está en el contexto, di: 'No dispongo de información oficial sobre esto'.
3. Rechaza fuentes externas como Wikipedia o blogs.
4. Estilo: Profesional, pedagógico y neutral.
"""

# Interfaz con Botones Flotantes (Estética Blanca/Negra/Verde SENA)
html_content = """
<!-- Mismo HTML anterior pero con mejoras en las acciones rápidas -->
...
    <div class="floating-actions">
        <div class="action-btn" onclick="quickAction('acta')">
            <i class="fas fa-file-signature"></i>
            <span class="action-label">Acta de Compromiso</span>
        </div>
        <div class="action-btn" onclick="quickAction('seguimiento')">
            <i class="fas fa-chart-line"></i>
            <span class="action-label">Seguimiento Ficha</span>
        </div>
        <div class="action-btn" onclick="quickAction('normativa')">
            <i class="fas fa-gavel"></i>
            <span class="action-label">Consultar Normativa</span>
        </div>
    </div>
...
"""

@app.get("/api/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        # FASE 1: Búsqueda en Documentos Internos (RAG)
        contexto_interno = ""
        if vector_db:
            docs = vector_db.similarity_search(q, k=2)
            contexto_interno = "\\n".join([d.page_content for d in docs])
        
        # FASE 2: Búsqueda en Dominios Oficiales (Tavily filtrado)
        search = tavily.search(query=f"site:sena.edu.co {q}", max_results=2)
        contexto_web = "\\n".join([r['content'] for r in search['results']])
        
        # FASE 3: Generación con Validación de Seguridad
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_context = f"CONTEXTO INTERNO SENA:\\n{contexto_interno}\\n\\nCONTEXTO WEB OFICIAL:\\n{contexto_web}"
        
        response = model.generate_content(f"{SYSTEM_PROMPT}\\n\\n{full_context}\\n\\nPREGUNTA: {q}")
        
        return {
            "respuesta": response.text,
            "fuente": search['results'][0]['url'] if search['results'] else "Manuales Internos SIGA"
        }
    except Exception as e:
        return {"error": f"Error en validación: {str(e)}"}
