package com.jobagent.vo;

import lombok.Data;

@Data
public class RuleVO {
    String id;
    String ruleName;
    String ruleDescription;
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
