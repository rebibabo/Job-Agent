package com.jobagent.utils;

import com.kennycason.kumo.CollisionMode;
import com.kennycason.kumo.WordCloud;
import com.kennycason.kumo.bg.CircleBackground;
import com.kennycason.kumo.bg.RectangleBackground;
import com.kennycason.kumo.font.KumoFont;
import com.kennycason.kumo.font.scale.LinearFontScalar;
import com.kennycason.kumo.font.scale.SqrtFontScalar;
import com.kennycason.kumo.image.AngleGenerator;
import com.kennycason.kumo.palette.ColorPalette;
import com.kennycason.kumo.WordFrequency;

import java.awt.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

public class WordCloudBuilder {
    private static int maxLength=100;
    private static int width=1500;
    private static int height=500;

    public static void setLength(int length) {WordCloudBuilder.maxLength = length;}
    public static void setWidth(int width) {WordCloudBuilder.width = width;}
    public static void setHeight(int height) {WordCloudBuilder.height = height;}

    private WordCloudBuilder() {}
    public static void generate(List<String> wordList, String outputFilePath) {
        // 构造词频数据
        HashMap<String, Integer> frequencyMap = new HashMap<>();
        for (String word : wordList) {
            frequencyMap.put(word, frequencyMap.getOrDefault(word, 0) + 1);
        }

        List<WordFrequency> topWords = frequencyMap.entrySet().stream()
                .sorted((e1, e2) -> e2.getValue().compareTo(e1.getValue()))  // 按频率降序
                .limit(WordCloudBuilder.maxLength)                                           // 取前 maxLength 个
                .map(e -> new WordFrequency(e.getKey(), e.getValue()))      // 转成 WordFrequency
                .collect(Collectors.toList());


        // 配置词云参数
        java.awt.Font font = new java.awt.Font("STSong-Light", Font.PLAIN, 22);  // 更大的基础字体
        Dimension dimension = new Dimension(WordCloudBuilder.width, WordCloudBuilder.height);
        WordCloud wordCloud = new WordCloud(dimension, CollisionMode.PIXEL_PERFECT);

// 减小 padding，使词语更紧凑
        wordCloud.setPadding(5);

// 改成矩形背景，更容易充满屏幕
        wordCloud.setBackground(new RectangleBackground(dimension));

// 设置背景色（可选：纯白色或透明）
        wordCloud.setBackgroundColor(new Color(255, 255, 255));

// 使用更丰富的颜色搭配
        wordCloud.setColorPalette(new ColorPalette(
                new Color(0x4055F1),
                new Color(0x408DF1),
                new Color(0x40AAF1),
                new Color(0x40C5F1),
                new Color(0x40D3F1),
                new Color(0xFFFFFF),
                new Color(0xFF5733),
                new Color(0xC70039),
                new Color(0x900C3F),
                new Color(0x581845)
        ));

// 设置字体缩放：大字体更大，小字体也适当加大
        wordCloud.setFontScalar(new LinearFontScalar(20, 120));

// 使用中文字体（注意确保服务器支持）
        wordCloud.setKumoFont(new KumoFont(font));

        // 生成词云
        wordCloud.build(topWords);
        wordCloud.writeToFile(outputFilePath); // 输出文件
    }
}
