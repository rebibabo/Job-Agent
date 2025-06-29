<template>
    <div>
        <el-form :inline="true" class="demo-form-inline" style="display: flex; flex-wrap: wrap; gap: 0px;">
            <!-- 工作城市 -->
            <el-form-item label="工作城市">
                <el-select v-model="localFilters.city" multiple placeholder="工作城市" style="width: 500px;"
                    @change="val => handleSelectChange('city', val)">
                    <el-option v-for="item in cityList" :key="item" :label="item" :value="item" />
                </el-select>
            </el-form-item>

            <!-- 经验要求 -->
            <el-form-item label="经验要求">
                <el-select v-model="localFilters.experience" multiple placeholder="经验要求" style="width: 260px;"
                    @change="val => handleSelectChange('experience', val)">
                    <el-option v-for="item in experienceList" :key="item" :label="item" :value="item" />
                </el-select>
            </el-form-item>

            <!-- 学历要求 -->
            <el-form-item label="学历要求">
                <el-select v-model="localFilters.degree" multiple placeholder="学历要求" style="width: 220px;"
                    @change="val => handleSelectChange('degree', val)">
                    <el-option v-for="item in degreeList" :key="item" :label="item" :value="item" />
                </el-select>
            </el-form-item>

            <!-- 工作岗位 -->
            <el-form-item label="工作岗位">
                <el-select v-model="localFilters.title" multiple placeholder="工作岗位" style="width: 690px;"
                    @change="val => handleSelectChange('title', val)">
                    <el-option v-for="item in titleList" :key="item" :label="item" :value="item" />
                </el-select>
            </el-form-item>

            <!-- 最大查询条数 -->
            <el-form-item label="最大条数/每城市/每岗位">
                <el-select v-model="localFilters.limitNum" placeholder="最大条数" style="width: 120px;"
                    @change="val => handleSelectChange('title', val)">
                    <el-option v-for="item in limitList" :key="item" :label="item" :value="item" />
                </el-select>
            </el-form-item>

            <!-- 公司行业 -->
            <el-form-item label="公司行业">
                <el-select v-model="localFilters.industry" multiple placeholder="公司行业" style="width: 500px;"
                    @change="val => handleSelectChange('industry', val)">
                    <el-option v-for="item in industryList" :key="item" :label="item" :value="item" />
                </el-select>
            </el-form-item>

            <!-- 公司规模 -->
            <el-form-item label="公司规模">
                <el-select v-model="localFilters.scale" multiple placeholder="公司规模" style="width: 260px;"
                    @change="val => handleSelectChange('scale', val)">
                    <el-option v-for="item in scaleList" :key="item" :label="item" :value="item" />
                </el-select>
            </el-form-item>

            <!-- 融资阶段 -->
            <el-form-item label="融资阶段">
                <el-select v-model="localFilters.stage" multiple placeholder="融资阶段" style="width: 220px;"
                    @change="val => handleSelectChange('stage', val)">
                    <el-option v-for="item in stageList" :key="item" :label="item" :value="item" />
                </el-select>
            </el-form-item>

            <!-- 关键词 -->
            <el-form-item label="关键词" label-width="68px">
                <el-input v-model="localFilters.keyword" placeholder="请输入关键词" style="width: 684px;" />
            </el-form-item>
            <!-- 按钮 -->
            <el-form-item>
                <el-button @click="resetForm">重置</el-button>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="openSaveRuleDialog">保存规则</el-button>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="openLoadRuleDialog">加载规则</el-button>
            </el-form-item>
        </el-form>

        <!-- 保存规则弹窗 -->
        <el-dialog title="保存规则" :visible.sync="ruleDialogVisible" width="500px">
            <el-form :model="ruleInfo" label-width="80px">
                <el-form-item label="规则名称">
                    <el-input v-model="ruleInfo.ruleName" placeholder="请输入规则名称" @keyup.enter.native="onRuleNameEnter"/>
                </el-form-item>
                <el-form-item label="规则描述">
                    <el-input type="textarea" v-model="ruleInfo.ruleDescription" ref="ruleDescription" placeholder="请输入规则描述" @keyup.enter.native="onUserDescEnter"/>
                </el-form-item>
            </el-form>

            <div style="margin-top: 10px;">
                <strong>规则属性：</strong>
                <pre
                    style="background: #f5f5f5; padding: 10px; border-radius: 4px; max-height: 300px; overflow: auto; white-space: pre-wrap; word-break: break-all;">
                    {{ convertFiltersToString(localFilters) }}
                </pre>
            </div>

            <template #footer>
                <el-button @click="ruleDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitRule">提交</el-button>
            </template>
        </el-dialog>

        <!-- 加载规则弹窗 -->
        <el-dialog title="加载规则" :visible.sync="loadRuleDialogVisible" width="800px">
            <el-table :data="ruleList" style="width: 100%">
                <el-table-column prop="ruleName" label="规则名称" width="200" />
                <el-table-column prop="ruleDescription" label="规则描述" />
                <el-table-column label="操作" width="180">
                    <template v-slot="scope">
                        <el-button type="primary" size="mini" @click="applyRule(scope.row)">选择</el-button>
                        <el-button type="danger" size="mini" @click="deleteRule(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <template #footer>
                <el-button @click="loadRuleDialogVisible = false">关闭</el-button>
            </template>
        </el-dialog>

    </div>
</template>
  
<script>
import { cityListAllAPI, industryListAllAPI, titleListAllAPI } from '@/api/job';
import { findRuleAPI, saveRuleAPI, loadRuleAPI, deleteRuleAPI } from '@/api/rule';

export default {
    name: 'SearchFilter',
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
            limitList: [30, 60, 90, 120, 150, 180, 210, 240, 270, 300],
            experienceList: ["不限", "在校生", "应届生", "1年以内", "1-3年", "3-5年", "5-10年", "10年以上"],
            degreeList: ["不限", "初中及以下", "中专/中技", "高中", "大专", "本科", "硕士", "博士"],
            scaleList: ["不限", "0-20人", "20-99人", "100-499人", "500-999人", "1000-9999人", "10000人以上"],
            stageList: ["不限", "未融资", "天使轮", "A轮", "B轮", "C轮", "D轮及以上", "已上市", "不需要融资"],
            localFilters: {
                keyword: '',
                limitNum: 30,
                city: ['不限'],
                experience: ['不限'],
                degree: ['不限'],
                title: ['不限'],
                industry: ['互联网'],
                scale: ['不限'],
                stage: ['不限'],
            },
            ruleDialogVisible: false,
            ruleInfo: {
                ruleName: '',
                ruleDescription: ''
            },
            loadRuleDialogVisible: false,
            ruleList: []
        };
    },
    mounted() {
        try {
            this.fetchCityListAll();
            this.fetchIndustryListAll();
            this.fetchTitleListAll();
        } catch (error) {
            console.error('fetchList error:', error);
        }
    },
    methods: {
        async fetchCityListAll() {
            try {
                const res = await cityListAllAPI();
                this.cityList = ['不限', ...res.data];
            } catch (error) {
                console.error('fetchCityList error:', error);
            }
        },
        async fetchIndustryListAll() {
            try {
                const res = await industryListAllAPI();
                this.industryList = ['不限', ...res.data];
            } catch (error) {
                console.error('fetchIndustryList error:', error);
            }
        },
        async fetchTitleListAll() {
            try {
                const res = await titleListAllAPI();
                this.titleList = ['不限', ...res.data];
            } catch (error) {
                console.error('fetchTitleList error:', error);
            }
        },
        handleSelectChange(field, val) {
            const last = val[val.length - 1];
            if (val.length === 0) {
                this.localFilters[field] = ['不限'];
            } else if (this.localFilters[field].length === 2 && this.localFilters[field][0] === '不限') {
                this.localFilters[field] = val.slice(1);
            } else if (last === '不限') {
                this.localFilters[field] = ['不限'];
            } else {
                this.localFilters[field] = val;
            }
            this.$emit('change', { ...this.localFilters });
        },
        resetForm() {
            this.localFilters = {
                keyword: '',
                limitNum: 30,
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
        },
        openSaveRuleDialog() {
            this.ruleInfo = { ruleName: '', ruleDescription: '' };
            this.ruleDialogVisible = true;
        },
        convertFiltersToString(filters) {
            const result = {};
            for (const key in filters) {
                const value = filters[key];
                if (Array.isArray(value)) {
                    result[key] = value.join(',');
                } else {
                    result[key] = value;
                }
            }
            return result;
        },
        submitRule() {
            if (!this.ruleInfo.ruleName) {
                this.$message.warning('请填写规则名称');
                return;
            }
            var params = {
                userId: this.$store.state.user.userInfo.id,
                ruleName: this.ruleInfo.ruleName,
            }
            findRuleAPI(params).then(res => {
                if (res.code == 0) {
                    this.$message.warning('规则已存在，请更换规则名称');
                } else {
                    params = {
                        userId: this.$store.state.user.userInfo.id,
                        ruleName: this.ruleInfo.ruleName,
                        ruleDescription: this.ruleInfo.ruleDescription,
                        ...this.convertFiltersToString(this.localFilters)
                    };
                    console.log(params);
                    saveRuleAPI(params).then(() => {
                        this.$message.success('规则保存成功');
                        this.ruleDialogVisible = false;
                    }).catch(err => {
                        console.error(err);
                        this.$message.error('规则保存失败');
                    });
                }
            }).catch(err => {
                console.error(err);
            });

        },
        openLoadRuleDialog() {
            loadRuleAPI(this.$store.state.user.userInfo.id).then(res => {
                this.ruleList = res.data || [];
                this.loadRuleDialogVisible = true;
            }).catch(err => {
                console.error(err);
                this.$message.error('加载规则失败');
            });
        },
        applyRule(rule) {
            // 将选中的规则应用到 localFilters
            this.localFilters = {
                keyword: rule.keyword || '',
                limitNum: Number(rule.limitNum) || 30,
                city: rule.city ? rule.city.split(',') : ['不限'],
                experience: rule.experience ? rule.experience.split(',') : ['不限'],
                degree: rule.degree ? rule.degree.split(',') : ['不限'],
                title: rule.title ? rule.title.split(',') : ['不限'],
                industry: rule.industry ? rule.industry.split(',') : ['不限'],
                scale: rule.scale ? rule.scale.split(',') : ['不限'],
                stage: rule.stage ? rule.stage.split(',') : ['不限']
            };
            this.loadRuleDialogVisible = false;
            this.$emit('change', { ...this.localFilters });
            this.$emit('submit');
        },
        deleteRule(rule) {
            this.$confirm(`确定要删除规则 "${rule.ruleName}" 吗？`, '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                deleteRuleAPI(rule.id).then(() => {
                    this.$message.success('规则删除成功');
                    // 重新加载规则列表
                    this.openLoadRuleDialog();
                }).catch(err => {
                    console.error(err);
                    this.$message.error('规则删除失败');
                });
            }).catch(() => {
                // 用户取消操作
            });
        },
        onRuleNameEnter() {
            if (this.ruleInfo.ruleName) {
                this.$refs.ruleDescription.focus();
            }
        },
        onUserDescEnter() {
            if (this.ruleInfo.ruleDescription && this.ruleInfo.ruleName) {
                this.submitRule();
            }
        }
    }
};
</script>
  
<style scoped></style>
  