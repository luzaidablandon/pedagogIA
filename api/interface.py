def get_html_content():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PedagogIA | SENA</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #ffffff; color: #000000; overflow: hidden; }
        
        /* Botones Flotantes estilo TikTok */
        .floating-actions { 
            position: fixed; right: 20px; top: 50%; transform: translateY(-50%); 
            display: flex; flex-direction: column; gap: 15px; z-index: 100; 
        }
        .action-group { position: relative; display: flex; align-items: center; justify-content: center; }
        .action-btn { 
            width: 55px; height: 55px; border-radius: 50%; background: #000; color: #fff; 
            display: flex; align-items: center; justify-content: center; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
            cursor: pointer; box-shadow: 0 4px 20px rgba(0,0,0,0.15); border: 2px solid transparent;
        }
        .action-btn:hover { background: #39A900; transform: scale(1.1); border-color: #fff; }
        .action-label { 
            position: absolute; right: 70px; background: #000; color: #fff; padding: 6px 12px; 
            border-radius: 8px; font-size: 11px; opacity: 0; transition: 0.3s; pointer-events: none; 
            white-space: nowrap; font-weight: 600;
        }
        .action-group:hover .action-label { opacity: 1; transform: translateX(-5px); }
        
        /* Chat Area */
        .chat-container { height: calc(100vh - 200px); overflow-y: auto; scrollbar-width: none; }
        .chat-container::-webkit-scrollbar { display: none; }
    </style>
</head>
<body class="flex flex-col h-screen">

    <!-- Header Ejecutivo -->
    <header class="p-6 border-b border-gray-100 flex justify-between items-center bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div class="flex items-center gap-4">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/83/SENA_logo.svg" alt="SENA" class="w-12 h-12">
            <div>
                <h1 class="text-xl font-bold tracking-tighter uppercase">Pedagog<span class="text-[#39A900]">IA</span></h1>
                <p class="text-[9px] uppercase tracking-[0.4em] text-gray-400 font-semibold">Sistema de Inteligencia Institucional</p>
            </div>
        </div>
        <div class="flex items-center gap-3">
            <span class="h-2 w-2 rounded-full bg-[#39A900] animate-pulse"></span>
            <span class="text-[10px] font-mono text-gray-400 uppercase">Estado: Operativo</span>
        </div>
    </header>

    <!-- Acciones Administrativas Flotantes -->
    <div class="floating-actions">
        <div class="action-group">
            <div class="action-btn" onclick="ejecutarAccion('acta')"><i class="fas fa-file-pen text-lg"></i></div>
            <span class="action-label">Nueva Acta</span>
        </div>
        <div class="action-group">
            <div class="action-btn" onclick="ejecutarAccion('notificacion')"><i class="fas fa-paper-plane text-lg"></i></div>
            <span class="action-label">Notificar Ficha</span>
        </div>
        <div class="action-group">
            <div class="action-btn" onclick="ejecutarAccion('reunion')"><i class="fas fa-calendar-check text-lg"></i></div>
            <span class="action-label">Agendar Reunión</span>
        </div>
        <div class="action-group">
            <div class="action-btn" onclick="ejecutarAccion('resumen')"><i class="fas fa-book-open text-lg"></i></div>
            <span class="action-label">Resumen Normativo</span>
        </div>
    </div>

    <!-- Main Chat -->
    <main class="flex-1 max-w-4xl w-full mx-auto p-6 flex flex-col justify-end">
        <div id="chat-box" class="chat-container space-y-6">
            <!-- Mensaje Inicial -->
            <div class="flex gap-4">
                <div class="w-9 h-9 bg-black rounded-full flex items-center justify-center text-white text-[10px] font-bold">IA</div>
                <div class="bg-gray-100 p-5 rounded-2xl rounded-tl-none max-w-[85%] text-sm leading-relaxed border border-gray-200">
                    Bienvenida, **Instructora Luz Aida**. ¿En qué proceso administrativo o pedagógico del SENA puedo asistirle hoy?
                </div>
            </div>
        </div>
    </main>

    <!-- Input Box -->
    <footer class="p-8 bg-white">
        <div class="max-w-4xl mx-auto flex gap-4 bg-gray-50 p-2 rounded-3xl border border-gray-100 shadow-inner">
            <input type="text" id="userInput" placeholder="Escriba su consulta institucional aquí..." 
                   class="flex-1 p-4 bg-transparent border-none focus:ring-0 outline-none text-sm">
            <button onclick="enviarMensaje()" class="bg-black text-white w-14 h-14 rounded-2xl flex items-center justify-center hover:bg-[#39A900] transition-all">
                <i class="fas fa-arrow-up"></i>
            </button>
        </div>
        <p class="text-[9px] text-center mt-4 text-gray-400 uppercase tracking-widest">Solo se utiliza información oficial de dominios SENA</p>
    </footer>

    <script>
        async function enviarMensaje() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chat-box');
            if(!input.value) return;

            const texto = input.value;
            input.value = '';
            
            chatBox.innerHTML += `<div class="flex justify-end gap-4 animate-fade-in">
                <div class="bg-black text-white p-5 rounded-2xl rounded-tr-none max-w-[85%] text-sm shadow-lg">${texto}</div>
            </div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch(`/api/preguntar?q=${encodeURIComponent(texto)}`);
                const data = await res.json();
                
                chatBox.innerHTML += `<div class="flex gap-4 animate-fade-in">
                    <div class="w-9 h-9 bg-[#39A900] rounded-full flex items-center justify-center text-white text-[10px] font-bold">IA</div>
                    <div class="bg-white p-5 rounded-2xl rounded-tl-none max-w-[85%] text-sm border border-gray-200 shadow-sm">
                        ${data.respuesta}
                        <div class="mt-3 pt-3 border-t border-gray-50 text-[10px] text-gray-400">
                            <b>Fuente:</b> ${data.fuente || 'Verificada institucional'}
                        </div>
                    </div>
                </div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (e) {
                console.error("Error de conexión");
            }
        }

        function ejecutarAccion(tipo) {
            const prompts = {
                'acta': 'Solicito apoyo para redactar un acta de compromiso por bajo rendimiento académico.',
                'notificacion': 'Redacta una notificación para informar a los aprendices sobre un cambio en la sesión de formación.',
                'reunion': 'Ayúdame a organizar una reunión para el equipo ejecutor de la ficha.',
                'resumen': 'Resume los lineamientos más recientes de la comunidad de instructores SENA.'
            };
            document.getElementById('userInput').value = prompts[tipo];
            enviarMensaje();
        }
    </script>
</body>
</html>
"""
