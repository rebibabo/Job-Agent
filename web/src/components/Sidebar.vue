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
      <!-- <div class="logo-container">
        <img v-if="!isCollapse" src="@/assets/logo.png" class="logo">
        <img v-else src="@/assets/logo-mini.png" class="logo-mini">
      </div> -->
      
      <el-menu-item index="/homePage">
        <i class="el-icon-s-home"></i>
        <span slot="title">首页</span>
      </el-menu-item>
      
      <el-menu-item index="/job">
        <i class="el-icon-s-data"></i>
        <span slot="title">职位查询</span>
      </el-menu-item>

      <el-menu-item index="/analysis">
        <i class="el-icon-s-data"></i>
        <span slot="title">职位分析</span>
      </el-menu-item>
      

      <!-- <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-s-order"></i>
          <span>订单管理</span>
        </template>
        <el-menu-item index="/order/list">订单列表</el-menu-item>
        <el-menu-item index="/order/statistics">订单统计</el-menu-item>
      </el-submenu> -->
      
      
      <!-- <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-user"></i>
          <span>用户管理</span>
        </template>
        <el-menu-item index="/user/list">用户列表</el-menu-item>
        <el-menu-item index="/user/group">用户分组</el-menu-item>
      </el-submenu>
      
      <el-menu-item index="/settings">
        <i class="el-icon-setting"></i>
        <span slot="title">系统设置</span>
      </el-menu-item> -->
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