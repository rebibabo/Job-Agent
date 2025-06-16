package org.example.jobagent.controller;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.example.jobagent.constant.JwtProperties;
import org.example.jobagent.constant.MessageConstant;
import org.example.jobagent.dto.UserLoginDTO;
import org.example.jobagent.entity.User;
import org.example.jobagent.service.UserService;
import org.example.jobagent.utils.JwtUtil;
import org.example.jobagent.vo.Result;
import org.example.jobagent.vo.UserLoginVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.example.jobagent.constant.JwtClaimsConstant;
import org.example.jobagent.exception.AccountNotFoundException;

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
