from typing import List
import numpy as np

class Metrics:
    def __init__(self, relevance: List[int]):
        self.relevance = np.array(relevance)
        
    def getNDCG(self, k=100):
        ''' Calculate NDCG@k for a given click list. '''
        k = min(k, len(self.relevance))
        relevance = self.relevance[:k]     # 0/1表示是否点击或者是否发送简历
        weights = 1 / np.log2(np.arange(2, k+2))  # 计算权重
        dcg = np.sum(relevance * weights)
        idcg = np.sum(np.sort(relevance)[::-1] * weights)
        return dcg / idcg if idcg != 0 else 0
        
    def getHitRatio(self, k=100):
        ''' Calculate click rate@k for a given click list. '''
        k = min(k, len(self.relevance))
        return sum(self.relevance[:k]) / k
    
    def getMAP(self):
        ''' Calculate mean average precision for a given click list. '''
        relevant_map = {}
        rank = 1
        for i in range(len(self.relevance)):
            if self.relevance[i] == 1:
                relevant_map[rank] = i+1
                rank += 1
        map_score = sum([rank / idx for rank, idx in relevant_map.items()])
        return map_score / len(relevant_map) if len(relevant_map) != 0 else 0
