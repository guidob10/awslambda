#!/usr/bin/python
import boto3
import psycopg2
import zipfile
from io import BytesIO
import io
import sys
import uuid
import csv
import os 
import tempfile
from io import StringIO

#Corta archivo luego del ultimo ; hace un copy en la base.
db_host = "base.us-east-2.rds.amazonaws.com"
db_port = 5432
db_name = "postgres"
db_user = "postgres"
db_pass = "x"

def create_conn():
    conn = None
    try:
        conn = psycopg2.connect("dbname={} user={} host={} password={}".format(db_name,db_user,db_host,db_pass))

    except Exception as ex:
        print("Cannot connect. ")
        print(ex)

    return conn


def lambda_handler(event, context):

    s3_resource = boto3.resource('s3')

    #Archivo llega como latin-1, si hay caracter especial mal formado lo salta y crea una nueva linea, pero queda correctamente una para ese registro
    #traigo archivos s3
    s3_client = boto3.client('s3')
    for record in event['Records']:
        filename = record['s3']['object']['key']
        txt_file = s3_resource.Object('bucketparaupload', filename).get()['Body'].read().decode('latin-1').splitlines()
        

    archivo_salida = ''
    i= 0
    for line in txt_file:
        #Elimino todo lo que sigue despues despues de la ultima ; ademas agrego salto de linea para poder utilizar el copy de pyscopg2
        try:
            archivo_salida += (line[0:line.rindex(';')]+ '\n')
            i= i+1
              
        except ValueError as exc:         
            print("Error con caracter especial, verificar linea " + str(i) + str(line) + " " + str(exc))

        except Exception as ex:
            print("Error al procesar linea:  " + line + " " +str(ex))
            error = True

    stringio_data = io.StringIO(archivo_salida)   
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = create_conn()
    conn.autocommit = True        
    cursortest = conn.cursor()   
    
    try:
        cursortest.execute("truncate table clients;")
        cursortest.execute("drop index if exists XIndex_CUIT_clients;")
        cursortest.copy_from(stringio_data, 'clients',sep=';')
        cursortest.execute("CREATE INDEX XIndex_CUIT_clients  ON clients (CUIT);") 
        
        conn.commit()
        conn.close()     

    except Exception as ex:
        print("Error en conexion/sentencia sql.")
        print(ex)    

