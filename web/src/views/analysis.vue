<template>
    <div style="max-width: 1200px; margin: 0 auto;">
        <LoadingDots :visible="loading" message="加载中，请稍候" />
        <JobFilter v-model="filters" @submit="onSubmit" @reset="onReset" />
        <br>

        <el-tabs type="border-card" style="height: 593px;" @tab-click="handleTabClick" >
            <el-tab-pane label="岗位薪资分析">
                <div style="display: flex; justify-content: center;">
                    <JobChart :key="`chart1_${chartTrigger}`" title="岗位薪资分析" :data="titleData" xField="title" :yFields="yFields" :sortFields="sortFields" />
                </div>
            </el-tab-pane>

            <el-tab-pane label="城市薪资分析">
                <div style="display: flex; justify-content: center;">
                    <JobChart :key="`chart2_${chartTrigger}`" title="城市薪资分析" :data="cityData" xField="city" :yFields="yFields" :sortFields="sortFields" />
                </div>
            </el-tab-pane>

            <el-tab-pane label="学历薪资分析">
                <div style="display: flex; justify-content: center;">
                    <JobChart :key="`chart3_${chartTrigger}`" title="学历薪资分析" :data="degreeData" xField="degree" :yFields="yFields"
                        :sortFields="sortFields" />
                </div>
            </el-tab-pane>

            <el-tab-pane label="工作经验薪资分析">
                <div style="display: flex; justify-content: center;">
                    <JobChart :key="`chart4_${chartTrigger}`" title="工作经验薪资分析" :data="experienceData" xField="experience" :yFields="yFields"
                        :sortFields="sortFields" />
                </div>
            </el-tab-pane>

            <el-tab-pane label="行业薪资分析">
                <div style="display: flex; justify-content: center;">
                    <JobChart :key="`chart5_${chartTrigger}`" title="行业薪资分析" :data="industryData" xField="industry" :yFields="yFields"
                        :sortFields="sortFields" />
                </div>
            </el-tab-pane>

            <el-tab-pane label="岗位技能词云图生成">
                <el-form :inline="true" class="demo-form-inline"
                    style="display: flex; flex-wrap: wrap; gap: 20px; margin-left: 40px;">
                    <el-form-item label="工作岗位">
                        <el-select v-model="selectedTitle" placeholder="工作岗位" style="width: 220px;">
                            <el-option v-for="item in titleList" :key="item" :label="item" :value="item" />
                        </el-select>
                    </el-form-item>

                    <el-button type="primary" @click="generateWordCloud" style="height: 41px;"
                        :loading="generating" size="small">查询</el-button>
                </el-form>

                <div v-if="wordCloudUrl" style="margin-top: 20px; text-align: center;">
                    <img :src="wordCloudUrl" alt="岗位技能词云图" style="max-width: 100%; height: 70%;" />
                </div>
            </el-tab-pane>
        </el-tabs>




    </div>
</template>
  
<script>
import JobChart from "@/components/JobChart.vue";
import JobFilter from "@/components/JobFilter.vue";
import LoadingDots from "@/components/LoadingDots.vue";
import { titleListAPI } from '@/api/job';
import { chartAPI, wordCloudAPI } from "@/api/chart"

export default {
    name: "JobAnalysis",
    components: { JobChart, JobFilter, LoadingDots },
    data() {
        return {
            loading: true,
            generating: false,  // 词云图生成时按钮的加载状态
            activeTab: '1', // 默认激活第一个 Tab
            chartTrigger: 0, // 用来强制刷新子组件，当vue组件的key发生变化时，会强制创建新组建，初始化ECharts动画
            cityData: [],  // 存放不同城市的岗位数量、最低薪资平均值、最高薪资平均值
            industryData: [],
            degreeData: [],
            experienceData: [],
            titleData: [],
            filters: {},        // 过滤规则
            titleList: [],
            selectedTitle: '',
            wordCloudUrl: '',    // 存放岗位技能词云图的 URL
            yFields: [
                { label: '最低薪资', value: 'salaryFloor', yAxisIndex: 0 },
                { label: '最高薪资', value: 'salaryCeiling', yAxisIndex: 0 },
                { label: '岗位个数', value: 'count', yAxisIndex: 1 }
            ],
            sortFields: [
                { label: '最低薪资', value: 'salaryFloor' },
                { label: '最高薪资', value: 'salaryCeiling' },
                { label: '岗位个数', value: 'count' }
            ],
            drawer: false,
            direction: 'btt',
        };
    },
    methods: {
        onSubmit() {
            this.fetchChartData();
        },
        onReset() {
            this.filters = {};
            this.fetchChartData();
            if (this.wordCloudUrl) {
                URL.revokeObjectURL(this.wordCloudUrl);
                this.wordCloudUrl = '';
            }
        },
        handleTabClick() {
            // 每次切换 Tab，chartTrigger +1，JobChart 会重新渲染，动画重新播放
            this.chartTrigger++;
        },
        handleClose(done) {
            done();
            this.generating = false;
        },
        formatOptions(options) {  
            if (!options || options.length === 0) return '';  // 空数组返回空字符串
            if (options.length === 1 && options[0] === '不限') return '';  // 不限选项返回空字符串
            return options.filter(opt => opt !== '不限').join(',');  // 去掉不限选项，用逗号分隔其他选项
        },
        reset() {
            this.cityData = [],
            this.industryData = [],
            this.degreeData = [],
            this.experienceData = [],
            this.titleData = []
        },
        async fetchTitleList() {
            try {
                const res = await titleListAPI();
                this.titleList = res.data
            } catch (error) {
                console.error('fetchTitleList error:', error);
            }
        },
        async fetchChartData() {
            try {
                this.loading = true;  // 开始加载
                this.reset();
                const params = {
                    city: this.formatOptions(this.filters.city),
                    experience: this.formatOptions(this.filters.experience),
                    degree: this.formatOptions(this.filters.degree),
                    industry: this.formatOptions(this.filters.industry),
                    scale: this.formatOptions(this.filters.scale),
                    stage: this.formatOptions(this.filters.stage),
                    title: this.formatOptions(this.filters.title),
                };
                const cityData = await chartAPI({ ...params, dimensionName: 'city' });
                const industryData = await chartAPI({ ...params, dimensionName: 'industry' });
                const degreeData = await chartAPI({ ...params, dimensionName: 'degree' });
                const experienceData = await chartAPI({ ...params, dimensionName: 'experience' });
                const titleData = await chartAPI({ ...params, dimensionName: 'title' });

                this.cityData = cityData.data;
                this.industryData = industryData.data;
                this.degreeData = degreeData.data;
                this.experienceData = experienceData.data;
                this.titleData = titleData.data;
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;  // 结束加载
            }
        },
        async generateWordCloud() {
            if (this.selectedTitle === '') {
                this.$message.error('请选择工作岗位');
                return;
            }
            this.generating = true; // 开始加载
            this.wordCloudUrl = '';
            try {
                const blob = await wordCloudAPI(this.selectedTitle);
                this.wordCloudUrl = URL.createObjectURL(blob);
            } catch (error) {
                console.error(error);
            } finally {
                this.generating = false; // 结束加载
            }
        }
    },
    async mounted() {
        this.fetchTitleList();
        this.fetchChartData();
    }
};
</script>
  