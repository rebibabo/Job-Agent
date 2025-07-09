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

        if (this.tableTimer) {
            clearInterval(this.tableTimer);
            this.tableTimer = null;
        }
        this.fetchJobList();
                
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
        axios.post('/crawl/start/joblist', params)
            .then(() => {
                this.progress = 0;
                this.status = null;
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
        // 采用递归方式，而不是轮循的方式，能够解决进度条卡顿的问题，及1s更新内，如果DOM没有渲染下来，又会开启下一轮的轮询，导致内存占用过高
        const poll = () => {
            console.log('[轮询触发]', new Date().toISOString());
    
            axios.get('/crawl/progress')
                .then(response => {
                    this.progress = response.data.percentage;
                    if (this.progress < 0) {
                        this.$message.error(response.data.error);
                    } else if (this.progress >= 100) {
                        this.loading = false;
                        this.status = 'success';
                        this.fetchJobList();
                        return;
                    } else {
                        this.fetchJobList();
                        setTimeout(poll, 1000);  // 下一轮
                    }
                })
                .catch((err) => {
                    this.$message.error(err.message || '获取进度失败');
                    this.status = 'exception';
                });
        }
    
        poll(); // 启动轮询
    },
    getJobTableTimer() {
        // 定时更新job列表
        this.tableTimer = setInterval(() => {
            this.fetchJobList();
        }, 1000); // 每1s更新一次
    },
    async fetchJobList() {
        try {
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
        }
    },
    async fetchJobListAndRestore() {
        await this.fetchJobList();
        this.$nextTick(() => {
            this.$refs.jobTableRef.restoreSelection();      // 还原表格的选中状态，支持跨页保存选中状态
        });
    }
}