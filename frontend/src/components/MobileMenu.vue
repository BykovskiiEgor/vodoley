<template>
    <div class="menu-container" v-if="isMobile">
      <router-link to="/" aria-label="Главная" class="menu-item">
        <div class="menu-icon">
            <HomeIcon/>
        </div>
        <span class="menu-label">Главная</span>
      </router-link>
      <router-link to="/cart" aria-label="Корзина" class="menu-item">
        <div class="menu-icon">         
          <IconCart/>
        </div>
        <span class="menu-label">Корзина</span>
      </router-link>  
      <router-link to="/categories" aria-label="Мой список" class="menu-item">
        <div class="menu-icon">
            <ItemsIcon/>
        </div>
        <span class="menu-label">Товары</span>
      </router-link>
      <!-- <router-link to="/profile" aria-label="Личный кабинет" class="menu-item">
        <div class="menu-icon">
            <IconProfile/>
        </div>
        <span class="menu-label">Профиль</span>
      </router-link>        -->
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import IconCart from './icons/IconCart.vue';
  import ItemsIcon from './icons/ItemsIcon.vue';
  import HomeIcon from './icons/HomeIcon.vue';
  import IconProfile from './icons/IconProfile.vue';
  
  const isMobile = ref(false);
  
  function checkScreenSize() {
    isMobile.value = window.innerWidth <= 1022;
  }
  
  onMounted(() => {
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
  });
  </script>
  
  <style scoped>
.menu-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around; 
  align-items: center;
  background-color: #ffff;
  box-shadow: 0 -2px 5px rgba(0,0,0,0.1); 
  padding: 8px 0;
  z-index: 1000; 
}

  .menu-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: var(--text-minor);
    text-decoration: none;
    font-size: 12px;
  }
  
  .menu-item:hover {
    color: var(--text-primary);
  }
  
  .menu-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 4px;
    --i-size: 24px;
  }
  
  .menu-icon svg {
    width: var(--i-size);
    height: var(--i-size);
  }
  
  .menu-label {
    display: block;
    font-size: 10px;
  }
  </style>
  