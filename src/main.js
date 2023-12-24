import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue'

import homepage from './homepage.vue';
import demoPage from './demoPage.vue';

// 定义根组件


// 定义路由
const routes = [
  {
    path: '/',
    component: homepage,
    meta: { title: 'homepage' }
  },
  {
    path: '/demopage',
    component: demoPage,
    meta: { title: 'demopage' }
  },
];

// 创建路由器
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 创建Vue应用
const app = createApp(App);

// 使用路由器
app.use(router);

// 挂载应用
app.mount('#app');
