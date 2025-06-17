package com.jobagent.dto;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import javax.validation.constraints.NotEmpty;
import java.util.ArrayList;
import java.util.List;

@Data
@ApiModel("分页查询职位接口参数")
public class JobPageDTO {

    // 基础字段
    @ApiModelProperty(value = "搜索关键词", example = "Java")
    private String keyword = "";

    @ApiModelProperty(value = "城市名称", example = "广州")
    private String city = "";

    // 列表字段（多选）
    @ApiModelProperty(value = "经验要求（可多选）", example = "[\"1-3年\", \"3-5年\"]")
    private List<String> experience = new ArrayList<>();

    @ApiModelProperty(value = "学历要求（可多选）", example = "[\"本科\", \"硕士\"]")
    private List<String> degree = new ArrayList<>();

    @ApiModelProperty(value = "行业（可多选）", example = "[\"互联网\", \"金融\"]")
    private List<String> industry = new ArrayList<>();

    @ApiModelProperty(value = "公司规模（可多选）", example = "[\"100-499人\", \"500-999人\"]")
    private List<String> scale = new ArrayList<>();

    @ApiModelProperty(value = "融资阶段（可多选）", example = "[\"A轮\", \"B轮\"]")
    private List<String> stage = new ArrayList<>();

    // 其他单值字段
    @ApiModelProperty(value = "职位性质", example = "全职")
    private String jobType = "";

    @ApiModelProperty(value = "职位类型", example = "技术")
    private String title = "";

    @ApiModelProperty(value = "薪资范围", example = "10k-20k")
    private String salary = "";

    @ApiModelProperty(value = "区域商圈", example = "天河区")
    private String areaBusiness = "";

    @ApiModelProperty(value = "页码", example = "1")
    private int page;

    @ApiModelProperty(value = "每页个数，最大30", example = "30")
    private int pageSize;
}
