<template>
    <el-form :inline="true" class="demo-form-inline" style="display: flex; flex-wrap: wrap; gap: 0px;">
        <!-- 工作城市 -->
        <el-form-item label="工作城市">
            <el-select v-model="localFilters.city" multiple placeholder="工作城市" style="width: 210px;"
                @change="val => handleSelectChange('city', val)" size="small">
                <el-option v-for="item in cityList" :key="item" :label="item" :value="item" />
            </el-select>
        </el-form-item>

        <!-- 经验要求 -->
        <el-form-item label="经验要求">
            <el-select v-model="localFilters.experience" multiple placeholder="经验要求" style="width: 210px;"
                @change="val => handleSelectChange('experience', val)" size="small">
                <el-option v-for="item in experienceList" :key="item" :label="item" :value="item" />
            </el-select>
        </el-form-item>

        <!-- 学历要求 -->
        <el-form-item label="学历要求">
            <el-select v-model="localFilters.degree" multiple placeholder="学历要求" style="width: 209px;"
                @change="val => handleSelectChange('degree', val)" size="small">
                <el-option v-for="item in degreeList" :key="item" :label="item" :value="item" />
            </el-select>
        </el-form-item>

        <!-- 工作岗位 -->
        <el-form-item label="工作岗位">
            <el-select v-model="localFilters.title" multiple placeholder="工作岗位" style="width: 209px;"
                @change="val => handleSelectChange('title', val)" size="small">
                <el-option v-for="item in titleList" :key="item" :label="item" :value="item" />
            </el-select>
        </el-form-item>

        <!-- 公司行业 -->
        <el-form-item label="公司行业">
            <el-select v-model="localFilters.industry" multiple placeholder="公司行业" style="width: 210px;"
                @change="val => handleSelectChange('industry', val)" size="small">
                <el-option v-for="item in industryList" :key="item" :label="item" :value="item" />
            </el-select>
        </el-form-item>

        <!-- 公司规模 -->
        <el-form-item label="公司规模">
            <el-select v-model="localFilters.scale" multiple placeholder="公司规模" style="width: 210px;"
                @change="val => handleSelectChange('scale', val)" size="small">
                <el-option v-for="item in scaleList" :key="item" :label="item" :value="item" />
            </el-select>
        </el-form-item>

        <!-- 融资阶段 -->
        <el-form-item label="融资阶段">
            <el-select v-model="localFilters.stage" multiple placeholder="融资阶段" style="width: 209px;"
                @change="val => handleSelectChange('stage', val)" size="small">
                <el-option v-for="item in stageList" :key="item" :label="item" :value="item" />
            </el-select>
        </el-form-item>

        <!-- 按钮 -->
        <el-form-item>
            <el-button type="primary" @click="$emit('submit')" size="small" style="margin-left: 155px;">查询</el-button>
        </el-form-item>
        <el-form-item>
            <el-button @click="resetForm" size="small" style="margin-left: 2px;">重置</el-button>
        </el-form-item>
    </el-form>
</template>
  
<script>
import { cityListAPI, industryListAPI, titleListAPI } from '@/api/job';

export default {
    name: 'JobFilter',
    model: {
        prop: 'filters',
        event: 'change'
    },
    props: {
        filters: {
            type: Object,
            default: () => ({})
        }
    },
    data() {
        return {
            cityList: [],
            industryList: [],
            titleList: [],
            experienceList: ["不限", "在校生", "应届生", "经验不限", "1年以内", "1-3年", "3-5年", "5-10年", "10年以上"],
            degreeList: ["不限", "初中及以下", "中专/中技", "高中", "大专", "本科", "硕士", "博士"],
            scaleList: ["不限", "0-20人", "20-99人", "100-499人", "500-999人", "1000-9999人", "10000人以上"],
            stageList: ["不限", "未融资", "天使轮", "A轮", "B轮", "C轮", "D轮及以上", "已上市", "不需要融资"],
            localFilters: {
                city: ['不限'],
                experience: ['不限'],
                degree: ['不限'],
                title: ['不限'],
                industry: ['不限'],
                scale: ['不限'],
                stage: ['不限'],
            }
        };
    },
    mounted() {
        try {
            this.fetchCityList();
            this.fetchIndustryList();
            this.fetchTitleList();
        } catch (error) {
            console.error('fetchList error:', error);
        }
    },
    methods: {
        // 获取可选城市列表
        async fetchCityList() {
            try {
                const res = await cityListAPI();
                this.cityList = ['不限', ...res.data];
            } catch (error) {
                console.error('fetchCityList error:', error);
            }
        },
        // 获取可选行业列表
        async fetchIndustryList() {
            try {
                const res = await industryListAPI();
                this.industryList = ['不限', ...res.data];
            } catch (error) {
                console.error('fetchIndustryList error:', error);
            }
        },
        // 获取可选职位列表
        async fetchTitleList() {
            try {
                const res = await titleListAPI();
                this.titleList = ['不限', ...res.data];
            } catch (error) {
                console.error('fetchTitleList error:', error);
            }
        },
        handleSelectChange(field, val) {
            const last = val[val.length - 1]; // 最后一个选项
            if (val.length === 0) {     // 如果清空了所有选项
                this.localFilters[field] = ['不限'];        // 将其设置为不限
            } else if (this.localFilters[field].length === 2 && this.localFilters[field][0] === '不限') {       // 如果之前是不限，现在选择了其他选项
                this.localFilters[field] = val.slice(1);    // 则只保留新选择的选项，取消不限选项
            } else if (last === '不限') {       // 如果之前多选了选项，现在选择了不限选项
                this.localFilters[field] = ['不限'];        // 则只保留不限选项
            } else {         // 否则，新增多选的选项
                this.localFilters[field] = val;
            }
            this.$emit('change', { ...this.localFilters });     // 触发父组件的 change 事件
        },
        resetForm() {
            // 重置表单
            this.localFilters = {
                city: ['不限'],
                experience: ['不限'],
                degree: ['不限'],
                title: ['不限'],
                industry: ['不限'],
                scale: ['不限'],
                stage: ['不限']
            };
            this.$emit('change', { ...this.localFilters });
            this.$emit('reset');
        }
    }
};
</script>
  
<style scoped>
.demo-form-inline ::v-deep(.el-form-item) {
  margin-bottom: 6px; /* 表单组件之间的行间距默认是 18px 左右，改小一点 */
}
</style>
  