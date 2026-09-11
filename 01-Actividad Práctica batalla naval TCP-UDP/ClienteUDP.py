"""
BATALLA NAVAL - CLIENTE (ATACANTE) - VERSIÓN UDP
---------------------------------------------------
En UDP no existe connect() en el sentido de "abrir una conexión":
no hay handshake ni sesión persistente. Cada datagrama se manda
suelto con sendto(), indicando la dirección destino cada vez.

Regla de oro sigue siendo: send = encode | receive = decode
"""

import socket

PORT = 5050
BUFFER = 1024


def main():
    host = input("IP del servidor (defensor) [127.0.0.1]: ").strip() or '127.0.0.1'
    direccion_servidor = (host, PORT)

    # 1) Crear el socket UDP (SOCK_DGRAM en vez de SOCK_STREAM)
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"[ATACANTE] Listo para atacar a {host}:{PORT} (UDP)")
    print("Tablero de 5x5. Filas A-E, columnas 1-5. Ejemplo: B3")
    print("Escribe SALIR para terminar la partida.\n")

    try:
        while True:
            ataque = input("Coordenada de ataque: ").strip()
            if not ataque:
                continue

            # send = encode. sendto() necesita los datos y la dirección destino.
            cliente_socket.sendto(ataque.encode('utf-8'), direccion_servidor)

            # receive = decode. recvfrom() bloquea hasta que llega respuesta.
            datos, _ = cliente_socket.recvfrom(BUFFER)
            respuesta = datos.decode('utf-8')

            if ataque.upper() == "SALIR":
                print(f"[ATACANTE] {respuesta}")
                break

            print(f"[ATACANTE] Resultado: {respuesta}")

            if respuesta == "TOCADO-GANASTE":
                print("[ATACANTE] ¡Ganaste la batalla naval!")
                break
    finally:
        cliente_socket.close()
        print("[ATACANTE] Socket cerrado.")


if __name__ == "__main__":
    main()