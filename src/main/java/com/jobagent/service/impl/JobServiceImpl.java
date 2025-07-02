package com.jobagent.service.impl;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.jobagent.dto.*;
import com.jobagent.entity.Job;
import com.jobagent.entity.JobInfo;
import com.jobagent.mapper.JobMapper;
import com.jobagent.service.JobService;
import com.jobagent.vo.PageResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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

    public PageResult pageFilter(JobPageFilterDTO jobPageFilterDTO){
        int pageNo = jobPageFilterDTO.getPage(),  pageSize = jobPageFilterDTO.getPageSize();
        PageHelper.startPage(pageNo, pageSize);
        Page<Job> page = jobMapper.pageQueryFilter(jobPageFilterDTO);

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

    @Override
    public List<String> cityListAll() {
        return jobMapper.cityListAll();
    }

    @Override
    public List<String> industryListAll() {
        return jobMapper.industryListAll();
    }

    @Override
    public List<String> titleListAll() {
        return jobMapper.titleListAll();
    }

    @Override
    @Transactional
    public void deleteByIds(DeleteJobDTO deleteJobDTO) {
        jobMapper.deleteUserJobByIds(deleteJobDTO);
        jobMapper.deleteJobByIds(deleteJobDTO);
    }

    @Override
    public void setViewStatus(JobViewDTO jobViewDTO) {
        jobMapper.setViewStatus(jobViewDTO);
    }

    @Override
    @Transactional
    public String insertJobs(InsertJobsDTO insertJobsDTO) {
        int total=0, insertNum=0, updateNum=0;
        for (JobInfo job : insertJobsDTO.getJobs()) {
            Integer jobId = jobMapper.selectJobIdIfExists(job);
            total++;
            if (jobId == null) {
                // 不存在，插入
                jobMapper.insertJob(job);
                insertNum++;
                jobId = job.getJobId(); // 主键已回填
            }
            else if (job.getDescription() != null) {
                jobMapper.updateDescription(job);
                updateNum++;
            }
            else {
                continue;
            }

            // 先插入公司
            jobMapper.insertCompanyIfNotExists(job);
            String filterHash = insertJobsDTO.getFilterHash();
            // 插入用户与岗位关联
            jobMapper.insertUserJobIfNotExists(insertJobsDTO.getUserId(), jobId, filterHash);
        }
        return "成功插入" + insertNum + "条数据，更新" + updateNum + "条岗位描述信息，共" + (total-insertNum) + "条重复数据";
    }

    @Override
    public PageResult getJobList(JobListDTO jobListDTO) {
        int pageNo = 1,  pageSize = jobListDTO.getMaxNum();
        PageHelper.startPage(pageNo, pageSize);
        Page<Job> page = jobMapper.getJobList(jobListDTO);

        long total = page.getTotal();
        List<Job> records = page.getResult();
        PageResult pageResult = new PageResult(total, records);
        pageResult._hasNext(pageNo, pageSize);
        return pageResult;
    }

    @Override
    public Boolean whetherAddDesc(WhetherAddDescDTO whetherAddDescDTO) {
        int result = jobMapper.findJobWithoutDesc(whetherAddDescDTO);
        return result == 0;
    }
}
