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

    @Select("select distinct industry from (select industry, count(*) from job group by industry having count(*) >=50) as t;")
    List<String> industryList();

    @Select("select distinct title from (select title, count(*) from job group by title having count(*) >=50) as t;")
    List<String> titleList();

    @Select("select city from (select distinct city, city_code, city_id from city where city_id like '%0100' order by city_id) as t;")
    List<String> cityListAll();

    @Select("select distinct subtype from industry;")
    List<String> industryListAll();

    @Select("select distinct name from title;")
    List<String> titleListAll();
}
