<template>
  <div class="navbar-wrapper">
    <div class="navbar-container">
      <div class="navbar-left">
        <router-link class="navbar-brand" :to="{ name: 'home' }">
          <IconLogo style="height: 30px; width: 80px; margin-top: 2px;" />
        </router-link>        
        <form class="search-container" @submit.prevent="search" :class="{ expanded: isExpanded, compact: isCompactMode}">
          <input type="search"
                 class="form-control search-input"
                 placeholder="Поиск..."
                 aria-label="Search"
                 v-model="searchQuery"
                 @input="onChange"
                 @keyup.enter="search"
                 @focus="expandSearch"
                 @blur="collapseSearch">
            <button type="button" class="search-button" @click="search">
              <SearchIcon />
            </button>            
          <div class="search-results" v-if="isExpanded && searchQuery">
            <ul class="search-list" v-if="products.length > 0">
              <li class="search-result-item" v-for="product in products" :key="product.id"
                  @click="goToProduct(product.id)">
                {{ product.name }}
              </li>
            </ul>
            <div v-if="products.length === 0 && searchQuery.trim()" class="search-no-results">
              Нет результатов
            </div>
          </div>          
        </form>
         
         
      </div>
      <div class="navbar-center">
        <div class='d-none d-md-flex justify-content-center gap-3 flex-grow-1'>
          <router-link class="nav-link active" :to="{ name: 'home' }">Главная</router-link>          
          <router-link class="nav-link active" :to="{ name: 'about' }">О нас</router-link>
          <router-link class="nav-link active" :to="{ name: 'categories' }">Каталог</router-link>
        </div>        
      </div>
      <div class="navbar-right">
        <div class='d-none d-md-flex justify-content-center gap-3 flex-grow-1'>
          <div class="navbar-icons">
          <router-link :to="{ name: 'cart' }" class="cart-icon">
            <CartIcon style="width: 35px; height: 35px;" />
            <span v-if="counter.count > 0" class="count-counter">
              <span class="count-counter-number">
                {{counter.count}}
              </span>
            </span>            
          </router-link>
          <router-link :to="{ name: 'profile' }" class="profile-icon">
            <IconProfile style="width: 30px; height: 30px;" />
          </router-link>
        </div>
        </div>        
      </div>
    </div>
  </div>
  <UploadPhoto v-model:showModal="showModal" />
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import IconLogo from './icons/IconLogo.vue';
import IconProfile from "./icons/IconProfile.vue";
import SearchIcon from './icons/SearchIcon.vue';
import SearchByPhotoIcon from './icons/SearchByPhotoIcon.vue';
import CartIcon from './icons/IconCart.vue'
import { useNavbar } from "../composables/useNavbar";
import { useCounterStore } from '@/stores/counter';
import UploadPhoto from './UploadPhoto.vue';

const counter = useCounterStore();

const isExpanded = ref(false);
const isCompactMode = ref(false);

const showModal = ref(false);


const expandSearch = () => {
  if (!isCompactMode.value) isExpanded.value = true;
};

const toggleCompactMode = () => {
  isCompactMode.value = !isCompactMode.value;
  isExpanded.value = false;
};

const collapseSearch = () => {
  if (!searchQuery.value && !isCompactMode.value) {
    isExpanded.value = false;
  }
};

const {
  searchQuery,
  products,
  user,
  userNull,
  onChange,
  search,
  goToProduct,
  cartCount,
  uniqueCount
  } = useNavbar();
</script>

<style scoped>
.navbar-wrapper {
  display: flex;
  align-items: center;
  width: inherit;
  height: 88px;
  background-color: var(--bs-body-bg);
}

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  height: 65%;
  padding: 0 20px;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 15px;
  height: 100%;
  width: 50%;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 20%;
  height: 100%;
}

.navbar-center{
  display: flex;
  align-items: center;
  width: 30%;
  height: 100%;  
}


.navbar-brand {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  text-decoration: none;
}

.search-container {
  display: flex;
  align-items: center;
  position: relative;
  height: 80%;
  width: 100%;
  max-width: 400px;
  transition: max-width 0.3s ease;
}

.search-container.expanded {
  max-width: 600px; 
}

.search-container.compact {
  max-width: 150px;
  margin-left: auto;
}

.extra-buttons {
  display: flex;
  gap: 10px;
  position: absolute;
  left: 100%;
  transform: translateX(10px);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.extra-buttons .extra-btn {
  background: #0464bd;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  color: white;
  font-weight: bold;
  transition: background 0.3s ease;
}

.extra-buttons .extra-btn:hover {
  background: #034a8a;
}

.search-input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
  width: 100%;
  height: 100%;
  transition: width 0.3s ease;
  padding-right: 40px;
}

.search-button {
  background-color: inherit;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  position: absolute;
  right: 1px;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  max-height: 300px;
  overflow-y: auto;
  z-index: 1000;  
  margin-top: 5px;
}

.search-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.search-result-item {
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-result-item:hover {
  background-color: #f0f0f0;
}

.search-no-results {
  padding: 10px;
  color: #666;
  text-align: center;
}

.custom-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  background-color: #0464bd;
  transition: background-color 0.3s ease;
  height: 80%;
}

.custom-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.navbar-icons{
  display: flex;
  align-items: center;
  justify-content: end;
  gap: 20px;
  flex-grow: 1;
}

.cart-icon{
  text-decoration: none !important;
  position: relative;
}

.count-counter{
  text-decoration: none !important;
  color: white;
  position: absolute;
  background-color: #003464;
  height: 15px;
  width: 15px;
  border-radius: 100vmin;
  display: flex;
  align-items: center;
  justify-content: center;
  bottom: 2px;   
  right: -5px;     
  font-size: 10px;
  
}

.count-counter-number{
  transform: translateY(-0.5px);
}

.icon-container {
  width: 40px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  --i-size: 24px;
  --i-color: currentColor;
  --i-s-width: 1.5;
}

.icon-container svg {
  width: 100%;
  height: 100%;
}

.sbib{
  background: none;
  border:none;
  padding: 0;
}

@media (max-width: 767px) {
  .navbar-left {
    width: 100%; 
    justify-content: space-between; 
  }

  .search-container {
    width: 100%; 
  }

  .search-input {
    width: 100%; 
  }
  .navbar-center{
    display: none;
  }

  .navbar-right{
    display: none;
  }
}
</style>