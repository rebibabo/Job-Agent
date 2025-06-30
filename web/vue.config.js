const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/api": {
        // 匹配所有以 /api 开头的请求
        target: "http://localhost:8081", // 目标服务器地址
        changeOrigin: true, // 改变请求头中的 Host 为目标地址
        pathRewrite: {
          "^/api": "", // 去掉路径中的 /api 前缀
        },
      },
      "/crawl": {
        target: "http://localhost:5000",
        changeOrigin: true,
        pathRewrite: {
          "^/crawl": "",
        },
      },
    },
  },
});
