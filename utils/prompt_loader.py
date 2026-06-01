from utils.config_handler import prompt_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


def load_system_prompts():
    try:
        system_prompt_path=get_abs_path(prompt_config['main_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yaml配置文件中没有main_prompt_path配置项")
        raise e     # 捕获到异常后，记录日志，然后把原异常重新抛出去

    try:
        return open(system_prompt_path,'r',encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_system_prompts]解析系统提示词错误，{str(e)}")
        raise e
    

def load_rag_prompts():
    try:
        rag_prompt_path=get_abs_path(prompt_config['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置文件中没有rag_summarize_prompt_path配置项")
        raise e     # 捕获到异常后，记录日志，然后把原异常重新抛出去

    try:
        return open(rag_prompt_path,'r',encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析RAG总结提示词错误，{str(e)}")
        raise e


def load_report_prompts():
    try:
        report_prompt_path=get_abs_path(prompt_config['report_prompt_path'])
    except KeyError as e:
        logger.error(f"[report_system_prompts]在yaml配置文件中没有report_prompt_path配置项")
        raise e     # 捕获到异常后，记录日志，然后把原异常重新抛出去

    try:
        return open(report_prompt_path,'r',encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[report_system_prompts]解析Report报告提示词错误，{str(e)}")
        raise e
    