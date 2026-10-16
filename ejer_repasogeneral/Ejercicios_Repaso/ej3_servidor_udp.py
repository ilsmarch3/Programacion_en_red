import socket
HOST = "0.0.0.0"
PUERTO = 5001
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PUERTO))
print(f"Servidor UDP escuchando en el puerto {PUERTO}...")

while True:
    # Espera un datagrama de cualquier cliente
    datos, direccion = servidor.recvfrom(1024)
    mensaje = datos.decode("utf-8").strip()   # strip quita espacios/saltos de linea sobrantes
    print(f"Datagrama de {direccion}: {mensaje!r}")

    if mensaje == "ESTADO":
        respuesta = "servidor activo"
    else:
        respuesta = "comando desconocido"

    # Se responde a la MISMA direccion de la que vino el datagrama
    servidor.sendto(respuesta.encode("utf-8"), direccion)
