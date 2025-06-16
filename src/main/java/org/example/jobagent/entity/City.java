package org.example.jobagent.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class City {
    private String province;
    private String city;
    private String region;
    private String cityId;
    private String provinceCode;
    private String cityCode;
    private String regionCode;
    private Float longitude;
    private Float latitude;
}
