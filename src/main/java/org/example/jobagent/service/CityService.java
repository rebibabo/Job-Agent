package org.example.jobagent.service;

import org.example.jobagent.entity.City;
import org.example.jobagent.entity.PageBean;

import java.util.List;


public interface CityService {
    List<City> list();
    List<City> listByCity(String city);
    PageBean page(Integer pageNo, Integer pageSize, String provinceName,
                  String cityName, String regionName);
}
