import logging
from CoolProp.CoolProp import PropsSI
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        p = req_body.get('p')
        p1 = req_body.get('p1')
        v1 = req_body.get('v1')
        p2 = req_body.get('p2')
        v2 = req_body.get('v2')
        f = req_body.get('f')

    if p and p1 and v1 and p2 and v2 and f:
        return func.HttpResponse(f"{PropsSI(p, p1, v1, p2, v2, f)}")
    else:
        return func.HttpResponse(
            "Please pass a valid input on the query string or in the request body",
            status_code=400
        )
