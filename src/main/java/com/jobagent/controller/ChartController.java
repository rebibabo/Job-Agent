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
@RequestMapping("/chart")
public class ChartController {
    @Autowired
    private ChartService chartService;

    @PostMapping
    public Result getChartData(@RequestBody ChartDTO chartDTO) {
        List<Map<String,Object>> chartData = chartService.getChartData(chartDTO);
        return Result.success(chartData);
    }

    @GetMapping(value="/wordCloud/{title}", produces=MediaType.IMAGE_PNG_VALUE)
    public ResponseEntity<byte[]> getWordCloudPicture(@PathVariable String title) {
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

        return ResponseEntity.ok()
                .contentType(MediaType.IMAGE_PNG)
                .body(imageBytes);
    }
}
