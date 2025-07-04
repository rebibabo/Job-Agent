<template>
    <div>
        <el-steps :active="stepIndex" finish-status="success" align-center>
            <el-step title="步骤 1" description="解析简历信息"></el-step>
            <el-step title="步骤 2" description="爬取岗位数据"></el-step>
            <el-step title="步骤 3" description="过滤岗位"></el-step>
            <el-step title="步骤 4" description="匹配度排序"></el-step>
            <el-step title="步骤 5" description="简历投递"></el-step>
        </el-steps>

        <el-dialog title="预览简历" :visible.sync="previewDialog" width="60%" top="50px">
            <iframe v-if="previewUrl" :src="previewUrl" width="100%" height="1000px" style="border:none"></iframe>
        </el-dialog>

        <br>
        <el-tabs v-model="activeTab" type="border-card" style="height: 1050px;">
            <!-- 简历上传 -->
            <el-tab-pane label="选择简历" name="resume">
                <div style="margin-left: 40px;"> 上传简历 </div>
                <br>
                <el-form :inline="true" class="demo-form-inline"
                    style="display: flex; flex-wrap: wrap; gap: 20px; margin-left: 40px;">
                    <el-upload class="upload-demo" drag :auto-upload="true" action="#" multiple
                        :before-upload="beforeUpload">
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                        <div class="el-upload__tip">只能上传PDF文件，且不超过4MB</div>
                    </el-upload>
                </el-form>


                <br>
                <div style="margin-left: 40px;"> 简历列表 </div>
                <br>
                <el-table :data="resumeList" border style="width: 50%; margin-left: 40px;"
                    @selection-change="handleSelectionChange" ref="resumeTable">
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
                <el-button type="primary" @click="handleParse" :disabled="selectedResume == null"
                    style="margin-left: 40px;">
                    选择简历
                </el-button>
                <br>
                <br>
                <el-timeline>
                    <el-timeline-item v-for="(activity, index) in activities" :key="index" :timestamp="activity.timestamp"
                        :color="!startParsing ? '#C0C4CC' : activeIndex <= index ? '#409EFF' : '#67C23A'"
                        :icon="activeIndex <= index && startParsing ? 'el-icon-loading' : ''">
                        <span :style="{ color: activeIndex > index ? '#000000' : '#C0C4CC' }">
                            {{ activity.content }}
                        </span>
                    </el-timeline-item>
                </el-timeline>

                <div v-if="finish" style="display: flex; justify-content: center; margin-top: 20px;">
                    <el-button type="primary" @click="handleNext" style="margin-left: 40px;">下一步</el-button>
                </div>
            </el-tab-pane>

            <!-- 爬取数据 -->
            <el-tab-pane label="获取岗位数据" name="crawl">
                <SearchFilter v-model="filters" @submit="onSubmit" @reset="onReset" />

                <el-form label-width="0" inline>

                    <el-form-item>
                        <el-button type="primary" @click="() => startJob(true)" :loading="loading">开始任务</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="danger" @click="stopJob">停止任务</el-button>
                    </el-form-item>

                </el-form>

                <el-progress :percentage="progress" :status="status" />
                <br>

                <JobTable :jobList="jobList" :filters="filters" :currentPage="currentPage" :pageSize="pageSize"
                    :totalNumber="totalNumber" :maxHeight="600" @update:currentPage="currentPage = $event"
                    @update:pageSize="pageSize = $event" @pagination-change="fetchJobListAndRestore" ref="jobTableRef" />

                <div v-if="timer === null && jobList.length !== 0"
                    style="display: flex; justify-content: center; margin-top: 20px;">
                    <el-button type="primary" @click="handleNext" style="margin-left: 40px;">下一步</el-button>
                </div>

            </el-tab-pane>

            <!-- 过滤岗位 -->
            <el-tab-pane label="过滤岗位" name="filter">

                <el-form :model="filterForm" :inline="true">
                    <el-form-item label-width="120px">
                        <template #label>
                            批处理大小
                            <el-tooltip class="item" effect="dark" content="每次处理的岗位数量，越大处理速度越快，但可能会影响准确性。" placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-slider v-model="filterForm.batchSize" style="width: 300px;" :step="10"
                            :format-tooltip="formatBatchSize"></el-slider>
                    </el-form-item>

                    <el-form-item label-width="120px">
                        <template #label>
                            过滤规则
                            <el-tooltip class="item" effect="dark" content="筛选掉不符合过滤要求的职位，包括实习/全职、学历要求、岗位要求、公司要求、地点要求等。"
                                placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-input v-model="filterForm.filterQuery" placeholder="请输入过滤规则" style="width: 600px;" />
                    </el-form-item>


                </el-form>

                <el-form :model="filterForm" :inline="true">
                    <el-form-item label-width="120px">
                        <template #label>
                            温度
                            <el-tooltip class="item" effect="dark" content="温度用于控制生成的随机性，值越大回答越发散，越小则更确定。" placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-slider v-model="filterForm.temperature" style="width: 300px;" :step="5"
                            :format-tooltip="formatTemperature" />
                    </el-form-item>


                    <el-form-item label="选择模型" label-width="120px">
                        <el-select v-model="filterForm.model" placeholder="请选择模型"
                            style="width: 300px; margin-right: 192px;">
                            <el-option v-for="item in models" :key="item" :label="item" :value="item">
                            </el-option>
                        </el-select>
                    </el-form-item>

                </el-form>

                <el-form label-width="0" inline>
                    <el-form-item>
                        <el-button type="primary" @click="handleFilter" :loading="loading">开始过滤</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="danger" @click="stopJob">停止任务</el-button>
                    </el-form-item>


                </el-form>

                <el-progress :percentage="progress" :status="status" />
                <br>
                <JobTable :jobList="jobList" :filters="filters" :currentPage="currentPage" :pageSize="pageSize"
                    :totalNumber="totalNumber" :maxHeight="600" @update:currentPage="currentPage = $event"
                    @update:pageSize="pageSize = $event" @pagination-change="fetchJobListAndRestore" ref="jobTableRef"
                    :deleteAll="false" :sentCVFrame="true" :selectedJobIds="selectedFilteredJobIds"
                    @selection-change="handleJobSelectionChange" />

                <div style="display: flex; justify-content: center; margin-top: 20px;">
                    <el-button type="primary" @click="handleNext" style="margin-left: 40px;">下一步</el-button>
                </div>

            </el-tab-pane>
            <el-tab-pane label="匹配度排序" name="sort">
                <el-form :model="rankForm" :inline="true">
                    <el-form-item label-width="120px">
                        <template #label>
                            批处理大小
                            <el-tooltip class="item" effect="dark" content="每次处理的岗位数量，越大处理速度越快，但可能会影响准确性。" placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-slider v-model="rankForm.batchSize" style="width: 300px;" :step="10"
                            :format-tooltip="formatBatchSize"></el-slider>
                    </el-form-item>

                    <el-form-item label-width="120px">
                        <template #label>
                            最低分数
                            <el-tooltip class="item" effect="dark" content="设置最低岗位匹配度分数的阈值" placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-slider v-model="rankForm.minScore" style="width: 300px;" :step="5"
                            :format-tooltip="formatScore" />
                    </el-form-item>


                </el-form>

                <el-form :model="rankForm" :inline="true">
                    <el-form-item label-width="120px">
                        <template #label>
                            温度
                            <el-tooltip class="item" effect="dark" content="温度用于控制生成的随机性，值越大回答越发散，越小则更确定。" placement="top">
                                <i class="el-icon-question" style="margin-left: 4px; cursor: pointer;" />
                            </el-tooltip>
                        </template>
                        <el-slider v-model="rankForm.temperature" style="width: 300px;" :step="5"
                            :format-tooltip="formatTemperature" />
                    </el-form-item>


                    <el-form-item label="选择模型" label-width="120px">
                        <el-select v-model="rankForm.model" placeholder="请选择模型" style="width: 300px; margin-right: 192px;">
                            <el-option v-for="item in models" :key="item" :label="item" :value="item">
                            </el-option>
                        </el-select>
                    </el-form-item>

                </el-form>

                <el-form label-width="0" inline>
                    <el-form-item>
                        <el-button type="primary" @click="handleRank" :loading="loading">开始排序</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="danger" @click="stopJob">停止任务</el-button>
                    </el-form-item>


                </el-form>

                <el-progress :percentage="progress" :status="status" />
                <br>
                <JobTable :jobList="jobList" :filters="filters" :currentPage="currentPage" :pageSize="pageSize"
                    :totalNumber="totalNumber" :maxHeight="600" @update:currentPage="currentPage = $event"
                    @update:pageSize="pageSize = $event" @pagination-change="fetchJobListAndRestore" ref="jobTableRef"
                    :deleteAll="false" :sentCVFrame="true" :selectedJobIds="selectedFilteredJobIds"
                    @selection-change="handleJobSelectionChange" :rankScore="true" />

                <div style="display: flex; justify-content: center; margin-top: 20px;">
                    <el-button type="primary" @click="handleNext" style="margin-left: 40px;">下一步</el-button>
                </div>
            </el-tab-pane>
            <el-tab-pane label="简历投递" name="deliver">简历投递</el-tab-pane>
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
import { getFilterJobAPI, startFilterAPI, startRankAPI } from '@/api/job';
import axios from 'axios';

export default {
    name: "sendResume",
    components: { SearchFilter, JobTable },
    data() {
        return {
            loading: false,
            activeTab: 'resume',
            resumeList: [],
            jobList: [],
            toBeFilteredJobList: [],
            selectedFilteredJobIds: [],
            status: null,
            progress: 0,
            timer: null,
            tableTimer: null,
            previewDialog: false,
            previewUrl: "",
            filters: {},
            selectedResume: null,
            startParsing: false,
            finish: false,
            currentPage: 1,
            pageSize: 40,
            totalNumber: 0,
            tabOrder: ['resume', 'crawl', 'filter', 'sort', 'deliver'],
            models: ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo', 'deepseek-r1'],
            filterForm: {
                filterQuery: "",
                batchSize: 50,
                model: 'gpt-4o-mini',
                temperature: 25
            },
            rankForm: {
                minScore: 60,
                batchSize: 50,
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

                // 你可以把单选的结果存储到 data 中
                this.selectedResume = lastRow;

            } else {
                this.selectedResume = selection[0] || null;
            }
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
            this.loading = true;
            this.status = null;
            var params = { userId: this.$store.state.user.userInfo.id, filterHash: getFiltersMD5(this.filters) };

            this.selectedFilteredJobIds = []

            this.jobList.forEach(job => {
                this.$refs.jobTableRef.toggleRowSelection(job, false);
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
                this.progress = 0;
                this.pollProgress();
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
            this.loading = true;
            this.status = null;

            this.selectedFilteredJobIds = []

            this.jobList.forEach(job => {
                this.$refs.jobTableRef.toggleRowSelection(job, false);
            });
            var params = { userId: this.$store.state.user.userInfo.id, filterHash: getFiltersMD5(this.filters) };

            getFilterJobAPI(params).then(res => {
                this.progress = 0;
                this.pollProgress();

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
        pollProgress() {
            // 定时向后端获取进度
            this.timer = setInterval(() => {
                axios.get('/crawl/progress')
                    .then(response => {
                        this.progress = response.data.percentage;
                        this.toBeFilteredJobList = response.data.results
                        this.selectedFilteredJobIds = response.data.results.map(item => item.id)
                        console.log(response.data.results);
                        if (this.progress < 0) {
                            this.$message.error(response.data.error);
                            clearInterval(this.timer);
                            clearInterval(this.tableTimer);
                        }
                        else if (this.progress >= 100) {
                            this.status = 'success';
                            this.loading = false;
                            clearInterval(this.timer);
                            clearInterval(this.tableTimer);
                            if (this.getCurrentIndex() === 1)
                                this.fetchJobList();
                        }

                        // 过滤 tab
                        if (this.getCurrentIndex() === 2) {
                            this.$nextTick(() => {
                                this.toBeFilteredJobList.forEach(filteredJob => {
                                    const matched = this.jobList.find(j => j.id === filteredJob.id);
                                    if (matched) {
                                        this.$refs.jobTableRef.toggleRowSelection(matched, true);
                                    }
                                });
                            });
                        }

                        // 匹配度排序 tab
                        if (this.getCurrentIndex() === 3) {
                            response.data.results.forEach(sortedJob => {
                                const matched = this.jobList.find(job => job.id === sortedJob.id);
                                if (matched) {
                                    this.$set(matched, "score", sortedJob.score);
                                }
                            });
                        }
                    })
                    .catch((err) => {
                        this.loading = false;
                        this.$message.error(err.message || '获取进度失败');
                        this.status = 'exception';
                        clearInterval(this.timer);
                    });
            }, 1000); // 每1秒轮询一次
        },
        fetchJobListAndRestore() {
            this.fetchJobList().then(() => {
                this.$nextTick(() => {
                    this.$refs.jobTableRef.restoreSelection(this.selectedFilteredJobIds);
                })
            })
        }
    },

    mounted() {
        this.getResumeList();
    },
    beforeDestroy() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
}

</script>