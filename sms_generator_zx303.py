def ip_to_hex(ip_str):
    return ''.join(f'{int(part):02X}' for part in ip_str.split('.'))

def port_to_hex(port):
    return f'{port:04X}'

def generar_sms(ip, puerto):
    ip_hex = ip_to_hex(ip)
    puerto_hex = port_to_hex(puerto)
    payload = f'78780766{ip_hex}{puerto_hex}0D0A'
    return payload.upper()

# Ejemplo de uso
if __name__ == "__main__":
    ip = input("Introduce la IP del servidor (ej: 192.168.1.100): ").strip()
    puerto = int(input("Introduce el puerto (ej: 6063): ").strip())
    sms_hex = generar_sms(ip, puerto)
    print(f"\n📤 SMS a enviar (hex): {sms_hex}")
    print(f"💡 Usa este mensaje con el número de teléfono del dispositivo (nano SIM instalada)")
