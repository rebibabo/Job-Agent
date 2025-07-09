package com.jobagent.controller;

import com.jobagent.dto.ChartDTO;
import com.jobagent.service.ChartService;
import com.jobagent.vo.Result;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;
import java.util.Map;

@Slf4j
@RestController
public class ChartController {
    @Autowired
    private ChartService chartService;

    @PostMapping
    @RequestMapping("/chart")
    /**
     * 根据不同维度，包括（city, title, experience, degree）进行分组, 应用过滤规则，实现分组求岗位数量、最低薪资平均值和最高薪资平均值
     */
    public Result getChartData(@RequestBody ChartDTO chartDTO) {
        List<Map<String,Object>> chartData = chartService.getChartData(chartDTO);
        return Result.success(chartData);
    }

    @GetMapping(value="/wordCloud/{title}", produces=MediaType.IMAGE_PNG_VALUE)
    /**
     * 根据岗位类型title，获取该岗位所有的skills技能标签，生成词云图
     */
    public ResponseEntity<byte[]> getWordCloudPicture(@PathVariable String title) {
        // 获取词云图的存放位置
        String picturePath = chartService.getWordCloudPicture(title);

        if (picturePath == null || picturePath.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        File imgFile = new File(picturePath);
        if (!imgFile.exists()) {
            return ResponseEntity.notFound().build();
        }

        byte[] imageBytes = null;
        try {
            imageBytes = Files.readAllBytes(imgFile.toPath());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        // 返回图片的二进制数据
        return ResponseEntity.ok()
                .contentType(MediaType.IMAGE_PNG)
                .body(imageBytes);
    }
}
