import axios from 'axios';
import { getFiltersMD5 } from "@/utils/encrypt";
import { jobListFilterAPI } from "@/api/job";

export default {
    onSubmit() {
        this.currentPage = 1;
        this.fetchJobList();
    },
    onReset() {
        this.filters = {};
        this.jobList = [];
    },
    startJob(getDesc = false) {
        // 清理可能残留的定时器
        this.loading = true;
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
        const params = { userId: this.$store.state.user.userInfo.id };
        params.getDesc = getDesc;
        for (const key in this.filters) {
            const value = this.filters[key];
            if (Array.isArray(value) && value.length === 1 && value[0] === '不限') {
                params[key] = [];
            } else {
                params[key] = value;
            }
        }
        params.filterHash = getFiltersMD5(this.filters);
        console.log(params)
        axios.post('/crawl/start/joblist', params)
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
        this.loading = false;
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        if (this.tableTimer) {
            clearInterval(this.tableTimer);
            this.tableTimer = null;
        }
        axios.get('/crawl/stop')
            .then(() => {
                this.status = 'exception';
            });
    },
    pollProgress() {
        // 定时向后端获取进度
        this.timer = setInterval(() => {
            axios.get('/crawl/progress')
                .then(response => {
                    this.progress = response.data.percentage;
                    if (this.progress < 0) {
                        this.$message.error(response.data.error);
                        clearInterval(this.timer);
                        clearInterval(this.tableTimer);
                    }
                    else if (this.progress >= 100) {
                        this.loading = false;
                        this.status = 'success';
                        clearInterval(this.timer);
                        clearInterval(this.tableTimer);
                        this.fetchJobList();
                    }
                })
                .catch((err) => {
                    this.$message.error(err.message || '获取进度失败');
                    this.status = 'exception';
                    clearInterval(this.timer);
                });
        }, 1000); // 每1秒轮询一次
    },
    getJobTableTimer() {
        this.tableTimer = setInterval(() => {
            this.fetchJobList();
        }, 1000); // 每1s更新一次
    },
    async fetchJobList() {
        try {
            const filterHash = getFiltersMD5(this.filters);
            const params = {
                userId: this.$store.state.user.userInfo.id,
                filterHash: filterHash,
                page: this.currentPage,
                pageSize: this.pageSize
            }
            console.log(params)
            const response = await jobListFilterAPI(params)
            this.jobList = response.data.items
            this.totalNumber = response.data.total
        } catch (error) {
            this.$message.error(error.message || '请求职位列表失败')
        }
    },
    async fetchJobListAndRestore() {
        await this.fetchJobList();
        this.$nextTick(() => {
            this.$refs.jobTableRef.restoreSelection();
        });
    }
}