package com.jobagent.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import com.jobagent.entity.User;

@Mapper
public interface UserMapper {
    @Select("select * from user where username=#{username}")
    User getByNamePassword(String username);
}
