<template>
    <div>
        <el-table :data="jobList" stripe border :max-height="maxHeight" style="width: 100%" ref="jobTable"
            @selection-change="handleSelectionChange" :row-key="row => row.id">
            <el-table-column type="selection" width="40"></el-table-column>
            <el-table-column prop="jobName" sortable label="工作名称" width="290" />
            <el-table-column prop="companyName" sortable label="公司名称" width="270" />
            <el-table-column prop="salary" sortable label="薪资" width="180" />
            <el-table-column prop="city" sortable label="工作城市" width="150" />
            <el-table-column prop="region" sortable label="城市区域" width="150" />
            <el-table-column prop="experience" sortable label="经验要求" width="150" />
            <el-table-column prop="degree" sortable label="学历要求" width="140" />
            <el-table-column prop="industry" sortable label="公司行业" width="150" />
            <el-table-column prop="title" sortable label="工作岗位" width="120" />
            <el-table-column prop="scale" sortable label="公司规模" width="150" />
            <el-table-column prop="stage" sortable label="融资阶段" width="150" />
            <el-table-column prop="score" sortable label="分数" width="100" v-if="rankScore" />
            <el-table-column label="操作"  min-width="180">
                <template #default="{ row }">
                    <el-button @click="viewJob(row)" :type="row.sentCv ? 'success' : row.viewed ? 'info' : 'primary'"
                        size="mini" style="width: 70px;">
                        {{ row.sentCv ? '已投递' : row.viewed ? '已查看' : '查看' }}
                    </el-button>
                    <el-button @click="confirmDelete([row.id])" type="danger" size="mini" style="width: 70px;">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <div style="display: flex; align-items: center; margin: 20px 0;">
            <el-button type="primary" @click="sendResume" :disabled="!selectedJobs.length" size="medium" v-if="!sentCVFrame">
                投递简历
            </el-button>
            <el-button type="danger" @click="confirmDeleteSelected" :disabled="!selectedJobs.length" size="medium" v-if="!sentCVFrame">
                删除所选
            </el-button>
            <el-button type="danger" @click="confirmaDeleteFilteredJob" size="medium" v-if="sentCVFrame">
                删除所有待过滤岗位
            </el-button>
            <el-button type="danger" @click="confirmDeleteAll" size="medium" v-if="deleteAll">
                删除全部
            </el-button>
        </div>

        <div style="flex: 1; display: flex; justify-content: center;">
            <el-pagination
                @size-change="onSizeChange"
                @current-change="onCurrentChange"
                :current-page="currentPage"
                :page-sizes="[20, 40, 60, 80, 100]"
                :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="totalNumber"
            />
        </div>
    </div>
</template>
  
<script>
import { nextTick } from 'vue'
import { setViewStatusAPI, deleteAPI, deleteALLAPI, deleteALLFilteredAPI } from '@/api/job'
import { getFiltersMD5 } from '@/utils/encrypt' 

export default {
    name: 'JobTable',
    props: {
        jobList: { type: Array, required: true },
        filters: { type: Object, required: false },
        currentPage: { type: Number, required: true },
        pageSize: { type: Number, required: true },
        totalNumber: { type: Number, required: true },
        maxHeight: { type: [Number, String], default: 850 },
        deleteAll: { type: Boolean, default: true },
        sentCVFrame: { type: Boolean, default: false },
        rankScore: { type: Boolean, default: false }
    },
    emits: ['view', 'delete', 'send', 'update:currentPage', 'update:pageSize', 'pagination-change'],
    data() {
        return {
            selectedJobs: [],
            selectedJobIds: [] // 用于跨页记忆
        }
    },
    methods: {
        toggleRowSelection(row, selected) {
            console.log("选择行", row, selected)
            this.$refs.jobTable.toggleRowSelection(row, selected);
        },
        handleSelectionChange(selection) {
            this.selectedJobs = selection
            this.selectedJobIds = [
                ...new Set([
                ...this.selectedJobIds,
                ...selection.map(item => item.id)
                ])
            ];
            this.$emit('selection-change', selection)
        },
        scrollUp() {
            nextTick(() => {
                const wrapper = this.$refs.jobTable?.$el.querySelector('.el-table__body-wrapper')
                if (wrapper) {
                    wrapper.scrollTop = 0
                }
            })
        },
        viewJob(row) {
            if (!row.url) {
                this.$message.warning('该职位没有有效的链接')
                return
            }
            const fullUrl = row.url.startsWith('http') ? row.url : `https://${row.url}`
            window.open(fullUrl, '_blank')
            setViewStatusAPI({ user_id: String(this.$store.state.user.userInfo.id), job_id: row.id })
            this.$emit('pagination-change')
        },
        confirmDelete(ids) {
            this.$confirm('确认删除所选岗位？')
                .then(() => {
                    deleteAPI({
                        user_id: String(this.$store.state.user.userInfo.id),
                        job_ids: ids,
                        filter_hash: getFiltersMD5(this.filters)
                    })
                        .then(() => {
                            this.$emit('pagination-change')
                        })
                        .catch(error => {
                            this.$message.error(error.message || '删除失败')
                        })
                })
                .catch(() => {
                    this.$message.info('已取消删除')
                })
        },
        confirmDeleteAll() {
            this.$confirm('确认删除全部岗位？')
                .then(() => {
                    deleteALLAPI({ userId: this.$store.state.user.userInfo.id, filterHash: getFiltersMD5(this.filters) })
                        .then(() => {
                            this.$emit('pagination-change')
                        })
                        .catch(error => {
                            this.$message.error(error.message || '删除失败')
                        })
                })
                .catch(() => {
                    this.$message.info('已取消删除')
                })
        },
        confirmDeleteSelected() {
            const ids = this.selectedJobs.map(job => job.id)
            if (ids.length === 0) {
                this.$message.warning('请先选择要删除的岗位')
                return
            }
            this.confirmDelete(ids)
        },
        confirmaDeleteFilteredJob() {
            this.$confirm('确认删除全部岗位？')
                .then(() => {
                    console.log(this.selectedJobIds.length)
                    deleteALLFilteredAPI({
                        user_id: this.$store.state.user.userInfo.id,
                        job_ids: this.selectedJobIds,
                        filter_hash: getFiltersMD5(this.filters)
                    })
                        .then(() => {
                            this.$emit('pagination-change')
                            this.selectedJobIds = []
                        })
                        .catch(error => {
                            this.$message.error(error.message || '删除失败')
                        })
                })
                .catch(() => {
                    this.$message.info('已取消删除')
                })
            
        },
        sendResume() {
            const ids = this.selectedJobs.map(job => job.id)
            if (ids.length === 0) {
                this.$message.warning('请先选择要投递简历的岗位')
                return
            }
            console.log('投递简历:', ids)
        },
        onSizeChange(size) {
            this.$emit('update:pageSize', size)
            this.$emit('pagination-change')
            this.scrollUp()
        },
        onCurrentChange(page) {
            this.$emit('update:currentPage', page)
            this.$emit('pagination-change')
            this.scrollUp()
        },
        restoreSelection(filteredJobIds = []) {
            this.$nextTick(() => {
                if (filteredJobIds.length === 0) {
                    this.jobList.forEach(row => {
                        this.$refs.jobTable.toggleRowSelection(
                            row,
                            this.selectedJobIds.includes(row.id)
                        );
                    });
                }
                else {
                    this.jobList.forEach(row => {
                        if (filteredJobIds.includes(row.id)) {
                            this.$refs.jobTable.toggleRowSelection(row, true);
                        }
                    });
                }
            });
        },
        async fetchJobListAndRestore() {
            await this.fetchJobList();
            this.$nextTick(() => {
                this.$refs.jobTableRef.restoreSelection();
            });
        }
    }
}
</script>
  
<style scoped></style>
  