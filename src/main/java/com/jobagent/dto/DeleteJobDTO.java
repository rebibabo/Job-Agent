package com.jobagent.dto;

import lombok.Data;

import java.util.List;

@Data
public class DeleteJobDTO {
    String user_id;
    String filter_hash;
    List<String> job_ids;
}
