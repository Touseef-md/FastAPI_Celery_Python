from fastapi import Request
# from ../tasks import log_acces 
from project.tasks import log_access

async def log_requests(request: Request, call_next):
    request_data = {
        'method': request.method,
        'url': str(request.url),
        'headers': dict(request.headers),
        'client_host': request.client.host,
    }
    print("INside the middleware: ", request)
    # print(request_data)
    print(request.url.query)
    log_access.delay(request.method +" "+ request.url.path + request.url.query)
    print("Task given to brker. Heading next")
    response = await call_next(request)
    return response
