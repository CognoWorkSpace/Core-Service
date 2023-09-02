from langchain.tools import BaseTool


class CustomTool(BaseTool):
    name = "Temperature Detector"
    description = "This is a custom tool for my temperature detection use case"

    def _run(self, input: str) -> str:
        # Your logic here
        return "temperature is not bad,huh,20 celceius"

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")

