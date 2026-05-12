import google.generativeai as genai
from api.herramientas import obtener_plantilla_administrativa

def procesar_consulta_institucional(query, contexto, selected_model):
    """
    Lógica de razonamiento del agente. Aplica filtros anti-alucinación 
    y prioriza exactitud institucional.
    """
    model = genai.GenerativeModel(selected_model)
    
    # Identificamos si es una labor administrativa por palabras clave
    tipo_admin = None
    if "acta" in query.lower(): tipo_admin = 'acta'
    elif "notific" in query.lower(): tipo_admin = 'notificacion'
    elif "reunión" in query.lower() or "reunion" in query.lower(): tipo_admin = 'reunion'
    
    plantilla = obtener_plantilla_administrativa(tipo_admin) if tipo_admin else ""
    
    prompt_blindado = f"""
    Eres PedagogIA, Asistente Oficial del SENA.
    
    RESTRICCIONES:
    - Solo responde basado en este CONTEXTO OFICIAL: {contexto}
    - Si vas a generar un documento, sigue esta PLANTILLA: {plantilla}
    - Prohibido usar fuentes no oficiales.
    - El tono debe ser pedagógico y neutral.
    
    CONSULTA: {query}
    """
    
    response = model.generate_content(prompt_blindado)
    return response.text
