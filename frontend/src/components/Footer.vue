<template>
  <footer class="footer py-5">
    <div class="container">
      <div class="footer-columns">
        <div class="year-name">
          <span>© {{ currentYear }} ИП Быковский А.И</span>
        </div>
        <div class="links">
          <router-link class="nav-link active" :to="{ name: 'home' }">Главная</router-link>          
          <router-link class="nav-link active" :to="{ name: 'about' }">О нас</router-link>
          <router-link class="nav-link active" :to="{ name: 'categories' }">Каталог</router-link> 
        </div>
        <div class="phone">
          <span>+7 (927) 940-25-32 </span>
        </div>
        <div class="warning">
          <span>Предложение не является публичной офертой. Цены на сайте и в розничной сети могут отличаться. Информация на сайте о товаре носит рекламный характер и расценивается как приглашение делать оферты на основании п.1 ст. 437 Гражданского кодекса РФ.</span>
        </div>
      </div>   
    </div>
  </footer>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Footer',
  data() {
    return {
      currentYear: new Date().getFullYear()
    };
  }
});
</script>

<style scoped>
.footer {
  background-color: #003464;
  margin-top: auto; 
}

.container{
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
  display: flex;
  flex-direction: column;  
}

.container span{
  color: white;
  font-size: 12px;
  font-weight: 100;
}

.footer-columns{
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 0.5fr 1fr 2fr;
  gap: 30px;
}

.links{
  display: flex;
  flex-direction: column;  
  color: white;
  font-size: 12px;
  font-weight: 100;
  gap: 5px;
}
</style>
