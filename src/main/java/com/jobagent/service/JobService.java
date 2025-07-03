package com.jobagent.service;

import com.jobagent.dto.*;
import com.jobagent.entity.Job;
import com.jobagent.vo.PageResult;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface JobService {
    PageResult page(JobPageDTO jobPageDTO);

    PageResult pageFilter(JobPageFilterDTO jobPageFilterDTO);

    List<String> cityList();

    List<String> industryList();

    List<String>  titleList();

    List<String> cityListAll();

    List<String> industryListAll();

    List<String> titleListAll();

    void deleteByIds(DeleteJobDTO deleteJobDTO);

    void setViewStatus(JobStatusDTO jobStatusDTO);

    String insertJobs(InsertJobsDTO insertJobsDTO);

    PageResult getJobList(JobListDTO jobListDTO);

    Boolean whetherAddDesc(WhetherAddDescDTO whetherAddDescDTO);

    void deleteFilterJob(FilterJobDTO deleteJobDTO);

    void setsentCVStatus(JobStatusDTO jobStatusDTO);

    List<Job> getFilterJob(FilterJobDTO filterJobDTO);

    void deleteUserJobByIds(DeleteJobDTO deleteJobDTO);
}
