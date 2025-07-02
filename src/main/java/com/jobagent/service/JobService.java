package com.jobagent.service;

import com.jobagent.dto.*;
import com.jobagent.vo.PageResult;
import com.jobagent.vo.Result;
import org.springframework.beans.factory.annotation.Autowired;
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

    void setViewStatus(JobViewDTO jobViewDTO);

    String insertJobs(InsertJobsDTO insertJobsDTO);

    PageResult getJobList(JobListDTO jobListDTO);

    Boolean whetherAddDesc(WhetherAddDescDTO whetherAddDescDTO);
}
