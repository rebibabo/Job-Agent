<template>
    <div style="max-width: 1200px; margin: 0 auto; height: 80px">
        <el-steps :active="stepIndex" finish-status="success" align-center>
            <el-step title="解析简历信息"></el-step>
            <el-step title="爬取岗位数据"></el-step>
            <el-step title="过滤岗位"></el-step>
            <el-step title="匹配度排序"></el-step>
            <el-step title="简历投递"></el-step>
        </el-steps>

        <el-dialog title="预览简历" :visible.sync="previewDialog" width="60%" top="40px">
            <iframe v-if="previewUrl" :src="previewUrl" width="100%" height="600px" style="border:none"></iframe>
        </el-dialog>

        <br>
        <el-tabs v-model="activeTab" type="border-card" style="height: auto; min-height: 600px;">
            <!-- 简历上传 -->
            <el-tab-pane label="选择简历" name="resume">
                <div style="display: flex; gap: 40px; margin: 20px 40px;">
                    <!-- 左侧：上传简历 -->
                    <div style="flex: 1; min-width: 320px;">
                        <div style="margin-bottom: 10px;">上传简历</div>
                        <el-form :inline="true" class="demo-form-inline">
                            <el-upload class="upload-demo" drag :auto-upload="true" action="#" multiple
                                :before-upload="beforeUpload">
                                <i class="el-icon-upload"></i>
                                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                                <div class="el-upload__tip">只能上传PDF文件，且不超过4MB</div>
                            </el-upload>
                        </el-form>
                    </div>

                    <!-- 右侧：简历列表 -->
                    <div style="flex: 1.5; min-width: 400px; margin-left: -90px;">
                        <div style="margin-bottom: 10px;">简历列表</div>
                        <el-table :data="resumeList" border @selection-change="handleSelectionChange"
                            ref="resumeTable">
                            <el-table-column type="selection" width="40" />
                            <el-table-column prop="name" sortable label="简历名称" width="300" />
                            <el-table-column prop="datetime" sortable label="创建时间" width="160" />
                            <el-table-column label="操作" min-width="120">
                                <template #default="{ row }">
                                    <el-button @click="handleView(row.name)" type="primary" size="mini"
                                        style="width: 56px;">查看</el-button>
                                    <el-button @click="confirmDelete(row.name)" type="danger" size="mini"
                                        style="width: 56px;">删除</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <br>
                        <el-button type="primary" @click="handleParse" :disabled="selectedResume == null"
                            style="margin-left: 40px;" size="small">
                            选择简历
                        </el-button>
                        <br>
                        <br>
                        <el-timeline>
                            <el-timeline-item v-for="(activity, index) in activities" :key="index"
                                :timestamp="activity.timestamp"
                                :color="!startParsing ? '#C0C4CC' : activeIndex <= index ? '#409EFF' : '#67C23A'"
                                :icon="activeIndex <= index && startParsing ? 'el-icon-loading' : ''">
                                <span :style="{ color: activeIndex > index ? '#000000' : '#C0C4CC' }">
                                    {{ activity.content }}
                                </span>
                            </el-timeline-item>
                        </el-timeline>

                    </div>
                </div>


                <div v-if="finish" style="display: flex; justify-content: center; margin-top: 20px;">
                    <el-button type="primary" @click="handleNext" style="margin-left: 40px;" size="small">下一步</el-button>
                </div>
            </el-tab-pane>

            <!-- 爬取数据 -->
            <el-tab-pane label="获取岗位数据" name="crawl">
                <!-- 抽屉 -->
                <el-drawer title="查询规则" size="50%" :visible.sync="filterDrawerVisible" direction="rtl" destroy-on-close>
                    <div style="margin-left: 20px;">
                        <SearchFilter v-model="filters" @submit="onSubmit" @reset="onReset" />
                    </div>
                </el-drawer>

                <el-form label-width="0" inline style="margin-bottom: -18px;">
                    <el-form-item>
                        <el-button type="primary" @click="filterDrawerVisible = true" size="small">查询规则</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="() => startJob(true)" :loading="crawlLoading"
                            size="small">开始任务</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="danger" @click="() => stopJob(1)" size="small">停止任务</el-button>
                    </el-form-item>

                </el-form>

                <el-progress :percentage="crawlProgress" :status="crawlStatus" />
                <br>

                <JobTable :jobList="jobList" :filters="filters" :currentPage="currentPage" :pageSize="pageSize"
                    :totalNumber="totalNumber" :maxHeight="600" @update:currentPage="currentPage = $event" :heightRatio="0.5"
                    @update:pageSize="pageSize = $event" @pagination-change="fetchJobListAndRestore" ref="jobTableCrawl" />

                <div v-if="timer === null && jobList.length !== 0"
                    style="display: flex; justify-content: center; margin-top: 10px;">
                    <el-button type="primary" @click="handleNext" style="margin-left: 40px;" size="small">下一步</el-button>
                </div>

            </el-tab-pane>

            <!-- 过滤岗位 -->
            <el-tab-pane label="过滤岗位" name="filter">

                <el-form :model="filterForm" :inline="true" class="demo-form-inline">
                    <el-form-item label-width="110px">
                        <template #label>
                            批处理大小
                            <el-tooltip class="item" effect="dark" content="每次处理的岗位数量，越大处理速度越快，但可能会影响准确性。" placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-slider v-model="filterForm.batchSize" style="width: 100px;" :step="10"
                            :format-tooltip="formatBatchSize"></el-slider>
                    </el-form-item>

                    <el-form-item label-width="70px">
                        <template #label>
                            温度
                            <el-tooltip class="item" effect="dark" content="温度用于控制生成的随机性，值越大回答越发散，越小则更确定。" placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-slider v-model="filterForm.temperature" style="width: 100px;" :step="5"
                            :format-tooltip="formatTemperature" />
                    </el-form-item>

                    <el-form-item label="选择模型" label-width="80px">
                        <el-select v-model="filterForm.model" placeholder="请选择模型" style="width: 130px;" size="small">
                            <el-option v-for="item in models" :key="item" :label="item" :value="item">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label-width="100px">
                        <template #label>
                            过滤规则
                            <el-tooltip class="item" effect="dark" content="筛选掉不符合过滤要求的职位，包括实习/全职、学历要求、岗位要求、公司要求、地点要求等。"
                                placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-input v-model="filterForm.filterQuery" placeholder="请输入过滤规则" style="width: 380px;"
                            size="small" />
                    </el-form-item>

                </el-form>

                <el-form label-width="0" inline class="demo-form-inline">
                    <el-form-item>
                        <el-button type="primary" @click="handleFilter" :loading="filterLoading"
                            size="small">开始过滤</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="danger" @click="() => stopJob(2)" size="small">停止任务</el-button>
                    </el-form-item>


                </el-form>

                <el-progress :percentage="filterProgress" :status="filterStatus" />
                <br>
                <JobTable :jobList="jobList" :filters="filters" :currentPage="currentPage" :pageSize="pageSize"
                    :totalNumber="totalNumber" :maxHeight="600" @update:currentPage="currentPage = $event"
                    @update:pageSize="pageSize = $event" @pagination-change="fetchJobListAndRestore" ref="jobTableFilter"
                    :deleteAll="false" :sentCVFrame="true" :selectedJobIds="selectedFilteredJobIds" :heightRatio="0.44"
                    @selection-change="handleJobSelectionChange" />

                <div style="display: flex; justify-content: center; margin-top: 10px;">
                    <el-button type="primary" @click="handleNext" style="margin-left: 40px;" size="small">下一步</el-button>
                </div>

            </el-tab-pane>

            <!-- 匹配度排序 -->
            <el-tab-pane label="匹配度排序" name="sort">
                <el-form :model="rankForm" :inline="true" class="demo-form-inline">
                    <el-form-item label-width="110px">
                        <template #label>
                            批处理大小
                            <el-tooltip class="item" effect="dark" content="每次处理的岗位数量，越大处理速度越快，但可能会影响准确性。" placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-slider v-model="rankForm.batchSize" style="width: 100px;" :step="10"
                            :format-tooltip="formatBatchSize" size="small"></el-slider>
                    </el-form-item>


                    <el-form-item label-width="70px">
                        <template #label>
                            温度
                            <el-tooltip class="item" effect="dark" content="温度用于控制生成的随机性，值越大回答越发散，越小则更确定。" placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-slider v-model="rankForm.temperature" style="width: 100px;" :step="5"
                            :format-tooltip="formatTemperature" size="small" />
                    </el-form-item>


                    <el-form-item label="选择模型" label-width="80px">
                        <el-select v-model="rankForm.model" placeholder="请选择模型" style="width: 130px;" size="small">
                            <el-option v-for="item in models" :key="item" :label="item" :value="item">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label-width="100px">
                        <template #label>
                            最低分数
                            <el-tooltip class="item" effect="dark" content="设置最低岗位匹配度分数的阈值" placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;"
                                    @change="handleThresholdChange" />
                            </el-tooltip>
                        </template>
                        <el-slider v-model="rankForm.minScore" style="width: 200px;" :step="10"
                            :format-tooltip="formatScore" size="small" />
                    </el-form-item>

                </el-form>

                <el-form label-width="0" inline style="margin-bottom: -19px;">
                    <el-form-item>
                        <el-button type="primary" @click="handleRank" :loading="rankLoading" size="small">开始排序</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="danger" @click="() => stopJob(3)" size="small">停止任务</el-button>
                    </el-form-item>


                </el-form>

                <el-progress :percentage="rankProgress" :status="rankStatus" />
                <br>
                <JobTable :jobList="jobList" :filters="filters" :currentPage="currentPage" :pageSize="pageSize"
                    :totalNumber="totalNumber" :maxHeight="600" @update:currentPage="currentPage = $event"
                    @update:pageSize="pageSize = $event" @pagination-change="fetchJobListAndRestore" ref="jobTableRank"
                    :deleteAll="false" :sentCVFrame="true" :selectedJobIds="selectedFilteredJobIds"
                    @selection-change="handleJobSelectionChange" :rankScore="true" :heightRatio="0.44"/>

                <div style="display: flex; justify-content: center; margin-top: 10px;">
                    <el-button type="primary" @click="handleNext" style="margin-left: 40px;" size="small">下一步</el-button>
                </div>
            </el-tab-pane>

            <!-- 简历投递 -->
            <el-tab-pane label="简历投递" name="deliver">
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

                    <el-form-item label-width="100px">
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

                <el-form inline  style="margin-top: -19px;">
                    <el-form-item>
                        <el-button type="primary" @click="startSendResume" :loading="sendLoading"
                            size="small">开始投递</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="danger" @click="() => stopJob(4)" size="small">停止投递</el-button>
                    </el-form-item>
                </el-form>

                <el-progress :percentage="sendProgress" :status="sendStatus" style="margin-top: -19px;"/>
                <br>

                <JobTable :jobList="jobList" :filters="filters" :currentPage="currentPage" :pageSize="pageSize"
                    :totalNumber="totalNumber" :maxHeight="700" @update:currentPage="currentPage = $event"
                    @update:pageSize="pageSize = $event" @pagination-change="fetchJobListAndRestore" ref="jobTableSend"
                    :deleteAll="false" :selectedJobIds="selectedFilteredJobIds" :noButton="true"
                    @selection-change="handleJobSelectionChange" @send="startSendResume" :heightRatio="0.5"/>

            </el-tab-pane>
        </el-tabs>

    </div>
</template>

<script>
import {
    uploadResumeAPI, getResumeListAPI, deleteResumeAPI, viewResumeAPI,
    getResumeContentAPI, getResumeSummaryAPI, getResumePictureAPI
} from '@/api/user'

import SearchFilter from "@/components/SearchFilter.vue";
import JobTable from "@/components/JobTable.vue";
import searchMethods from '@/utils/searchMethod.js';
import { getFiltersMD5 } from '@/utils/encrypt';
import { getFilterJobAPI, startFilterAPI, startRankAPI, sendResumeAPI } from '@/api/job';
import axios from 'axios';

const STORAGE_KEY = 'greetings-history';
const MAX_HISTORY_LENGTH = 10;

export default {
    name: "sendResume",
    components: { SearchFilter, JobTable },
    data() {
        return {
            activeTab: 'resume',
            resumeList: [],
            jobList: [],
            greetingsHistory: [],
            toBeFilteredJobList: [],
            selectedFilteredJobIds: [],
            filterDrawerVisible: false,
            filterProgress: 0,
            filterLoading: false,
            filterStatus: null,
            rankProgress: 0,
            rankLoading: false,
            rankStatus: null,
            crawlProgress: 0,
            crawlLoading: false,
            crawlStatus: null,
            sendProgress: 0,
            sendLoading: false,
            sendStatus: null,
            timer: null,
            tableTimer: null,
            previewDialog: false,
            previewUrl: "",
            filters: {},
            selectedResume: null,
            startParsing: false,
            finish: false,
            currentPage: 1,
            pageSize: 20,
            totalNumber: 0,
            scoreMap: {}, // 保存跨页score
            tabOrder: ['resume', 'crawl', 'filter', 'sort', 'deliver'],
            models: ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo', 'deepseek-r1'],
            filterForm: {
                filterQuery: "",
                batchSize: 50,
                model: 'gpt-4o-mini',
                temperature: 25
            },
            rankForm: {
                minScore: 70,
                batchSize: 50,
                model: 'gpt-4o-mini',
                temperature: 25
            },
            sendForm: {
                message: "",
                polish: true,
                model: 'gpt-4o-mini',
                temperature: 25
            },
            activities: [{
                content: '提取文本',
            }, {
                content: '提取摘要',
            }, {
                content: '生成图片',
            }],
            activeIndex: 0,
            stepIndex: 0
        };
    },
    watch: {
        'rankForm.minScore'() {
            // 滑块变化时，重新执行自动勾选逻辑
            this.selectLowScore();
        },
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
    methods: {
        ...searchMethods,
        formatBatchSize(val) {
            return val / 10 + 5;
        },
        formatTemperature(val) {
            return val / 50;
        },
        formatScore(val) {
            return val / 10;
        },
        beforeUpload(file) {
            console.log(file.type, file.size)
            const isPDF = file.type === 'application/pdf';
            const isLt4M = file.size / 1024 / 1024 < 4;

            if (!isPDF) {
                this.$message.error('只允许上传 PDF 文件');
                return false;
            }
            if (!isLt4M) {
                this.$message.error('文件大小不能超过 4MB');
                return false;
            }
            // 构造 FormData
            const formData = new FormData();
            formData.append("file", file);

            uploadResumeAPI(formData)
                .then(res => {
                    this.$message.success("上传成功");
                    console.log(res.data);
                    this.getResumeList();
                })
                .catch(err => {
                    const msg = err.response?.data?.message || '上传失败';
                    this.$message.error(msg);
                    console.error(err);
                });

            // 返回 false，阻止 el-upload 自己继续提交
            return false;
        },
        confirmDelete(name) {
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
        getResumeList() {
            getResumeListAPI()
                .then(res => {
                    this.resumeList = res.files;
                })
                .catch(err => {
                    this.$message.error(err);
                    console.error(err);
                });
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
        handleSelectionChange(selection) {
            this.finish = false;
            this.startParsing = false;
            this.stepIndex = 0;
            this.activeIndex = 0;
            if (selection.length > 1) {
                // 只允许最后一项被选中
                const lastRow = selection[selection.length - 1];

                // 清除其他选择
                this.$refs.resumeTable.clearSelection();
                this.$refs.resumeTable.toggleRowSelection(lastRow, true);

                this.selectedResume = lastRow;

            } else {
                this.selectedResume = selection[0] || null;
            }
        },
        handleThresholdChange() {
            this.rankForm.minScore = this.threshold;
            this.fetchJobListAndRestore();
        },
        handleJobSelectionChange(selection) {
            const currentPageSelectedIds = selection.map(item => item.id);
            const currentPageAllIds = this.jobList.map(item => item.id);
            let newSelected = this.selectedFilteredJobIds.filter(id => !currentPageAllIds.includes(id));
            newSelected = newSelected.concat(currentPageSelectedIds);
            this.selectedFilteredJobIds = newSelected;
        },
        getCurrentIndex() {
            return this.tabOrder.indexOf(this.activeTab);
        },
        handleNext() {
            const currentIndex = this.getCurrentIndex();
            console.log("当前索引", currentIndex)
            if (currentIndex >= 0 && currentIndex < this.tabOrder.length - 1) {
                this.activeTab = this.tabOrder[currentIndex + 1];
                this.stepIndex = currentIndex + 1;
            }
        },
        startJob(getDesc = false) {
            // 清理可能残留的定时器
            this.crawlLoading = true;
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
            this.crawlStatus = null;
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
                    this.crawlProgress = 0;
                    this.pollProgress(this.getCurrentIndex());
                    this.getJobTableTimer();
                })
                .catch((res) => {
                    if (res.status === 410) {
                        this.$message.warning('任务已启动，请勿重复启动');
                    }
                });
        },
        stopJob(index) {
            this.updateLoading(false, index);
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
                    this.crawlStatus = 'exception';
                });
        },
        async handleParse() {
            this.finish = false;
            try {
                this.startParsing = true;
                this.activeIndex = 0;

                const params = {
                    userId: this.$store.state.user.userInfo.id,
                    file: this.selectedResume.name,
                };

                // 第一步
                const res1 = await getResumeContentAPI(params);
                this.activeIndex = 1;
                this.$set(this.activities[res1.step - 1], "timestamp", res1.datetime);

                // 第二步
                const res2 = await getResumeSummaryAPI(params);
                this.activeIndex = 2;
                this.$set(this.activities[res2.step - 1], "timestamp", res2.datetime);

                // 第三步
                const res3 = await getResumePictureAPI(params);
                this.activeIndex = 3;
                this.$set(this.activities[res3.step - 1], "timestamp", res3.datetime);

                console.log("全部流程完成");
                this.finish = true;
            } catch (err) {
                console.error("执行出错", err);
                this.startParsing = false;
            }
        },
        handleFilter() {
            if (this.filterForm.filterQuery.trim() === "") {
                this.$message.warning("请输入过滤规则");
                return;
            }

            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
            this.filterLoading = true;
            this.filterStatus = null;
            var params = { userId: this.$store.state.user.userInfo.id, filterHash: getFiltersMD5(this.filters) };

            this.selectedFilteredJobIds = []

            this.jobList.forEach(job => {
                this.$refs.jobTableFilter.toggleRowSelection(job, false);
            });
            getFilterJobAPI(params).then(res => {
                params = {
                    "userId": this.$store.state.user.userInfo.id,
                    "jobs": res.data,
                    "filterQuery": this.filterForm.filterQuery,
                    "batchSize": this.formatBatchSize(this.filterForm.batchSize),
                    "model": this.filterForm.model,
                    "temperature": this.formatTemperature(this.filterForm.temperature),
                }
                console.log(params);
                this.filterProgress = 0;
                this.pollProgress(this.getCurrentIndex());
                startFilterAPI(params).then(res => {
                    console.log("开始过滤", res);
                }).catch(err => {
                    if (err.status === 410) {
                        this.$message.warning('任务已启动，请勿重复启动');
                    }
                    else {
                        console.error("过滤出错", err);
                    }
                });

            }).catch(err => {
                console.error("过滤出错", err);
            });

        },
        handleRank() {
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
            if (this.selectedResume === null) {
                this.$message.warning("请先选择简历");
                return;
            }
            this.rankLoading = true;
            this.rankStatus = null;

            this.selectedFilteredJobIds = []

            this.jobList.forEach(job => {
                this.$refs.jobTableRank.toggleRowSelection(job, false);
            });
            var params = { userId: this.$store.state.user.userInfo.id, filterHash: getFiltersMD5(this.filters) };

            getFilterJobAPI(params).then(res => {
                this.filterProgress = 0;
                this.pollProgress(this.getCurrentIndex());

                const params = {
                    "userId": this.$store.state.user.userInfo.id,
                    "jobs": res.data,
                    "minScore": this.formatScore(this.rankForm.minScore),
                    "batchSize": this.formatBatchSize(this.rankForm.batchSize),
                    "model": this.rankForm.model,
                    "temperature": this.formatTemperature(this.rankForm.temperature),
                    "resumeName": this.selectedResume.name,
                }
                startRankAPI(params).then(res => {
                    console.log("开始排序", res);
                }).catch(err => {
                    if (err.status === 410) {
                        this.$message.warning('任务已启动，请勿重复启动');
                    }
                    else {
                        console.error("排序出错", err);
                    }
                });
            }).catch(err => {
                console.error("过滤出错", err);
            });
        },
        updateProgress(progress, index) {
            if (index === 1) { // crawl
                this.crawlProgress = progress
            }
            if (index === 2) { // filter
                this.filterProgress = progress
            }
            if (index === 3) { // rank
                this.rankProgress = progress
            }
            if (index === 4) { // send
                this.sendProgress = progress
            }
        },
        updateStatus(status, index) {
            if (index === 1) { // crawl
                this.crawlStatus = status
            }
            if (index === 2) { // filter
                this.filterStatus = status
            }
            if (index === 3) { // rank
                this.rankStatus = status
            }
            if (index === 4) { // send
                this.sendStatus = status
            }
        },
        updateLoading(loading, index) {
            if (index === 1) { // crawl
                this.crawlLoading = loading
            }
            if (index === 2) { // filter
                this.filterLoading = loading
            }
            if (index === 3) { // rank
                this.rankLoading = loading
            }
            if (index === 4) { // send
                this.sendLoading = loading
            }
        },
        pollProgress(index) {
            // 定时向后端获取进度
            this.timer = setInterval(() => {
                axios.get('/crawl/progress')
                    .then(response => {
                        this.updateProgress(response.data.percentage, index);
                        this.toBeFilteredJobList = response.data.results
                        console.log(response.data.results);
                        if (response.data.percentage < 0) {
                            this.$message.error(response.data.error);
                            clearInterval(this.timer);
                            clearInterval(this.tableTimer);
                        }
                        else if (response.data.percentage >= 100) {
                            this.updateStatus('success', index);
                            this.updateLoading(false, index);
                            clearInterval(this.timer);
                            clearInterval(this.tableTimer);
                            if (this.getCurrentIndex() === 1)
                                this.fetchJobList();
                        }

                        // 过滤 tab
                        if (this.getCurrentIndex() === 2) {
                            this.selectedFilteredJobIds = response.data.results.map(item => item.id)
                            this.$refs.jobTableFilter.selectedJobIds = [...this.selectedFilteredJobIds]
                            this.$nextTick(() => {
                                this.toBeFilteredJobList.forEach(filteredJob => {

                                    const matched = this.jobList.find(j => j.id === filteredJob.id);
                                    if (matched) {
                                        console.log("选中过滤", filteredJob.id);
                                        this.$refs.jobTableFilter.toggleRowSelection(matched, true);
                                    }
                                });
                            });
                        }

                        // 匹配度排序 tab
                        if (this.getCurrentIndex() === 3) {
                            response.data.results.forEach(sortedJob => {
                                this.scoreMap[sortedJob.id] = sortedJob.score;
                            });
                            this.$nextTick(() => {
                                this.fetchJobListAndRestore();
                                this.selectLowScore();
                            });
                        }

                        // 投递简历tab
                        if (this.getCurrentIndex() === 4) {
                            this.fetchJobList();
                        }
                    })
                    .catch((err) => {
                        this.updateLoading(false, index);
                        this.$message.error(err.message || '获取进度失败');
                        this.updateStatus('exception', index);
                        clearInterval(this.timer);
                    });
            }, 1000); // 每1秒轮询一次
        },
        selectLowScore() {
            // 先取消所有勾选，再重新勾选符合条件的
            this.jobList.forEach(job => {
                this.$refs.jobTableRank.toggleRowSelection(job, false);
            });
            this.selectedFilteredJobIds = [];

            this.jobList.forEach(job => {
                const score = this.scoreMap[job.id];
                if (
                    score != null &&
                    score < this.formatScore(this.rankForm.minScore)
                ) {
                    this.$refs.jobTableRank.toggleRowSelection(job, true);
                    this.selectedFilteredJobIds.push(job.id);
                }
            });
        },
        fetchJobListAndRestore() {
            this.fetchJobList().then(() => {
                this.$nextTick(() => {
                    if (this.getCurrentIndex() === 2) {
                        this.$refs.jobTableFilter.restoreSelection(this.selectedFilteredJobIds);
                    }
                    if (this.getCurrentIndex() === 3) {
                        this.$refs.jobTableRank.restoreSelection(this.selectedFilteredJobIds);
                    }
                    // 恢复分数
                    this.jobList.forEach(job => {
                        if (this.scoreMap[job.id] != null) {
                            console.log(this.scoreMap);
                            this.$set(job, 'score', this.scoreMap[job.id]);
                        }
                    });

                })
            });
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
            if (this.$refs.jobTableSend.selectedJobs.length === 0) {
                this.$message.warning("请先选择职位");
                return;
            }
            this.sendStatus = null;
            this.sendProgress = 0;
            this.sendLoading = true;
            const params = {
                "userId": this.$store.state.user.userInfo.id,
                "jobs": this.$refs.jobTableSend.selectedJobs,
                "message": this.sendForm.message,
                "resumeName": this.selectedResume.name,
                "polish": this.sendForm.polish,
                "model": this.sendForm.model,
                "temperature": this.formatTemperature(this.sendForm.temperature),
            }
            console.log(params)
            this.pollProgress(this.getCurrentIndex());
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
        this.getResumeList();
        this.loadHistory();
    },
    beforeDestroy() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
}

</script>

<style scoped>
.demo-form-inline ::v-deep(.el-form-item) {
    margin-bottom: 3px;
    /* 默认是 18px 左右，改小一点 */
}
</style>
  