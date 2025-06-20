<template>
    <div>
        <h1 style="font-size: 27px;">职位查询系统</h1>

        <!-- 直接使用 JobFilter 组件 -->
        <JobFilter v-model="filters" @submit="onSubmit" @reset="onReset" />

        <LoadingDots :visible="loading" message="加载中，请稍候" />
        <br />

        <el-table :data="jobList" stripe border max-height="850" style="width: 100%" ref="jobTable" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="40"></el-table-column>
            <el-table-column prop="jobName" sortable label="工作名称" width="300" />
            <el-table-column prop="companyName" sortable label="公司名称" width="280" />
            <el-table-column prop="salary" sortable label="薪资" width="180" />
            <el-table-column prop="city" sortable label="工作城市" width="150" />
            <el-table-column prop="region" sortable label="城市区域" width="150" />
            <el-table-column prop="experience" sortable label="经验要求" width="180" />
            <el-table-column prop="degree" sortable label="学历要求" width="150" />
            <el-table-column prop="industry" sortable label="公司行业" width="180" />
            <el-table-column prop="title" sortable label="工作岗位" width="180" />
            <el-table-column prop="scale" sortable label="公司规模" width="150" />
            <el-table-column prop="stage" sortable label="融资阶段" width="150" />
            <el-table-column label="操作">
                <template #default="{ row }">
                    <el-button @click="handleViewJob(row.url, row.id)" :type="row.sentCv ? 'success' : row.viewed ? 'info' : 'primary'" size="mini" style="width: 70px;">{{ row.sentCv ? '已投递' : row.viewed ? '已查看' : '查看' }}</el-button>
                    <el-button @click="handleDeleteJob([row.id])" type="danger" size="mini">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <div style="display: flex; align-items: center; justify-content: space-between; margin: 20px 0;">
        <!-- 左边：删除所选按钮 -->
        <el-button type="danger" @click="deleteSelectedJobs" :disabled="!selectedJobs.length" size="mini">
            删除所选
        </el-button>

        <el-button type="primary" @click="sendResume" :disabled="!selectedJobs.length" size="mini">
            投递简历
        </el-button>

        <!-- 中间：分页 -->
        <div style="flex: 1; display: flex; justify-content: center;">
            <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[20, 40, 60, 80, 100]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalNumber"
            />
        </div>

        <!-- 右边可以留空，也可以添加其他按钮或元素 -->
        <div style="width: 100px;"></div> <!-- 占位用，如无需可删掉 -->
        </div>
    </div>
</template>
  
<script>
import JobFilter from '@/components/JobFilter.vue';  // 请根据你的路径调整
import LoadingDots from '@/components/LoadingDots.vue';
import { jobListAPI, deleteAPI, setViewStatusAPI } from '@/api/job';
import { nextTick } from 'vue'

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
            selectedJobs: []
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
                    userId: this.$store.state.user.userInfo.id,
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
        scrollUp() {
            nextTick(() => {
                const tableWrapper = document.querySelector('.el-table__body-wrapper')
                if (tableWrapper) {
                    tableWrapper.scrollTop = 0
                }
            })
        },
        handleSizeChange(size) {
            this.pageSize = size;
            this.fetchJobList();
            this.scrollUp();
        },
        handleCurrentChange(page) {
            this.currentPage = page;
            this.fetchJobList();
            this.scrollUp();
        },
        deleteJob(ids) {
            var params = {
                user_id: String(this.$store.state.user.userInfo.id),
                job_ids: ids
            }
            deleteAPI(params)
            .then(() => {
                this.fetchJobList();
            })
            .catch(error => {
                this.$message.error(error.message || '删除失败');
            });
        },
        handleViewJob(url, job_id) {
            if (!url) {
                this.$message.warning('该职位没有有效的链接');
                return;
            }
            const fullUrl = url.startsWith('http') ? url : `https://${url}`;
            window.open(fullUrl, '_blank');
            const params = {
                user_id: String(this.$store.state.user.userInfo.id),
                job_id: job_id
            }
            console.log(params)
            setViewStatusAPI(params)
            this.fetchJobList();
        },
        handleSelectionChange(selection) {
            this.selectedJobs = selection;
        },
        onSubmit() {
            this.currentPage = 1;
            this.fetchJobList();
            this.scrollUp();
        },
        onReset() {
            this.currentPage = 1;
            this.fetchJobList();
            this.scrollUp();
        },
        
        handleDeleteJob(ids) {
            this.$confirm('确认删除该职位？')
                .then(() => {
                    this.deleteJob(ids)
                })
               .catch(() => {
                    this.$message.info('已取消删除');
                });
        },
        deleteSelectedJobs() {
            const ids = this.selectedJobs.map(job => job.id);
            if (ids.length === 0) {
                this.$message.warning('请先选择要删除的岗位');
                return;
            }
            this.$confirm('确认删除所选岗位？')
                .then(() => {
                    this.deleteJob(ids);
                })
                .catch(() => {
                    this.$message.info('已取消删除');
                });
        },
        sendResume() {
            const ids = this.selectedJobs.map(job => job.id);
            if (ids.length === 0) {
                this.$message.warning('请先选择要投递简历的岗位');
                return;
            }
            
        }
    },
    mounted() {
        this.fetchJobList();
    }
};
</script>
  
<style></style>
  