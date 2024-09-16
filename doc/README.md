Antes de seguir con esta guia, por favor leer el archivo llamado INSTALL.md para instalar todos los paquetes necesarios

- Abrir CMD, Powershell o bash
- Iniciar el Servidor introduciendo alguno de los siguientes comandos en la consola:
    - Para iniciar el Server:
        - IPv4:
            py .\gameServer.py --host (IP del servidor) --port (Puerto del servidor) --difficulty (Dificultad de la partida, puede ser 0, 1 o 2) --ipv 4

            Ejemplo:
                py .\gameServer.py --host 127.0.0.1 --port 5000 --difficulty 0 --ipv 4
        
        - IPv6:
            py .\gameServer.py --host (IP del servidor) --port (Puerto del servidor) --difficulty (Dificultad de la partida, puede ser 0, 1 o 2) --ipv 6

            Ejemplo:
                py .\gameServer.py --host ::1 --port 5000 --difficulty 0 --ipv 6

- Iniciar el cliente introduciendo alguno de los siguientes comandos en la consola:
    - Para iniciar el Client: 
        -IPv4:
            py .\clientServer.py --host (IP del servidor) --port (Puerto del servidor) --user (Nombre de usuario a eleccion) --ipv 4

            Ejemplo:
                py .\clientServer.py --host 127.0.0.1 --port 5000 --user Santi --ipv 4

        -IPv6:
            py .\clientServer.py --host (IP del servidor) --port (Puerto del servidor) --user (Nombre de usuario a eleccion) --ipv 6

            Ejemplo:
                py .\clientServer.py --host ::1 --port 5000 --user Santi --ipv 6
    
    

