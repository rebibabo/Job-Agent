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
                        <el-button type="primary" @click="() => startJob(true)">开始任务</el-button>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="danger" @click="stopJob">停止任务</el-button>
                    </el-form-item>

                    <el-progress :percentage="progress" :status="status" />
                </el-form>

                <JobTable
                    :jobList="jobList"
                    :filters="filters"
                    :currentPage="currentPage"
                    :pageSize="pageSize"
                    :totalNumber="totalNumber"
                    :maxHeight="600"
                    @update:currentPage="currentPage = $event"
                    @update:pageSize="pageSize = $event"
                    @pagination-change="fetchJobList"
                    ref="jobTableRef"
                />

                <div v-if="timer === null && jobList.length !== 0" style="display: flex; justify-content: center; margin-top: 20px;">
                    <el-button type="primary" @click="handleNext" style="margin-left: 40px;">下一步</el-button>
                </div>

            </el-tab-pane>

            <!-- 过滤岗位 -->
            <el-tab-pane label="过滤岗位" name="filter">
                <JobTable
                    :jobList="jobList"
                    :currentPage="currentPage"
                    :pageSize="pageSize"
                    :totalNumber="totalNumber"
                    :maxHeight="600"
                    @update:currentPage="currentPage = $event"
                    @update:pageSize="pageSize = $event"
                    @pagination-change="fetchJobList"
                    ref="jobTableRef"
                />

            </el-tab-pane>
            <el-tab-pane label="匹配度排序" name="sort">匹配度排序</el-tab-pane>
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

export default {
    name: "sendResume",
    components: { SearchFilter, JobTable },
    data() {
        return {
            activeTab: 'resume',
            progress: 0,
            resumeList: [],
            jobList: [],
            status: null,
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
        handleNext() {
            const tabOrder = ['resume', 'crawl', 'filter', 'sort', 'deliver'];
            const currentIndex = tabOrder.indexOf(this.activeTab);
            console.log("当前索引", currentIndex)
            if (currentIndex >= 0 && currentIndex < tabOrder.length - 1) {
                this.activeTab = tabOrder[currentIndex + 1];
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
    },

    mounted() {
        this.getResumeList();
    }
}

</script>