from ulid import ULID


class LlmInteractionHelper:
    @staticmethod
    def get_log_key(keyword: str):
        generate_id = str(ULID())
        return f"keyword={keyword}/generate_id={generate_id}/output.json"
