package com.jobagent.controller;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import com.jobagent.constant.JwtProperties;
import com.jobagent.constant.MessageConstant;
import com.jobagent.dto.UserLoginDTO;
import com.jobagent.entity.User;
import com.jobagent.service.UserService;
import com.jobagent.utils.JwtUtil;
import com.jobagent.vo.Result;
import com.jobagent.vo.UserLoginVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import com.jobagent.constant.JwtClaimsConstant;
import com.jobagent.exception.AccountNotFoundException;

import java.util.HashMap;
import java.util.Map;

@Slf4j
@RestController
@Api(tags="用户相关接口")
public class UserController {
    @Autowired
    private UserService userService;
    @Autowired
    private JwtProperties jwtProperties;

    @ApiOperation("员工登录")
    @PostMapping("/login")
    public Result<UserLoginVO> login(@RequestBody UserLoginDTO userLoginDTO) {
        log.info("员工登录：{}", userLoginDTO);
        User user = userService.login(userLoginDTO);

        if (user == null) {
            //账号不存在
            throw new AccountNotFoundException(MessageConstant.ACCOUNT_NOT_FOUND);
        }

        Map<String, Object> claims = new HashMap<>();
        claims.put(JwtClaimsConstant.USER_ID, user.getId());
        log.info("claims: {}", claims);
        String token = JwtUtil.createJWT(
                jwtProperties.getAdminSecretKey(),
                jwtProperties.getAdminTtl(),
                claims);

        UserLoginVO employeeLoginVO = UserLoginVO.builder()
                .id(user.getId())
                .userName(user.getUsername())
                .token(token)
                .build();

        return Result.success(employeeLoginVO);
    }
}
