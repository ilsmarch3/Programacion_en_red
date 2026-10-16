import socket

HOST = "0.0.0.0"   # 0.0.0.0 = escuchar en todas las interfaces de red del equipo
PUERTO = 5000
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PUERTO))
servidor.listen(5)
print(f"Servidor de eco escuchando en el puerto {PUERTO}...")

while True:
    conexion, direccion = servidor.accept()
    print(f"Cliente conectado desde {direccion}")

    buffer = ""   
    while True:
        datos = conexion.recv(1024)   # recibe HASTA 1024 bytes
        if not datos:
            print(f"Cliente {direccion} se desconecto")
            break
        buffer += datos.decode("utf-8")

        # Mientras haya al menos un mensaje completo en el buffer, lo extraemos
        while "\n" in buffer:
            mensaje, buffer = buffer.split("\n", 1)
            print(f"Recibido de {direccion}: {mensaje}")
            conexion.sendall((mensaje + "\n").encode("utf-8"))
    conexion.close()
