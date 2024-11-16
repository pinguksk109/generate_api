import os
from dotenv import load_dotenv

load_dotenv()


class Env:
    def __init__(self):
        self.aws_region = self._get_env_variable("AWS_REGION")
        self.s3_endpoint = self._get_env_variable("S3_ENDPOINT")
        self.s3_bucketname = self._get_env_variable("S3_BUCKETNAME")
        self.dynamodb_endpoint = self._get_env_variable("DYNAMODB_ENDPOINT")
        self.llm_prompt_table = self._get_env_variable("LLM_PROMPT_TABLE")

    def _get_env_variable(self, key: str) -> str:
        value = os.environ.get(key)
        if not value:
            raise ValueError(
                f"Environment variable '{key}' is not set or empty."
            )
        return value
