package com.jobagent.service.impl;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.jobagent.mapper.CityMapper;
import com.jobagent.entity.City;
import com.jobagent.vo.PageResult;
import com.jobagent.service.CityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CityServiceImpl implements CityService {

    @Autowired
    private CityMapper cityMapper;

    @Override
    public List<City> list(){
        return cityMapper.list();
    }

    @Override
    public List<City> listByCity(String city){
        return cityMapper.listByCity(city);
    }

    @Override
    public PageResult page(Integer pageNo, Integer pageSize, String provinceName, String cityName, String regionName){
        PageHelper.startPage(pageNo,pageSize);

        List<City> cityList = cityMapper.listFilter(provinceName, cityName, regionName);
        Page<City> p = (Page<City>) cityList;

        PageResult pageBean = new PageResult(p.getTotal(), p.getResult());
        return pageBean;
    }

}
