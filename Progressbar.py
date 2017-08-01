#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import time
import sys


class Progressbar(object):
	"""
	   clase que creara la barra de progreso para las descargas 

	   install[##########          ]  20%

	"""

	__TAMAÑOBARRA = 30
	__SUBDIVISION = 28

	__PROGRESSCHAR = ''
	__TAREANOMBRE = ''
	__VALOR = 0


	def __init__(self, taskName, valorinicial, Progresschar='#'):
		"""  Recibe los valores y inicializa la clase. """
		if (len(Progresschar)!=1):
			Progresschar = '#'
		self.__taskName = taskName
		self.__Valor = valorinicial
		self.__PROGRESSCHAR = Progresschar
		self.__MuestraBarra()



	def run(self):
		"""Ejecuta la clase con los valores pasados."""
		self.ProgressBar(self.__taskName, self.__initValue)
		for val in range(102):
			self.setValue(val)
			time.sleep(0.001)



	def __MuestraBarra(self):
		""" Muestra la barra segun el progreso. """
		vaciado = int(self.__Valor/2)
		llenado = self.__SUBDIVISION-vaciado
		barra = str(vaciado*self.__PROGRESSCHAR)+str(vaciado*' ')
		Llenado = '{0}[{1}] {2:3d}%'.format(self.__taskName,barra, self.__Valor)
		print(Llenado, end='' if self.__Valor <= 100 and self.__Valor >= 100 else '\n')

	def setValor(self, val):
		""" Da el valor a progressbar y lo actualiza. """
		if(isinstance(val,int) and val >= 0 and val <= 100):
			self.__value = val
			self.__Limpia()
			self.__MuestraBarra()

	def __Limpia(self):
		""" Va limpiando la barra y re-escribiendo """
		print('\r'*(self.__TAMAÑOBARRA+len(self.__taskName)),end='')

		
		



#a = Progressbar('install', 20)

