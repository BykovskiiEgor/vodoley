<template>
  <header>
    <Navbar />
  </header>  
  <div class="container"> 
    <div>
      <h3 style="margin-bottom: 32px;">Каталог</h3>
    </div>
    <div class="category-container">
      <div 
        class="category-card" 
        v-for="category in categories" 
        :key="category.id">   
          <div class="category-header">
            <router-link class="category-link" :to="`/products/${category.id}`">
              <img loading="lazy" class="category-image" :src="category.image ? category.image : '/images/waterdrop.png'" />
              <h5 style="margin-left: 10px; padding-bottom: 8px;">{{ category.name }}</h5>
            </router-link>            
          </div>
          <div v-if="category.children && category.children.length">
            <div class="children-list">
              <TreeNode 
                :children="category.children" 
                :max="5" 
                :collapsed-categories="collapsedCategories"
                @toggle-collapse="toggleCollapse"
                v-if="!collapsedCategories.includes(category.id)"
              />
            </div>      
          </div>
      </div>
    </div>
  </div>    
  <MobileMenu />
  <Footer />
</template>



<script setup lang="ts">
import { defineAsyncComponent } from 'vue';
const MobileMenu = defineAsyncComponent(() => import('../components/MobileMenu.vue'));
const Navbar = defineAsyncComponent(() => import('../components/Navbar.vue'));
const Footer = defineAsyncComponent(() => import('../components/Footer.vue'));
const TreeNode = defineAsyncComponent(() => import('../components/TreeNode.vue')); 
import { useCategories } from '@/composables/useCategories';


const {
  categories,
  collapsedCategories,
  toggleCollapse,
} = useCategories();

</script>

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.category-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
}


.category-image{
  width: 80px;
  height: 80px;
  object-fit: cover;
}

.category-link {
  text-decoration: none;
  color: inherit;
}

.section-header {
  margin-bottom: 40px;
}

.category-card {
  padding: 5px;
  margin-bottom: 20px;  
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

@media (max-width: 440px) {
  .category-container {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .category-card {
    padding: 10px;
    margin-bottom: 12px;
  }

  .category-image {
    width: 50px;
    height: 50px;
  }
}

@media (min-width: 441px) and (max-width: 767px) {
  .category-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .category-card {
    padding: 12px;
  }

  .category-image {
    width: 60px;
    height: 60px;
  }

}

@media (min-width: 768px) and (max-width: 1023px) {
  .category-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .category-container {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
