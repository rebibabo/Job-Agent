<template>
    <div>
        <!-- 岗位表格 -->
        <el-table :data="jobList" stripe border :height="height" style="width: 100%" ref="jobTable"
            @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="40"></el-table-column>
            <el-table-column prop="jobName" sortable label="工作名称" :width="jobNameWidth">
                <template #default="{ row }">
                    <el-tooltip effect="dark" placement="top" :content="`
                            技能需求：${row.skills || '无'}
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
                    <el-tooltip effect="dark" placement="top">
                        <template #content>
                            <div>
                                经验要求：{{ row.experience || '无' }}<br />
                                学历要求：{{ row.degree || '无' }}
                            </div>
                        </template>
                        <span>{{ row.title }}</span>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column prop="companyName" sortable label="公司名称" width="200">
                <template #default="{ row }">
                    <el-tooltip effect="dark" placement="top">
                        <template #content>
                            <div>
                                行业：{{ row.industry || '无' }}<br />
                                规模：{{ row.scale || '无' }}<br />
                                融资：{{ row.stage || '无' }}
                            </div>
                        </template>
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

        <!-- 岗位下方按钮 -->
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

        <!-- 岗位分页 -->
        <div
            :style="{ width: '80%', display: 'flex', justifyContent: 'center', marginTop: buttonTopMargin + 'px', marginLeft: '150px' }">
            <el-pagination @size-change="onSizeChange" @current-change="onCurrentChange" :current-page="currentPage"
                :page-sizes="[20, 40, 60, 80, 100]" :page-size="pageSize" layout="sizes, total, prev, pager, next, jumper"
                :total="totalNumber" />
        </div>

        <!-- 投递简历弹窗界面 -->
        <el-dialog title="投递简历" :visible.sync="sendResumeDialogVisible" :before-close="handleBeforeClose" width="65%">
            <el-table :data="resumeList" border style="width: 100%;" @selection-change="handleResumeSelectionChange"
                ref="resumeTable">
                <el-table-column type="selection" width="55">
                </el-table-column>
                <el-table-column prop="name" sortable label="简历名称" width="320" />
                <el-table-column prop="datetime" sortable label="创建时间" width="270" />
                <el-table-column label="操作" min-width="120">
                    <template #default="{ row }">
                        <el-button @click="handleView(row.name)" type="primary" size="mini"
                            style="width: 60px;">查看</el-button>
                        <el-button @click="confirmDeleteResume(row.name)" type="danger" size="mini"
                            style="width: 60px;">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <br>

            <el-form inline label-width="80px" :model="sendForm">
                <el-form-item label="选择模型" label-width="80px">
                    <el-select v-model="sendForm.model" placeholder="请选择模型" style="width: 130px;" size="small">
                        <el-option v-for="item in models" :key="item" :label="item" :value="item">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label-width="100px">
                    <template #label>
                        温度
                        <el-tooltip class="item" effect="dark" content="温度用于控制生成的随机性，值越大回答越发散，越小则更确定。" placement="top">
                            <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                        </el-tooltip>
                    </template>
                    <el-slider v-model="sendForm.temperature" style="width: 100px;" :step="5"
                        :format-tooltip="formatTemperature" />
                </el-form-item>

                <el-form-item>
                    <template #label>
                        问候语
                        <el-tooltip class="item" effect="dark" content="发送给Boss的问候语，如：“hr您好，我是xxx，于xx年毕业于xxx学校...”"
                            placement="top">
                            <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                        </el-tooltip>
                    </template>
                    <el-select v-model="sendForm.message" placeholder="请输入或选择问候语" filterable allow-create
                        default-first-option style="width: 300px" size="small">
                        <el-option v-for="(item, index) in greetingsHistory" :key="item" :label="item" :value="item">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span>{{ item }}</span>
                                <el-button type="text" icon="el-icon-close" size="mini"
                                    @click.stop="removeGreeting(index)" />
                            </div>
                        </el-option>
                    </el-select>
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

            <el-form inline>
                <el-form-item>
                    <el-button type="primary" @click="startSendResume" :loading="sendLoading" size="small">开始投递</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="danger" @click="stopJob" size="small">停止投递</el-button>
                </el-form-item>
            </el-form>

            <el-progress :percentage="sendProgress" :status="sendStatus" />
        </el-dialog>

        <!-- 预览简历弹窗界面 -->
        <el-dialog title="预览简历" :visible.sync="previewDialog" width="60%" top="40px">
            <iframe v-if="previewUrl" :src="previewUrl" width="100%" height="600px" style="border:none"></iframe>
        </el-dialog>
    </div>
</template>
  
<script>
import { nextTick } from 'vue'
import { setViewStatusAPI, deleteAPI, deleteALLAPI, deleteALLFilteredAPI } from '@/api/job'
import { getFiltersMD5 } from '@/utils/encrypt'
import { getResumeListAPI, deleteResumeAPI, viewResumeAPI } from '@/api/user'
import { sendResumeAPI } from '@/api/job'
import axios from 'axios'

const STORAGE_KEY = 'greetings-history';
const MAX_HISTORY_LENGTH = 10;      // 问候语历史记录最大长度

export default {
    name: 'JobTable',
    props: {
        jobList: { type: Array, required: true },       // 岗位分页列表
        filters: { type: Object, required: false },     // 过滤规则
        currentPage: { type: Number, required: true },  // 当前页
        pageSize: { type: Number, required: true },     // 每页条数
        totalNumber: { type: Number, required: true },  // 总条数
        deleteAll: { type: Boolean, default: true },    // 是否显示删除全部按钮
        sentCVFrame: { type: Boolean, default: false }, // 是否在智能投递简历页面
        rankScore: { type: Boolean, default: false },   // 是否新增分数列
        noButton: { type: Boolean, default: false },    // 是否隐藏按钮
        heightRatio: { type: Number, default: 0.6 },    // 表格高度占比
    },
    computed: {
        jobNameWidth() {    // 用来调整表格宽度
            return 250 + (this.rankScore ? 0 : 70);
        },
        buttonTopMargin() { // 用来调整按钮距离表格下方的间距
            return this.noButton ? -25 : -50;
        }
    },
    emits: ['view', 'delete', 'send', 'update:currentPage', 'update:pageSize', 'pagination-change'],
    data() {
        return {
            selectedJobs: [],   // 存放当前页选中的岗位信息
            selectedJobIds: [], // 用于跨页记忆，存放选中的岗位id
            resumeList: [],     // 简历列表
            greetingsHistory: [],       // 问候语历史记录
            sendResumeDialogVisible: false,
            stopFlag: false,
            sendProgress: 0,
            sendLoading: false,
            sendStatus: null,
            previewDialog: false,
            previewUrl: "",
            selectedResume: null,   // 选中的简历
            height: window.innerHeight * this.heightRatio,      // 表格高度
            timer: null,        // 定时器，用来轮循投递简历进度
            models: ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo', 'deepseek-r1'],
            sendForm: {     // 发送简历的表单信息
                message: "",
                polish: true,
                model: 'gpt-4o-mini',
                temperature: 25
            },
        }
    },
    methods: {
        updateTableHeight() {
            this.height = window.innerHeight * this.heightRatio;
        },
        formatTemperature(val) {
            return val / 50;
        },
        toggleRowSelection(row, selected) {
            // 必须要外显这个函数，否则父组件无法选中表格内的行
            this.$refs.jobTable.toggleRowSelection(row, selected);
        },
        handleSelectionChange(selection) {
            // 当前页原始选中的ID
            const originalSelectedIds = this.selectedJobs.map(item => item.id);
            // 当前页所有数据的ID
            const currentPageIds = this.jobList.map(item => item.id);
            // 更新当前页选中的岗位信息
            this.selectedJobs = selection
            // 当前页目前选中的ID
            const selectedIds = selection.map(item => item.id);
            // 新增的选中项
            const newId = selectedIds.filter(id => !originalSelectedIds.includes(id));
            // 移除的选中项
            const removeId = originalSelectedIds.filter(id => !selectedIds.includes(id));
            // 合并新的选中项
            this.selectedJobIds = [
               ...new Set([
                   ...this.selectedJobIds,
                   ...newId
                ])
            ];
            // console.log("当前页原始选中ID", originalSelectedIds)
            // console.log("当前页所有数据ID", currentPageIds)
            // console.log("当前页选中ID", selectedIds)
            // console.log("新增选中项", newId)
            // console.log("移除选中项", removeId)
            // 从跨页选中的所有ID中删除当前页所有的反选的ID
            this.selectedJobIds = this.selectedJobIds.filter(id => !removeId.includes(id) || !currentPageIds.includes(id));
            this.$emit('selection-change', selection)
            // console.log("新的跨页选中ID", this.selectedJobIds)
        },
        scrollUp() {
            // 当换页的时候，滚动条回到顶部
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
            // 根据jobId删除选中的岗位
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
            // 删除所有页的岗位
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
            // 删除所有页被选中的岗位，但只删除user_job中的元素，不删除job表中的数据
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
        confirmDeleteResume(name) {
            this.$confirm('确认删除所选简历？' + name)
                .then(() => {
                    deleteResumeAPI(name)
                        .then(res => {
                            this.$message.success("删除成功");
                            console.log(res.data);
                            this.getResumeList();
                        })
                        .catch(err => {
                            const msg = err.response?.data?.message || '删除失败';
                            this.$message.error(msg);
                            console.error(err);
                        });
                })
                .catch(() => {
                    this.$message.info('已取消删除')
                })

        },
        handleView(name) {
            this.previewUrl = "";
            viewResumeAPI(name)
                .then(res => {
                    this.previewUrl = res.url;
                    this.previewDialog = true;
                })
                .catch(err => {
                    this.$message.error("加载预览地址失败," + err.message);
                })
        },

        pollProgress() {
            // 采用递归的方式轮循1s中获取后端进度
            const poll = () => {
                if (this.stopFlag) {
                    this.stopFlag = false;
                    return;
                }
                axios.get('/crawl/progress')
                    .then(response => {
                        this.sendProgress = response.data.percentage;

                        if (this.sendProgress < 0) {
                            this.$message.error(response.data.error);
                            this.sendStatus = 'exception';
                            return;
                        }

                        if (this.sendProgress >= 100) {
                            this.sendLoading = false;
                            this.sendStatus = 'success';
                            this.$emit('pagination-change');
                            return;
                        }

                        // 继续下一轮轮询
                        setTimeout(poll, 1000);
                    })
                    .catch((err) => {
                        this.$message.error(err.message || '获取进度失败');
                        this.sendStatus = 'exception';
                    });
            };

            poll(); // 启动轮询
        },
        startSendResume() {
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
        stopJob() {
            this.stopFlag = true;
            this.sendLoading = false;
            if (this.tableTimer) {
                clearInterval(this.tableTimer);
                this.tableTimer = null;
            }
            axios.get('/crawl/stop')
                .then(() => {
                    this.sendStatus = 'exception';
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
                // 如果参数为空，则根据this.selectedJobIds恢复选中状态
                if (filteredJobIds.length === 0) {
                    this.jobList.forEach(row => {
                        if (this.selectedJobIds.includes(row.id)) {
                            this.$refs.jobTable.toggleRowSelection(row, true);
                        }
                    });
                }
                // 否则，根据传入参数恢复选中状态
                else {
                    this.selectedJobIds = filteredJobIds;
                    this.jobList.forEach(row => {
                        if (filteredJobIds.includes(row.id)) {
                            this.$refs.jobTable.toggleRowSelection(row, true);
                        }
                    });
                }
            });
        },
        handleResumeSelectionChange(selection) {
            // 只选择一个简历
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
            // 获取JobList的同时，从selectedJobIds中恢复选中状态
            await this.fetchJobList();
            this.$nextTick(() => {
                this.$refs.jobTableRef.restoreSelection();
            });
        },
        removeGreeting(index) {
            this.greetingsHistory.splice(index, 1);
            this.saveHistory();
        },
        saveHistory() {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(this.greetingsHistory));
        },
        loadHistory() {
            const saved = localStorage.getItem(STORAGE_KEY);
            if (saved) {
                this.greetingsHistory = JSON.parse(saved);
            }
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
        this.loadHistory();     // 加载问候语历史记录
    },
    watch: {
        'sendForm.message'(newVal) {
            if (
                newVal &&
                !this.greetingsHistory.includes(newVal)
            ) {
                this.greetingsHistory.unshift(newVal); // 新的加到最前面
                if (this.greetingsHistory.length > MAX_HISTORY_LENGTH) {
                    this.greetingsHistory.pop(); // 移除最旧的
                }
                this.saveHistory();
            }
        }
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.updateTableHeight);
    },
}
</script>