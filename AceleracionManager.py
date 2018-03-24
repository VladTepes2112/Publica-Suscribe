#!/usr/bin/env python
# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------------------------------
# Archivo: AceleracionManager.py

# Autor(es): Perla Velasco & Yonathan Mtz.
# Descripción:
#
#   Ésta clase define el rol de un subscriptor que consume los mensajes de una cola
#   específica.
#   Las características de ésta clase son las siguientes:
#
#                                        AceleracionManager.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Recibir mensajes     |  - Se subscribe a la   |
#           |      Subscriptor      |  - Notificar al         |    cola de 'direct     |
#           |                       |    monitor.             |    acceleration'.      |
#           |                       |  - Filtrar valores      |  - Define un rango en  |
#           |                       |    extremos de tempera- |    el que la accelera- |
#           |                       |    tura.                |    ción tiene valores  |
#           |                       |                         |    válidos.            |
#           |                       |                         |  - Notifica al monitor |
#           |                       |                         |    un segundo después  |
#           |                       |                         |    de recibir el       |
#           |                       |                         |    mensaje.            |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |   start_consuming()    |          None            |  - Realiza la conexi- |
#           |                        |                          |    ón con el servidor |
#           |                        |                          |    de RabbitMQ local. |
#           |                        |                          |  - Declara el tipo de |
#           |                        |                          |    tipo de intercam-  |
#           |                        |                          |    bio y a que cola   |
#           |                        |                          |    se va a subscribir.|
#           |                        |                          |  - Comienza a esperar |
#           |                        |                          |    los eventos.       |
#           +------------------------+--------------------------+-----------------------+
#           |                        |   ch: propio de Rabbit   |  - Contiene la lógica |
#           |                        | method: propio de Rabbit |    de negocio.        |
#           |       callback()       |   properties: propio de  |  - Se manda llamar    |
#           |                        |         RabbitMQ         |    cuando un evento   |
#           |                        |       String: body       |    ocurre.            |
#           +------------------------+--------------------------+-----------------------+
#           |                        |   nombre: nombre del     |  - Envía los datos al |
#           |                        |      paciente que cayó   |    monitor para que   |
#           |                        | identificador: identifi- |    sean impresos      |
#           |       imprimir()       |      cador del paciente  |  - Se manda llamar    |
#           |                        |      que cayó            |    cuando un evento   |
#           |                        |                          |    ocurre.            |
#           +------------------------+--------------------------+-----------------------+
#
#
#--------------------------------------------------------------------------------------------------

import pika
import sys
from SignosVitales import SignosVitales


class AceleracionManager:
    aceleracion_maxima = 0
    status = ""
    values_parameters = 0


    def start_consuming(self):

        #   +--------------------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con el servidor que aloja a RabbitMQ |
        #   +--------------------------------------------------------------------------------------+
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        channel = connection.channel()
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir el tipo de intercambio y de que cola recibirá datos |
        #   +----------------------------------------------------------------------------------------+
        channel.exchange_declare(exchange='direct_acceleration',
                                 type='direct')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        severity = 'aceleracion'
        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con la cola que se definio |
        #   +----------------------------------------------------------------------------+
        channel.queue_bind(exchange='direct_acceleration',
                            queue=queue_name, routing_key=severity)
        print(' [*] Inicio de monitoreo de temperatura. Presiona CTRL+C para finalizar el monitoreo')
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir las acciones que se realizarán al ocurrir un método |
        #   +----------------------------------------------------------------------------------------+
        channel.basic_consume(self.callback,
                              queue=queue_name,
                              no_ack=True)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        values = body.split(':')
        vector_x = float(values[3])
        vector_y = float(values[4])
        vector_z = float(values[5])

        if (vector_x > -0.129 and vector_x < 0.536) and (vector_y > -0.171 and vector_y < 0.999) and (vector_z > -0.999 and vector_y < 0.999):
	        self.imprimir(values[2], values[1])
        elif (vector_x > -0.236 and vector_x < 0.624) and (vector_y > -0.250 and vector_y < 0.999) and (vector_z > 0.525 and vector_y < 0.999):
            self.imprimir(values[2], values[1])
        elif (vector_x > -0.042 and vector_x < 0.599) and (vector_y > 0.690 and vector_y < 0.999) and (vector_z > 0.020 and vector_y < 0.783):
            self.imprimir(values[2], values[1])
        elif (vector_x > -0.812 and vector_x < 0.171) and (vector_y > 0.080 and vector_y < 0.999) and (vector_z > -0.45 and vector_y < 0.999):
            self.imprimir(values[2], values[1])

    def imprimir(self, nombre, identificador):
        monitor = SignosVitales()
        monitor.print_notification('+----------+-----------------------+----------+')
        monitor.print_notification('|   ' + str(identificador) + '   |     SE HA CAIDO   |  ' + str(nombre) + '   |')
        monitor.print_notification('+----------+-----------------------+----------+')
        monitor.print_notification('')
        monitor.print_notification('')


test = AceleracionManager()
test.start_consuming()
