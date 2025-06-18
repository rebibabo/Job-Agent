package com.jobagent.mapper;

import com.github.pagehelper.Page;
import com.jobagent.dto.JobPageDTO;
import com.jobagent.entity.Job;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface JobMapper {
    Page<Job> pageQuery(@Param("jobPageDTO") JobPageDTO jobPageDTO);

    @Select("SELECT city \n" +
            "FROM city \n" +
            "WHERE city IN (SELECT DISTINCT city FROM job) \n" +
            "GROUP BY city, city_code\n" +
            "ORDER BY city_code;")
    List<String> cityList();

    @Select("SELECT DISTINCT industry FROM job;")
    List<String> industryList();

    @Select("SELECT DISTINCT title FROM job;")
    List<String> titleList();
}
