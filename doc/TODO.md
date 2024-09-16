Algunas opciones de mejoras pueden ser:
    - Crear un modo competitivo:
        - Crear un modo en el que el servidor crea un solo tablero comun para todos los jugadores y que gane aquel que logre
        terminarlo en el menor tiempo posible o el ultimo que quede en pie. Deberia haber un timeout por inactividad para evitar que los jugadores no ingresen ningun movimiento y asi ganar por ser el ultimo en pie

    - Implementar mecanismos anti-bloqueo en el Cliente:
        - En el caso del cliente, el loop de Networking y la GUI corren en hilos diferentes, lo cual significa que comparten el espacio de memoria y otros recursos. Si se dan las condiciones, estoo puede causar una condicion de carrera lo cual puede llevar al bloqueo de recursos y la relentizacion (o inutilizacion) del programa. Se podrian implementar semaforos o locks. (Solucion implementada, se usa queue para datos compartidos entre hilos)
