package com.jobagent.dto;

import lombok.Data;

import java.util.List;

@Data
public class RuleSaveDTO {
    String ruleName;
    String ruleDescription;
    String userId;
    String keyword;
    String city;
    String degree;
    String industry;
    String title;
    String experience;
    String scale;
    String stage;
    Integer limitNum;
}
