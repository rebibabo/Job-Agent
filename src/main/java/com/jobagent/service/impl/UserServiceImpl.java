package com.jobagent.service.impl;

import com.jobagent.dto.UserAddDTO;
import com.jobagent.dto.UserPasswordDTO;
import lombok.extern.slf4j.Slf4j;
import com.jobagent.constant.MessageConstant;
import com.jobagent.dto.UserLoginDTO;
import com.jobagent.entity.User;
import com.jobagent.exception.PasswordErrorException;
import com.jobagent.exception.AccountNotFoundException;
import com.jobagent.mapper.UserMapper;
import com.jobagent.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.DigestUtils;

@Slf4j
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserMapper userMapper;

    @Transactional
    @Override
    public User login(UserLoginDTO userLoginDTO) {
        String username = userLoginDTO.getUsername();
        String password = userLoginDTO.getPassword();

        User user = userMapper.getByNamePassword(username);
        if (user == null) {
            throw new AccountNotFoundException(MessageConstant.ACCOUNT_NOT_FOUND);
        }
//        password = DigestUtils.md5DigestAsHex(password.getBytes());
        if (!password.equals(user.getPassword())) {
            //密码错误
            throw new PasswordErrorException(MessageConstant.PASSWORD_ERROR);
        }

        //3、返回实体对象
        log.info("用户验证成功");
        return user;
    }

    @Transactional
    @Override
    public Boolean changePassword(UserPasswordDTO userPasswordDTO) {
        Integer count = userMapper.getUserInfo(userPasswordDTO);
        if (count == 1) {
            userMapper.changePassword(userPasswordDTO);
            return true;
        }
        return false;
    }

    @Transactional
    @Override
    public Boolean addUser(UserAddDTO userAddDTO) {
        Integer count = userMapper.getByName(userAddDTO.getUsername());
        if (count >= 1) {
            return false;
        }
        userMapper.addUser(userAddDTO);
        return true;
    }
}
