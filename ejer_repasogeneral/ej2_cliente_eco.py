import socket

HOST = "127.0.0.1"   # IP del servidor (127.0.0.1 = este mismo equipo). Cambiar si esta en otra PC.
PUERTO = 5000
cliente = socket.create_connection((HOST, PUERTO))
buffer = ""  

for mensaje in ["hola", "redes", "adios"]:
    cliente.sendall((mensaje + "\n").encode("utf-8"))
    while "\n" not in buffer:
        datos = cliente.recv(1024)
        if not datos:          # el servidor cerro la conexion
            break
        buffer += datos.decode("utf-8")   # decode al recibir

    respuesta, buffer = buffer.split("\n", 1)
    print(f"Enviado: {mensaje!r:10} -> Respuesta: {respuesta!r}")

cliente.close()  
