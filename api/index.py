@app.get("/preguntar")
@app.get("/api/preguntar")
async def preguntar(q: str = Query(...)):
    try:
        # 1. Búsqueda con Tavily
        search = tavily.search(query=q, max_results=2)
        context = "\n".join([r['content'] for r in search['results']])
        
        # 2. Lógica de selección de modelo flexible
        # Intentamos con el nombre técnico estándar de la versión más reciente
        model_name = 'gemini-2.0-flash-exp' # Nombre técnico común para las versiones más nuevas
        
        try:
            model = genai.GenerativeModel(model_name)
            # Prueba rápida para ver si el modelo existe
            prompt = f"Eres PedagogIA. Contexto: {context}. Pregunta: {q}. Responde ejecutivo."
            response = model.generate_content(prompt)
        except Exception:
            # Si el anterior falla, usamos el nombre 'gemini-1.5-flash' que es el más estable a nivel global
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Eres PedagogIA. Contexto: {context}. Pregunta: {q}. Responde ejecutivo."
            response = model.generate_content(prompt)
        
        return {"respuesta": response.text}
        
    except Exception as e:
        return {"error": f"Error técnico: {str(e)}"}
