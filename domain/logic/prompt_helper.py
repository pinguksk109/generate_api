from langchain.prompts import PromptTemplate


class PromptHelper:
    @staticmethod
    def getPrompt(prompt: str, input_data):
        if isinstance(input_data, str):
            prompt_template = PromptTemplate(
                input_variables=["keyword"],
                template=prompt,
            )
            prompt = prompt_template.format(keyword=input_data)
        return prompt
