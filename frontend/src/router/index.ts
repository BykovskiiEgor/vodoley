import { createRouter, createWebHistory } from 'vue-router'

const HomeView = () => import('../views/HomeView.vue')
const ProductDetailsView = () => import('../views/ItemView.vue')
const CartView = () => import('../views/CartView.vue')
const ProductsView = () => import('../views/ProductsView.vue')
const CategoriesView = () => import('../views/CategoriesView.vue')
const RecommendationsView = () => import('../views/RecommendationsView.vue')
const DiscountView = () => import('../views/DiscountView.vue')
const SearchItemsView = () => import('../views/SearchItemsView.vue')
const OrderView = () => import('../views/OrderView.vue')
const UserProfileView = () => import('../views/UserProfileView.vue')
const LoginView = () => import('../views/LogInView.vue')
const SearchByImageView = () => import('@/views/SearchByImageView.vue')
const AboutView = () => import('../views/AboutView.vue')



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,      
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,      
    },
    {
      path: '/current-items/:id',
      name: 'ProductDetails',
      component: ProductDetailsView,
      props: true,       
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView,
      props: true,      
    },
    {
      path: '/order',
      name: 'order',
      component: OrderView,
      props: true,      
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
    },
    {
      path: '/profile',
      name: 'profile',
      component: UserProfileView,
      props: true,
      meta: {        
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
    },

    {
      path: '/discounts',
      name: 'discounts',
      component: DiscountView,
      props: true,      
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
