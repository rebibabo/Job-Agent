package com.jobagent.dto;

import lombok.Data;

import java.util.List;

@Data
public class DeleteFilterJobDTO {
    String userId;
    String filterHash;
}
