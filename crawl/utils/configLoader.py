import yaml
from typing import Any, Optional
from loguru import logger

def inject_config(config_path: str = 'config.yml', yaml_path: Optional[str] = None):
    """
    类装饰器：将YAML配置的指定路径部分注入到被装饰的类中
    
    参数:
        config_path: YAML配置文件路径
        yaml_path: YAML文件中的路径，用点号分隔 (如 'database.mysql')
                  如果为None，则加载整个配置
        
    使用示例:
        @inject_config('my_config.yml', 'database.mysql')
        class MySQLConfig:
            pass
            
        然后可以通过 MySQLConfig.config 访问配置的database.mysql部分
    """
    def decorator(cls):
        # 读取配置文件
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                full_config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            logger.warning(f"配置文件 {config_path} 未找到，使用空配置")
            full_config = {}
        except yaml.YAMLError as e:
            logger.warning(f"配置文件 {config_path} 解析错误: {e}，使用空配置")
            full_config = {}
        
        # 获取指定路径的配置
        def get_nested_config(config: dict, path: Optional[str]) -> Any:
            if not path:
                return config
            keys = path.split('.')
            current = config
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    logger.warning(f"配置路径 '{path}' 不存在于配置文件中，使用空配置")
                    return {}
            return current
        
        config_data = get_nested_config(full_config, yaml_path)
        
        # 将配置添加到类属性
        cls.config = config_data
        
        # 添加一个方法来重新加载配置
        @classmethod
        def reload_config(cls, path: Optional[str] = None) -> bool:
            """重新加载配置"""
            nonlocal config_path, yaml_path
            path = path or config_path
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    full_config = yaml.safe_load(f) or {}
                cls.config = get_nested_config(full_config, yaml_path)
                return True
            except Exception as e:
                logger.error(f"重新加载配置失败: {e}")
                return False
        
        cls.reload_config = reload_config
        
        # 保留原始类的文档字符串
        cls.__doc__ = cls.__doc__ or f"配置注入类 (配置来自: {config_path}, 路径: {yaml_path})"
        
        return cls
    
    return decorator
