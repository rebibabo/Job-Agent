package com.jobagent.controller;

import com.jobagent.dto.*;
import com.jobagent.entity.Job;
import com.jobagent.service.JobService;
import com.jobagent.vo.PageResult;
import com.jobagent.vo.Result;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

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
        /**
         * 根据搜索的过滤规则，以及页数和每页的条数，返回指定页的所有岗位信息
         */
        log.info("岗位分页查询，参数为：{}",  jobPageDTO);
        PageResult pageResult = jobService.page(jobPageDTO);
        return Result.success(pageResult);
    }

    @PostMapping("/pageFilter")
    @ApiOperation("分页查询岗位")
    public Result<PageResult> page(@RequestBody JobPageFilterDTO jobPageFilterDTO){
        /**
         * 根据搜索过滤规则的hash值，用户id，以及页数和每页的条数，返回指定页的所有岗位信息
         */
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
    @ApiOperation("查询数据库中有哪些城市的岗位")
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
        /**
         * 根据jobId列表，以及应用的过滤规则hash值，删除用户下指定规则获取到的岗位，删除job表以及user_job表中的元素
         */
        log.info("删除岗位: {}", deleteJobDTO);
        jobService.deleteByIds(deleteJobDTO);
        return Result.success();
    }

    @PostMapping("/deleteFilter")
    public Result deleteFilterJob(@RequestBody FilterJobDTO filterJobDTO) {
        /**
         * 删除指定用户指定过滤规则hash值的所有岗位，但仅删除user_job中的，并且不删除已投递的岗位信息
         * 此接口应用于用户想要删除指定过滤规则获取到的岗位历史记录，重新获取一批新的数据用以过滤、排序并自动投递简历
         */
        log.info("删除指定过滤规则的岗位: {}", filterJobDTO);
        jobService.deleteFilterJob(filterJobDTO);
        return Result.success();
    }

    @PostMapping("/deleteUserJob")
    public Result deleteUserJob(@RequestBody DeleteJobDTO deleteJobDTO) {
        /**
         * 同/delete接口，只不过不删除job表中的数据，而只删除user_job数据
         * 这样做的目的是为了减少重复获取岗位描述description的工作，（获取description较为耗时）
         */
        log.info("删除user_job中的内容，但不删除job表: {}", deleteJobDTO);
        jobService.deleteUserJobByIds(deleteJobDTO);
        return Result.success();
    }

    @PostMapping("/filterJob")
    public Result<List<Job>> getFilterJob(@RequestBody FilterJobDTO filterJobDTO) {
        /**
         * 根据过滤规则hash值和用户id，获取该用户历史搜索的岗位列表
         */
        log.info("查询指定过滤规则的岗位列表: {}", filterJobDTO);
        List<Job> result = jobService.getFilterJob(filterJobDTO);
        return Result.success(result);
    }

    @PostMapping("/view")
    public Result setViewStatus(@RequestBody JobStatusDTO jobStatusDTO) {
        /**
         * 设置用户某个岗位已查看状态
         */
        log.info("设置已查看状态: {}", jobStatusDTO);
        jobService.setViewStatus(jobStatusDTO);
        return Result.success();
    }

    @PostMapping("/sent")
    public Result setsentCVStatus(@RequestBody JobStatusDTO jobStatusDTO) {
        /**
         * 设置用户某个岗位已发送简历状态
         */
        log.info("设置已投递状态: {}", jobStatusDTO);
        jobService.setsentCVStatus(jobStatusDTO);
        return Result.success();
    }

    @PostMapping("/insert")
    public Result insertJobs(@RequestBody InsertJobsDTO insertJobsDTO) {
        /**
         * 批量查询岗位信息，需要操作三张表
         * 表1：job表，唯一判断条件为:(city, jobName, companyId)，当岗位信息存在时，不插入，如果存在但是job表中描述信息为null，且传入的参数中描述不为null，则更新描述信息
         * 表2：company表，唯一判断条件为companyId，如果新增岗位所属的公司不存在，则插入
         * 表3：user_job表，关联userId和jobId，并有filterHash表示搜索条件的hash值，以及该用户是否向查看该岗位详情、是否发送简历等信息
         */
        log.info("新增岗位: {}", insertJobsDTO);
        String message = jobService.insertJobs(insertJobsDTO);
        return Result.success(message);
    }

    @PostMapping("/list")
    public Result<PageResult> getJobList(@RequestBody JobListDTO jobListDTO) {
        /**
         * 根据jobId列表，获取用户下最多maxNum的岗位信息
         */
        log.info("查询岗位: {}", jobListDTO);
        PageResult pageResult = jobService.getJobList(jobListDTO);
        return Result.success(pageResult);
    }

    @PostMapping("/desc")
    public Result<Boolean> whetherAddDesc(@RequestBody WhetherAddDescDTO whetherAddDescDTO) {
        /**
         * 根据唯一约束条件(city, jobName, companyId)和userId，判断是否需要为该岗位更新描述信息
         * 如果岗位不存在，或者岗位存在但是description为null，则返回true，表示需要更新，否则返回false
         */
        log.info("查询是否添加带有描述的岗位{}", whetherAddDescDTO);
        Boolean result = jobService.whetherAddDesc(whetherAddDescDTO);
        return Result.success(result);
    }

}
