import autogen
from dotenv import load_dotenv
import os

load_dotenv()

config_list = [
    {
        'api_base': "https://api.llama-api.com",
        'model': 'llama-13b-chat',
        'api_key': os.getenv('api_key'),
    }
]

llm_config = {
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

coder_asistant = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
    system_message="Software engineer of a tech company"
)


user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get(
        "content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message=""""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task = """
Write python code to output number 1 to 100, and then store the code in a file
"""

user_proxy.initiate_chat(coder_asistant, message=task)
