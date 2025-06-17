<template>
    <div>
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
            <el-form-item label="关键词">
                <el-input v-model="input" clearable placeholder="关键词" prefix-icon="el-icon-search"
                    style="width: 284px;"></el-input>
            </el-form-item>
            <el-form-item label="工作城市">
                <el-select v-model="city" placeholder="工作城市" multiple style="width: 270px;">
                    <el-option v-for="item in cityList" :key="item.code" :label="item.name" :value="item.code">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="经验要求">
                <el-select v-model="experience" placeholder="经验要求" multiple style="width: 270px;">
                    <el-option v-for="item in experienceList" :key="item.code" :label="item.name" :value="item.code">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="学历要求">
                <el-select v-model="degree" placeholder="学历要求" multiple style="width: 270px;">
                    <el-option v-for="item in degreeList" :key="item.code" :label="item.name" :value="item.code">
                    </el-option>
                </el-select>
            </el-form-item>
            <br>
            <el-form-item label="公司行业">
                <el-select v-model="industry" placeholder="公司行业" multiple style="width: 270px;">
                    <el-option v-for="item in industryList" :key="item.code" :label="item.name" :value="item.code">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="公司规模">
                <el-select v-model="scale" placeholder="公司规模" multiple style="width: 270px;">
                    <el-option v-for="item in scaleList" :key="item.code" :label="item.name" :value="item.code">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="融资阶段">
                <el-select v-model="stage" placeholder="公司规模" multiple style="width: 270px;">
                    <el-option v-for="item in stageList" :key="item.code" :label="item.name" :value="item.code">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="工作性质">
                <el-select v-model="jobType" placeholder="公司规模" multiple style="width: 270px;">
                    <el-option v-for="item in jobTypeList" :key="item.code" :label="item.name" :value="item.code">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">查询</el-button>
            </el-form-item>

        </el-form>



        <el-table :data="tableData" stripe border max-height="500" style="width: 100%">
            <el-table-column prop="name" sortable label="工作名称" width="480">
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
            <el-table-column prop="title" sortable label="岗位分类" width="180">
            </el-table-column>
            <el-table-column prop="scale" sortable label="公司规模" width="180">
            </el-table-column>
            <el-table-column prop="stage" sortable label="融资阶段" width="180">
            </el-table-column>
            <el-table-column label="操作">
                <el-table-column label="操作">
                    <template #default="{ row }">
                        <el-button @click="handleViewJob(row.url)" type="text" size="small">
                            查看
                        </el-button>
                    </template>
                </el-table-column>
            </el-table-column>
        </el-table>

        <br>

        <el-pagination background layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange"
            @current-change="handleCurrentChange" :total="1000">
        </el-pagination>
    </div>
</template>

<script>
export default {
    name: 'JobQuery',
    methods: {
        handleSizeChange(size) {
            console.log(`size: ${size}`)
        },
        handleCurrentChange(currentPage) {
            console.log(`currentPage: ${currentPage}`)
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
        onSubmit() {
            alert(this.city)
        },
    },
    data() {
        return {
            tableData: [
                {
                    name: "Java高级开发工程师",
                    type: "0",
                    url: "https://www.zhipin.com/job_detail/703b71fa4cc7080003B939i5GFFX.html",
                    salary: "25-50K·16薪",
                    salaryFloor: 400000,
                    salaryCeiling: 800000,
                    crawlDate: "2025-06-17",
                    city: "北京",
                    region: "朝阳区",
                    experience: "5-10年",
                    degree: "本科",
                    industry: "互联网",
                    title: "Java",
                    skills: "Java,Spring,MyBatis,Redis,MySQL,物联网经验,分布式经验,搜索/推荐/广告经验,不接受居家办公,平台,交易系统",
                    scale: "15-50人",
                    stage: "B轮",
                    welfare: "五险一金,绩效奖金,带薪年假,免费体检,免费住宿,免费食宿,员工旅游,员工宿舍,员工健身房,员工文化活动,员工健康管理,员工培训",
                    description: ""
                }],
            input: '',
            city: ['不限'],
            experience: ['不限'],
            degree: ['不限'],
            industry: ['不限'],
            scale: ['不限'],
            stage: ['不限'],
            salary: ['不限'],
            jobType: ['不限'],
            cityList: [{
                code: '选项1',
                name: '不限'
            }, {
                code: '选项2',
                name: '北京'
            }, {
                code: '选项3',
                name: '上海'
            }, {
                code: '选项4',
                name: '广州'
            }, {
                code: '选项5',
                name: '深圳'
            }],
            industryList: [
                {
                    code: 0,
                    name: "不限"
                },
                {
                    code: 101,
                    name: "IT互联网"
                },
                {
                    code: 102,
                    name: "电子商务"
                },
                {
                    code: 103,
                    name: "金融"
                },
                {
                    code: 104,
                    name: "房地产"
                },
                {
                    code: 105,
                    name: "教育培训"
                },
                {
                    code: 106,
                    name: "医疗健康"
                },
                {
                    code: 107,
                    name: "农业"
                },
                {
                    code: 108,
                    name: "制造业"
                },
                {
                    code: 109,
                    name: "其他"
                }
            ],
            experienceList: [
                {
                    code: 0,
                    name: "不限"
                },
                {
                    code: 108,
                    name: "在校生"
                },
                {
                    code: 102,
                    name: "应届生"
                },
                {
                    code: 101,
                    name: "经验不限"
                },
                {
                    code: 103,
                    name: "1年以内"
                },
                {
                    code: 104,
                    name: "1-3年"
                },
                {
                    code: 105,
                    name: "3-5年"
                },
                {
                    code: 106,
                    name: "5-10年"
                },
                {
                    code: 107,
                    name: "10年以上"
                }
            ],

            degreeOptions: [{
                value: '不限',
                label: '不限'
            }, {
                value: '大专',
                label: '大专'
            }, {
                value: '本科',
                label: '本科'
            }, {
                value: '硕士',
                label: '硕士'
            }, {
                value: '博士',
                label: '博士'
            }],

            salaryList: [
                {
                    code: 0,
                    name: "不限",
                    "lowSalary": 0,
                    "highSalary": 0
                },
                {
                    code: 402,
                    name: "3K以下",
                    "lowSalary": 0,
                    "highSalary": 3
                },
                {
                    code: 403,
                    name: "3-5K",
                    "lowSalary": 3,
                    "highSalary": 5
                },
                {
                    code: 404,
                    name: "5-10K",
                    "lowSalary": 5,
                    "highSalary": 10
                },
                {
                    code: 405,
                    name: "10-20K",
                    "lowSalary": 10,
                    "highSalary": 20
                },
                {
                    code: 406,
                    name: "20-50K",
                    "lowSalary": 20,
                    "highSalary": 50
                },
                {
                    code: 407,
                    name: "50K以上",
                    "lowSalary": 50,
                    "highSalary": 0
                }
            ],
            stageList: [
                {
                    code: 0,
                    name: "不限"
                },
                {
                    code: 801,
                    name: "未融资"
                },
                {
                    code: 802,
                    name: "天使轮"
                },
                {
                    code: 803,
                    name: "A轮"
                },
                {
                    code: 804,
                    name: "B轮"
                },
                {
                    code: 805,
                    name: "C轮"
                },
                {
                    code: 806,
                    name: "D轮及以上"
                },
                {
                    code: 807,
                    name: "已上市"
                },
                {
                    code: 808,
                    name: "不需要融资"
                }
            ],
            scaleList: [
                {
                    code: 0,
                    name: "不限"
                },
                {
                    code: 301,
                    name: "0-20人"
                },
                {
                    code: 302,
                    name: "20-99人"
                },
                {
                    code: 303,
                    name: "100-499人"
                },
                {
                    code: 304,
                    name: "500-999人"
                },
                {
                    code: 305,
                    name: "1000-9999人"
                },
                {
                    code: 306,
                    name: "10000人以上"
                }
            ],
            degreeList: [
                {
                    code: 0,
                    name: "不限"
                },
                {
                    code: 209,
                    name: "初中及以下"
                },
                {
                    code: 208,
                    name: "中专/中技"
                },
                {
                    code: 206,
                    name: "高中"
                },
                {
                    code: 202,
                    name: "大专"
                },
                {
                    code: 203,
                    name: "本科"
                },
                {
                    code: 204,
                    name: "硕士"
                },
                {
                    code: 205,
                    name: "博士"
                }
            ],
            jobTypeList: [
                {
                    code: 0,
                    name: "不限"
                },
                {
                    code: 1901,
                    name: "全职"
                },
                {
                    code: 1903,
                    name: "兼职"
                },
                {
                    code: 1902,
                    name: "实习"
                }
            ]
        }
    }
}
</script>

<style></style>