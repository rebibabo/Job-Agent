<template>
    <div>
        <el-table :data="jobList" stripe border :max-height="maxHeight" style="width: 100%" ref="jobTable"
            @selection-change="handleSelectionChange" :row-key="row => row.id">
            <el-table-column type="selection" width="40"></el-table-column>
            <el-table-column prop="jobName" sortable label="工作名称" :width="jobNameWidth">
                <template #default="{ row }">
                    <el-tooltip effect="dark" placement="top" :content="`
                            ${row.skills || '无'}
                    `">
                        <span>{{ row.jobName }}</span>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column prop="city" sortable label="城市" width="90px">
                <template #default="{ row }">
                    <el-tooltip effect="dark" placement="top" :content="`
                            ${row.region || '无'}
                    `">
                        <span>{{ row.city }}</span>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column prop="title" sortable label="工作岗位" width="120">
                <template #default="{ row }">
                    <el-tooltip effect="dark" placement="top" :content="`
                            经验要求：${row.experience || '无'} |
                            学历要求：${row.degree || '无'}
                    `">
                        <span>{{ row.title }}</span>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column prop="companyName" sortable label="公司名称" width="200">
                <template #default="{ row }">
                    <el-tooltip effect="dark" placement="top" :content="`
                            行业：${row.industry || '无'} |
                            规模：${row.scale || '无'} |
                            融资：${row.stage || '无'} 
                    `">
                        <span>{{ row.companyName }}</span>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column prop="salary" sortable label="薪资" width="140" />
            <el-table-column prop="score" sortable label="分数" width="80" v-if="rankScore" />
            <el-table-column label="操作" min-width="180">
                <template #default="{ row }">
                    <el-button @click="viewJob(row)" :type="row.sentCv ? 'success' : row.viewed ? 'info' : 'primary'"
                        size="mini" style="width: 70px;">
                        {{ row.sentCv ? '已投递' : row.viewed ? '已查看' : '查看' }}
                    </el-button>
                    <el-button @click="confirmDelete([row.id])" type="danger" size="mini"
                        style="width: 70px;">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <div style="display: flex; align-items: center; margin: 20px 0;">
            <el-button type="primary" @click="sendResume" :disabled="!selectedJobs.length" size="small"
                v-if="!sentCVFrame && !noButton">
                投递简历
            </el-button>
            <el-button type="danger" @click="confirmDeleteSelected" :disabled="!selectedJobs.length" size="small"
                v-if="!sentCVFrame && !noButton">
                删除所选
            </el-button>
            <el-button type="danger" @click="confirmaDeleteFilteredJob" size="small" v-if="sentCVFrame && !noButton">
                删除所有待过滤岗位
            </el-button>
            <el-button type="danger" @click="confirmDeleteAll" size="small" v-if="deleteAll && !noButton">
                删除全部
            </el-button>
        </div>

        <div style="flex: 1; display: flex; justify-content: center;">
            <el-pagination @size-change="onSizeChange" @current-change="onCurrentChange" :current-page="currentPage"
                :page-sizes="[20, 40, 60, 80, 100]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper"
                :total="totalNumber" />
        </div>

        <el-dialog title="投递简历" :visible.sync="sendResumeDialogVisible" :before-close="handleBeforeClose">
            <div> 选择简历 </div>
            <br>
            <el-table :data="resumeList" border style="width: 100%;" @selection-change="handleResumeSelectionChange"
                ref="resumeTable">
                <el-table-column type="selection" width="55">
                </el-table-column>
                <el-table-column prop="name" sortable label="简历名称" width="400" />
                <el-table-column prop="datetime" sortable label="创建时间" width="300" />
                <el-table-column label="操作" min-width="160">
                    <template #default="{ row }">
                        <el-button @click="handleView(row.name)" type="primary" size="mini"
                            style="width: 60px;">查看</el-button>
                        <el-button @click="confirmDelete(row.name)" type="danger" size="mini"
                            style="width: 60px;">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <br>

            <el-form inline label-width="80px" :model="sendForm">
                <el-form-item>
                    <template #label>
                        问候语
                        <el-tooltip class="item" effect="dark" content="发送给Boss的问候语，如：“hr您好，我是xxx，于xx年毕业于xxx学校...”"
                            placement="top">
                            <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                        </el-tooltip>
                    </template>
                    <el-input v-model="sendForm.message" placeholder="请输入问候语" style="width: 400px;" />
                </el-form-item>

                <el-form-item>
                    <template #label>
                        润色
                        <el-tooltip class="item" effect="dark" content="系统将根据各个岗位描述对问候语进行优化，提升Boss回复率。" placement="top">
                            <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                        </el-tooltip>
                    </template>
                    <el-switch v-model="sendForm.polish" />

                </el-form-item>
            </el-form>

            <el-form inline label-width="80px" :model="sendForm">
                <el-form-item label="选择模型">
                    <el-select v-model="sendForm.model" placeholder="请选择模型">
                        <el-option v-for="item in models" :key="item" :label="item" :value="item">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label-width="120px">
                    <template #label>
                        温度
                        <el-tooltip class="item" effect="dark" content="温度用于控制生成的随机性，值越大回答越发散，越小则更确定。" placement="top">
                            <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                        </el-tooltip>
                    </template>
                    <el-slider v-model="sendForm.temperature" style="width: 300px;" :step="5"
                        :format-tooltip="formatTemperature" />
                </el-form-item>
            </el-form>

            <el-form inline>
                <el-form-item>
                    <el-button type="primary" @click="startSendResume" :loading="sendLoading">开始投递</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="danger" @click="() => stopJob(4)">停止投递</el-button>
                </el-form-item>
            </el-form>

            <el-progress :percentage="sendProgress" :status="sendStatus" />
        </el-dialog>
    </div>
</template>
  
<script>
import { nextTick } from 'vue'
import { setViewStatusAPI, deleteAPI, deleteALLAPI, deleteALLFilteredAPI } from '@/api/job'
import { getFiltersMD5 } from '@/utils/encrypt'
import { getResumeListAPI } from '@/api/user'
import { sendResumeAPI } from '@/api/job'
import axios from 'axios'

export default {
    name: 'JobTable',
    props: {
        jobList: { type: Array, required: true },
        filters: { type: Object, required: false },
        currentPage: { type: Number, required: true },
        pageSize: { type: Number, required: true },
        totalNumber: { type: Number, required: true },
        deleteAll: { type: Boolean, default: true },
        sentCVFrame: { type: Boolean, default: false },
        rankScore: { type: Boolean, default: false },
        noButton: { type: Boolean, default: false }
    },
    computed: {
        jobNameWidth() {
            return 250 + (this.rankScore ? 0 : 70);
        }
    },
    emits: ['view', 'delete', 'send', 'update:currentPage', 'update:pageSize', 'pagination-change'],
    data() {
        return {
            selectedJobs: [],
            selectedJobIds: [], // 用于跨页记忆
            resumeList: [],
            sendResumeDialogVisible: false,
            sendProgress: 0,
            sendLoading: false,
            sendStatus: null,
            selectedResume: null,
            maxHeight: window.innerHeight * 0.6,
            timer: null,
            models: ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo', 'deepseek-r1'],
            sendForm: {
                message: "",
                polish: true,
                model: 'gpt-4o-mini',
                temperature: 25
            },
        }
    },
    methods: {
        updateTableHeight() {
            this.maxHeight = window.innerHeight * 0.6;
        },
        formatTemperature(val) {
            return val / 50;
        },
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
            this.sendResumeDialogVisible = true
        },
        pollProgress() {
            // 定时向后端获取进度
            this.timer = setInterval(() => {
                axios.get('/crawl/progress')
                    .then(response => {
                        this.sendProgress = response.data.percentage;
                        if (this.sendProgress < 0) {
                            this.$message.error(response.data.error);
                            clearInterval(this.timer);
                        }
                        else if (this.sendProgress >= 100) {
                            this.sendLoading = false;
                            this.sendStatus = 'success';
                            clearInterval(this.timer);
                            this.$emit('pagination-change')
                        }
                    })
                    .catch((err) => {
                        this.$message.error(err.message || '获取进度失败');
                        this.sendStatus = 'exception';
                        clearInterval(this.timer);
                    });
            }, 1000); // 每1秒轮询一次
        },
        startSendResume() {
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
            if (this.sendForm.message === "") {
                this.$message.warning("请先输入问候语");
                return;
            }
            if (this.selectedResume === null) {
                this.$message.warning("请先选择简历");
                return;
            }
            if (this.selectedJobs.length === 0) {
                this.$message.warning("请先选择职位");
                return;
            }
            this.sendStatus = null;
            this.sendProgress = 0;
            this.sendLoading = true;
            const params = {
                "userId": this.$store.state.user.userInfo.id,
                "jobs": this.selectedJobs,
                "message": this.sendForm.message,
                "resumeName": this.selectedResume.name,
                "polish": this.sendForm.polish,
                "model": this.sendForm.model,
                "temperature": this.formatTemperature(this.sendForm.temperature),
            }
            console.log(params)
            this.pollProgress();
            sendResumeAPI(params)
                .then(res => {
                    console.log("开始发送简历", res);
                })
                .catch(err => {
                    if (err.status === 410) {
                        this.$message.warning('任务已启动，请勿重复启动');
                    }
                    else {
                        console.error("发送简历出错", err);
                    }
                });
        },
        handleBeforeClose(done) {
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
            done();
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
        handleResumeSelectionChange(selection) {
            if (selection.length > 1) {
                const lastRow = selection[selection.length - 1];

                // 清除其他选择
                this.$refs.resumeTable.clearSelection();
                this.$refs.resumeTable.toggleRowSelection(lastRow, true);

                this.selectedResume = lastRow;

            } else {
                this.selectedResume = selection[0] || null;
            }
        },
        async fetchJobListAndRestore() {
            await this.fetchJobList();
            this.$nextTick(() => {
                this.$refs.jobTableRef.restoreSelection();
            });
        }
    },
    mounted() {
        getResumeListAPI()
            .then(res => {
                this.resumeList = res.files;
            })
            .catch(err => {
                this.$message.error(err);
                console.error(err);
            });
        window.addEventListener('resize', this.updateTableHeight);
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.updateTableHeight);
    },
}
</script>
  
<style scoped></style>
  