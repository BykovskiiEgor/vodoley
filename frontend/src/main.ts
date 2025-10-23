import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia';
import App from './App.vue'
import router from './router';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useCounterStore } from '@/stores/counter';
import { vMaska } from 'maska/vue';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { useProductsStore } from '@/stores/productsStore'

const app = createApp(App);
const pinia = createPinia();


app.use(pinia);
pinia.use(piniaPluginPersistedstate)
app.use(router);
app.directive('maska', vMaska)

app.mount('#app')

const counter = useCounterStore();
counter.updateCountFromCart();

const productsStore = useProductsStore()