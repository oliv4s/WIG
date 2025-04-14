import socket
import threading
import struct
import binascii
from datetime import datetime

HOST = '0.0.0.0'
PORT = 6063

def bcd_to_int(bcd):
    return ((bcd >> 4) * 10) + (bcd & 0x0F)

def decode_datetime(b):
    year = 2000 + bcd_to_int(b[0])
    month = bcd_to_int(b[1])
    day = bcd_to_int(b[2])
    hour = bcd_to_int(b[3])
    minute = bcd_to_int(b[4])
    second = bcd_to_int(b[5])
    return datetime(year, month, day, hour, minute, second)

def decode_gps_coords(raw_bytes):
    # Convert from 4 bytes to int
    raw = int.from_bytes(raw_bytes, byteorder='big')
    # Convert back to degrees: (value / 30000) = degrees * 60 + minutes
    degrees_minutes = raw / 30000
    degrees = int(degrees_minutes / 60)
    minutes = degrees_minutes - degrees * 60
    return degrees + minutes / 60

def handle_client(conn, addr):
    print(f"🔌 Conexión recibida de {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break

        hex_str = binascii.hexlify(data).decode('utf-8')
        print(f"📩 Paquete recibido (hex): {hex_str}")

        if hex_str.startswith('7878') and hex_str[6:8] == '10':
            # Decodificar protocolo 0x10 (GPS)
            content = data[4:-2]  # Excluye start, length, stop
            dt = decode_datetime(content[0:6])
            lat_bytes = content[8:12]
            lon_bytes = content[12:16]

            latitude = decode_gps_coords(lat_bytes)
            longitude = decode_gps_coords(lon_bytes)

            # Obtener dirección (N/S, E/W)
            state = content[17]
            ns = 'N' if (state & 0b00000010) else 'S'
            ew = 'E' if (state & 0b00000001) else 'W'

            print(f"📍 Fecha/Hora: {dt}")
            print(f"🌐 Coordenadas: {latitude:.6f}° {ns}, {longitude:.6f}° {ew}")
            print("-" * 40)

        # Enviar ACK (mínimo)
        try:
            conn.sendall(binascii.unhexlify("787801100D0A"))
        except:
            pass

    conn.close()
    print(f"🔌 Conexión cerrada con {addr}")

def start_server():
    print(f"🛰️  Servidor ZX303 escuchando en {HOST}:{PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
