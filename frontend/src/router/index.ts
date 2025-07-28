import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductDetailsView from '../views/ItemView.vue'
import CartView from '../views/CartView.vue'
import ProductsView from '../views/ProductsView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import RecommendationsView from '../views/RecommendationsView.vue'
import DiscountView from '../views/DiscountView.vue'
import SearchItemsView from '../views/SearchItemsView.vue'
import OrderView from '../views/OrderView.vue'
import UserProfileView from '../views/UserProfileView.vue'
import LoginView from '../views/LogInView.vue'
import SearchByImageView from '@/views/SearchByImageView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        breadcrumb: 'Главная',
      },
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
      meta: {
        breadcrumb: 'О нас',
      },
    },
    {
      path: '/current-items/:id',
      name: 'ProductDetails',
      component: ProductDetailsView,
      props: true 
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView,
      props: true,
      meta: {
        breadcrumb: 'Корзина',
      },
    },
    {
      path: '/order',
      name: 'order',
      component: OrderView,
      props: true,
      meta: {
        breadcrumb: 'Заказ',
      }, 
    },
    {
      path: '/products/:categoryID',
      name: 'products',
      component: ProductsView,
      props: true,      
    },
    {
      path: '/categories',
      name: 'categories',
      component: CategoriesView,
      props: true, 
      meta: {
        breadcrumb: 'Каталог',
      }, 
    },
    {
      path: '/profile',
      name: 'profile',
      component: UserProfileView,
      props: true,
      meta: {
        breadcrumb: 'Профиль',
        requiresAuth: true 
      },
      beforeEnter: (to, from, next) => {
        const user = localStorage.getItem('user');
        
        if (!user) {
          next({ name: 'auth' }); 
        } else {
          next();
        }
      }
    },
    {
      path: '/auth',
      name: 'auth',
      component: LoginView,
      props: true 
    },

    {
      path: '/recommendations',
      name: 'recommendations',
      component: RecommendationsView,
      props: true, 
      meta: {
        breadcrumb: 'Рекомендации',
      }, 
    },

    {
      path: '/discounts',
      name: 'discounts',
      component: DiscountView,
      props: true,
      meta: {
        breadcrumb: 'Скидки',
      }, 
    },
    
    {
      path: '/search',
      name: 'search',
      component: SearchItemsView,
      props: route => ({ query: route.query.q })
    },

    {
      path: '/search-by-image',
      name: 'search-by-image',
      component: SearchByImageView,     
    },
  ]
})

export default router
