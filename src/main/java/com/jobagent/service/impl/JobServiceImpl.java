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
        int pageNo = jobPageDTO.getPage(),  pageSize = jobPageDTO.getPageSize();
        PageHelper.startPage(pageNo, pageSize);
        Page<Job> page = jobMapper.pageQuery(jobPageDTO);

        long total = page.getTotal();
        List<Job> records = page.getResult();
        PageResult pageResult = new PageResult(total, records);
        pageResult._hasNext(pageNo, pageSize);
        return pageResult;
    }

    @Override
    public List<String> cityList() {
        return jobMapper.cityList();
    }

    @Override
    public List<String> industryList() {
        return jobMapper.industryList();
    }

    @Override
    public List<String> titleList() {
        return jobMapper.titleList();
    }
}
