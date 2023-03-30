import requests
import lxml.html as html
import os
import datetime
from dotenv import load_dotenv
import telegram
import asyncio
import schedule
import time

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Función asincrónica para enviar mensajes a Telegram


async def send_telegram_message(token, chat_id, message):
    bot = telegram.Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except telegram.error.TelegramError as e:
        print(f"Error al enviar mensaje a Telegram: {str(e)}")

# Función asincrónica para obtener los datos del sitio web y enviarlos a Telegram


async def parse_home(token, chat_id):
    try:
        # * Obtener la página web
        response = requests.get(os.getenv('HOME_URL'))
        if response.status_code == 200:
            # * Obtener el contenido de la página
            home = response.content.decode('utf-8', errors='ignore')
            # * Convierte en un objeto de lxml
            parsed = html.fromstring(home)
            # * Obtiene los links de las noticias
            dollar_types = parsed.xpath(os.getenv('XPATH_LINKS'))
            # * Fecha de hoy para crear carpeta
            today = datetime.date.today().strftime('%d-%m-%Y')
            # * Crear la carpeta para guardar los archivos de hoy si no existe
            if not os.path.isdir(today):
                os.mkdir(today)

            # * Obtengo la cantidad de ciclos a ejecutar en base a la cantidad de tipos de dolar
            for i in range(len(dollar_types)):
                try:
                    # * Se obtienen los datos a enviar
                    title = parsed.xpath(os.getenv('XPATH_DOLLAR_TYPE'))[i]
                    precio_compra = parsed.xpath(
                        os.getenv('XPATH_PRICE_BUY'))[i]
                    precio_venta = parsed.xpath(
                        os.getenv('XPATH_PRICE_SELL'))[i]
                    variacion = parsed.xpath(os.getenv('XPATH_VARIATION'))[i]
                    fecha = parsed.xpath(os.getenv('XPATH_DATE'))[i]

                    # * Construir el nombre de archivo único
                    filename = f'{today}/{title.strip().replace("/","")}.txt'
                    # * Abrir el archivo en modo escritura y codificación utf-8
                    with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
                        # * Escribir cada dato en una línea separada
                        f.write('Dolar: ' + str(title) + '\n')
                        f.write('Precio compra: ' + str(precio_compra) + '\n')
                        f.write('Precio venta: ' + str(precio_venta) + '\n')
                        f.write('Variación: ' + str(variacion) + '\n')
                        f.write(
                            'Fecha: ' + str(fecha.strip().split(" ")[0]) + '\n')
                        f.write(
                            'Hora: ' + str(fecha.strip().split(" ")[1]) + '\n')
                    # * Crear el mensaje a enviar a Telegram
                    message = f"{title}\nPrecio compra: {precio_compra}\nPrecio venta: {precio_venta}\nVariación: {variacion}\nFecha: {fecha.strip().split(' ')[0]}\nHora: {fecha.strip().split(' ')[1]}"

                    # * Enviar el mensaje a Telegram
                    await send_telegram_message(token, chat_id, message)
                except IndexError:
                    return ""
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

# Se define la tarea a ejecutar


def job(telegram_token, telegram_chat_id):
    asyncio.run(parse_home(telegram_token, telegram_chat_id))


def run():
    # Obtener el valor de la variable de entorno TELEGRAM_BOT_TOKEN
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    # Obtener el valor de la variable de entorno TELEGRAM_CHAT_ID
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    # Se ejecuta la función cada 3 horas
    schedule.every(3).hours.do(
        job, telegram_token, telegram_chat_id)


if __name__ == '__main__':
    run()
    # bucle infinito para ejecutar la tarea programada
    while True:
        schedule.run_pending()
        time.sleep(60)
