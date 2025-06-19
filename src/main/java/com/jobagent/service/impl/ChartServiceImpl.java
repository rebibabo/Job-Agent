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
            map.put(chartDTO.getDimensionName(), vo.getDimensionValue());
            map.put("count", vo.getCount());
            map.put("salaryFloor", vo.getSalaryFloor());
            map.put("salaryCeiling", vo.getSalaryCeiling());
            mapList.add(map);
        }
        return mapList;
    }

    @Override
    public String getWordCloudPicture(String title) {
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
