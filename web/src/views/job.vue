<template>
    <div>
        <h1 style="font-size: 27px;">职位查询系统</h1>

        <JobFilter v-model="filters" @submit="onSubmit" @reset="onReset" />

        <LoadingDots :visible="loading" message="加载中，请稍候" />
        <br />

        <JobTable
            :jobList="jobList"
            :currentPage="currentPage"
            :pageSize="pageSize"
            :totalNumber="totalNumber"
            :deleteAll="false"
            @update:currentPage="currentPage = $event"
            @update:pageSize="pageSize = $event"
            @pagination-change="fetchJobListAndRestore"
            ref="jobTableRef"
        />

    </div>
</template>
  
<script>
import JobFilter from '@/components/JobFilter.vue'
import LoadingDots from '@/components/LoadingDots.vue'
import JobTable from '@/components/JobTable.vue'
import { jobListAPI } from '@/api/job'

export default {
    name: 'JobQuery',
    components: { JobFilter, LoadingDots, JobTable },
    data() {
        return {
            filters: { city: ['不限'], experience: ['不限'], degree: ['不限'], title: ['不限'], industry: ['不限'], scale: ['不限'], stage: ['不限'] },
            loading: true,
            jobList: [],
            currentPage: 1,  
            pageSize: 40,    
            totalNumber: 0,  
        }
    },
    methods: {
        formatOptions(options) {
            if (!options || options.length === 0) return ''
            if (options.length === 1 && options[0] === '不限') return ''
            return options.filter(opt => opt !== '不限').join(',')
        },
        async fetchJobList() {
            try {
                this.loading = true
                const params = {
                    userId: this.$store.state.user.userInfo.id,
                    city: this.formatOptions(this.filters.city),
                    experience: this.formatOptions(this.filters.experience),
                    degree: this.formatOptions(this.filters.degree),
                    industry: this.formatOptions(this.filters.industry),
                    scale: this.formatOptions(this.filters.scale),
                    stage: this.formatOptions(this.filters.stage),
                    title: this.formatOptions(this.filters.title),
                    page: this.currentPage,
                    pageSize: this.pageSize
                }
                const response = await jobListAPI(params)
                this.jobList = response.data.items
                this.totalNumber = response.data.total
            } catch (error) {
                this.$message.error(error.message || '请求职位列表失败')
            } finally {
                this.loading = false
            }
        },
        onSubmit() {
            this.currentPage = 1
            this.fetchJobListAndRestore()
            this.$refs.jobTableRef.scrollUp()
        },
        onReset() {
            this.currentPage = 1
            this.fetchJobListAndRestore()
            this.$refs.jobTableRef.scrollUp()
        },
        async fetchJobListAndRestore() {
            await this.fetchJobList();
            this.$nextTick(() => {
                this.$refs.jobTableRef.restoreSelection();
            });
        }
    },
    mounted() {
        this.fetchJobList()
    }
}
</script>
  
