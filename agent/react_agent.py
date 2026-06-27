from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.middle_ware import monitor_tool, log_before_model, report_prompt_switch
from agent.tools.agent_tools import (rag_summarize, get_weather,test_qweather_connection, get_user_location, get_user_id,get_current_month, fetch_external_data, fill_context_for_report)
from langchain_core.messages import AIMessage

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize, get_weather,test_qweather_connection,
                    get_user_location, get_user_id,get_current_month, 
                    fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }

        # 第三个参数context就是上下文runtime中的信息，就是我们做提示词切换的标记
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if isinstance (latest_message,AIMessage) and latest_message.content:
                yield latest_message.content.strip() + "\n"


