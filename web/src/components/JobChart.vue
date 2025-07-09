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
    },
    data() {
        return {
            chartInstance: null,
            localSortField: this.sortFields[0].value,
            localIsAscending: false,
            dynamicWidth: "1000px",
            isFirstRender: true // 添加首次渲染标志
        };
    },
    computed: {
        chartRefName() {
            return `chart_${this._uid}`;
        },
        chartStyle() {
            return {
                width: this.dynamicWidth,
                height: '480px'
            };
        }
    },
    mounted() {
        this.initChart();
    },
    methods: {
        initChart() {
            this.calculateWidth();
            this.$nextTick(() => {
                this.chartInstance = echarts.init(this.$refs[this.chartRefName]);
                this.updateChart();
                this.isFirstRender = false;
            });
        },
        calculateWidth() {
            // 自适应表格的宽度，每一个元素占150px像素，最多是最大宽度1150px，最小宽度400px
            if (this.data && this.data.length > 0) {
                const baseWidth = this.data.length * 150;
                const maxWidth = 1150;
                const minWidth = 400;
                const finalWidth = Math.max(Math.min(baseWidth, maxWidth), minWidth);
                this.dynamicWidth = `${finalWidth}px`;
            }
        },
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
                yAxisIndex: y.yAxisIndex || 0,
                data: sortedData.map(item => item[y.value] || 0),
                animation: true, // 确保动画开启
                animationDuration: 1000, // 设置动画持续时间
                animationEasing: 'elasticOut' // 设置动画缓动效果
            }));

            const option = {
                title: { text: this.title, top: 0, textStyle: { fontSize: 20 } },
                tooltip: { trigger: 'axis' },
                legend: { data: this.yFields.map(y => y.label), right: 10 },
                grid: { top: 80, bottom: 120, left: 70, right: 70 },
                xAxis: { 
                    data: xAxisData, 
                    axisLabel: { interval: 0, rotate: 45 } 
                },
                yAxis: [    // 左边y轴为薪资
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
                series: series,
                animation: true, // 确保图表整体动画开启
                animationDuration: 2000,
                animationEasing: 'bounceIn'
            };

            // 如果是首次渲染，直接设置option
            // 如果不是首次渲染，使用setOption的notMerge模式来保留动画
            if (this.chartInstance) {
                this.chartInstance.setOption(option, {
                    notMerge: !this.isFirstRender
                });
            }
        }
    },
    watch: {
        data: {
            handler() {
                this.calculateWidth();
                this.$nextTick(() => {
                    if (this.chartInstance) {
                        this.chartInstance.resize();
                        this.updateChart();
                    }
                });
            },
            deep: true
        }
    },
    beforeDestroy() {
        if (this.chartInstance) {
            this.chartInstance.dispose();
        }
    }
};
</script>