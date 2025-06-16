package org.example.jobagent.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.example.jobagent.entity.City;

import java.util.List;

@Mapper
public interface CityMapper {
    @Select("select * from city")
    List<City> list();

    @Select("select * from city where city=#{city}")
    List<City> listByCity(String city);

    List<City> listFilter(String provinceName, String cityName, String regionName);
}
