import datetime
from rest_framework.response import Response

def response(message:str, data:any, status:int)->Response:
    if not isinstance(data, dict):
        data = {"data":data}
    return Response(
        {
            **{"message":message},
            **data,
            **{"timestamp":datetime.datetime.now()}
        },status=status)