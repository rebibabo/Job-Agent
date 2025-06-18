package com.jobagent.controller;

import com.jobagent.dto.JobPageDTO;
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
        log.info("岗位分页查询，参数为：{}",  jobPageDTO);
        PageResult pageResult = jobService.page(jobPageDTO);
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

}
