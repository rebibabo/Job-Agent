package com.jobagent.controller;

import com.jobagent.dto.UserAddDTO;
import com.jobagent.dto.UserPasswordDTO;
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
@RequestMapping("/user")
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
        // 将userId放到claims中，用来生成token
        claims.put(JwtClaimsConstant.USER_ID, user.getId());
        log.info("claims: {}", claims);
        String token = JwtUtil.createJWT(
                jwtProperties.getAdminSecretKey(),
                jwtProperties.getAdminTtl(),        // 登录会话持续时长，超过则需要重新登录
                claims);

        UserLoginVO employeeLoginVO = UserLoginVO.builder()
                .id(user.getId())
                .userName(user.getUsername())
                .token(token)
                .build();

        return Result.success(employeeLoginVO);
    }

    @PostMapping("/changePassword")
    public Result<String> changePassword(@RequestBody UserPasswordDTO userPasswordDTO) {
        /**
         * 要求获取用户名和老密码，验证身份成功后才修改密码为新密码
         */
        log.info("修改用户密码:{}", userPasswordDTO);
        Boolean result = userService.changePassword(userPasswordDTO);
        if (result) {
            return Result.success();
        }
        return Result.error("验证失败");
    }

    @PostMapping("/register")
    public Result<String> addUser(@RequestBody UserAddDTO userAddDTO) {
        /**
         * 注册新用户
         */
        log.info("添加用户:{}",  userAddDTO);
        Boolean result = userService.addUser(userAddDTO);
        if (result) {
            return Result.success();
        }
        return Result.error("用户名已存在");
    }

    @GetMapping("/delete/{userId}")
    public Result deleteUser(@PathVariable("userId") Integer userId) {
        /**
         * 注销用户，admin用户不允许删除
         */
        log.info("删除用户:{}", userId);
        if (userId == 1) {
            return Result.error("不能删除admin用户");
        }
        userService.deleteUser(userId);
        return Result.success();
    }
}
