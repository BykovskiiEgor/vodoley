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
  import Navbar from '../components/Navbar.vue';
  import Footer from '../components/Footer.vue';
  import MobileMenu from '../components/MobileMenu.vue';
  import Pagination from '../components/Pagination.vue';
  import { useDiscounts } from '../composables/useDiscounts';
  import ItemCard from '../components/ItemCard.vue'

  const {
    products,
    currentPage, 
    totalPages,    
    cart,
    addToCart,
    increment,
    decrement,
    fetchProducts,
  } = useDiscounts();
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

  .text-decoration-line-through {
  text-decoration: line-through;
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
  