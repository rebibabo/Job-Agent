package com.jobagent.dto;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Data
@ApiModel("分页查询职位接口参数")
public class ChartDTO {
    @ApiModelProperty(value = "用于分析的维度", example = "city/degree/experience/title")
    private String dimensionName = "";

    @ApiModelProperty(value = "城市名称（可多选，逗号分隔）", example = "广州,北京")
    private String city = "";

    @ApiModelProperty(value = "经验要求（可多选，逗号分隔）", example = "1-3年,3-5年")
    private String experience = "";

    @ApiModelProperty(value = "学历要求（可多选，逗号分隔）", example = "本科,硕士")
    private String degree = "";

    @ApiModelProperty(value = "行业（可多选，逗号分隔）", example = "互联网,金融")
    private String industry = "";

    @ApiModelProperty(value = "公司规模（可多选，逗号分隔）", example = "100-499人,500-999人")
    private String scale = "";

    @ApiModelProperty(value = "融资阶段（可多选，逗号分隔）", example = "A轮,B轮")
    private String stage = "";

    @ApiModelProperty(value = "职位类型（可多选，逗号分隔）", example = "技术")
    private String title = "";

    @ApiModelProperty(value = "薪资范围（可多选，逗号分隔）", example = "10k-20k")
    private String salary = "";

    // 添加方法将字符串转换为List（可选）
    public List<String> getCityList() {
        return splitStringToList(this.city);
    }

    public List<String> getExperienceList() {
        return splitStringToList(this.experience);
    }

    public List<String> getDegreeList() {
        return splitStringToList(this.degree);
    }

    public List<String> getIndustryList() {
        return splitStringToList(this.industry);
    }

    public List<String> getScaleList() {
        return splitStringToList(this.scale);
    }

    public List<String> getStageList() {
        return splitStringToList(this.stage);
    }

    public List<String> getTitleList() {
        return splitStringToList(this.title);
    }

    public List<String> getSalaryList() {
        return splitStringToList(this.salary);
    }

    private List<String> splitStringToList(String str) {
        if (str == null || str.trim().isEmpty()) {
            return new ArrayList<>();
        }
        return Arrays.asList(str.split("\\s*,\\s*"));
    }
}
