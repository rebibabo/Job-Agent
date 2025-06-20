package com.jobagent.dto;

import lombok.Data;

import java.util.List;

@Data
public class DeleteJobDTO {
    String user_id;
    List<String> job_ids;
}
