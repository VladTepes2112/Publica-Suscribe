#!/usr/bin/env python
# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------------------------------
# Archivo: SensorRitmoCardiaco.py
# Autor(es): Perla Velasco & Yonathan Mtz.
# Descripción:
#
#   Ésta clase define el rol de un publicador que envia mensajes a una cola
#   específica.
#   Las características de ésta clase son las siguientes:
#
#                                      SensorRitmoCardiaco.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Enviar mensajes      |  - Se conecta a la cola|
#           |      Publicador       |                         |    'direct rhythm'.    |
#           |                       |                         |  - Envia datos de los  |
#           |                       |                         |    latidos del corazón.|
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Inicializa los va- |
#           |       __init__()       |      String: nombre      |    lores de nombre e  |
#           |                        |                          |    id.                |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Genera de manera a-|
#           |        set_id()        |           None           |    leatoria el id del |
#           |                        |                          |    usuario.           |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Devuelve el nombre |
#           |       get_name()       |           None           |    del usuario al cual|
#           |                        |                          |    fue asignado el    |
#           |                        |                          |    sensor.            |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Realiza la conexión|
#           |                        |                          |    con el servidor    |
#           |                        |                          |    de RabbitMQ local. |
#           |                        |                          |  - Define a que cola  |
#           |     start_service()    |           None           |    enviará los mensa- |
#           |                        |                          |    jes.               |
#           |                        |                          |  - Define que tipo de |
#           |                        |                          |    publicación se uti-|
#           |                        |                          |    lizará.            |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Genera un número   |
#           |     simulate_data()    |           None           |    aleatorio entre 60 |
#           |                        |                          |    y 150.             |
#           +------------------------+--------------------------+-----------------------+
#
#
#--------------------------------------------------------------------------------------------------

import pika
import random


class SensorRitmoCardiaco:
    nombre = None
    id = 0

    def __init__(self, nombre):
        self.nombre = nombre
        self.id = int(self.set_id())

    def set_id(self):
        return random.randint(1000, 5000)

    def get_name(self):
        return self.nombre

    def start_service(self):
        #   +--------------------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con el servidor que aloja a RabbitMQ |
        #   +--------------------------------------------------------------------------------------+
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir el tipo de intercambio y de que cola recibirá datos |
        #   +----------------------------------------------------------------------------------------+
        channel.exchange_declare(exchange='direct_rhythm', type='direct')
        severity = 'ritmo_cardiaco'
        ritmo_cardiaco_generado = self.simulate_data()
        mensaje = 'RC:' + str(self.id) + ':' + self.nombre + \
            ':' + str(ritmo_cardiaco_generado)
        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite enviar datos a la cola seleccionada.            |
        #   +----------------------------------------------------------------------------+
        channel.basic_publish(exchange='direct_rhythm',
                              routing_key=severity, body=mensaje)
        print('+---------------+--------------------+-------------------------------+-------+')
        print('|      ' + str(self.id) +'     |     ' + self.nombre +'     |    RITMO CARDIACO ENVIADO     |  ' + str(ritmo_cardiaco_generado) + '  |')
        print('+---------------+--------------------+-------------------------------+-------+')
        print('')
        connection.close()

    def simulate_data(self):
        return random.randint(int(60), int(150))
