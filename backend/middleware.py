import datetime
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
import boto3


class CloudWatchMetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.client = boto3.client("cloudwatch")

    async def dispatch(self, request, call_next):
        # Response Time
        start_time = datetime.datetime.now()
        response = await call_next(request)
        end_time = datetime.datetime.now()

        # Response Time in Milliseconds
        response_time = (end_time - start_time).total_seconds() * 1000

        # Called API
        path = request.url.path.split("?")[0]

        # Status Code
        code = response.status_code

        metric_dimensions = [{"Name": "API", "Value": path}]
        metric_data = [
            {
                "MetricName": "Requests",
                "Dimensions": metric_dimensions,
                "Timestamp": end_time,
                "Unit": "Count",
                "Value": 1
            },
            {
                "MetricName": "RequestLatency",
                "Dimensions": metric_dimensions,
                "Timestamp": end_time,
                "Unit": "Milliseconds",
                "Value": response_time
            },
            {
                "MetricName": f"{self._code_to_status(code)}StatusCode",
                "Dimensions": metric_dimensions,
                "Timestamp": end_time,
                "Unit": "Count",
                "Value": 1
            }
        ]

        # Send to CloudWatch Metrics
        self.client.put_metric_data(Namespace="CustomMetrics", MetricData=metric_data)

        # Debug
        print(f"Path: {path}, Status Code: {code}, Response Time: {response_time}")
        print(metric_data)

        return response

    def _code_to_status(self, code: int) -> str:
        if 100 <= code <= 599:
            return f"{code // 100}xx"
        else:
            return "Unknown"
