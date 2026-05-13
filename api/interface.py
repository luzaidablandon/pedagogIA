def get_html_content():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PedagogIA | SENA</title>
    
    <!-- Carga del Favicon (.ico) -->
    <link rel="icon" type="image/x-icon" href="/imagenes/logo.ico">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #ffffff; color: #000000; display: flex; flex-direction: column; height: 100vh; margin: 0; }
        .chat-container { flex: 1; overflow-y: auto; padding: 20px; scrollbar-width: none; display: flex; flex-direction: column; gap: 1.5rem; }
        .chat-container::-webkit-scrollbar { display: none; }
        .floating-actions { position: fixed; right: 20px; top: 45%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 15px; z-index: 50; }
        .action-group { position: relative; display: flex; align-items: center; justify-content: center; }
        .action-btn { width: 50px; height: 50px; border-radius: 50%; background: #000; color: #fff; display: flex; align-items: center; justify-content: center; transition: 0.3s; cursor: pointer; border: none; }
        .action-btn:hover { background: #39A900; transform: scale(1.1); }
        .action-label { position: absolute; right: 60px; background: #000; color: #fff; padding: 5px 10px; border-radius: 6px; font-size: 10px; opacity: 0; pointer-events: none; white-space: nowrap; }
        .action-group:hover .action-label { opacity: 1; }
        .input-area { background: white; border-top: 1px solid #f0f0f0; padding: 20px; z-index: 100; }
    </style>
</head>
<body>

    <!-- Header con Logo Local y Subtítulo -->
    <header class="p-4 border-b flex justify-between items-center bg-white">
        <div class="flex items-center gap-3">
            <!-- Carga del Logo Local (.png) -->
            <img src="/imagenes/logo.png" alt="SENA" class="w-12 h-12 object-contain">
            <div>
                <h1 class="text-lg font-bold tracking-tighter uppercase leading-none">PEDAGOG<span class="text-[#39A900]">IA</span></h1>
                <!-- Subtítulo solicitado -->
                <p class="text-[10px] text-gray-500 font-medium mt-1">Agente IA de orientaciones para la virtualidad SENA</p>
            </div>
        </div>
        <div class="text-[9px] text-gray-300 font-mono">ESTADO: LUZ_AIDA_ACTIVA</div>
    </header>

    <div class="floating-actions">
        <div class="action-group">
            <button class="action-btn" onclick="ejecutarAccion('acta')"><i class="fas fa-file-signature"></i></button>
            <span class="action-label">Acta</span>
        </div>
        <div class="action-group">
            <button class="action-btn" onclick="ejecutarAccion('notificacion')"><i class="fas fa-paper-plane"></i></button>
            <span class="action-label">Notificación</span>
        </div>
        <div class="action-group">
            <button class="action-btn" onclick="ejecutarAccion('reunion')"><i class="fas fa-calendar-alt"></i></button>
            <span class="action-label">Reunión</span>
        </div>
    </div>

    <main id="chat-box" class="chat-container max-w-3xl mx-auto w-full">
        <div class="flex gap-3">
            <div class="w-8 h-8 bg-black rounded-full flex items-center justify-center text-white text-[8px] font-bold">IA</div>
            <div class="bg-gray-100 p-4 rounded-2xl rounded-tl-none text-sm max-w-[80%]">
                Bienvenida Instructora. El agente de virtualidad está activo. ¿Qué tarea administrativa realizaremos?
            </div>
        </div>
    </main>

    <footer class="input-area">
        <div class="max-w-3xl mx-auto relative flex items-center">
            <input type="text" id="userInput" 
                   placeholder="Escriba aquí su requerimiento..." 
                   class="w-full p-4 pr-16 bg-gray-50 border border-gray-200 rounded-2xl focus:outline-none focus:border-[#39A900] text-sm shadow-inner"
                   onkeypress="if(event.key === 'Enter') enviarMensaje()">
            <button onclick="enviarMensaje()" 
                    class="absolute right-2 w-10 h-10 bg-black text-white rounded-xl flex items-center justify-center hover:bg-[#39A900] transition-colors">
                <i class="fas fa-arrow-up"></i>
            </button>
        </div>
    </footer>

    <script>
        async function enviarMensaje() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chat-box');
            if(!input.value) return;

            const texto = input.value;
            input.value = '';
            
            chatBox.innerHTML += `<div class="flex justify-end gap-3">
                <div class="bg-black text-white p-4 rounded-2xl rounded-tr-none text-sm max-w-[80%]">${texto}</div>
            </div>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch(`/api/preguntar?q=${encodeURIComponent(texto)}`);
                const data = await res.json();
                
                chatBox.innerHTML += `<div class="flex gap-3">
                    <div class="w-8 h-8 bg-[#39A900] rounded-full flex items-center justify-center text-white text-[8px] font-bold">IA</div>
                    <div class="bg-white p-4 rounded-2xl rounded-tl-none text-sm max-w-[80%] border shadow-sm">
                        ${data.respuesta}
                    </div>
                </div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (e) { console.error(e); }
        }

        function ejecutarAccion(tipo) {
            const prompts = {
                'acta': 'Generar borrador de acta de compromiso académica.',
                'notificacion': 'Redactar notificación oficial para aprendices virtuales.',
                'reunion': 'Agenda de reunión de equipo pedagógico.'
            };
            document.getElementById('userInput').value = prompts[tipo];
            enviarMensaje();
        }
    </script>
</body>
</html>
"""
