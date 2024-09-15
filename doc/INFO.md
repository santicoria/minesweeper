
Arquitectura general de la aplicacion:

    - Servidores:
        - Servidor principal:
            El servidor maneja 2 funcionalidades principales:
                - Logica del juego
                - Servidor de chat

        - Servidor Cliente
            Le permite a cada cliente participar en la partida de buscaminas y entrar al chat del servidor. La GUI del cliente (basada en Tkinter) le permite al usuario interactuar con eel juego de forma mas simple e intuitiva


Distribucion de procesos e hilos:

    -Procesos:
        - GameServer:
            El servidor principal del juego corre como un prceso separado. Este maneja:
                - La generacion del tablero
                - Almacena datos sobre estados del juego y movimientos de los usuarios
                - Responde a los request de los usuarios (como chequear minas o actualizar el estado del juego)
            Correr este proceso de forma independiente permite tener la logica de juego separada del chat y la GUI del cliente
        
        - Servidor de chat:
            El servidor del chat es un servidor independiente que corre de forma asincrona al GameServer. Este permite manejar multiples conexiones sin interferir con las operaciones de I/O del GameServer
    
    -Hilos:
        - GUI:
            La aplicacion utiliza Tkinter para generar la GUI. Esta GUI corre en el hilo principal, ya que Tkinter debe
            correr en el hilo principal para poder hacer actualizaciones de UI

        - Networking:
            - Todas las tareas de networking de la aplicacion (tanto para el juego como para el chat), son manejadas en un
            hilo diferente al de la GUI, para evitar que el loop de asyncio interfiera con la GUI.

            - En este hilo de networking, se corren las diferentes tareas (conectarse al servidor de juego o chat, mandar o 
            recibir mensajes) utilizando asyncio.

            - La comunicacion entre el hilo de networking y el de Tkinter es lograda con una cola (queue.Queue) que permite
            una comunicacion thread-safe.

            - Cuando llega un mensaje a asyncio, estos son agregados a una cola, y Tkinter chequea la cola de forma periodica, para luego actualizar la GUI cuando y como corresponda.

- IPC e ITC:
    - IPC:
        - Comunicacion entre el servidor de cliente y el servidor de juego:
            - Se utiliza un socket TCP que permite conexiones IPv4 e IPv6





    