import uuid
import os

def do_file_name(file_name):
    """处理文件的名字使用uuid"""
    return str(uuid.uuid1()) + os.path.splitext(file_name)[1]