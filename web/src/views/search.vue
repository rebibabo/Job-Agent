<template>
    <div>
        <h1 style="font-size: 27px;">职位搜索系统</h1>

        <SearchFilter v-model="filters" @submit="onSubmit" @reset="onReset"/>

        <el-form label-width="0" inline>
            <el-form-item>
                <el-button type="primary" @click="fetchJobList">历史记录</el-button>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="() => startJob(false)">开始任务</el-button>
            </el-form-item>
            <el-form-item>
                <el-button type="danger" @click="stopJob">停止任务</el-button>
            </el-form-item>

            
        </el-form>

        <el-progress :percentage="progress" :status="status"/>
        <br>

        <JobTable
            :jobList="jobList"
            :filters="filters"
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

import SearchFilter from "@/components/SearchFilter.vue";
import JobTable from "@/components/JobTable.vue";
import searchMethods from '@/utils/searchMethod.js';

export default {
    name: 'JobSearch',
    components: { SearchFilter, JobTable },
    data() {
        return {
            progress: 0,
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
        ...searchMethods,

    },
    beforeDestroy() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
}
</script>
