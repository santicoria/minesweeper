- Abrir CMD, Powershell o bash
- Iniciar el Servidor introduciendo alguno de los siguientes comandos en la consola:
    - Para iniciar el Server:
        - IPv4:
            py .\minesweeper.py --mode server --host (IP del servidor) --port (Puerto del servidor) --difficulty (Dificultad de la partida, puede ser 0, 1 o 2) --ipv 4

            Ejemplo:
                py .\minesweeper.py --mode server --host 127.0.0.1 --port 5000 --difficulty 0 --ipv 4
        
        - IPv6:
            py .\minesweeper.py --mode server --host (IP del servidor) --port (Puerto del servidor) --difficulty (Dificultad de la partida, puede ser 0, 1 o 2) --ipv 6

            Ejemplo:
                py .\minesweeper.py --mode server --host ::1 --port 5000 --difficulty 0 --ipv 6

- Iniciar el cliente introduciendo alguno de los siguientes comandos en la consola:
    - Para iniciar el Client: 
        -IPv4:
            py .\minesweeper.py --mode client --host (IP del servidor) --port (Puerto del servidor) --user (Nombre de usuario a eleccion) --ipv 4

            Ejemplo:
                py .\minesweeper.py --mode client --host 127.0.0.1 --port 5000 --user Santi --ipv 4

        -IPv6:
            py .\minesweeper.py --mode client --host (IP del servidor) --port (Puerto del servidor) --user (Nombre de usuario a eleccion) --ipv 6

            Ejemplo:
                py .\minesweeper.py --mode client --host ::1 --port 5000 --user Santi --ipv 6
    
    

