package com.jobagent.controller;

import com.jobagent.service.ChartService;
import com.jobagent.vo.Result;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/chart")
public class ChartController {
    @Autowired
    private ChartService chartService;

    @PostMapping("/{dimensionName}")
    public Result getChartData(@PathVariable String dimensionName) {
        List<Map<String,Object>> chartData = chartService.getChartData(dimensionName);
        return Result.success(chartData);
    }
}
