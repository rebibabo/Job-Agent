package com.jobagent.entity;

import io.swagger.annotations.ApiModel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Job {
    private String securityId;
    private String lid;
    private String jobName;
    private String jobType;
    private String companyId;
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

