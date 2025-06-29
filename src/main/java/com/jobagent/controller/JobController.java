package com.jobagent.controller;

import com.jobagent.dto.*;
import com.jobagent.service.JobService;
import com.jobagent.vo.PageResult;
import com.jobagent.vo.Result;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/job")
@Slf4j
@Api(tags = "岗位相关接口")
public class JobController {
    @Autowired
    private JobService jobService;

    @PostMapping("/page")
    @ApiOperation("分页查询岗位")
    public Result<PageResult> page(@RequestBody JobPageDTO jobPageDTO){
        log.info("岗位分页查询，参数为：{}",  jobPageDTO);
        PageResult pageResult = jobService.page(jobPageDTO);
        return Result.success(pageResult);
    }

    @PostMapping("/pageFilter")
    @ApiOperation("分页查询岗位")
    public Result<PageResult> page(@RequestBody JobPageFilterDTO jobPageFilterDTO){
        log.info("岗位分页查询，参数为：{}",  jobPageFilterDTO);
        PageResult pageResult = jobService.pageFilter(jobPageFilterDTO);
        return Result.success(pageResult);
    }

    @GetMapping("/city")
    @ApiOperation("查询数据库中有哪些城市的工作")
    public Result<List<String>> cityList(){
        log.info("查询数据库中的城市");
        return Result.success(jobService.cityList());
    }

    @GetMapping("/industry")
    @ApiOperation("查询数据库中有哪些行业")
    public Result<List<String>> industryList(){
        log.info("查询数据库中的行业");
        return Result.success(jobService.industryList());
    }

    @GetMapping("/title")
    @ApiOperation("查询数据库中有哪些岗位")
    public Result<List<String>> titleList(){
        log.info("查询数据库中的岗位");
        return Result.success(jobService.titleList());
    }

    @GetMapping("/cityAll")
    @ApiOperation("查询数据库中有哪些城市的工作")
    public Result<List<String>> cityListAll(){
        log.info("查询数据库中的城市");
        return Result.success(jobService.cityListAll());
    }

    @GetMapping("/industryAll")
    @ApiOperation("查询数据库中有哪些行业")
    public Result<List<String>> industryListAll(){
        log.info("查询数据库中的行业");
        return Result.success(jobService.industryListAll());
    }

    @GetMapping("/titleAll")
    @ApiOperation("查询数据库中有哪些岗位")
    public Result<List<String>> titleListAll(){
        log.info("查询数据库中的岗位");
        return Result.success(jobService.titleListAll());
    }

    @PostMapping("/delete")
    public Result deleteJobs(@RequestBody DeleteJobDTO deleteJobDTO) {
        log.info("删除岗位: {}", deleteJobDTO);
        jobService.deleteByIds(deleteJobDTO);
        return Result.success();
    }

    @PostMapping("/view")
    public Result setViewStatus(@RequestBody JobViewDTO jobViewDTO) {
        log.info("设置已查看状态: {}", jobViewDTO);
        jobService.setViewStatus(jobViewDTO);
        return Result.success();
    }

    @PostMapping("/insert")
    public Result insertJobs(@RequestBody InsertJobsDTO insertJobsDTO) {
        log.info("新增岗位: {}", insertJobsDTO);
        String message = jobService.insertJobs(insertJobsDTO);
        return Result.success(message);
    }

    @PostMapping("/list")
    public Result<PageResult> getJobList(@RequestBody JobListDTO jobListDTO) {
        log.info("查询岗位: {}", jobListDTO);
        PageResult pageResult = jobService.getJobList(jobListDTO);
        return Result.success(pageResult);
    }

}
