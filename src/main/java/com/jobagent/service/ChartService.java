package com.jobagent.service;

import java.util.List;
import java.util.Map;

public interface ChartService {
    List<Map<String, Object>> getChartData(String dimensionName);
}
