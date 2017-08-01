#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
from multiprocessing import Process, Manager


class Descarga():


	def __init__(self, args = None):
		self.url = args


	def descarga(self,orden,rango,frag):
		"se usa try catch para menejar posibles errores"
		try:
			print("Obteniendo fragmeto {}. Descargando desde byte {} hasta byte {}.".format(orden,*rango))
			"urllib.request.Requests(url) realiza la peticion a la url."
			req = urllib.request.Request(self.url)
			req.add_header('Range', 'bytes={}-{}'.format(*rango))
			data = urllib.request.urlopen(req).read()
			if data:
				frag[orden]=data
				print('Fragmento {} descargado correctamente. Obtenidos {} bytes.'.format(orden,len(data)))
			else:
				frag[orden]=None
		except:
			frag[orden]='#Error'
			raise


	def Descarga_paralela(self,fragmentos,nombre):
		ranges=None 
		with urllib.request.urlopen(self.url) as f:
			'comprobamos que el servidor acepte la descarga parcial.'
			if f.getheader("Accept-Ranges", "none").lower() != "bytes":
				print('Descarga parcial no soportada, iniciando descarga...')
			else:
				print('Descarga parcial soportada')
				'se obtiene el tamaño total del archivo.'
				size = int(f.getheader("Content-Length", "none"))
				print("Tamaño Total: {} bytes".format(size))
				
				#Dividimos ese tamaño en intervalos de acuerdo al número de procesos que lanzaremos
				
				tamF = size//fragmentos
				print('Fragmentos: {}.\nTamaño aproximado por fragmento: {} bytes.'.format(fragmentos, tamF))
				ranges = [[i, i+tamF-1] for i in range (0, size, tamF)]
				ranges[-1][-1]=size
				# se usa una diccionario compartido por los procesos, la clave sera el orden de cada fragmento de bytes tiene en el archivo final.
				manager = Manager()
				d = manager.dict()
				# Lanza todos los procesos.
				#target toma como parametro al metodo descarga de esta clase y args toma el
				#orden, rango y los fragmetos en los que se desea la descarga.
				workers = [Process(target=self.descarga, args=(i,r,d)) for i, r in enumerate(ranges)]
				for w in workers:
					w.start()
				for w in workers:
					w.join()
				#reconstruimos el archivo usando cada fragmento en su orden correcto.
				with open(nombre, 'wb') as f:
					for i in range(fragmentos):
						data = d[i]
						if data == None or data == '#Error.':
							print('El fragmento {} no se pude descargar. No se puede reconstruir el archivo.'.format(i))
							break
						else:
							f.write(data)
					else:
						print('Archivo descargado con exito.')



b = Descarga('https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Bow_Lake_beim_Icefields_Parkway.jpg/1280px-Bow_Lake_beim_Icefields_Parkway.jpg')
b.Descarga_paralela(16,'imagen.jpg')				

