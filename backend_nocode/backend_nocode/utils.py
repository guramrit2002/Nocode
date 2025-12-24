import datetime
from rest_framework.response import Response

def response(message:str, data:any, status:int)->Response:
    data = {"data":data}
    print({
            **{"message":message},
            **data,
            **{"timestamp":datetime.datetime.now()}
        })
    return Response(
        {
            **{"message":message},
            **data,
            **{"timestamp":datetime.datetime.now()}
        },status=status)