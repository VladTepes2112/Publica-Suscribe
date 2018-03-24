#!/usr/bin/env python
# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------------------------------
# Archivo: TemporizadorManager.py
#
# Autor(es): Miembros del equipo de desarrollo de DevForce
# Descripción:
#
#   Ésta clase define el rol de un subscriptor que consume los mensajes de una cola
#   específica.
#   Las características de ésta clase son las siguientes:
#
#                                        TemporizadorManager.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Recibir mensajes     |  - Se subscribe a la   |
#           |      Subscriptor      |  - Notificar al         |    cola de 'direct     |
#           |                       |    monitor.             |    timer'.             |
#           |                       |                         |  - Recupera y muestra  |
#           |                       |                         |    la hora a la que un |
#           |                       |                         |    paciente toma su    |
#           |                       |                         |    medicamento.        |
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
#           |                        |                          |  - Lee los argumentos |
#           |                        |                          |    con los que se e-  |
#           |                        |                          |    jecuta el programa |
#           |                        |                          |    para establecer el |
#           |                        |                          |    valor máximo que   |
#           |                        |                          |    puede tomar la     |
#           |                        |                          |    temperatura.       |
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
#
#
#--------------------------------------------------------------------------------------------------

import pika
import sys
from SignosVitales import SignosVitales


class TemporizadorManager:
    status = ""


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
        channel.exchange_declare(exchange='direct_timer',
                                 type='direct')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        severity = 'temporizador'
        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con la cola que se definio |
        #   +----------------------------------------------------------------------------+
        channel.queue_bind(exchange='direct_timer',
                            queue=queue_name, routing_key=severity)
        print(' [*] Inicio de monitoreo del temporizador. Presiona CTRL+C para finalizar el monitoreo')
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir las acciones que se realizarán al ocurrir un método |
        #   +----------------------------------------------------------------------------------------+
        channel.basic_consume(self.callback,
                              queue=queue_name,
                              no_ack=True)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        values = body.split(';')
        nombre = str(values[2])
        nombre_medicamento = str(values[3])
        hora = str(values[4])
        dosis = str(values[5])

        monitor = SignosVitales()
        monitor.print_notification('+----------+--------------+----------------------+----------+----------+----------+')
        monitor.print_notification('|   ' + str(values[1]) + '   |  ' + str(nombre) +   '   |     HORA DE MEDICAMENTO   |  ' + str(nombre_medicamento) + '   |  DOSIS: ' + dosis + '  |  ' + str(hora) + ' |')
        monitor.print_notification('+----------+--------------+----------------------+----------+----------+----------+')
        monitor.print_notification('')
        monitor.print_notification('')



test = TemporizadorManager()
test.start_consuming()
