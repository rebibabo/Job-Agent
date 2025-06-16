package org.example.jobagent.controller;

import lombok.extern.slf4j.Slf4j;
import org.example.jobagent.entity.City;
import org.example.jobagent.entity.PageBean;
import org.example.jobagent.service.CityService;
import org.example.jobagent.vo.Result;
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
        PageBean pageBean = cityService.page(pageNo, pageSize, provinceName, cityName, regionName);
        return Result.success(pageBean);
    }
}
