package com.jobagent.dto;

import lombok.Data;

@Data
public class UserPasswordDTO {
    private Long userId;
    private String userName;
    private String oldPassword;
    private String newPassword;
}
