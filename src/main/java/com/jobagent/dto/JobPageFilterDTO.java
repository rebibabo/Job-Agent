package com.jobagent.dto;

import lombok.Data;

@Data
public class JobPageFilterDTO {
    private String userId;
    private String filterHash;
    private Integer page;
    private Integer pageSize;
}
