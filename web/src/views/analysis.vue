<template>
    <div>
        <LoadingDots :visible="loading" message="加载中，请稍候" />
        <JobFilter v-model="filters" @submit="onSubmit" @reset="onReset" />
        <br>

        <el-drawer title="岗位技能词云图生成" :visible.sync="drawer" :direction="direction" :before-close="handleClose" size="60%">
            <el-form :inline="true" class="demo-form-inline" style="display: flex; flex-wrap: wrap; gap: 20px; margin-left: 40px;">
                <el-form-item label="工作岗位">
                    <el-select v-model="selectedTitle" placeholder="工作岗位" style="width: 220px;">
                        <el-option v-for="item in titleList" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>

                <el-button type="primary" @click="generateWordCloud" style="height: 41px;" :loading="generating">查询</el-button>
            </el-form>

            <div v-if="wordCloudUrl" style="margin-top: 20px; text-align: center;">
                <img :src="wordCloudUrl" alt="岗位技能词云图" style="max-width: 100%; max-height: 500px;" />
            </div>

        </el-drawer>

        <el-button @click="drawer = true" type="primary"
            style="height: 36px; line-height: 36px; padding: 0 16px; margin-left: 1000px;">
            技能分析
        </el-button>


        <JobChart title="岗位薪资分析" :data="titleData" xField="title" :yFields="yFields" :sortFields="sortFields"
            chartWidth="2250px" chartHeight="500px" />

        <div style="display: flex; flex-wrap: wrap; gap: 0px;">
            <JobChart title="城市薪资分析" :data="cityData" xField="city" :yFields="yFields" :sortFields="sortFields"
                chartWidth="740px" chartHeight="430px" />

            <JobChart title="学历薪资分析" :data="degreeData" xField="degree" :yFields="yFields" :sortFields="sortFields"
                chartWidth="550px" chartHeight="430px" />

            <JobChart title="工作经验薪资分析" :data="experienceData" xField="experience" :yFields="yFields"
                :sortFields="sortFields" chartWidth="530px" chartHeight="430px" />

            <JobChart title="行业薪资分析" :data="industryData" xField="industry" :yFields="yFields" :sortFields="sortFields"
                chartWidth="400px" chartHeight="430px" />
        </div>



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
            generating: false,
            cityData: [],
            industryData: [],
            degreeData: [],
            experienceData: [],
            titleData: [],
            filters: {},
            titleList: [],
            selectedTitle: '',
            wordCloudUrl: '',
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
        handleClose(done) {
            done();
            this.generating = false;
        },
        formatOptions(options) {
            if (!options || options.length === 0) return '';
            if (options.length === 1 && options[0] === '不限') return '';
            return options.filter(opt => opt !== '不限').join(',');
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
  