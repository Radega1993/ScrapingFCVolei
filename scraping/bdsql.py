# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import re

from  resources.auth import auth

class PYbd(object):
    """docstring for PYbd."""

    def push_data(self, data):
        try:
            connection = auth()

            if data != []:
                for key, value in data.items():
                    value = re.sub('[^a-zA-Z0-9òàèìùáéíóúÀÈÌÒÙÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', ' ', value)
                    if key == "nombre_liga":
                        nombre_liga = value
                    elif key == "grupo":
                        grupo = value
                    elif key == "numero_jornada":
                        numero_jornada = value
                    elif key == "local":
                        local = value
                    elif key == "visitant":
                        visitant = value
                    elif key == "dia":
                        dia = value
                    elif key == "hora":
                        hora = value
                    else:
                        lugar = value

                mySql_insert_query = "INSERT INTO partidos \
                                    (nombre_liga, grupo, numero_jornada, \
                                     local, visitant, dia, hora, lugar)\
                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (nombre_liga, grupo, numero_jornada, local, visitant, dia, hora, lugar)

                cursor = connection.cursor()
                cursor.execute(mySql_insert_query, val)
                connection.commit()
                print(cursor.rowcount, "Record inserted successfully into partidos table")
                cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert record into partidos table {}".format(error))

        finally:
            if (connection.is_connected()):
                connection.close()
                print("MySQL connection is closed")
