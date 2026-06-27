"""
通义千问（Tongyi / DashScope）配置模块
使用 langchain 社区版集成，提供 ChatTongyi 和 DashScopeEmbeddings 实例
采用懒加载模式，避免 import 时立即实例化导致启动崩溃
"""
import os
from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_config
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv(encoding="utf-8")

model=ChatTongyi(
    model=rag_config['chat_model_name'],
    DASHSCOPE_API_KEY=os.getenv("DASHSCOPE_API_KEY", "")
    )

# # 3. 简单调用示例
# def simple_chat():
#     messages = [
#         SystemMessage(content="你是一个乐于助人的助手。"),
#         HumanMessage(content="请介绍一下你自己。")
#     ]
#     response = model.invoke(messages)
#     print(response.content)

# if __name__ == "__main__":
#     simple_chat()
