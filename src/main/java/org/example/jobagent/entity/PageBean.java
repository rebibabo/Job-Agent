package org.example.jobagent.entity;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;

@Data
@AllArgsConstructor
public class PageBean {
    Long total;
    List<City> list;
}
