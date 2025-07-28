<template>  
    <header>
      <Navbar />
    </header>
    <div class="container">
      <div class="columns-data" :class="{ 'single-column': !availableAttributes.length }">
        <div v-if="availableAttributes.length" class="filter-container">                    
          <div  v-for="(attr, index) in availableAttributes" :key="index">
            <label :for="attr.name">{{ attr.name }}</label>
            <select 
              v-model="attributeFilters[attr.name]" 
              @change="fetchProducts(currentPage)"
              class="form-select"
            >
              <option value="">Все</option>
              <option v-for="value in attr.values" :key="value" :value="value">
                {{ value }}
              </option>
            </select>
          </div>                     
        </div>
        <div class="products-container">
          <!-- <div class="sort-container">
            <form class="sort" @submit.prevent="fetchProducts(currentPage)">              
              <select v-model="filter" class="form-select">
                <option disabled value="">Наличие</option>
                <option>Все</option>
                <option value="exists">В наличии</option>
                <option value="not_exists">Под заказ</option>
              </select>
              <select v-model="sort" class="form-select">
                <option disabled value="">Цена</option>
                <option>Без сортировки</option>
                <option value="asc">Цена меньше</option>
                <option value="desc">Цена больше</option>
              </select>    
            </form>    
          </div>   -->
          <div class="filter-attributes-container">                  
            <template v-for="(value, key) in attributeFilters" :key="key">
              <div v-if="value" class="selected-attribute">
                <strong>{{ key }}:</strong> {{ value }}
                <button
                  type="button"
                  @click="clearFilter(key)"
                  class="clear-btn"
                >
                  ✕
                </button>
              </div>
            </template>
          </div>       
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
          <Pagination
          class="pagin"
          :currentPage="currentPage"
          :totalPages="totalPages"
          @page-changed="fetchProducts"
        />           
        </div>        
      </div>            
    </div>          
    <footer>
      <Footer/>
    </footer>
    <MobileMenu />
</template>
  
  <script setup lang="ts">
  import Navbar from '../components/Navbar.vue';
  import Footer from '../components/Footer.vue';
  import MobileMenu from '../components/MobileMenu.vue';
  import Pagination from '../components/Pagination.vue';
  import { useSearch } from '../composables/useSearch';
  import ItemCard from '../components/ItemCard.vue';
  
  const {
    products,
    currentPage, 
    totalPages,
    filter,
    sort,
    cart,
    addToCart,
    increment,
    decrement,
    fetchProducts,
    availableAttributes,
    attributeFilters,
    clearFilter,
  } = useSearch();
  </script>
  
  <style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.columns-data{
  display: grid;
  grid-template-columns: minmax(150px, 180px) 1fr;
  gap: 40px;
}

.columns-data.single-column {
  grid-template-columns: 1fr;
}

.filter-container {
  display: flex;
  flex-direction: column;
}

.filter {
  display: flex;
  gap: 4px;
  flex-direction: column;
}

.sort-container{
  display: flex;
  flex-direction: row;
  justify-content: end;
  margin-bottom: 20px;
}

.sort{
  display: flex;
  gap: 4px;
}

.pagin{
  margin-top: 30px;
}

.filter-attributes-container{
  display: flex;  
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
  