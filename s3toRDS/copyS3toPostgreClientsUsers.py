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

#Ver si tiene que estar publica, si lore ejecutaba desde una vpc cerrada desde la ec2)
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

    #traigo archivos s3
    s3_client = boto3.client('s3')
    for record in event['Records']:
        filename = record['s3']['object']['key']
        print(filename)
        data = s3_client.get_object(Bucket='bucketparaupload', Key=filename)     
        contents = data['Body']
        contentsdata = contents.read().decode('utf-8') 
        stringio_data = io.StringIO(contentsdata)   

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = create_conn()
        conn.autocommit = True        
        cursortest = conn.cursor()   
        try:
            
            if 'clients' in filename:
                print('ejecuto querys clients ')
                cursortest.execute("truncate table clients;")
                cursortest.execute("drop index if exists XIndex_CUIT_clients;")
                cursortest.copy_from(stringio_data, 'clients (registro)')        
                cursortest.execute("update clients set cuit = substring(registro,30,11);")
                cursortest.execute("CREATE INDEX XIndex_CUIT_clients  ON clients USING btree (cuit COLLATE pg_catalog.default );") 
                
            if 'users' in filename:
                print('ejecuto querys users')
                cursortest.execute("truncate table users;")
                cursortest.execute("drop index if exists XIndex_CUIT_users;")
                cursortest.copy_from(stringio_data, 'users (registro)')        
                cursortest.execute("update users set cuit = substring(registro,30,11);")
                cursortest.execute("CREATE INDEX XIndex_CUIT_users  ON users USING btree (cuit COLLATE pg_catalog.default );") 
                
            conn.commit()
            conn.close()       
            
        except Exception as ex:
            print("Error en conexion/sentencia sql.")
            print(ex)    
        

