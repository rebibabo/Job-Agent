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
    </div>
</template>

<script>
import axios from 'axios';
import SearchFilter from "@/components/SearchFilter.vue";

export default {
    name: 'JobSearch',
    components: { SearchFilter },
    data() {
        return {
            progress: 0,
            status: null,
            timer: null,
            filters: {},
        };
    },
    methods: {
        onSubmit() {
            console.log(this.filters);
        },
        onReset() {
            this.filters = {};
        },
        startJob() {
            console.log(this.$store.state.user.userInfo.id)
            // 假设启动任务接口
            this.status = null;
            axios.post('/search/joblist/start', { userId: this.$store.state.user.userInfo.id })
                .then(() => {
                    this.progress = 0;
                    this.pollProgress();
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
            axios.post('/search/joblist/stop', { userId: this.$store.state.user.userInfo.id })
                .then(() => {
                    this.status = 'exception';
                });
        },
        pollProgress() {
            // 定时向后端获取进度
            this.timer = setInterval(() => {
                axios.post('/search/joblist/progress', { userId: this.$store.state.user.userInfo.id })
                    .then(response => {
                        this.progress = response.data.percentage;
                        if (this.progress >= 100) {
                            this.status = 'success';
                            clearInterval(this.timer);
                        }
                    })
                    .catch(() => {
                        this.status = 'exception';
                        clearInterval(this.timer);
                    });
            }, 1000); // 每1秒轮询一次
        }
    },
    beforeDestroy() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
}
</script>
