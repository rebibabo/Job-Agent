package com.jobagent.mapper;

import com.github.pagehelper.Page;
import com.jobagent.dto.*;
import com.jobagent.entity.Job;
import com.jobagent.entity.JobInfo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface JobMapper {
    Page<Job> pageQuery(@Param("jobPageDTO") JobPageDTO jobPageDTO);

    // 根据过滤规则哈希值和用户id过滤出爬取的数据
    @Select("select j.*, c.*, c.name companyName, u.* from job j, company c, user_job u where user_id=#{jobPageFilterDTO.userId} and filter_hash=#{jobPageFilterDTO.filterHash} and j.id=u.job_id and c.id=j.companyId")
    Page<Job> pageQueryFilter(@Param("jobPageFilterDTO") JobPageFilterDTO jobPageFilterDTO);

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

    void deleteUserJobByIds(@Param("deleteJobDTO") DeleteJobDTO deleteJobDTO);
    void deleteJobByIds(@Param("deleteJobDTO") DeleteJobDTO deleteJobDTO);

    @Update("UPDATE user_job SET viewed = 1 WHERE user_id = #{jobViewDTO.user_id} AND job_id = #{jobViewDTO.job_id}")
    void setViewStatus(@Param("jobViewDTO") JobViewDTO jobViewDTO);

    // 单条插入公司，返回是否成功（或直接无返回）
    int insertCompanyIfNotExists(JobInfo job);

    // 判断jobInfo是否存在，如果存在，返回jobId，否则返回null
    Integer selectJobIdIfExists(JobInfo jobInfo);

    // 单条插入岗位，返回插入的主键job_id
    int insertJob(JobInfo job);

    // 插入用户-岗位关联，避免重复
    int insertUserJobIfNotExists(@Param("userId") String userId, @Param("jobId") Integer jobId, @Param("filterHash") String filterHash);

    void updateDescription(JobInfo job);

    Page<Job> getJobList(@Param("jobListDTO") JobListDTO jobListDTO);

    int findJobWithoutDesc(@Param("whetherAddDescDTO") WhetherAddDescDTO whetherAddDescDTO);

}
