package com.jobagent.mapper;

import com.github.pagehelper.Page;
import com.jobagent.dto.JobPageDTO;
import com.jobagent.entity.Job;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface JobMapper {
    Page<Job> pageQuery(@Param("jobPageDTO") JobPageDTO jobPageDTO);
}
