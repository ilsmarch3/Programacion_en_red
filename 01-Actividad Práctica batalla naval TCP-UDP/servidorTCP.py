"""
BATALLA NAVAL - SERVIDOR (DEFENSOR)
------------------------------------
El defensor espera de forma pasiva: bind -> listen -> accept.
Cada ataque que llega es una PETICIÓN de texto (request).
Cada AGUA/TOCADO que se devuelve es una RESPUESTA de texto (response).
Regla de oro: send = encode | receive = decode
"""

import socket
import random

# Configuraciones iniciales del juego y red
TAM = 5            # Tamaño del tablero: 5x5 (filas A-E, columnas 1-5)
NUM_BARCOS = 3     # Cantidad total de barcos a hundir
PORT = 5050        # Puerto por donde el servidor escuchará las conexiones


def crear_barcos(tam, num_barcos):
    """Coloca los barcos en posiciones aleatorias del tablero."""
    barcos = set() # Usamos un conjunto (set) para evitar posiciones duplicadas
    
    # Mientras no tengamos los barcos requeridos, seguimos generando coordenadas
    while len(barcos) < num_barcos:
        fila = random.randint(0, tam - 1) # Genera un índice de fila (0 a 4)
        col = random.randint(0, tam - 1)  # Genera un índice de columna (0 a 4)
        barcos.add((fila, col))           # Añade la tupla al conjunto
    return barcos


def coord_a_indices(coord, tam):
    """Convierte una coordenada tipo 'B3' en índices de matriz (fila, columna)."""
    coord = coord.strip().upper() # Limpia espacios y convierte a mayúsculas
    if len(coord) < 2:
        return None # Retorna None si el formato es muy corto (inválido)
    
    try:
        # Convierte la letra a índice: 'A' es 65 en ASCII. 'B'(66) - 'A'(65) = 1 (índice 1)
        fila = ord(coord[0]) - ord('A')
        # Convierte el número (ej. '3') a entero y le resta 1 para usar base 0
        col = int(coord[1:]) - 1
    except ValueError:
        return None # Falla si el segundo carácter no es un número
    
    # Verifica que los índices calculados no se salgan del tablero
    if 0 <= fila < tam and 0 <= col < tam:
        return fila, col
    return None


def main():
    # Inicializa el estado del juego
    barcos = crear_barcos(TAM, NUM_BARCOS)
    tocados = set() # Registro de los barcos que ya han sido impactados

    # 1) Crear el socket
    # AF_INET = IPv4 | SOCK_STREAM = TCP (Garantiza que los datos lleguen en orden)
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permite reutilizar el puerto inmediatamente después de cerrar el servidor
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2) bind: atar el socket a una IP y puerto
    # '0.0.0.0' indica que escuchará en todas las interfaces de red disponibles
    servidor_socket.bind(('0.0.0.0', PORT))

    # 3) listen: esperar pasivamente conexiones entrantes
    servidor_socket.listen(1) # Permite 1 conexión en cola como máximo
    print(f"[DEFENSOR] Esperando conexión en el puerto {PORT}...")
    print(f"[DEFENSOR] Tablero {TAM}x{TAM} con {NUM_BARCOS} barcos escondidos.")

    # 4) accept: aceptar la conexión del atacante (el programa se detiene aquí hasta que alguien se conecte)
    conexion, direccion = servidor_socket.accept()
    print(f"[DEFENSOR] Conectado con el atacante: {direccion}")

    try:
        # Bucle principal de la partida
        while True:
            # receive = decode. Recibimos hasta 1024 bytes del cliente.
            datos = conexion.recv(1024)
            if not datos:
                # Si 'datos' está vacío, el cliente se desconectó de forma inesperada
                print("[DEFENSOR] El atacante cerró la conexión.")
                break

            # Decodifica los bytes recibidos a texto normal (UTF-8)
            peticion = datos.decode('utf-8').strip()
            print(f"[DEFENSOR] Ataque recibido: {peticion}")

            # Condición de salida si el cliente decide rendirse o salir
            if peticion.upper() == "SALIR":
                conexion.send("CHAO".encode('utf-8')) # Despedida codificada
                break

            # Procesa la jugada
            indices = coord_a_indices(peticion, TAM)

            # Lógica de respuesta según la coordenada enviada
            if indices is None:
                respuesta = "COORDENADA INVALIDA"
            elif indices in tocados:
                respuesta = "YA DISPARASTE AHI"
            elif indices in barcos:
                tocados.add(indices) # Registra el impacto exitoso
                # Si la cantidad de impactos es igual a la de barcos, el juego termina
                if tocados == barcos:
                    respuesta = "TOCADO-GANASTE"
                else:
                    respuesta = "TOCADO"
            else:
                respuesta = "AGUA" # Falló el disparo

            # send = encode. Convertimos el texto a bytes antes de enviarlo por la red
            conexion.send(respuesta.encode('utf-8'))
            print(f"[DEFENSOR] Respuesta enviada: {respuesta}")

            # Verifica si el cliente ganó para cerrar el ciclo
            if respuesta == "TOCADO-GANASTE":
                print("[DEFENSOR] ¡Todos los barcos hundidos! Fin de la partida.")
                break
    finally:
        # Limpieza de recursos: es fundamental cerrar siempre los sockets
        conexion.close()
        servidor_socket.close()
        print("[DEFENSOR] Conexión cerrada.")


if __name__ == "__main__":
    main()