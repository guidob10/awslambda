import json
import boto3
import zipfile
import io
from io import BytesIO
from io import StringIO
import sys

#Descromprime archivo .zip que llega por trigger y lo guarda en otro bucket

def lambda_handler(event, context):

    s3_resource = boto3.resource('s3')
    #Llega evento desde trigger s3 al subir .zip a carpeta guidob10/carpetatest/
    for record in event['Records']:
        filetrigger = record['s3']['object']['key']
        zip_obj = s3_resource.Object(bucket_name="guidob10", key=filetrigger)        
        
    buffer = BytesIO(zip_obj.get()["Body"].read())

    z = zipfile.ZipFile(buffer)

    for filename in z.namelist():
        print(filename)
        file_info = z.getinfo(filename)
        contentsdata = z.open(filename).read()
        #Esto solo hace el upload en el bucle, le pasa nombre del archivo dentro del zip con filename

        s3_resource.meta.client.upload_fileobj(
            z.open(filename),
            Bucket="bucketparaupload",
            Key='result_ard/' + f'{filename}')   
    

