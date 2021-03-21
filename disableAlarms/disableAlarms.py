import json

import boto3
import re

def lambda_handler(event, context):
    client = boto3.client('cloudwatch')
    paginator = client.get_paginator('describe_alarms')
    i = 0
    cant = 0
    alarmMaxRecords = 100    
    
    #Paginator es un objeto Python
    #El paginator es por si hay mas de 50 alarmas, hay que iterarlo y va trayendo de hasta 100 (default 50)    
    #Se puede utilizar el parametro AlarmNamePrefix para filtrar por las que comienzan con x string
    for alarmas in paginator.paginate(MaxRecords=alarmMaxRecords):
        n = 0
        #Recorro hasta fin de lista de alarmas
        while n < len(alarmas.get('MetricAlarms')): 
            alarma = alarmas.get('MetricAlarms')[n]
            #En este caso filtramos por las alarmas que contengan x string dentro
            if 'xxxx' in alarma.get('AlarmName'):
                client.disable_alarm_actions(AlarmNames=[alarma.get('AlarmName')])    
                cant += 1    
            n += 1        
        i += 1

    mensaje = ('Se procesaron '+ str(i) + ' paginas de ' + str(alarmMaxRecords) + ' alarmas; se deshabilitaron ' + str(cant) +' alarmas' )

    return {
        'statusCode': 200,
        'body': json.dumps(mensaje)
    }
    
     