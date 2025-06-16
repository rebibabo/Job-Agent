package org.example.jobagent.service.impl;

import lombok.extern.slf4j.Slf4j;
import org.example.jobagent.constant.MessageConstant;
import org.example.jobagent.dto.UserLoginDTO;
import org.example.jobagent.entity.User;
import org.example.jobagent.exception.PasswordErrorException;
import org.example.jobagent.exception.AccountNotFoundException;
import org.example.jobagent.mapper.UserMapper;
import org.example.jobagent.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.DigestUtils;

@Slf4j
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserMapper userMapper;

    @Override
    public User login(UserLoginDTO userLoginDTO) {
        String username = userLoginDTO.getUsername();
        String password = userLoginDTO.getPassword();

        User user = userMapper.getByNamePassword(username);
        if (user == null) {
            throw new AccountNotFoundException(MessageConstant.ACCOUNT_NOT_FOUND);
        }
        password = DigestUtils.md5DigestAsHex(password.getBytes());
        if (!password.equals(user.getPassword())) {
            //密码错误
            throw new PasswordErrorException(MessageConstant.PASSWORD_ERROR);
        }

        //3、返回实体对象
        log.info("用户验证成功");
        return user;
    }
}
