Server: 
    py .\minesweeper.py --mode server --host 127.0.0.1 --port 5000 --difficulty 0 --ipv 4
    py .\minesweeper.py --mode server --host ::1 --port 5000 --difficulty 0 --ipv 6
    
Client: 
    py .\minesweeper.py --mode client --host 127.0.0.1 --port 5000 --user Santi --ipv 4
    py .\minesweeper.py --mode client --host ::1 --port 5000 --user Santi --ipv 6


read:
[y, x, estado, numero, bool]



* Uso de Sockets con conexión de clientes múltiples de manera concurrente. (DONE: Cliente, Servidor)
* Uso de mecanismos de IPC (PENDING: Opciones: Sistema de puntajes contra demas usuarios, live feed)
* Uso de asincronismo de I/O 
* Uso de cola de tareas distribuidas 
* Parseo de argumentos por línea de comandos (DONE: Server configs)
