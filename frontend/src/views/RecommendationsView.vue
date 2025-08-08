<template>
  <div class="page-container">
    <header>
      <Navbar />
    </header>
    <main class="content-wrap">
      <div class="container">
        <TransitionGroup name="fade" tag="div" class="item-container">
              <ItemCard
                v-for="product in products"
                :key="product.id"
                :product="product"
                :cart="cart"
                :currentPage="currentPage"
                @add-to-cart="addToCart"
                @increment="increment"
                @decrement="decrement"
              />
            </TransitionGroup>
      </div>
      <Pagination
        :currentPage="currentPage"
        :totalPages="totalPages"
        @page-changed="fetchProducts"
        />
    </main>
    <footer>
      <Footer/>
    </footer>
    <MobileMenu />
  </div>
</template>


<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const Navbar = defineAsyncComponent(() => import('../components/Navbar.vue'));
const Footer = defineAsyncComponent(() => import('../components/Footer.vue'));
const MobileMenu = defineAsyncComponent(() => import('../components/MobileMenu.vue'));
const Pagination = defineAsyncComponent(() => import('../components/Pagination.vue'));
import { useRecommendations } from '../composables/useRecommendations';
const ItemCard = defineAsyncComponent(() => import('../components/ItemCard.vue'));

const {
  products,
  currentPage, 
  totalPages,  
  cart,
  addToCart,
  increment,
  decrement,
  fetchProducts,
} = useRecommendations();
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



.container {
  margin-top: 20px;
}

.item-container{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 440px) {
  .item-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
}

@media (min-width: 441px) and (max-width: 767px) {
  .item-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .item-container {
    grid-template-columns: repeat(3, 1fr);
  }  
}

@media (min-width: 1024px) {
  .item-container {
    grid-template-columns: repeat(4, 1fr);
  }
}

</style>
    