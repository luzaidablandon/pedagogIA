def obtener_plantilla_administrativa(tipo):
    """
    Retorna la estructura base según el lineamiento pedagógico y administrativo 
    del SENA para asegurar consistencia documental.
    """
    plantillas = {
        'acta': (
            "ESTRUCTURA DE ACTA DE COMPROMISO SENA:\n"
            "- Identificación: Nombre aprendiz, Documento, Ficha.\n"
            "- Hechos: Descripción de la falta (académica o disciplinaria).\n"
            "- Compromisos: Acciones de mejora con fechas límite.\n"
            "- Consecuencias: Citación a comité en caso de incumplimiento.\n"
            "Redacta el borrador siguiendo esta estructura de forma profesional."
        ),
        'notificacion': (
            "FORMATO DE COMUNICACIÓN OFICIAL:\n"
            "- Encabezado: Fecha y Grupo/Ficha destinatario.\n"
            "- Asunto: Claridad sobre el cambio o novedad.\n"
            "- Cuerpo: Explicación técnica y pedagógica del motivo.\n"
            "- Cierre: Instrucciones de seguimiento para el aprendiz.\n"
            "Redacta de forma directa y ejecutiva."
        ),
        'reunion': (
            "PROTOCOLO DE CITACIÓN DE REUNIÓN EQUIPO EJECUTOR:\n"
            "- Orden del día sugerido.\n"
            "- Espacio para revisión de evidencias de aprendizaje.\n"
            "- Seguimiento a casos de deserción o bajo rendimiento.\n"
            "Propón una agenda técnica basada en los procesos SIGA-GFPI."
        )
    }
    return plantillas.get(tipo, "")
