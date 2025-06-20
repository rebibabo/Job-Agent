package com.jobagent.service.impl;

import com.jobagent.dto.RuleFindDTO;
import com.jobagent.dto.RuleSaveDTO;
import com.jobagent.mapper.RuleMapper;
import com.jobagent.service.RuleService;
import com.jobagent.vo.RuleVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RuleServiceImpl implements RuleService {
    @Autowired
    private RuleMapper ruleMapper;


    public void saveRule(RuleSaveDTO ruleSaveDTO) {
        ruleMapper.saveRule(ruleSaveDTO);
    }

    public Integer findRule(RuleFindDTO ruleFindDTO) {
        return ruleMapper.findRule(ruleFindDTO);
    }

    public List<RuleVO> loadRule(Integer userId) {
        return ruleMapper.loadRule(userId);
    }

    public void deleteRule(Integer ruleId) {
        ruleMapper.deleteRule(ruleId);
    }

}
