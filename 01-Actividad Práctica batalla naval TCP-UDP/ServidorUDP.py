"""
BATALLA NAVAL - SERVIDOR (DEFENSOR) - VERSIÓN UDP
---------------------------------------------------
Diferencia clave con TCP: UDP no tiene conexión.
No hay listen() ni accept(). Solo se hace bind() y luego se
reciben datagramas con recvfrom(), que además de los datos
devuelve la dirección (IP, puerto) de quien los mandó.
Esa dirección hay que guardarla para poder responder con sendto().

Regla de oro sigue siendo: send = encode | receive = decode
"""

import socket
import random

TAM = 5           # Tablero de 5x5 (filas A-E, columnas 1-5)
NUM_BARCOS = 3     # Cantidad de barcos (de 1 casilla cada uno)
PORT = 5050
BUFFER = 1024


def crear_barcos(tam, num_barcos):
    """Coloca los barcos en posiciones aleatorias del tablero."""
    barcos = set()
    while len(barcos) < num_barcos:
        fila = random.randint(0, tam - 1)
        col = random.randint(0, tam - 1)
        barcos.add((fila, col))
    return barcos


def coord_a_indices(coord, tam):
    """Convierte una coordenada tipo 'B3' en índices (fila, columna)."""
    coord = coord.strip().upper()
    if len(coord) < 2:
        return None
    try:
        fila = ord(coord[0]) - ord('A')
        col = int(coord[1:]) - 1
    except ValueError:
        return None
    if 0 <= fila < tam and 0 <= col < tam:
        return fila, col
    return None


def main():
    barcos = crear_barcos(TAM, NUM_BARCOS)
    tocados = set()

    # 1) Crear el socket UDP (SOCK_DGRAM en vez de SOCK_STREAM)
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2) bind: atar el socket a una IP y puerto (esto es lo único
    #    que se necesita, no hay listen() ni accept() en UDP)
    servidor_socket.bind(('0.0.0.0', PORT))

    print(f"[DEFENSOR] Escuchando datagramas UDP en el puerto {PORT}...")
    print(f"[DEFENSOR] Tablero {TAM}x{TAM} con {NUM_BARCOS} barcos escondidos.")

    direccion_atacante = None

    while True:
        # receive = decode. recvfrom() devuelve (datos, direccion_origen)
        datos, direccion = servidor_socket.recvfrom(BUFFER)
        direccion_atacante = direccion  # guardamos a quién responderle

        peticion = datos.decode('utf-8').strip()
        print(f"[DEFENSOR] Ataque recibido de {direccion}: {peticion}")

        if peticion.upper() == "SALIR":
            servidor_socket.sendto("CHAO".encode('utf-8'), direccion_atacante)
            print("[DEFENSOR] El atacante terminó la partida.")
            break

        indices = coord_a_indices(peticion, TAM)

        if indices is None:
            respuesta = "COORDENADA INVALIDA"
        elif indices in tocados:
            respuesta = "YA DISPARASTE AHI"
        elif indices in barcos:
            tocados.add(indices)
            if tocados == barcos:
                respuesta = "TOCADO-GANASTE"
            else:
                respuesta = "TOCADO"
        else:
            respuesta = "AGUA"

        # send = encode. sendto() necesita los datos Y la dirección destino,
        # porque en UDP no hay una conexión previa que "recuerde" a quién enviar.
        servidor_socket.sendto(respuesta.encode('utf-8'), direccion_atacante)
        print(f"[DEFENSOR] Respuesta enviada: {respuesta}")

        if respuesta == "TOCADO-GANASTE":
            print("[DEFENSOR] ¡Todos los barcos hundidos! Fin de la partida.")
            break

    servidor_socket.close()
    print("[DEFENSOR] Socket cerrado.")


if __name__ == "__main__":
    main()