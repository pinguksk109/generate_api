from typing import Self
import boto3
from botocore.exceptions import ClientError
from application.port.llm_answer_log_port import LlmAnswerLogPort
from application.config import AppConfig


class S3LlmAnswerLogRepository(LlmAnswerLogPort):

    def __init__(self) -> None:
        self._config = None
        self._client = None
        self._bucket_name = None

    def set_config(self, config: AppConfig) -> Self:
        self._config = config
        self._client = boto3.client(
            "s3", endpoint_url=self._config.env.s3_endpoint
        )
        self._bucket_name = self._config.env.s3_bucketname
        return self

    def save(self, key: str, body: str) -> None:
        try:
            self._client.put_object(
                Bucket=self._bucket_name, Key=key, Body=body
            )
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise Exception(
                "Failed to save log to s3: {key} body: {body} error_message: {error_message}"
            )
