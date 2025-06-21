package com.jobagent.mapper;

import com.jobagent.dto.UserAddDTO;
import com.jobagent.dto.UserPasswordDTO;
import org.apache.ibatis.annotations.*;
import com.jobagent.entity.User;

@Mapper
public interface UserMapper {
    @Select("select * from user where username=#{username}")
    User getByNamePassword(String username);

    @Select("select count(*) from user where id=#{userPasswordDTO.userId} and password=#{userPasswordDTO.oldPassword}")
    Integer getUserInfo(@Param("userPasswordDTO") UserPasswordDTO userPasswordDTO);

    @Update("update user set password=#{userPasswordDTO.newPassword} where id=#{userPasswordDTO.userId}")
    void changePassword(@Param("userPasswordDTO")UserPasswordDTO userPasswordDTO);

    @Select("select count(*) from user where username=#{username}")
    Integer getByName(String username);

    @Insert("insert into user(username, password) values (#{userAddDTO.username}, #{userAddDTO.password})")
    void addUser(@Param("userAddDTO") UserAddDTO userAddDTO);

    @Delete("delete from user where id=#{userId}")
    void deleteUser(@Param("userId") int userId);

    @Delete("delete from user_job where id=#{userId}")
    void deleteUserJobByUserId(@Param("userId") int userId);

    @Delete("delete from job where id in (select job_id from user_job where user_id=#{userId} and filter_hash is not null)")
    void deleteJobByUserId(@Param("userId") int userId);
}
