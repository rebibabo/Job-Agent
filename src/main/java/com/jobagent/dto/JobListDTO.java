package com.jobagent.dto;

import lombok.Data;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Data
public class JobListDTO {
    private String userId;
    private String jobIds;
    private Integer maxNum;

    public List<String> getJobIdsList() {
        return splitStringToList(this.jobIds);
    }

    private List<String> splitStringToList(String str) {
        if (str == null || str.trim().isEmpty()) {
            return new ArrayList<>();
        }
        return Arrays.asList(str.split("\\s*,\\s*"));
    }
}
