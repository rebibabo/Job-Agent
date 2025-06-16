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
                            <el-dropdown @command="handleCommand">
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
                                    <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                                    <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
                        </div>
                    </div>
                </el-header>

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

export default {
    name: 'App',
    components: { Sidebar },
    data() {
        return {
            isCollapse: false
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
                console.log("进入个人中心");
            }
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
        }
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
}
</style>