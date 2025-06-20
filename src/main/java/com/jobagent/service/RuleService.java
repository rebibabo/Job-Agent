package com.jobagent.service;

import com.jobagent.dto.RuleFindDTO;
import com.jobagent.dto.RuleSaveDTO;
import com.jobagent.vo.RuleVO;

import java.util.List;

public interface RuleService {
    void saveRule(RuleSaveDTO ruleSaveDTO);

    Integer findRule(RuleFindDTO ruleFindDTO);

    List<RuleVO> loadRule(Integer userId);

    void deleteRule(Integer ruleId);
}
