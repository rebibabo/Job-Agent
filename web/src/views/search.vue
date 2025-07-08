<template>
    <div style="max-width: 1200px; margin: 0 auto;">
        <!-- 抽屉 -->
        <el-drawer title="查询规则" size="50%" :visible.sync="filterDrawerVisible" direction="rtl" destroy-on-close>
            <div style="margin-left: 20px;">
                <SearchFilter v-model="filters" @submit="onSubmit" @reset="onReset" />
            </div>
        </el-drawer>

        <!-- 原来的三个按钮 -->
        <el-form label-width="0" inline>
            <el-form-item>
                <el-button type="primary" @click="filterDrawerVisible = true" size="small">查询规则</el-button>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="() => startJob(false)" :loading="loading" size="small">开始任务</el-button>
            </el-form-item>
            <el-form-item>
                <el-button type="danger" @click="stopJob" size="small">停止任务</el-button>
            </el-form-item>
        </el-form>

        <!-- 进度条 -->
        <el-progress :percentage="progress" :status="status" style="margin-top: -19px;"/>
        <br />

        <!-- 表格 -->
        <JobTable :jobList="jobList" :filters="filters" :currentPage="currentPage" :pageSize="pageSize"
            :totalNumber="totalNumber" @update:currentPage="currentPage = $event" :heightRatio="0.7"
            @update:pageSize="pageSize = $event" @pagination-change="fetchJobListAndRestore" ref="jobTableRef" />
    </div>
</template>

<script>

import SearchFilter from "@/components/SearchFilter.vue";
import JobTable from "@/components/JobTable.vue";
import searchMethods from '@/utils/searchMethod.js';

export default {
    name: 'JobSearch',
    components: { SearchFilter, JobTable },
    props: {
        selectedJobIds: {
            type: Array,
            default: () => []
        },
    },
    data() {
        return {
            filterDrawerVisible: false,
            progress: 0,
            jobList: [],
            status: null,
            timer: null,
            tableTimer: null,
            filters: {},
            currentPage: 1,
            pageSize: 40,
            loading: false,
            totalNumber: 0,
        };
    },
    methods: {
        ...searchMethods,

    },
    beforeDestroy() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
}
</script>
