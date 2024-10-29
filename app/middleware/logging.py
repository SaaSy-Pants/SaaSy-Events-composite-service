import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

#Configuring the logger
logger = logging.getLogger("composite_service_logger")
logger.setLevel(logging.INFO)

#Creating console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

#Creating formatter and add it to the handlers
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

#Adding the handlers to the logger
if not logger.handlers:
    logger.addHandler(console_handler)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        method = request.method
        url = request.url.path
        client_host = request.client.host

        logger.info(f"Incoming request: {method} {url} from {client_host}")

        try:
            response: Response = await call_next(request)
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            raise e

        process_time = (time.time() - start_time) * 1000
        status_code = response.status_code

        logger.info(
            f"Response: {status_code} for {method} {url} in {process_time:.2f}ms"
        )

        return response
