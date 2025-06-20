package com.jobagent.controller;

import com.jobagent.dto.RuleFindDTO;
import com.jobagent.dto.RuleSaveDTO;
import com.jobagent.service.RuleService;
import com.jobagent.vo.Result;
import com.jobagent.vo.RuleVO;
import lombok.extern.slf4j.Slf4j;
import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/rule")
@Slf4j
public class RuleController {
    @Autowired
    private RuleService ruleService;

    @PostMapping("/save")
    public void saveRule(@RequestBody RuleSaveDTO ruleSaveDTO) {
        ruleService.saveRule(ruleSaveDTO);
    }

    @PostMapping("/find")
    public Result findRule(@RequestBody RuleFindDTO ruleFindDTO) {
        log.info("查询规则:{}", ruleFindDTO);
        Integer found = ruleService.findRule(ruleFindDTO);
        log.info("规则个数{}", found);
        if (found > 0) {
            return Result.error("规则名已存在");
        }
        return Result.success();
    }

    @GetMapping("/load/{userId}")
    public Result loadRule(@PathVariable Integer userId) {
        log.info("查询用户{}的规则",  userId);
        return Result.success(ruleService.loadRule(userId));
    }

    @GetMapping("/delete/{roleId}")
    public Result deleteRule(@PathVariable Integer roleId) {
        log.info("删除规则{}",  roleId);
        ruleService.deleteRule(roleId);
        return Result.success();
    }
}
