package com.jobagent.service;

import com.jobagent.dto.UserAddDTO;
import com.jobagent.dto.UserLoginDTO;
import com.jobagent.dto.UserPasswordDTO;
import com.jobagent.entity.User;
import org.springframework.stereotype.Service;

@Service
public interface UserService {
    User login(UserLoginDTO userLoginDTO);

    Boolean changePassword(UserPasswordDTO userPasswordDTO);

    Boolean addUser(UserAddDTO userAddDTO);

    void deleteUser(Integer userId);
}
