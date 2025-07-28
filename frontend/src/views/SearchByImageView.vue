<template>
    <div class="page-container">
          <header>
              <Navbar />
          </header>
          <div class="container px-4 px-lg-5">
              <!-- <div class="filter-container mb-4">
                  <form class="filter" @submit.prevent="(currentPage)">
                      <h5 style="padding-top: 5px;">Фильтры</h5>
                      <select v-model="filter" class="form-select">
                          <option>Все</option>
                          <option value="exists">В наличии</option>
                          <option value="not_exists">Под заказ</option>
                      </select>
                      <select v-model="sort" class="form-select">
                          <option>Без сортировки</option>
                          <option value="asc">Цена меньше</option>
                          <option value="desc">Цена больше</option>
                      </select>         
                  </form>
              </div> -->
          </div>
          <main class="content-wrap">
            <div class="container">
              <div class="row justify-content-center gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4">
                <div v-for="product in productsStore.products" :key="product.id" class="col mb-5">
                  <div class="card h-100">
                      <router-link :to="`/current-items/${product.id}`">
                        <img 
                          class="card-img-top" 
                          :src="product.images.length ? `http://127.0.0.1:8000${product.images[0].image}` : '/images/vodoley.jpg'" 
                          :alt="`Image for ${product.name}`"
                        />
                      </router-link>
                      <div class="card-body text-center p-4">
                          <h5 class="fw-bolder">{{ product.name }}</h5>
                          <div v-if="product.discount_percent > 0">
                              <div class="text-muted text-decoration-line-through">{{ product.price }}₽</div>
                              <div class="text-danger">{{ product.discount_price }}₽</div>
                          </div>
                          <div v-else>
                              <div>{{ product.price }}₽</div>
                          </div>
                      </div>
                      <div v-if="!product.available" class="text-center p-4">
                          <p class="text-danger">Нет в наличии</p>
                      </div>  
                      <div v-else>
                          <button v-if="!cart[product.id]" @click="addToCart(product)" class="btn btn-outline-dark mt-auto">
                              Добавить в корзину
                          </button>
                          <div v-else class="quantity-controls d-flex justify-content-between align-items-center">
                              <button @click="decrement(product)" class="btn">-</button>
                              <span>{{ cart[product.id].quantity }}</span>
                              <button @click="increment(product)" class="btn">+</button>
                          </div>    
                      </div>
                    </div>
                  </div>                                           
                </div>
              </div>
              <!-- <Pagination
              :currentPage="currentPage"
              :totalPages="totalPages"
              @page-changed="fetchProducts"
              /> -->
          </main>
          <footer>
              <Footer/>
          </footer>
          <MobileMenu />
      </div>
  </template>

<script setup lang="ts">
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import MobileMenu from '../components/MobileMenu.vue';
import { useSearchByImage } from '../composables/useSearchByImage';

const {
  products,
  cart,
  addToCart,
  increment,
  decrement,
  productsStore,
} = useSearchByImage();

import { useRoute } from 'vue-router';
import type { RouteLocationNormalized } from 'vue-router';
const route = useRoute() as RouteLocationNormalized & { state?: { products: any[] } };

const foundProducts = route.state?.products || []

</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-wrap {
  flex: 1;
}

.filter-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.filter {
  display: flex;
  gap: 10px;
}

.container {
  margin-top: 20px;
}

.card {
  border: 1px solid #ddd;
}

.card-header {
  background-color: #f7f7f7;
}

.form-select {
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #ddd;
  font-size: 16px;
}

.btn {
  padding: 5px 15px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;   
  width: 100%;
}

.category-link {
  text-decoration: none;
  color: inherit;
}

.category-link h5 {
  margin-bottom: 10px;
}

.category-card {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 20px;
  max-height: 400px;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.category-card:hover {
  overflow: auto;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.collapse-button {
  background-color: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
}

.collapse-button:focus {
  outline: none;
}
</style>
