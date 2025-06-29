package com.jobagent.controller;

import com.jobagent.vo.PageResult;
import lombok.extern.slf4j.Slf4j;
import com.jobagent.entity.City;
import com.jobagent.service.CityService;
import com.jobagent.vo.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Slf4j
@RestController
@RequestMapping("cities")
public class CityController {

    @Autowired
    private CityService cityService;

//    @RequestMapping(value="/cities", method=RequestMethod.GET)
    @GetMapping
    public Result getCities() {
        log.info("查询全部城市信息");
        List<City> cityList = cityService.list();
        return Result.success(cityList);
    }

    @GetMapping("/{city}")
    public Result getCityById(@PathVariable("city") String city) {
        log.info("查询{}城市", city);
        List<City> cityList = cityService.listByCity(city);
        return Result.success(cityList);
    }

    @GetMapping("/page")
    public Result page(
            @RequestParam(defaultValue = "1") Integer pageNo,
            @RequestParam(defaultValue = "10") Integer pageSize,
            @RequestParam(defaultValue = "") String provinceName,
            @RequestParam(defaultValue = "") String cityName,
            @RequestParam(defaultValue = "") String regionName) {
        log.info("分页查询，参数{},{},{},{},{}",  pageNo, pageSize, provinceName, cityName, regionName);
        PageResult pageResult = cityService.page(pageNo, pageSize, provinceName, cityName, regionName);
        return Result.success(pageResult);
    }
}
