import threading
from dbutils.pooled_db import PooledDB
import pymysql  # 可根据需要替换为其他数据库驱动
from utils.configLoader import inject_config
from loguru import logger
import redis

redis_connector = redis.Redis(host='localhost', port=6379, db=0)

@inject_config("application.yml", "database.mysql")
class DatabasePool:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_pool()
        return cls._instance
    
    def _init_pool(self):
        """初始化连接池"""
        self.pool = PooledDB(
            creator=pymysql,  # 使用pymysql作为数据库驱动
            maxconnections=self.config['max-connections'],  # 连接池允许的最大连接数
            mincached=5,  # 初始化时连接池中至少创建的空闲连接
            maxcached=10,  # 连接池中最多闲置的连接
            blocking=True,  # 连接池中如果没有可用连接后是否阻塞等待
            host=self.config['host'],  # 数据库地址
            port=self.config['port'],  # 数据库端口
            user=self.config['username'],  # 数据库用户名
            password=self.config['password'],  # 数据库密码
            database=self.config['database-name'],  # 数据库名
        )
        
        self.pool_dict = PooledDB(
            creator=pymysql,  
            maxconnections=self.config['max-connections'], 
            mincached=5,  
            maxcached=10,  
            blocking=True, 
            host=self.config['host'],  
            port=self.config['port'],  
            user=self.config['username'],
            password=self.config['password'], 
            database=self.config['database-name'], 
            cursorclass=pymysql.cursors.DictCursor  # 返回字典形式的游标
        )
    
    def execute(self, sql, args=None, return_dict=False):
        """
        执行SQL语句
        :param sql: SQL语句
        :param args: SQL参数
        :return: result
        """
        conn = None
        cursor = None
        try:
            if return_dict:
                conn = self.pool_dict.connection()
            else:
                conn = self.pool.connection()
            cursor = conn.cursor()
            
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
                
            # 如果是查询操作，获取结果
            if sql.strip().lower().split(' ')[0] in ['select', 'show']:
                result = cursor.fetchall()
            else:
                result = cursor.rowcount
                conn.commit()
            
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            message = eval(str(e))[1]
            logger.warning(f"执行SQL语句失败：{sql}，原因：{message}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def close(self):
        """关闭连接池"""
        if hasattr(self, 'pool') and self.pool:
            self.pool.close()
            self.pool = None

# 全局连接池实例
db_pool = DatabasePool()