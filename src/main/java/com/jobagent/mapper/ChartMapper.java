package com.jobagent.mapper;

import com.jobagent.vo.SalaryVO;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Service;

import java.util.List;

@Mapper
public interface ChartMapper {
    @Select("select ${dimensionName} as dimensionValue, avg(salaryFloor) salaryFloor, avg(salaryCeiling) salaryCeiling,count(*) count from job group by ${dimensionName} order by avg(salaryFloor) desc;")
    List<SalaryVO> getChartData(@Param("dimensionName") String dimensionName);
}
