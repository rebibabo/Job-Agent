<template>
    <div class="login-container">
        <div class="login-wrapper">
            <!-- 左侧图片 -->
            <div class="login-left">
                <img src="@/assets/login.png" alt="Login Image" class="login-image" style="width:100%;">
            </div>

            <!-- 右侧表单 -->
            <div class="login-right">
                <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on"
                    label-position="left">
                    <div class="title-container">
                        <img src="@/assets/logo.png" alt="Login Image" class="login-image" style="width:100%;">
                    </div>

                    <el-form-item prop="username">
                        <el-input ref="username" v-model="loginForm.username" placeholder="用户名" prefix-icon="el-icon-user"
                            name="username" type="text" tabindex="1" auto-complete="on" />
                    </el-form-item>
                    <br>

                    <el-form-item prop="password">
                        <el-input :key="passwordType" ref="password" v-model="loginForm.password" :type="passwordType"
                            placeholder="密码" prefix-icon="el-icon-lock" name="password" tabindex="2" auto-complete="off"
                            @keyup.enter.native="handleLogin">
                            <template #suffix>
                                <span class="show-pwd" @click.stop="showPwd">
                                    <i :class="passwordType === 'password' ? 'el-icon-view' : 'el-icon-refresh'"></i>
                                </span>
                            </template>
                        </el-input>
                    </el-form-item>
                    <br>

                    <el-form-item :inline="true" class="demo-form-inline" style="display: flex; flex-wrap: wrap; gap: 27px;">
                        <el-button :loading="loading" class="login-btn" size="mini" type="primary" style="width: 100px"
                            @click.native.prevent="handleLogin">
                            <span v-if="!loading">登录</span>
                            <span v-else>登录中...</span>
                        </el-button>

                        <el-button :loading="loading" class="register-btn" size="mini" type="primary" style="width: 100px"
                            @click.native.prevent="handleRegister">
                            注册
                        </el-button>
                    </el-form-item>

                </el-form>
            </div>

            <!-- 注册账户弹窗 -->
            <el-dialog title="注册账户" :visible.sync="dialogVisible" width="400px">
                <el-form :model="userInfo" label-width="80px" :rules="loginRules">
                    <el-form-item label="用户名">
                        <el-input v-model="userInfo.username" placeholder="请输入新的用户名" style="width: 260px;"/>
                    </el-form-item>
                    <el-form-item label="密码">
                        <el-input type="password" v-model="userInfo.password" placeholder="请输入密码"  style="width: 260px;"/>
                    </el-form-item>
                </el-form>

                <template #footer>
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="submitRule">提交</el-button>
                </template>
            </el-dialog>
        </div>
    </div>
</template>
  
<script>
import { userAddAPI } from '@/api/auth'
import { getMD5LowerCase } from '@/utils/encrypt'

export default {
    name: 'userLogin',
    data() {
        return {
            loginForm: {
                username: 'admin',
                password: '123456'
            },
            loginRules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' },
                    { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 5, max: 15, message: '长度在 5 到 15 个字符', trigger: 'blur' }
                ]
            },
            userInfo: {
                username: '',
                password: ''
            },
            loading: false,
            passwordType: 'password',
            redirect: undefined,
            dialogVisible: false
        }
    },
    watch: {
        $route: {
            handler: function (route) {
                this.redirect = route.query && route.query.redirect
            },
            immediate: true
        }
    },
    methods: {
        showPwd() {
            this.passwordType = this.passwordType === 'password' ? 'text' : 'password'
            this.$nextTick(() => {
                this.$refs.password.focus()
            })
        },
        handleLogin() {
            this.$refs.loginForm.validate(valid => {
                if (valid) {
                    this.loading = true
                    // 这里替换为你的实际登录API调用
                    const params = {
                        username: this.loginForm.username,
                        password: getMD5LowerCase(this.loginForm.password)
                    }
                    this.$store.dispatch('user/login', params)
                        .then(() => {
                            this.$router.push({ path: this.redirect || '/' })
                            this.loading = false
                        })
                        .catch((error) => {
                            console.log(error)
                            this.loading = false
                            this.$message.error(error.message);
                        })
                } else {
                    console.log('表单验证失败!')
                    return false
                }
            })
        },
        handleRegister() {
            this.dialogVisible = true
        },
        submitRule() {
            const params = {
                username: this.userInfo.username,
                password: getMD5LowerCase(this.userInfo.password)
            }
            userAddAPI(params).then(() => {
                this.$message.success('注册成功')
                this.dialogVisible = false
                this.$refs.loginForm.resetFields()
            }).catch((error) => {
                this.$message.error(error.msg)
            })
        },
    }
}
</script>
  
<style lang="scss" scoped>
$bg: #43474d;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
    min-height: 45vh;
    width: 70%;
    max-width: 1000px;
    margin: 300px auto 0;

    .login-wrapper {
        display: flex;
        background-color: $bg;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);

        .login-left {
            flex: 1.8;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #f5f7fa;

            .login-image {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
        }

        .login-right {
            flex: 1;
            padding: 60px 40px;

            .login-form {
                width: 80%;
                max-width: 300px;
                margin: 0 auto;
            }
        }
    }

    .tips {
        font-size: 14px;
        color: #fff;
        margin-bottom: 10px;

        span {
            &:first-of-type {
                margin-right: 16px;
            }
        }
    }

    .svg-container {
        padding: 6px 5px 6px 15px;
        color: $dark_gray;
        vertical-align: middle;
        width: 30px;
        display: inline-block;
    }

    .title-container {
        position: relative;

        .title {
            font-size: 26px;
            color: $light_gray;
            margin: 0 auto 40px auto;
            text-align: center;
            font-weight: bold;
        }
    }

    .show-pwd {
        position: absolute;
        right: 10px;
        top: 1px;
        font-size: 16px;
        color: $dark_gray;
        cursor: pointer;
        user-select: none;
    }

    .login-btn {
        border-radius: 17px;
        padding: 11px 20px !important;
        margin-top: 10px;
        font-weight: 500;
        font-size: 12px;
        border: 0;
        font-weight: 500;
        color: #333333;
        background-color: #ffc200;

        &:hover,
        &:focus {
            background-color: #ffc200;
            color: #ffffff;
        }
    }

    .register-btn {
        border-radius: 17px;
        padding: 11px 20px !important;
        margin-top: 10px;
        font-weight: 500;
        font-size: 12px;
        border: 0;
        font-weight: 500;
        color: #333333;
        background-color: rgb(91, 143, 231);

        &:hover,
        &:focus {
            background-color: rgb(91, 143, 231);
            color: #ffffff;
        }
    }
}
</style>