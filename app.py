import os
import telebot
import dotenv
import logging
from dotenv import dotenv_values
from wakeonlan import send_magic_packet

dotenv.load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))

logging.basicConfig(
    level=logging.INFO,                                 # Nivel de registro mínimo
    format='%(asctime)s - %(levelname)s - %(message)s', # Formato del registro
    filename='app.log',                                 # Nombre del archivo de registro
    filemode='a'                                        # Modo de escritura: 'w' (crear nuevo archivo) o 'a' (adjuntar al archivo existente)
)

# Cargar las variables de entorno desde el archivo .env
env_vars = dotenv_values('.env')

# Diccionario de dispositivos autorizadas
dic_authorized_devices = {}

# Iterar sobre las variables de entorno y almacenar las que no contienen "token"
for key, value in env_vars.items():
    if 'token' not in key.lower():
        dic_authorized_devices[key] = value

devices = list(dic_authorized_devices.keys())


# Función para encender una device
def start_device(name, mac_address):
    print(f"Sending power signal to {name}...")
    logging.info(f"Sending power signal to {name}...")
    try:
        send_magic_packet(mac_address)
        return (f"Signal sent correctly to {name}.")
    except:
        return (f"Error sending signal to {name}.")


# Manejar todos los mensajes
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    for device in devices:
        if text == str(device).lower():
            # respuesta = verify_and_turn_on(message.text.lower())
            mac_address = dic_authorized_devices[device]
            respuesta = start_device(device, mac_address)
            logging.info(respuesta)
            bot.send_message(message.chat.id, respuesta)
            return

    logging.info(f'{text} device no find')
    bot.send_message(message.chat.id, f'{text} device no find')
    print(f'{text} device no find')

import time
# Ejecutar el programa
if __name__ == '__main__':
    print('start')
    while True:
        try:
            bot.polling()
        except:
            print("Error")
            logging.warning('Error')
        time.sleep(5)
