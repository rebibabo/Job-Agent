<template>
    <el-menu
      :default-active="activeMenu"
      class="el-menu-vertical"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
      :collapse="isCollapse"
      :collapse-transition="false"
      router
    >
      
      <el-menu-item index="/homePage" @click="$emit('menu-click', '')">  <!-- 点击菜单栏时设置顶部导航栏的标题 -->
        <i class="el-icon-s-home"></i>
        <span slot="title">首页</span>
      </el-menu-item>

      <el-menu-item index="/search" @click="$emit('menu-click', '职位获取系统')">
        <i class="el-icon-s-data"></i>
        <span slot="title">职位获取</span>
      </el-menu-item>
      
      <el-menu-item index="/job" @click="$emit('menu-click', '职位查询系统')">
        <i class="el-icon-s-data"></i>
        <span slot="title">职位查询</span>
      </el-menu-item>

      <el-menu-item index="/analysis" @click="$emit('menu-click', '职位分析系统')">
        <i class="el-icon-s-data"></i>
        <span slot="title">职位分析</span>
      </el-menu-item>

      <el-menu-item index="/sendResume" @click="$emit('menu-click', '智能投递系统')">
        <i class="el-icon-s-data"></i>
        <span slot="title">智能投递</span>
      </el-menu-item>
 
    </el-menu>
  </template>
  
  <script>
  export default {
    name: 'AppSidebar',
    props: {
        isCollapse: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
        activeMenu: this.$route.path
        }
    },
    watch: {
      $route(newVal) {
        this.activeMenu = newVal.path
      }
    }
  }
  </script>
  
  <style lang="scss" scoped>
  .el-menu-vertical {
    min-height: 98vh;
    border-right: none;
    
    &:not(.el-menu--collapse) {
      width: 210px;
    }
  }
  
  .logo-container {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #2b2f3a;
    
    .logo {
      height: 32px;
    }
    
    .logo-mini {
      height: 24px;
    }
  }
  
  .el-menu-item.is-active {
    background-color: #263445 !important;
  }
  
  .el-submenu .el-menu-item {
    min-width: auto;
  }
  </style>