<template>
  <div class="item-card ">
      <router-link :to="`/current-items/${product.id}?page=${currentPage}`" @click="saveScrollPosition">
        <div class="image-container">
          <img class="item-img" :src="product.images.length ? product.images[0].image : '/images/vodoley.jpg'" :alt="`Image for ${product.name}`"/>
        </div>
      </router-link>
      <div class="card-body">
          <span class="item-article">Арт. {{product.article}}</span>
          <h5 class="item-name">{{ product.name }}</h5>
          <span class="item-rating" v-if="parseFloat(product.avg_rating) > 0">                
            <star-rating class="star-rating" :rating="parseFloat(product.avg_rating)" :read-only="true" :star-size="15" />                
          </span>
          <span v-else class="none-rating"></span>
          <span class="item-status" :class="quantityStatusClass(product.quantity_status)">
            {{ product.quantity_status }}
          </span>
          <span class="item-price-container" v-if="product.discount_percent > 0">
              <div class="text-muted text-decoration-line-through">{{ product.price }}₽</div>
              <div class="text-danger">{{ product.discount_price }}₽</div>
          </span>
          <span class="item-price-container" v-else>
              <div class="item-price">{{ product.price }}₽</div>
          </span>              
      </div>          
      <div v-if="!product.available || product.quantity === 0" class="not-available">
        <button disabled>                               
              В корзину
          </button>
      </div>  
      <div v-else class="buttons-cintainer"> 
          <button v-if="!cart[product.id]" @click="addToCart(product)" class="add-to-cart">                               
              В корзину
          </button>
          <div v-else class="quantity-control">
              <button @click="decrement(product)"><IconMinus/></button>
              <span>{{ cart[product.id].quantity }}</span>
              <button @click="increment(product)"><IconPlus/></button>
          </div>    
      </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';
// @ts-ignore
import StarRating from 'vue-star-rating';
import IconPlus from './icons/IconPlus.vue';
import IconMinus from './icons/IconMinus.vue';

export default defineComponent({
  components: {
    StarRating,
    IconPlus,
    IconMinus,
  },
  name: 'ItemCard',
  props: {
    // products: {
    //   type: Array as PropType<Array<any>>,
    //   required: true
    // },
    product: {
      type: Object as PropType<any>,
      required: true
    },
    cart: {
      type: Object as PropType<{ [key: string]: any }>,
      required: true
    },
    currentPage: {
      type: Number,
      required: true
    },
    sort: {
      type: String,
      required: false,
      default: ''
    },
    attributeFilters: {
      type: Object as PropType<{ [key: string]: any }>,
      required: false,
      default: () => ({})
    },
    filter: {
      type: String,
      required: false,
      default: ''
    },
  },
  methods: {
    addToCart(product: any) {
      this.$emit('add-to-cart', product);
    },
    increment(product: any) {
      this.$emit('increment', product);
    },
    decrement(product: any) {
      this.$emit('decrement', product);
    },
    quantityStatusClass(status: string) {
      if (status === 'В наличии') return 'in-stock';
      if (status === 'Скоро закончится') return 'less-in-stock';
      if (status === 'Много') return 'text-success';
      return '';
    },

    saveScrollPosition() {
      localStorage.setItem("scrollY", window.scrollY.toString());       
    },
  }
});
</script>

<style scoped>
::v-deep(.star-rating svg) {  
  display: flex;
}

.in-stock{
  color: #217F0E
}

.less-in-stock{
  color: #C8790B
}

*:disabled {
  background-color: #00346475;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;  
  margin-top: auto;
  opacity: 1;
}

/* .item-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
} */

.image-container {
  height: 200px; 
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 5px;
}

.item-img {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
}

.item-card {
  display: flex;
  flex-direction: column; 
  gap: 10px;
  padding-bottom: 20px;
  max-height: 430px;
}

.card-body {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.item-article{
  font-size: 12px;
  opacity: 60%;
  margin-bottom: 4px;
}

.item-name {
  font-size: 16px;
  margin-bottom: 1px;
  text-align: left; 
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis; 
}

.item-rating{
  display: flex;
  align-items: center;  
  margin-bottom: 16px;
  justify-content: left;  
}

.none-rating{
  margin-bottom: 16px;
}

.star-rating{
  margin: 0;
}

.item-status{
  margin-top: auto;
  display: block;
  font-size: 12px;
}

.item-price-container {
  margin-bottom: 11px;
}

.item-price-container div{
  font-weight: 650;
  font-size: 16px;
}

.buttons-cintainer{
  display: flex;
}

.not-available{
  display: flex;
  justify-content: start; 
  align-items: center; 
  margin-top: auto; 
  height: 40px;   
}

.add-to-cart{
  background-color: #003464;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;  
  margin-top: auto;
}

.quantity-control{
  background-color: #003464;
  color: #fff;
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  margin-top: auto;
  display: flex;
  justify-content: start; 
  align-items: center; 
  margin-top: auto; 
  height: 40px;   
}

.quantity-control button{
  background-color: #003464;
  color: #fff;
  border: none; 
  display: flex; 
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: center;
}

.quantity-control span{
  padding-left: 22px;
  padding-right: 22px;
  display: flex; 
} 

@media (max-width: 440px) {
  /* .item-container {
    grid-template-columns: repeat(2, 1fr);    
  }   */

  .item-img {
    width: 140px;
    height: 140px;
  }
}

@media (min-width: 441px) and (max-width: 767px) {
  /* .item-container {
    grid-template-columns: repeat(2, 1fr);   
  } */

  .item-img {
    width: 180px;
    height: 180px;
  }

}

@media (min-width: 768px) and (max-width: 1023px) {
  /* .item-container {
    grid-template-columns: repeat(3, 1fr);
  } */
}

@media (min-width: 1024px) {
  /* .item-container {
    grid-template-columns: repeat(4, 1fr);
  } */
}
</style>
