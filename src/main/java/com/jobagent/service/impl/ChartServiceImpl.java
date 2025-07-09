package com.jobagent.service.impl;

import com.jobagent.dto.ChartDTO;
import com.jobagent.mapper.ChartMapper;
import com.jobagent.service.ChartService;
import com.jobagent.utils.WordCloudBuilder;
import com.jobagent.vo.SalaryVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class ChartServiceImpl implements ChartService {
    @Autowired
    private ChartMapper chartMapper;
    @Override
    public List<Map<String, Object>> getChartData(ChartDTO chartDTO) {
        List<SalaryVO> rawList = chartMapper.getChartData(chartDTO);
        List<Map<String, Object>> mapList = new ArrayList<>();
        for (SalaryVO vo : rawList) {
            Map<String, Object> map = new HashMap<>();
            map.put(chartDTO.getDimensionName(), vo.getDimensionValue());       // chartDTO.dimensionName为待分析维度的名称，例如city，而vo.dimensionValue为维度具体的值，例如北京
            map.put("count", vo.getCount());
            map.put("salaryFloor", vo.getSalaryFloor());
            map.put("salaryCeiling", vo.getSalaryCeiling());
            mapList.add(map);
        }
        return mapList;
    }

    @Override
    public String getWordCloudPicture(String title) {
        // 获取该岗位所有的skills列表，每一个skills由多个skills组成，由逗号分隔
        List<String> skillsList = chartMapper.getTitleSkills(title);
        List<String> skillList = new ArrayList();
        for (String skills : skillsList) {
            List<String> skillListSplit = Arrays.asList(skills.split(","));
            skillList.addAll(skillListSplit);
        }
        String filePath = "tmp/" + title + ".png";
        WordCloudBuilder.generate(skillList, filePath);
        return filePath;
    }
}
