package org.example.jobagent.service;

import org.example.jobagent.dto.UserLoginDTO;
import org.example.jobagent.entity.User;
import org.springframework.stereotype.Service;

@Service
public interface UserService {
    User login(UserLoginDTO userLoginDTO);
}
