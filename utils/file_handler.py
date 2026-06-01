import os,hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader

def get_file_md5_hex(filepath):         #获取md5值
    if not os.path.exists(filepath):        #判断路径下的文件是否存在
        logger.error(f"[md5计算]文件{filepath}不存在")
        return  
    if not os.path.isfile(filepath):        #判断路径下的是不是文件
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return
    
    md5_obj=hashlib.md5()

    chunk_size=4096     #4KB分片，避免文件过大
    try:
        with open(filepath,'rb')as f:       #以二进制模式读取文件
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
                """
                chunk=f.read(chunk_size)
                while chunk:
                    md5_obj.update(chunk)
                    chunk=f.read(chunk_size)
                """
            md5_hex=md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件{filepath}md5失败，{str(e)}")
        return None
    

def listdir_with_allowed_type(path:str,allowed_types:tuple[str]):        #返回文件夹内的文件列表（允许的文件后缀）
    files=[]

    if not os.path.isdir(path):
        logger.error(f"[文件]路径下{path}不是文件夹")
        return allowed_types
    
    for f in os.listdir(path):      #循环路径下的所有文件
        if f.endswith(allowed_types):               # endswith ： 文件的后缀
            files.append(os.path.join(path,f))      #为files添加可用的文件路径字符串
             
    return tuple(files)     #返回元组类型，避免list被改变
    

def pdf_loader(filepath: str, password=None) -> list[Document]:
    return PyPDFLoader(filepath, password).load()


def txt_loader(filepath:str) -> list[Document]:  
    return TextLoader(filepath,encoding='utf-8').load()