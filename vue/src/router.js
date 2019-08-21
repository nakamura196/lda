import Vue from 'vue';
import Router from 'vue-router';
import Index from './pages/Index.vue';
import SearchByPage from './pages/SearchByPage.vue';
import ListByPage from './pages/ListByPage.vue';

import SearchByPage4saga from './pages/SearchByPage4saga.vue';
import ListByPage4saga from './pages/ListByPage4saga.vue';

import Text from './pages/Text.vue';
import Text4saga from './pages/Text4saga.vue';

import Main from './pages/Main.vue';

import Saga from './pages/Saga.vue';
import Edit from './pages/Edit.vue';

import Viewer from './pages/Viewer.vue';

import SearchByWork from './pages/SearchByWork.vue';
import ListByWork from './pages/ListByWork.vue';

import Landing from './pages/Landing.vue';
import Login from './pages/Login.vue';
import Profile from './pages/Profile.vue';
import MainNavbar from './layout/MainNavbar.vue';
import MainFooter from './layout/MainFooter.vue';

Vue.use(Router);

export default new Router({
  linkExactActiveClass: 'active',
  routes: [
    {
      path: '/',
      name: 'index',
      components: { default: Index, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/text',
      name: 'text',
      components: { default: Text, header: MainNavbar, footer: MainFooter },
      props: {
        //header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/text4saga',
      name: 'text4saga',
      components: { default: Text4saga, header: MainNavbar, footer: MainFooter },
      props: {
        //header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/saga',
      name: 'saga',
      components: { default: Saga, header: MainNavbar, footer: MainFooter },
      props: {
        //header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/edit',
      name: 'edit',
      components: { default: Edit, header: MainNavbar, footer: MainFooter },
      props: {
        //header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/searchByPage',
      name: 'searchByPage',
      components: { default: SearchByPage, header: MainNavbar, footer: MainFooter },
      props: {
        //header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/listByPage',
      name: 'listByPage',
      components: { default: ListByPage, header: MainNavbar, footer: MainFooter },
      props: {
        //header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/searchByPage4saga',
      name: 'searchByPage4saga',
      components: { default: SearchByPage4saga, header: MainNavbar, footer: MainFooter },
      props: {
        //header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/listByPage4saga',
      name: 'listByPage4saga',
      components: { default: ListByPage4saga, header: MainNavbar, footer: MainFooter },
      props: {
        //header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/searchByWork',
      name: 'searchByWork',
      components: { default: SearchByWork, header: MainNavbar, footer: MainFooter },
      props: {
        //header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/listByWork',
      name: 'listByWork',
      components: { default: ListByWork, header: MainNavbar, footer: MainFooter },
      props: {
        //header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/landing',
      name: 'landing',
      components: { default: Landing, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    },
    {
      path: '/login',
      name: 'login',
      components: { default: Login, header: MainNavbar },
      props: {
        header: { colorOnScroll: 400 }
      }
    },
    {
      path: '/profile',
      name: 'profile',
      components: { default: Profile, header: MainNavbar, footer: MainFooter },
      props: {
        header: { colorOnScroll: 400 },
        footer: { backgroundColor: 'black' }
      }
    }
  ],
  scrollBehavior: to => {
    if (to.hash) {
      return { selector: to.hash };
    } else {
      return { x: 0, y: 0 };
    }
  }
});
