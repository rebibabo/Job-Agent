<template>
    <div id="app">
        <el-container style="min-height: 100vh;">
            <!-- 侧边栏区域 -->
            <el-aside width="auto" style="min-height: 100vh;">
                <sidebar ref="sidebarRef" :is-collapse="isCollapse" @toggle-collapse="toggleCollapse" />
            </el-aside>

            <!-- 主内容区域 -->
            <el-container>
                <!-- 顶部导航栏 -->
                <el-header height="50px">
                    <div class="header-content">
                        <!-- 侧边栏折叠按钮 -->
                        <el-button type="text" icon="el-icon-s-fold" @click="toggleCollapse"
                            style="font-size: 18px;"></el-button>
                        <!-- 顶部右侧个人中心 -->
                        <div class="right-menu">
                            <el-dropdown @command="handleCommand" :disabled="!$store.state.user.userInfo.userName">
                                <span class="el-dropdown-link">
                                    <el-avatar size="small"
                                        src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"></el-avatar>
                                    <span style="margin-left: 5px;" v-if="$store.state.user.userInfo.userName">
                                        欢迎，{{ $store.state.user.userInfo.userName }}
                                    </span>
                                    <span style="margin-left: 5px;" v-else>
                                        未登录
                                    </span>
                                </span>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item command="profile">修改密码</el-dropdown-item>
                                    <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                                    <el-dropdown-item command="delete">注销账户</el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
                        </div>
                    </div>
                </el-header>

                <!-- 个人中心弹窗 -->
                <el-dialog title="个人中心" :visible.sync="dialogVisible" width="400px">
                    <el-form :model="userInfo" label-width="80px">
                        <el-form-item label="用户名">
                            <el-input v-model="userInfo.userName" placeholder="请输入新的用户名" style="width: 260px;"
                            @keyup.enter.native="onUsernameEnter" />
                        </el-form-item>
                        <el-form-item label="旧密码">
                            <el-input type="password" v-model="userInfo.oldPassword" placeholder="请输入原始密码" ref="oldPasswordInput"
                                style="width: 260px;" @keyup.enter.native="onOldPasswordEnter" />
                        </el-form-item>
                        <el-form-item label="新密码">
                            <el-input type="password" v-model="userInfo.newPassword" placeholder="请输入新的密码" ref="newPasswordInput"
                                style="width: 260px;" @keyup.enter.native="submitRule" />
                        </el-form-item>
                    </el-form>

                    <template #footer>
                        <el-button @click="dialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="submitRule">提交</el-button>
                    </template>
                </el-dialog>

                <!-- 页面主要内容 -->
                <el-main>
                    <router-view />
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>
  
<script>
import Sidebar from './components/Sidebar.vue'
import { changePasswordAPI, deleteUserAPI } from '@/api/user'
import { getMD5LowerCase } from '@/utils/encrypt'

export default {
    name: 'App',
    components: { Sidebar },
    data() {
        return {
            isCollapse: false,
            dialogVisible: false,
            userInfo: {
                userId: this.$store.state.user.userInfo.id,
                userName: this.$store.state.user.userInfo.userName,
                oldPassword: '',
                newPassword: ''
            }
        }
    },
    methods: {
        toggleCollapse() {
            this.isCollapse = !this.isCollapse
        },
        handleCommand(command) {
            console.log(command)
            if (command === 'logout') {
                this.logout();
            } else if (command === 'profile') {
                this.dialogVisible = true;
            } else if (command === 'delete') {
                this.deleteUser();
            }
        },
        deleteUser() {
            this.$confirm('确认注销账户吗？', "提示", {
                "confirmButtonText": "确定",
                "cancelButtonText": "取消",
                "type": "warning"
            })
                .then(() => {
                    deleteUserAPI(this.$store.state.user.userInfo.id).then(res => {
                        if (res.code === 1) {
                            this.$message.success('注销账户成功，请重新登录');
                            this.$store.dispatch('user/logout')
                            this.$router.push('/login')
                        } else {
                            this.$message.error(res.msg);
                        }
                    }).catch(err => {
                        console.log(err)
                        this.$message.error(err.msg);
                    })
                })
                .catch(() => {
                    console.log("用户取消注销账户")
                })
        },
        logout() {
            this.$confirm('确认退出登录吗？', "提示", {
                "confirmButtonText": "确定",
                "cancelButtonText": "取消",
                "type": "warning"
            })
                .then(() => {
                    console.log("用户确认退出登录")
                    this.$store.dispatch('user/logout')
                    this.$router.push('/login')
                })
                .catch(() => {
                    console.log("用户取消退出登录")
                })
        },
        submitRule() {
            if (this.userInfo.newPassword === '') {
                this.$message.error('新密码不能为空');
                return;
            }
            if (this.userInfo.oldPassword === '') {
                this.$message.error('旧密码不能为空');
                return;
            }
            if (this.userInfo.newPassword === this.userInfo.oldPassword) {
                this.$message.error('新密码不能和旧密码相同');
                return;
            }
            const params = { ...this.userInfo }
            params.oldPassword = getMD5LowerCase(params.oldPassword);
            params.newPassword = getMD5LowerCase(params.newPassword);
            changePasswordAPI(params).then(res => {
                if (res.code === 1) {
                    this.$message.success('修改密码成功，请重新登录');
                    this.$store.dispatch('user/logout')
                    this.$router.push('/login')
                    this.dialogVisible = false;
                } else {
                    this.$message.error(res.msg);
                }
            }).catch(err => {
                console.log(err)
                this.$message.error(err.msg);
            })
        },
        onUsernameEnter() {
            console.log('onUsernameEnter')
            if (!this.userInfo.oldPassword) {
                this.$refs.oldPasswordInput.focus();
            } else if (!this.userInfo.newPassword) {
                this.$refs.newPasswordInput.focus();
            } else {
                this.submitRule();
            }
        },
        onOldPasswordEnter() {
            if (!this.userInfo.newPassword) {
                this.$refs.newPasswordInput.focus();
            } else {
                this.submitRule();
            }
        },
    }
}
</script>
  
<style lang="scss">
html,
body {
    overflow: hidden;
    /* 禁用所有滚动 */
}

#app {
    font-family: Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
}

.el-header {
    background: #fff;
    box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
    z-index: 1;

    .header-content {
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 20px;
    }
}

.el-main {
    background: #f0f2f5;
    flex: 1;
}

.el-dropdown-link {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.el-container {
    height: 98vh;
    display: flex;
}</style>