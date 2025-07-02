<template>
    <div>
        <el-table :data="jobList" stripe border :max-height="maxHeight" style="width: 100%" ref="jobTable"
            @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="40"></el-table-column>
            <el-table-column prop="jobName" sortable label="工作名称" width="300" />
            <el-table-column prop="companyName" sortable label="公司名称" width="280" />
            <el-table-column prop="salary" sortable label="薪资" width="180" />
            <el-table-column prop="city" sortable label="工作城市" width="150" />
            <el-table-column prop="region" sortable label="城市区域" width="150" />
            <el-table-column prop="experience" sortable label="经验要求" width="150" />
            <el-table-column prop="degree" sortable label="学历要求" width="140" />
            <el-table-column prop="industry" sortable label="公司行业" width="180" />
            <el-table-column prop="title" sortable label="工作岗位" width="180" />
            <el-table-column prop="scale" sortable label="公司规模" width="150" />
            <el-table-column prop="stage" sortable label="融资阶段" width="150" />
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
            <el-button type="primary" @click="sendResume" :disabled="!selectedJobs.length" size="medium">
                投递简历
            </el-button>
            <el-button type="danger" @click="confirmDeleteSelected" :disabled="!selectedJobs.length" size="medium">
                删除所选
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
import { setViewStatusAPI, deleteAPI } from '@/api/job'

export default {
    name: 'JobTable',
    props: {
        jobList: { type: Array, required: true },
        currentPage: { type: Number, required: true },
        pageSize: { type: Number, required: true },
        totalNumber: { type: Number, required: true },
        maxHeight: { type: [Number, String], default: 850 }
    },
    emits: ['view', 'delete', 'send', 'update:currentPage', 'update:pageSize', 'pagination-change'],
    data() {
        return {
            selectedJobs: []
        }
    },
    methods: {
        handleSelectionChange(selection) {
            this.selectedJobs = selection
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
                    deleteAPI({ user_id: String(this.$store.state.user.userInfo.id), job_ids: ids })
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
    }
}
</script>
  
<style scoped></style>
  