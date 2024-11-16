import boto3
from botocore.exceptions import ClientError
from typing import Self
from application.config import AppConfig
from application.port.prompt_port import PromptPort
from enum import Enum


class PromptIds(Enum):
    TRIVIA = "6f7ec006-6017-18b4-72a1-d059f19746b7"


class DynamoPromptRepository(PromptPort):
    def __init__(self):
        self._config = None
        self._dynamodb = None
        self._table = None

    def set_config(self, config: AppConfig) -> Self:
        self._config = config
        self._client = boto3.client(
            "dynamodb",
            region_name=self._config.env.aws_region,
            endpoint_url=self._config.env.dynamodb_endpoint,
        )
        self._table = self._config.env.llm_prompt_table
        return self

    async def get_prompt(self, prompt_id: Enum) -> str:
        try:
            response = self._client.query(
                TableName=self._table,
                KeyConditionExpression="prompt_id = :v1",
                ExpressionAttributeValues={":v1": {"S": prompt_id.value}},
            )
        except ClientError as e:
            raise Exception(
                f"Failed to get item from DynamoDB: {e.response['Error']['Message']} Target prompt ID: {prompt_id.value}"
            )

        item = response["Items"]
        return item[0]["prompt"]["S"]
