<template>
    <div>
        <h1 style="font-size: 27px;">职位查询系统</h1>

        <!-- 直接使用 JobFilter 组件 -->
        <JobFilter v-model="filters" @submit="onSubmit" @reset="onReset" />

        <LoadingDots :visible="loading" message="加载中，请稍候" />
        <br />

        <el-table :data="jobList" stripe border max-height="850" style="width: 100%">
            <el-table-column prop="jobName" sortable label="工作名称" width="480" />
            <el-table-column prop="salary" sortable label="薪资" width="180" />
            <el-table-column prop="city" sortable label="工作城市" width="180" />
            <el-table-column prop="region" sortable label="城市区" width="180" />
            <el-table-column prop="experience" sortable label="经验要求" width="180" />
            <el-table-column prop="degree" sortable label="学历要求" width="180" />
            <el-table-column prop="industry" sortable label="公司行业" width="180" />
            <el-table-column prop="title" sortable label="工作岗位" width="180" />
            <el-table-column prop="scale" sortable label="公司规模" width="180" />
            <el-table-column prop="stage" sortable label="融资阶段" width="180" />
            <el-table-column label="操作">
                <template #default="{ row }">
                    <el-button @click="handleViewJob(row.url)" type="text" size="small">查看</el-button>
                </template>
            </el-table-column>
        </el-table>

        <br />

        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
                :page-sizes="[20, 40, 60, 80, 100]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper"
                :total="totalNumber" />
        </div>
    </div>
</template>
  
<script>
import JobFilter from '@/components/JobFilter.vue';  // 请根据你的路径调整
import LoadingDots from '@/components/LoadingDots.vue';
import { jobListAPI } from '@/api/job';

export default {
    name: 'JobQuery',
    components: { JobFilter, LoadingDots },
    data() {
        return {
            filters: {
                city: ['不限'],
                experience: ['不限'],
                degree: ['不限'],
                title: ['不限'],
                industry: ['不限'],
                scale: ['不限'],
                stage: ['不限'],
            },
            loading: true,
            currentPage: 1,
            pageSize: 40,
            totalNumber: 0,
            jobList: [],
        };
    },

    methods: {
        formatOptions(options) {
            if (!options || options.length === 0) return '';
            if (options.length === 1 && options[0] === '不限') return '';
            return options.filter(opt => opt !== '不限').join(',');
        },
        async fetchJobList() {
            try {
                this.loading = true;
                console.log(this.loading)
                const params = {
                    city: this.formatOptions(this.filters.city),
                    experience: this.formatOptions(this.filters.experience),
                    degree: this.formatOptions(this.filters.degree),
                    industry: this.formatOptions(this.filters.industry),
                    scale: this.formatOptions(this.filters.scale),
                    stage: this.formatOptions(this.filters.stage),
                    title: this.formatOptions(this.filters.title),
                    page: this.currentPage,
                    pageSize: this.pageSize,
                };
                const response = await jobListAPI(params);
                this.jobList = response.data.items;
                this.totalNumber = response.data.total;
            } catch (error) {
                this.$message.error(error.message || '请求职位列表失败');
            } finally {
                this.loading = false;
            }
        },
        handleSizeChange(size) {
            this.pageSize = size;
            this.fetchJobList();
        },
        handleCurrentChange(page) {
            this.currentPage = page;
            this.fetchJobList();
        },
        handleViewJob(url) {
            if (!url) {
                this.$message.warning('该职位没有有效的链接');
                return;
            }
            const fullUrl = url.startsWith('http') ? url : `https://${url}`;
            window.open(fullUrl, '_blank');
        },
        onSubmit() {
            this.currentPage = 1;
            this.fetchJobList();
        },
        onReset() {
            this.currentPage = 1;
            this.fetchJobList();
        }
    },
    mounted() {
        this.fetchJobList();
    }
};
</script>
  
<style></style>
  