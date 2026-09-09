"""
BATALLA NAVAL - CLIENTE (ATACANTE)
------------------------------------
El atacante inicia la comunicación con connect() hacia la IP del defensor.
Cada coordenada que envía es una PETICIÓN de texto (request).
Cada AGUA/TOCADO que recibe es una RESPUESTA de texto (response).
Regla de oro: send = encode | receive = decode
"""

import socket

PORT = 5050 # Debe coincidir exactamente con el puerto del servidor


def main():
    # Solicita la IP al usuario. Si presiona Enter sin escribir nada, usa '127.0.0.1' (localhost)
    host = input("IP del servidor (defensor) [127.0.0.1]: ").strip() or '127.0.0.1'

    # 1) Crear el socket
    # Configuración idéntica al servidor: IPv4 (AF_INET) y TCP (SOCK_STREAM)
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) connect: iniciar la comunicación con el defensor
    # Intenta establecer la conexión con la IP y puerto proporcionados
    cliente_socket.connect((host, PORT))
    print(f"[ATACANTE] Conectado al defensor en {host}:{PORT}")
    print("Tablero de 5x5. Filas A-E, columnas 1-5. Ejemplo: B3")
    print("Escribe SALIR para terminar la partida.\n")

    try:
        # Bucle principal de envío de ataques
        while True:
            # Pide la coordenada al usuario
            ataque = input("Coordenada de ataque: ").strip()
            
            # Si el usuario presiona Enter sin escribir nada, vuelve a pedir
            if not ataque:
                continue

            # send = encode. Codifica el texto a bytes y lo envía al servidor
            cliente_socket.send(ataque.encode('utf-8'))

            # Si el usuario quiere salir, espera la respuesta de despedida y rompe el ciclo
            if ataque.upper() == "SALIR":
                respuesta = cliente_socket.recv(1024).decode('utf-8')
                print(f"[ATACANTE] {respuesta}")
                break

            # receive = decode. Espera la respuesta del servidor (AGUA, TOCADO, etc.)
            datos = cliente_socket.recv(1024)
            if not datos:
                # Si los datos están vacíos, el servidor se cayó o cerró la conexión
                print("[ATACANTE] El defensor cerró la conexión.")
                break

            # Convierte los bytes de respuesta a texto
            respuesta = datos.decode('utf-8')
            print(f"[ATACANTE] Resultado: {respuesta}")

            # Verifica si el servidor confirmó la victoria para terminar el juego localmente
            if respuesta == "TOCADO-GANASTE":
                print("[ATACANTE] ¡Ganaste la batalla naval!")
                break
    finally:
        # Cierra el socket al finalizar, ya sea por victoria, por salir, o por error
        cliente_socket.close()
        print("[ATACANTE] Conexión cerrada.")


if __name__ == "__main__":
    main()