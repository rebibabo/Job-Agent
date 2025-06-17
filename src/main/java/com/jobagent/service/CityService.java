package com.jobagent.service;

import com.jobagent.entity.City;
import com.jobagent.vo.PageResult;

import java.util.List;


public interface CityService {
    List<City> list();
    List<City> listByCity(String city);
    PageResult page(Integer pageNo, Integer pageSize, String provinceName,
                    String cityName, String regionName);
}
