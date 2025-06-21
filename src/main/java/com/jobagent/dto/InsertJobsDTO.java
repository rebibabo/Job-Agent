package com.jobagent.dto;

import com.jobagent.entity.JobInfo;
import lombok.Data;

import java.util.List;


@Data
public class InsertJobsDTO {
    private String userId;
    private String filterHash;
    private List<JobInfo> jobs;
}
