package com.jobagent.entity;

import lombok.Data;

@Data
public class JobInfo {
    private String securityId;
    private Integer jobId;   //回填，插入job会自动生成主键id
    private String jobName;
    private String jobType;
    private String companyId;
    private String companyName;
    private String url;
    private String salary;
    private int salaryFloor;
    private int salaryCeiling;
    private String crawlDate;
    private String city;
    private String region;
    private String experience;
    private String degree;
    private String industry;
    private String title;
    private String skills;
    private String description;
    private String scale;
    private String stage;
    private String welfare;
}
