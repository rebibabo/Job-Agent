<template>
    <div>
        <h1 style="font-size: 27px;">职位搜索系统</h1>

        <SearchFilter v-model="filters" @submit="onSubmit" @reset="onReset"/>

        <el-form label-width="0" inline>
            
            <el-form-item>
                <el-button type="primary" @click="startJob">开始任务</el-button>
            </el-form-item>
            <el-form-item>
                <el-button type="danger" @click="stopJob">停止任务</el-button>
            </el-form-item>

            <el-progress :percentage="progress" :status="status"/>
        </el-form>

        <JobTable
            :jobList="jobList"
            :currentPage="currentPage"
            :pageSize="pageSize"
            :totalNumber="totalNumber"
            :maxHeight="700"
            @update:currentPage="currentPage = $event"
            @update:pageSize="pageSize = $event"
            @pagination-change="fetchJobList"
            ref="jobTableRef"
        />
    </div>
</template>

<script>
import axios from 'axios';
import SearchFilter from "@/components/SearchFilter.vue";
import { getFiltersMD5 } from "@/utils/encrypt";
import { jobListFilterAPI } from "@/api/job";
import JobTable from "@/components/JobTable.vue";

export default {
    name: 'JobSearch',
    components: { SearchFilter, JobTable },
    data() {
        return {
            progress: 0,
            loading: false,
            jobList: [],
            status: null,
            timer: null,
            tableTimer: null,
            filters: {},
            currentPage: 1,
            pageSize: 40,
            totalNumber: 0
        };
    },
    methods: {
        onSubmit() {
            this.currentPage = 1;
            this.fetchJobList();
        },
        onReset() {
            this.filters = {};
        },
        startJob() {
            // 清理可能残留的定时器
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
            if (this.tableTimer) {
                clearInterval(this.tableTimer);
                this.tableTimer = null;
            }
            this.fetchJobList();

            // 假设启动任务接口
            this.status = null;
            const params = {userId: this.$store.state.user.userInfo.id};
            for (const key in this.filters) {
                const value = this.filters[key];
                if (Array.isArray(value) && value.length === 1 && value[0] === '不限') {
                    params[key] = [];
                } else {
                    params[key] = value;
                }
            }
            params.filterHash = getFiltersMD5(this.filters);
            axios.post('/crawl/joblist/start', params)
                .then(() => {
                    this.progress = 0;
                    this.pollProgress();
                    this.getJobTableTimer();
                })
                .catch((res) => {
                    if (res.status === 410) {
                        this.$message.warning('任务已启动，请勿重复启动');
                    }
                });
        },
        stopJob() {
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
            if (this.tableTimer) {
                clearInterval(this.tableTimer);
                this.tableTimer = null;
            }
            axios.post('/crawl/joblist/stop', { userId: this.$store.state.user.userInfo.id })
                .then(() => {
                    this.status = 'exception';
                });
        },
        pollProgress() {
            // 定时向后端获取进度
            this.timer = setInterval(() => {
                axios.post('/crawl/joblist/progress', { userId: this.$store.state.user.userInfo.id })
                    .then(response => {
                        this.progress = response.data.percentage;
                        if (this.progress < 0) {
                            this.$message.error(response.data.error);
                            clearInterval(this.timer);
                            clearInterval(this.tableTimer);
                        }
                        else if (this.progress >= 100) {
                            this.status = 'success';
                            clearInterval(this.timer);
                            clearInterval(this.tableTimer);
                        }
                    })
                    .catch(() => {
                        this.status = 'exception';
                        clearInterval(this.timer);
                    });
            }, 1000); // 每1秒轮询一次
        },
        getJobTableTimer() {
            this.tableTimer = setInterval(() => {
                this.fetchJobList();
            }, 10000); // 每10s更新一次
        },
        async fetchJobList() {
            try {
                this.loading = true
                const params = {
                    userId: this.$store.state.user.userInfo.id,
                    filterHash: getFiltersMD5(this.filters),
                    page: this.currentPage,
                    pageSize: this.pageSize
                }
                const response = await jobListFilterAPI(params)
                this.jobList = response.data.items
                this.totalNumber = response.data.total
            } catch (error) {
                this.$message.error(error.message || '请求职位列表失败')
            } finally {
                this.loading = false
            }
        },
    },
    beforeDestroy() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    },
    mounted() {
        this.fetchJobList();
    }
}
</script>
