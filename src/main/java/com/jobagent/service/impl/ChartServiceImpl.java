package com.jobagent.service.impl;

import com.jobagent.mapper.ChartMapper;
import com.jobagent.service.ChartService;
import com.jobagent.vo.SalaryVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ChartServiceImpl implements ChartService {
    @Autowired
    private ChartMapper chartMapper;
    @Override
    public List<Map<String, Object>> getChartData(String dimensionName) {
        List<SalaryVO> rawList = chartMapper.getChartData(dimensionName);
        List<Map<String, Object>> mapList = new ArrayList<>();
        for (SalaryVO vo : rawList) {
            Map<String, Object> map = new HashMap<>();
            map.put(dimensionName, vo.getDimensionValue());
            map.put("count", vo.getCount());
            map.put("salaryFloor", vo.getSalaryFloor());
            map.put("salaryCeiling", vo.getSalaryCeiling());
            mapList.add(map);
        }
        return mapList;
    }
}
