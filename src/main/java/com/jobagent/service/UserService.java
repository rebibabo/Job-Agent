package com.jobagent.service;

import com.jobagent.dto.UserLoginDTO;
import com.jobagent.entity.User;
import org.springframework.stereotype.Service;

@Service
public interface UserService {
    User login(UserLoginDTO userLoginDTO);
}
