package com.jobagent.vo;

import io.swagger.annotations.ApiModel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
@ApiModel("返回岗位和薪资的关系")
public class SalaryVO {
    private String dimensionValue;
    private int count;
    private int salaryFloor;
    private int salaryCeiling;
}
