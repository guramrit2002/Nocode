import datetime
from rest_framework.response import Response

def response(message:str, data:dict, status:int)->Response:
    return Response(
        {
            **{"message":message},
            **data,
            **{"timestamp":datetime.datetime.now()}
        },status=status)