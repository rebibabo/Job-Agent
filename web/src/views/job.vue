<template>
    <div>
        <h1 style="font-size: 30px;">职位查询系统</h1>
        <el-form :inline="true" class="demo-form-inline" style="display: flex; flex-wrap: wrap; gap: 10px;">
            <el-form-item label="关键词">
                <el-input v-model="input" clearable placeholder="关键词" prefix-icon="el-icon-search"
                    style="width: 284px;"></el-input>
            </el-form-item>
            <el-form-item label="工作城市">
                <el-select v-model="city" placeholder="工作城市" multiple style="width: 270px;"
                    @change="val => handleSelectChange('city', val)">
                    <el-option v-for="item in cityList" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="经验要求">
                <el-select v-model="experience" placeholder="经验要求" multiple style="width: 270px;"
                    @change="val => handleSelectChange('experience', val)">
                    <el-option v-for="item in experienceList" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="学历要求">
                <el-select v-model="degree" placeholder="学历要求" multiple style="width: 270px;"
                    @change="val => handleSelectChange('degree', val)">
                    <el-option v-for="item in degreeList" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="工作岗位">
                <el-select v-model="title" placeholder="工作岗位" multiple style="width: 270px;"
                    @change="val => handleSelectChange('title', val)">
                    <el-option v-for="item in titleList" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="公司行业">
                <el-select v-model="industry" placeholder="公司行业" multiple style="width: 270px;"
                    @change="val => handleSelectChange('industry', val)">
                    <el-option v-for="item in industryList" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="公司规模">
                <el-select v-model="scale" placeholder="公司规模" multiple style="width: 270px;"
                    @change="val => handleSelectChange('scale', val)">
                    <el-option v-for="item in scaleList" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="融资阶段">
                <el-select v-model="stage" placeholder="公司规模" multiple style="width: 270px;"
                    @change="val => handleSelectChange('stage', val)">
                    <el-option v-for="item in stageList" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="工作性质">
                <el-select v-model="jobType" placeholder="公司规模" multiple style="width: 270px;"
                    @change="val => handleSelectChange('jobType', val)">
                    <el-option v-for="item in jobTypeList" :key="item" :label="item" :value="item">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">查询</el-button>
            </el-form-item>
            <el-form-item>
                <el-button @click="resetForm()">重置</el-button>
            </el-form-item>
        </el-form>

        <br>

        <el-table :data="jobList" stripe border max-height="850" style="width: 100%">
            <el-table-column prop="jobName" sortable label="工作名称" width="480">
            </el-table-column>
            <el-table-column prop="salary" sortable label="薪资" width="180">
            </el-table-column>
            <el-table-column prop="city" sortable label="工作城市" width="180">
            </el-table-column>
            <el-table-column prop="region" sortable label="城市区" width="180">
            </el-table-column>
            <el-table-column prop="experience" sortable label="经验要求" width="180">
            </el-table-column>
            <el-table-column prop="degree" sortable label="学历要求" width="180">
            </el-table-column>
            <el-table-column prop="industry" sortable label="公司行业" width="180">
            </el-table-column>
            <el-table-column prop="title" sortable label="工作岗位" width="180">
            </el-table-column>
            <el-table-column prop="scale" sortable label="公司规模" width="180">
            </el-table-column>
            <el-table-column prop="stage" sortable label="融资阶段" width="180">
            </el-table-column>
            <el-table-column label="操作">
                <template #default="{ row }">
                    <el-button @click="handleViewJob(row.url)" type="text" size="small">
                        查看
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <br>

        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
                :page-sizes="[20, 40, 60, 80, 100]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper"
                :total="totalNumber">
            </el-pagination></div>
        </div>
</template>

<script>
import { cityListAPI, industryListAPI, titleListAPI, jobListAPI } from '@/api/job';

export default {
    name: 'JobQuery',
    methods: {
        handleSizeChange(size) {
            this.pageSize = size;
            this.fetchJobList();
        },
        handleCurrentChange(currentPage) {
            this.currentPage = currentPage;
            this.fetchJobList();
        },
        handleViewJob(url) {
            if (!url) {
                this.$message.warning('该职位没有有效的链接');
                return;
            }

            // 确保URL以http/https开头
            const fullUrl = url.startsWith('http') ? url : `https://${url}`;

            window.open(fullUrl, '_blank');
        },
        formatOptions(options) {
            // 如果数组包含"不限"且只有这一个元素，返回空字符串
            if (options.length === 1 && options[0] === "不限") {
                return "";
            }
            // 否则过滤掉"不限"（如果有），并用逗号拼接剩余元素
            return options.filter(opt => opt !== "不限").join(",");
        },
        onSubmit() {
            this.currentPage = 1;
            this.fetchJobList();
        },
        async fetchCityList() {
            try {
                const response = await cityListAPI();
                this.cityList = response.data;
                this.cityList.unshift('不限');
            } catch (error) {
                this.$message.error('获取城市列表失败');
            }
        },
        async fetchIndustryList() {
            try {
                const response = await industryListAPI();
                this.industryList = response.data;
                this.industryList.unshift('不限');
            } catch (error) {
                this.$message.error('获取行业列表失败');
            }
        },
        async fetchTitleList() {
            try {
                const response = await titleListAPI();
                this.titleList = response.data;
                this.titleList.unshift('不限');
            } catch (error) {
                this.$message.error('获取行业列表失败');
            }
        },
        async fetchJobList() {
            try {
                var params = {
                    keyword: this.input,
                    city: this.formatOptions(this.city),
                    experience: this.formatOptions(this.experience),
                    degree: this.formatOptions(this.degree),
                    industry: this.formatOptions(this.industry),
                    scale: this.formatOptions(this.scale),
                    stage: this.formatOptions(this.stage),
                    salary: this.formatOptions(this.salary),
                    jobType: this.formatOptions(this.jobType),
                    title: this.formatOptions(this.title),
                    page: this.currentPage,
                    pageSize: this.pageSize
                }
                const response = await jobListAPI(params);
                this.jobList = response.data.items;
                this.totalNumber = response.data.total;
            } catch (error) {
                this.$message.error(error.message);
            }
        },
        // 处理多选“不限”互斥逻辑
        handleSelectChange(field, newVal) {
            const lastElement = newVal[newVal.length - 1]
            // 如果原始为不限，现在点击了其他选项，则清除不限选项
            if (newVal.length === 0) {
                this[field] = ['不限']
            }
            else if (this[field].length === 2 && this[field][0] === '不限') {
                this[field] = newVal.slice(1);
            }
            // 如果原始为其他选项，现在点击了不限，则清除其他选项
            else if (lastElement === '不限') {
                this[field] = ['不限'];
            }
            else {
                this[field] = newVal;
            }
        },
        resetForm() {
            this.input = '';
            this.city = ['不限'];
            this.experience = ['不限'];
            this.degree = ['不限'];
            this.title = ['不限'];
            this.industry = ['不限'];
            this.scale = ['不限'];
            this.stage = ['不限'];
            this.salary = ['不限'];
            this.jobType = ['不限'];
            this.currentPage = 1;
            this.fetchJobList();
        },
    },
    mounted() {
        console.log(this.$store.state.user.userInfo)
        this.fetchCityList();
        this.fetchIndustryList();
        this.fetchTitleList();
        this.fetchJobList();
    },
    data() {
        return {
            currentPage: 1,
            pageSize: 40,
            totalNumber: 0,
            jobList: [],
            input: '',
            city: ['不限'],
            experience: ['不限'],
            degree: ['不限'],
            title: ['不限'],
            industry: ['不限'],
            scale: ['不限'],
            stage: ['不限'],
            salary: ['不限'],
            jobType: ['不限'],
            cityList: [],
            industryList: [],
            titleList: [],
            experienceList: ["不限", "在校生", "应届生", "经验不限", "1年以内", "1-3年", "3-5年", "5-10年", "10年以上"],
            salaryList: ["不限", "3K以下", "3-5K", "5-10K", "10-20K", "20-50K", "50K以上"],
            stageList: ["不限", "未融资", "天使轮", "A轮", "B轮", "C轮", "D轮及以上", "已上市", "不需要融资"],
            scaleList: ["不限", "0-20人", "20-99人", "100-499人", "500-999人", "1000-9999人", "10000人以上"],
            degreeList: ["不限", "初中及以下", "中专/中技", "高中", "大专", "本科", "硕士", "博士"],
            jobTypeList: ["不限", "全职", "兼职", "实习"]
        }
    }
}
</script>

<style></style>