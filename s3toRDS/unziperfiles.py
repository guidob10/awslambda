import boto3
import json
import zipfile
from io import BytesIO

#Descromprime archivo .zip que llega por trigger y lo guarda en otro bucket

def lambda_handler(event, context):
#no hay folders en s3, esta el bucket y si vemos carpeta es que son parte del nombre carpetatest/clientes.zip     

    s3_resource = boto3.resource('s3')
    #Llega evento desde trigger s3 al subir .zip a carpeta guidob10/carpetatest/
    for record in event['Records']:
        filetrigger = record['s3']['object']['key']
        zip_obj = s3_resource.Object(bucket_name="guidob10", key=filetrigger)        

    #Leo archivos en memoria
    buffer = BytesIO(zip_obj.get()["Body"].read())

    #Descomprimo archivos, lo recorro y subo a otro bucket (no debe ser el mismo bucket) 
    z = zipfile.ZipFile(buffer)
    for filename in z.namelist():
        file_info = z.getinfo(filename)  
        s3_resource.meta.client.upload_fileobj(
            z.open(filename),
            Bucket="bucketparaupload",
            Key='result_files/' + f'{filename}')    
         
