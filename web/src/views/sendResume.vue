<template>
    <div>
        <el-upload class="upload-demo" drag :auto-upload="true" action="#" multiple :before-upload="beforeUpload">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip">只能上传PDF文件，且不超过4MB</div>
        </el-upload>
    </div>
</template>

<script>
import request from '@/utils/request'

export default {
    name: "sendResume",
    data() {
        return {
            uploadUrl: "http://localhost:8081/resume/" + this.$store.state.user.userInfo.id,

        };
    },
    methods: {
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

            // 动态 url
            const userId = this.$store.state.user.userInfo.id;
            const url = `/crawl/resume/${userId}`;

            // 发送
            request.post(url, formData, {
                headers: { "Content-Type": "multipart/form-data", "token": this.$store.state.user.userInfo.token },
            })
            .then(res => {
                this.$message.success("上传成功");
                console.log(res.data);
            })
            .catch(err => {
                const msg = err.response?.data?.message || '上传失败';
                this.$message.error(msg);
                console.error(err);
            });

            // 返回 false，阻止 el-upload 自己继续提交
            return false;
        }
    }
}
</script>