import datetime
from rest_framework.response import Response

def response(message:str, data:any, status:int)->Response:
    
    if "errors" in data or "error" in data:
        data = {"error":data["errors"]} if "errors" in data else {"error":data["error"]}
    else:
        data = {"data":data}
    return Response(
        {
            **{"message":message},
            **data,
            **{"timestamp":datetime.datetime.now()}
        },status=status)