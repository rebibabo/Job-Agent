package com.jobagent.vo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.io.Serializable;
import java.util.List;

@Data
@Slf4j
@AllArgsConstructor
@NoArgsConstructor
public class PageResult<T> implements Serializable {

    private Long total;      // 总记录数
    private boolean hasNext; // 是否还有下一页
    private List<T> items;   // 当前页数据

    public PageResult(Long total, List<T> items) {
        this.total = total;
        this.items = items;
    }

    // 添加计算 hasNext 的逻辑
    public void _hasNext(Integer pageNo, Integer pageSize) {
        if (total == 0 || pageSize == 0) this.hasNext = false;
        int totalPages = (int) Math.ceil((double) total / pageSize);
        this.hasNext = pageNo < totalPages;
    }

}