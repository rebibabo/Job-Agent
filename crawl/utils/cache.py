import itertools
import json
import os
from loguru import logger
import datetime

class CachedIterator:
    # 将多个数组组合的遍历索引缓存起来，避免重复遍历，用于爬虫意外断开后恢复遍历
    def __init__(self, arrays, cache_path=None):
        """
        :param arrays: 输入的数组列表，例如 [a, b, c]。
        :param cache_path: 缓存文件路径，用于保存和加载索引。
        """
        self.arrays = arrays
        self.cache_path = cache_path

        # 使用范围生成索引组合
        self.combinations = list(itertools.product(*[range(len(arr)) for arr in arrays]))
        self.index = 0  # 当前主索引
        self.total = len(self.combinations)  # 总数
        self.array_indices = [
            {"index": 0, "value": arr[0]} if arr else {"index": 0, "value": None}
            for arr in arrays
        ]

        # 如果缓存路径存在，则加载索引
        if cache_path and os.path.exists(cache_path):
            self._load_cache()

    def _load_cache(self):
        """加载缓存文件中的索引"""
        try:
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                if "index" in cache_data and "array_indices" in cache_data:
                    self.index = cache_data["index"]
                    self.array_indices = cache_data["array_indices"]
                else:
                    logger.warning("缓存数据无效，重新从 0 开始。")
        except (json.JSONDecodeError, IOError):
            logger.warning("缓存文件无效，重新从 0 开始。")

    def _save_cache(self):
        """保存当前索引到缓存文件"""
        if self.cache_path:
            if not os.path.exists(os.path.dirname(self.cache_path)):
                os.makedirs(os.path.dirname(self.cache_path))
            cache_data = {
                "index": self.index,
                "total": self.total,
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "array_indices": self.array_indices
            }
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=4, ensure_ascii=False)

    def __iter__(self):
        return self

    def __next__(self):
        """返回下一个元组，并更新缓存"""
        if self.index < len(self.combinations):
            current_indices = self.combinations[self.index]
            result = []

            for i, idx in enumerate(current_indices):
                value = self.arrays[i][idx]
                self.array_indices[i] = {"index": idx, "value": value}
                result.append(value)

            self._save_cache()
            self.index += 1
            if len(result) == 1:
                return result[0]
            else:
                return tuple(result)
        else:
            self.clear()
            raise StopIteration    
        
    def clear(self):
        # 将索引恢复至开始状态
        self.index = 0
        self.array_indices = [
            {"index": 0, "value": arr[0]} if arr else {"index": 0, "value": None}
            for arr in self.arrays
        ]
        self._save_cache()

    def __len__(self):
        return len(self.combinations)