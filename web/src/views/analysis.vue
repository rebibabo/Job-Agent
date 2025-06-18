<template>
    <div>
        <h1 style="font-size: 27px;">岗位分析</h1>

        <JobFilter v-model="filters" @submit="onSubmit" @reset="onReset" />

        <JobChart title="岗位薪资分析" 
        :data="titleData" 
        xField="title" 
        :yFields="[
            { label: '最低薪资', value: 'salaryFloor', yAxisIndex: 0 },
            { label: '最高薪资', value: 'salaryCeiling', yAxisIndex: 0 },
            { label: '岗位个数', value: 'count', yAxisIndex: 1 }
        ]" 
        :sortFields="[
            { label: '最低薪资', value: 'salaryFloor' },
            { label: '最高薪资', value: 'salaryCeiling' },
            { label: '岗位个数', value: 'count' }
        ]" 
        chartWidth="2200px"
        chartHeight="500px"/>
    </div>
</template>
  
<script>
import JobChart from "@/components/JobChart.vue";
import JobFilter from "@/components/JobFilter.vue";
import { cityChartAPI, industryChartAPI, degreeChartAPI, experienceChartAPI, titleChartAPI } from "@/api/chart"

export default {
    name: "JobAnalysis",
    components: { JobChart, JobFilter },
    data() {
        return {
            cityData: [],
            industryData: [],
            degreeData: [],
            experienceData: [],
            titleData: [],
            filters: {}
        };
    },
    methods: {
        onSubmit() {
            console.log("查询条件:", this.filters)
            // 发起查询逻辑...
        },
        onReset() {
            console.log("查询条件:", this.filters)
            // 重置逻辑...
        },
        async fetchData() {
            const cityData = await cityChartAPI(this.filters);
            const industryData = await industryChartAPI(this.filters);
            const degreeData = await degreeChartAPI(this.filters);
            const experienceData = await experienceChartAPI(this.filters);
            const titleData = await titleChartAPI(this.filters);
            this.cityData = cityData.data;
            this.industryData = industryData.data;
            this.degreeData = degreeData.data;
            this.experienceData = experienceData.data;
            this.titleData = titleData.data;
            // console.log(this.titleData);
        }
    },
    async mounted() {
        await this.fetchData();
        // console.log(this.titleData);
    }
};
</script>
  