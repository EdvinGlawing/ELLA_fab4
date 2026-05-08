from fastapi import FastAPI, Request
from starlette.responses import Response
from starlette.middleware.base import RequestResponseEndpoint
import time
import mlflow
from .constants import MONITORING_PATH


def logging_middleware(app: FastAPI):
    @app.middleware("http")
    async def mlflow_middleware(
        request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        mlflow.set_tracking_uri(f"sqlite:///{MONITORING_PATH / 'mlflow.db'}")
        start_time = time.perf_counter()

        # Ange experiment explicit så agents.py inte kan störa
        with mlflow.start_run(
            run_name=f"{request.method} {request.url.path}",
            experiment_id=mlflow.set_experiment("brottsbalken").experiment_id,
        ):
            try:
                response = await call_next(request)
            except Exception as e:
                mlflow.set_tag("error", str(e))
                raise

            elapsed_time_seconds = time.perf_counter() - start_time

            mlflow.log_metric("status_code", response.status_code)
            mlflow.log_metric("latency_seconds", elapsed_time_seconds)
            mlflow.log_params(
                {
                    "endpoint": request.url.path,
                    "method": request.method,
                    "is_error": response.status_code >= 400,
                }
            )
            mlflow.set_tags(
                {
                    "environment": "dev",
                    "client_ip": request.client.host,  # ← bugg: du hade request.url.path här
                    "method": request.method,
                }
            )

        return response