<template>
    <div>
        <!-- 排序控件 -->
        <div style="margin-bottom: 10px;">
            <el-radio-group v-model="localSortField" size="small" @change="updateChart">
                <el-radio-button v-for="item in sortFields" :key="item.value" :label="item.value">
                    {{ item.label }}
                </el-radio-button>
            </el-radio-group>

            <el-switch v-model="localIsAscending" active-text="升序" inactive-text="降序" @change="updateChart"
                style="margin-left: 20px;"></el-switch>
        </div>
        <br>
        <!-- 图表 -->
        <div :ref="chartRefName" :style="chartStyle"></div>
    </div>
</template>
  
<script>
import * as echarts from "echarts";

export default {
    name: "JobChart",
    props: {
        title: { type: String, default: "数据分析" },
        data: { type: Array, required: true },
        xField: { type: String, required: true },
        yFields: {
            type: Array,
            required: true
            // 每个元素：{ label: '岗位个数', value: 'count', yAxisIndex: 0 }
        },
        sortFields: { type: Array, required: true },
        chartWidth: { type: String, default: "1000" },
        chartHeight: { type: String, default: "500px" }
    },
    data() {
        return {
            chartInstance: null,
            localSortField: this.sortFields[0].value,
            localIsAscending: false
        };
    },
    computed: {
        chartRefName() {
            return `chart_${this._uid}`;
        },
        chartStyle() {
            return {
                width: this.chartWidth,
                height: this.chartHeight
            };
        }
    },
    mounted() {
        this.chartInstance = echarts.init(this.$refs[this.chartRefName]);
        this.updateChart();
    },
    methods: {
        updateChart() {
            const sortedData = [...this.data].sort((a, b) => {
                const field = this.localSortField;
                if (this.localIsAscending) {
                    return (a[field] || 0) - (b[field] || 0);
                } else {
                    return (b[field] || 0) - (a[field] || 0);
                }
            });

            const xAxisData = sortedData.map(item => item[this.xField]);
            const series = this.yFields.map(y => ({
                name: y.label,
                type: "bar",
                yAxisIndex: y.yAxisIndex || 0, // 默认为左轴
                data: sortedData.map(item => item[y.value] || 0)
            }));

            const option = {
                title: { text: this.title, top: 0, textStyle: { fontSize: 20 } },
                tooltip: { trigger: 'axis' },
                legend: { data: this.yFields.map(y => y.label), right: 10 },
                grid: { top: 80, bottom: 120, left: 70, right: 70 },
                xAxis: { data: xAxisData, axisLabel: {interval: 0,  rotate: 45  } },
                yAxis: [
                    {
                        type: 'value',
                        name: '薪资 (年)',
                    },
                    {
                        type: 'value',
                        name: '岗位个数',
                        position: 'right'
                        
                    }
                ],
                series: series
            };

            this.chartInstance.setOption(option);
        }
    },
    watch: {
        data: {
            handler() {
            this.updateChart();
            },
            deep: true // 深度监听，防止数据内部变化不触发
        }
        }
};
</script>
  