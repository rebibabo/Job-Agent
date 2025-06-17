package com.jobagent.service.impl;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.jobagent.dto.JobPageDTO;
import com.jobagent.entity.Job;
import com.jobagent.mapper.JobMapper;
import com.jobagent.service.JobService;
import com.jobagent.vo.PageResult;
import com.jobagent.vo.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class JobServiceImpl implements JobService {
    @Autowired
    private JobMapper jobMapper;

    public PageResult page(JobPageDTO jobPageDTO){
        PageHelper.startPage(jobPageDTO.getPage(), jobPageDTO.getPageSize());
        Page<Job> page = jobMapper.pageQuery(jobPageDTO);

        long total = page.getTotal();
        List<Job> records = page.getResult();

        return new PageResult(total, records);
    }
}
