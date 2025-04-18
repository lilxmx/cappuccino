import json
import os
from openai import OpenAI
from utils import get_base64_screenshot

class verifier:
    """
    Parameters:
    - verifier_api_key (str): API key for the verifier client
    - verifier_base_url (str): Base URL for the verifier client
    - verifier_model (str): Model to be used by the verifier client
    - controlledOS (str): The operating system being controlled
    - run_folder (str): The folder to store the run data
    - task (str): The task generated by planner

    Returns:
    - completion (str): The full output of LLM
    - thinking (str): LLM's thinking process
    - is_completed (str): Whether the task is completed
    """
    def __init__(self, verifier_api_key, verifier_base_url, verifier_model):
        self.verifier_client = OpenAI(
            api_key=verifier_api_key,
            base_url=verifier_base_url,
        )
        self.verifier_model = verifier_model
        self.controlledOS = os.environ["CONTROLLED_OS"]
        self.run_folder = os.environ["RUN_FOLDER"]


    def _get_system_prompt(self):
        return f"""
You are a verifier.
You need to help me use {self.controlledOS} system according to the following information.
You now need to help me verify whether the task has been completed based on the screenshot of the current desktop, and give your thinking process and results according to the specified json format.
You only need to determine whether the web page or software has been opened or whether the target content has been found. If you extract text and cannot judge based on the picture, is completed is set to true.

## Output format:
```json
{{
    "thinking": "Describe your thoughts.",
    "is_completed": true/false,
}}
```

## Output example:
```json
{{
    "thinking": "The current page shows that the GitHub opened successfully.",
    "is_completed": true
}}
"""
    
    def _get_user_prompt(self, task):
        return f"""
Please determine whether the current task has been completed.
## task:
{task}
"""
    
    def _parse_is_completed(self, content):
        json_str = content.replace("```json","").replace("```","").strip()
        json_dict = json.loads(json_str)
        return json_dict["thinking"], json_dict["is_completed"]

    def __call__(self, task_dict, min_pixels=3136, max_pixels=12845056):
        base64_screenshot = get_base64_screenshot(self.run_folder)
        messages=[
            {
                "role": "system",
                "content": self._get_system_prompt(),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": self._get_user_prompt(task_dict["task"])},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_screenshot}"},
                    },
                ],
            }
        ]
        completion = self.verifier_client.chat.completions.create(
            model=self.verifier_model,
            messages=messages
        )
        content = completion.choices[0].message.content
        thinking, is_completed = self._parse_is_completed(content)
        return completion, thinking, is_completed
