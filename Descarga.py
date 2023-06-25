#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import requests
from concurrent.futures import ThreadPoolExecutor


class Descarga:

    def __init__(self, url):
        self.url = url

    def descarga(self, range_start, range_end):
        headers = {'Range': 'bytes={}-{}'.format(range_start, range_end)}
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print('Error en la descarga: {}'.format(str(e)))
            return None

    def descarga_paralela(self, fragmentos, nombre):
        try:
            response = requests.head(self.url)
            accept_ranges = response.headers.get('Accept-Ranges', 'none').lower()
            if accept_ranges != 'bytes':
                print('Descarga parcial no soportada, iniciando descarga secuencial...')
            else:
                print('Descarga parcial soportada')
                size = int(response.headers.get('Content-Length', 0))
                print("Tamaño Total: {} bytes".format(size))

                tamF = size // fragmentos
                print('Fragmentos: {}.\nTamaño aproximado por fragmento: {} bytes.'.format(fragmentos, tamF))

                ranges = [(i * tamF, min((i + 1) * tamF - 1, size - 1)) for i in range(fragmentos)]

                with ThreadPoolExecutor() as executor:
                    fragmentos_descargados = list(executor.map(lambda r: self.descarga(*r), ranges))

                with open(nombre, 'wb') as f:
                    for fragmento in fragmentos_descargados:
                        if fragmento is None:
                            print('No se pudo descargar un fragmento. No se puede reconstruir el archivo.')
                            break
                        f.write(fragmento)
                    else:
                        print('Archivo descargado con éxito.')
        except requests.exceptions.RequestException as e:
            print('Error en la descarga: {}'.format(str(e)))


b = Descarga('https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Bow_Lake_beim_Icefields_Parkway.jpg/1280px-Bow_Lake_beim_Icefields_Parkway.jpg')
b.descarga_paralela(16, 'imagen.jpg')



b = Descarga('https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Bow_Lake_beim_Icefields_Parkway.jpg/1280px-Bow_Lake_beim_Icefields_Parkway.jpg')
b.Descarga_paralela(16,'imagen.jpg')				

