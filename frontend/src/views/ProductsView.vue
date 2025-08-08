<template>  
    <header>
      <Navbar />
    </header>
    <div class="container">      
      <div class="columns-data" :class="{ 'single-column': !availableAttributes.length }">
        <div class="filters-column-container">                    
          <div v-if="showFilters" class="filters-content">
            <div v-if="availableAttributes.length" class="filter-container">                    
              <div v-for="(attr, index) in orderedAttributes" :key="index" class="filter-wrapper">
                <label :for="attr.name">{{ attr.name }}</label>
                <select 
                  :value="attributeFilters[attr.name] || 'Все'" 
                  @change="(e) => onAttributeFilterChange(attr.name, (e.target as HTMLSelectElement).value)"
                  class="form-select">
                  <option>Все</option>
                  <option v-for="value in attr.values" :key="value" :value="value">
                    {{ value }}
                  </option>
                </select>
              </div>                           
            </div>
            <div class='single-column-price-filter'>
              <label>Цена</label>
              <div class="single-column-price-inputs">
                <div class="price-input">
                  <label for="min-price" style="margin-right: 10px;">От</label>
                  <input
                    @input="handlePriceMinInput"
                    :value="priceMin"
                    type="text"
                    id="min-price"                    
                    :placeholder="priceMinPlaceholder"
                    />                  
                </div> 
                <div class="price-input">
                  <label for="max-price" style="margin-right: 10px;">До</label>
                  <input
                    @input="handlePriceMaxInput"
                    :value="priceMax"
                    type="text"                    
                    id="max-price"                    
                    :placeholder="maxPricePlaceholder"
                    />                  
                </div>   
              </div>                
            </div>
          </div>
        </div>        
        <div class="products-container">          
          <div class="sort-container">
            <button class="toggle-filters-btn" @click="showFilters = !showFilters">
              {{ showFilters ? 'Скрыть фильтры' : 'Показать фильтры' }}
            </button>
            <form class="sort">              
              <select v-model="filter" class="form-select">
                <option disabled value="">Наличие</option>
                <option value="">Все</option>
                <option value="exists">В наличии</option>
                <option value="not_exists">Под заказ</option>
              </select>
              <select v-model="sort" class="form-select">
                <option disabled value="">Цена</option>
                <option value="">Без сортировки</option>
                <option value="asc">Цена меньше</option>
                <option value="desc">Цена больше</option>
              </select>    
            </form>    
          </div>  
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
          v-model:currentPage="currentPage"
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
import { defineAsyncComponent } from 'vue';
const Navbar = defineAsyncComponent(() => import('../components/Navbar.vue'));
const Footer = defineAsyncComponent(() => import('../components/Footer.vue'));
const MobileMenu = defineAsyncComponent(() => import('../components/MobileMenu.vue'));
const Pagination = defineAsyncComponent(() =>  import('../components/Pagination.vue'));
import { useProducts } from '../composables/useProducts';
const ItemCard = defineAsyncComponent(() => import('../components/ItemCard.vue'));
import { watch, ref, computed } from 'vue';

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
  priceMin,
  priceMax,
  maxPricePlaceholder,
  priceMinPlaceholder,
  handlePriceMinInput,
  handlePriceMaxInput,
} = useProducts();

const showFilters = ref(false);

const orderedAttributes = computed(() => {
  return [...availableAttributes.value].sort((a, b) => 
    a.name.length - b.name.length
  );
});

function saveFiltersToSession() {  
  const filtersToSave = {
    filter: filter.value,
    sort: sort.value,
    priceMn: priceMin.value,
    priceMx: priceMax.value,
    attributeFilters: { ...attributeFilters.value },    
  };
  localStorage.setItem('savedFilters', JSON.stringify(filtersToSave));
}

watch([filter, sort], () => {
  saveFiltersToSession();
  fetchProducts(currentPage.value);
});

watch([priceMax, priceMin], () => {
  saveFiltersToSession();
});

function onAttributeFilterChange(name: string, value: string | null) {
  if (value === null) return; 

  const newFilters = { ...attributeFilters.value };
  if (value === 'Все') {
    delete newFilters[name];
  } else {
    newFilters[name] = value;
  }
  attributeFilters.value = newFilters;

  saveFiltersToSession();
  fetchProducts(1);
}

watch(attributeFilters, saveFiltersToSession, { deep: true });
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
  grid-template-rows: auto;
  gap: 40px;
  align-items: start;
}

.columns-data.single-column {
  grid-template-columns: 1fr;
}

.toggle-filters-btn {
  background-color: #002a51;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;  
}

.filters-content {
  transition: all 0.3s ease;
  overflow: hidden;
}

.price-filter-container{
  display: flex;
  flex-direction: row;
  margin-top: 10px;
}

.price-inputs{
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.price-input input {
  border: none;
  border-bottom: 1px solid #003464;
  outline: none;
  width: 110px;
}

.apply-price-btn{
  margin-top: 10px;
  background-color: #002a51;;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer; 
  width: 190px;
}

.filter {
  display: flex;
  gap: 4px;
  flex-direction: column;
}

.sort-container{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
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
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: scale(0.98);
}

.clear-btn{
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.item-container{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

.single-column-price-filter{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: start;
  margin-top: 20px;
}

.single-column-price-inputs{
  display: flex;
  gap: 10px;
  flex-direction: row;
  margin-left: 10px;
}

.filters-column-container{
  display: flex;
  flex-direction: column;
}

.filter-container{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
}

.selected-attribute {
  background: #f0f0f0;
  padding: 5px 10px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.filter-wrapper{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

@media (max-width: 440px) {
  .item-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .columns-data {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .filter-container {
    grid-template-columns: 1fr;
    padding: 10px;
    margin-bottom: 5px;
  }
  
  .sort-container {
    flex-direction: row;
    align-items: stretch;
  }
  
  .sort {
    flex-direction: column;
    width: 100%;
  }
  
  .price-inputs {
    flex-direction: column;
  }

  .single-column-price-filter{
    padding: 10px;
    margin-top: 0px;
  }

  .toggle-filters-btn{
    padding: 4px 8px;
    font-size: 14px;
    margin-right: 5px;
  }

  .sort-container{
    margin-bottom: 10px;
  }

  .form-select{
    padding: 4px 8px;    
  }
  
 
}

@media (min-width: 441px) and (max-width: 767px) {
  .item-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .filter-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .item-container {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .filter-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .item-container {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .filter-container {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>