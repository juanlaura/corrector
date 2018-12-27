#!/usr/local/bin/python3
import sys
import json
import socket
import logging
from pandasworker import PandasWorker

PORT = 5007
BUFFER_SIZE = 1024
class TCPServer:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.DEBUG)

        self.logger.info("Iniciando servidor...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((socket.gethostname(), PORT))
        self.socket.listen(10)

    def correr(self):
        """Bucle principal del servidor. Acepta conexiones y hace el dispatch
        en el mismo hilo."""
        self.logger.info("Escuchando..")
        while True:
            (connection, address) = self.socket.accept()
            self.logger.info("Conexión aceptada de {}".format(address))
            self.procesar_cliente(connection)
            connection.close()
            self.logger.info("Conexión cerrada")

    def procesar_cliente(self, connection):
        """Maneja un socket a cliente, recibiendo toda la información hasta
        que el cliente avise que no escribirá más con shutdown(WR).
        Este esquema es similar al que utiliza HTTP.
        Se procesa el trabajo y se le envía una respuesta.
        Esta función abstrae al resto del JSON."""
        buffer = connection.recv(BUFFER_SIZE)
        request = b""
        while buffer:
            self.logger.debug("Buffer cargado de longitud: {}".format(buffer))
            request += buffer
            buffer = connection.recv(BUFFER_SIZE)

        self.logger.debug("Datos recibidos: {}".format(request))
        # Cargamos el trabajo y lo mandamos a procesar.
        trabajo = json.loads(request)
        respuesta = self.correr_trabajo(trabajo)
        self.logger.debug("Enviando respuesta: {}".format(respuesta))
        #sendall() nos abstrae del loop de envío
        connection.sendall(json.dumps(respuesta).encode("utf-8"))

    def correr_trabajo(self, trabajo):
        return {"error": "", "output": "todo OK!"}

    def __del__(self):
        self.socket.close()

if __name__ == "__main__":
    # Preparamos el servidor
    ServerWorker = TCPServer()
    ServerWorker.correr()
    # Cargamos el json de la entrada estándar.
    #ejercicios = json.loads(sys.stdin.read())

    #if args.worker_type == "pandas":
    #    worker = PandasWorker(ejercicios)
0
    #worker.correr()
    #print(json.dumps(worker.respuestas()))
