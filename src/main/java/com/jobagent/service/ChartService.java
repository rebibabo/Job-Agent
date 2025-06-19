package com.jobagent.service;

import com.jobagent.dto.ChartDTO;

import java.util.List;
import java.util.Map;

public interface ChartService {
    List<Map<String, Object>> getChartData(ChartDTO chartDTO);

    String getWordCloudPicture(String title);
}
