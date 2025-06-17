import hashlib
import random
import string

def md5_encrypt(text):
    """对字符串进行MD5加密"""
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))  # 注意要先编码为bytes
    return md5.hexdigest()  # 返回32位十六进制字符串

def builder(cls):
    class FieldDescriptor:
        def __init__(self, name):
            self.name = name
        
        def __call__(self, value):
            def wrapper(instance):
                setattr(instance, self.name, value)
                return instance
            return wrapper
    
    # 为类添加动态方法（方法名 = 属性名 + "_"）
    for name, annotation in cls.__annotations__.items():
        # 添加方法到类中
        def create_method(name):
            def method(self, value):
                setattr(self, name, value)
                return self
            method.__name__ = f"{name}_"  # 方法名改为 属性名_
            return method
        
        setattr(cls, f"{name}_", create_method(name))  # 设置方法名为 属性名_
    
    return cls

def generate_random_id(length):
    """生成随机ID，长度为length，字符集为0-9a-zA-Z"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))