<template>
  <header>
    <Navbar />
  </header>
  <div class="container">    
    <div v-if="cartEmpty" class="empty">
      <span> В корзине пусто</span>
      <span> Перейдите в каталог, чтобы <br> добавить нужные товары</span>      
      <router-link class="catalog-link" :to="{ name: 'categories' }">
        <button class="catalog-button">
          Каталог
        </button>
      </router-link>
    </div>
    <div v-else class="cart-container">
      <div class="products-column">
        <div class="name-clean-container">
          <h3>Корзина</h3>
          <button class="clean-cart" @click="clearCart">Очистить <IconTrash/></button>          
        </div>
        <div class="names">
          <span class="cell-text">Товар</span>
          <span></span>  
          <div class="price-quantity-container">
            <div class="wrapper">
              <span class="cell-text">Цена</span>
            </div>
            <div class="wrapper">
              <span class="cell-text">Количество</span>
            </div>
            <div class="wrapper">
              <span class="cell-text" style="margin-right: 12px;">Итог</span>
            </div>                        
          </div>        
        </div>
        <div class="product-card" v-for="product in products" :key="product.id">   
          <span class="border-line"></span>   
          <div class="product-card-wrapper">
            <div class="image-container">
              <img class="item-img" :src="product.images.length ? product.images[0].image : '/images/vodoley.jpg'" :alt="`Image for ${product.name}`"/>
            </div>
            <div class="product-info">
              <span class="item-article">Арт. {{product.article}}</span>
              <h5 class="item-name">{{ product.name }}</h5>                                                                   
            </div>
            <div class="price-quantity-container">
              <div class="item-price-wrapper">
                <span class="item-price-container" v-if="product.discount_price ?? 0 >  0">
                <div class="text-muted text-decoration-line-through">{{ product.price }} ₽</div>
                <div class="text-danger">{{ product.discount_price }} ₽</div>
                </span>
                <span class="item-price-container" v-else>
                    <div class="item-price">{{ product.price }} ₽</div>
                </span> 
              </div>   
              <div class="quantity-control-wrapper">         
                <div class="quantity-control">
                    <button @click="decrement(product)"><IconMinusBlack/></button>
                    <span>{{ products[product.id].quantity }}</span>
                    <button @click="increment(product)"><IconPlusBlack/></button>
                </div> 
              </div>    
              <div class="total-price-wrapper">           
                <span>{{ calculatedPrices.items.find(item => item.id === product.id)?.itemTotal || 0 }} ₽</span>
              </div> 
            </div>
            <div>
              <div class="del-button-wrappper">
                <button class="del-button" @click="removeFromCart(product.id)">
                  <IconTrash/> 
                </button>
              </div>              
            </div>
          </div>                                                 
        </div>
        <div v-if="isMobile" class="for-mobile" v-for="product in products" :key="product.id">
          <span class="border-line"></span>   
          <div class="product-card-wrapper-mobile">
            <div class="image-container">
              <img class="item-img" :src="product.images.length ? product.images[0].image : '/images/vodoley.jpg'" :alt="`Image for ${product.name}`"/>
            </div>
            <span class="mobile-wrapper">
              <div class="product-info-mobile">
                <span class="item-article">Арт. {{product.article}}</span>
                <h5 class="item-name">{{ product.name }}</h5>                                                                   
              </div>
              <div class="price-quantity-container">
                <!-- <div class="item-price-wrapper">
                  <span class="item-price-container" v-if="product.discount_price ?? 0 >  0">
                  <div class="text-muted text-decoration-line-through">{{ product.price }} ₽</div>
                  <div class="text-danger">{{ product.discount_price }} ₽</div>
                  </span>
                  <span class="item-price-container" v-else>
                      <div class="item-price">{{ product.price }} ₽</div>
                  </span> 
                </div>    -->
                <span class="quantity-wrapper">
                  <div class="quantity-control-wrapper">         
                  <div class="quantity-control">
                      <button @click="decrement(product)"><IconMinusBlack/></button>
                      <span>{{ products[product.id].quantity }}</span>
                      <button @click="increment(product)"><IconPlusBlack/></button>
                  </div> 
                </div>    
                <div class="total-price-wrapper">           
                  <span class="total-price">{{ calculatedPrices.items.find(item => item.id === product.id)?.itemTotal || 0 }} ₽</span>
                </div> 
                </span>                
              </div>              
            </span>           
            <div class="del-button-wrapper-mobile">
              <button class="del-button" @click="removeFromCart(product.id)">
                <IconNoBlack/> 
              </button>
            </div>                                      
          </div>               
        </div>
        <span class="border-line"></span>   
      </div>      
      <div class="make-order-buttons">
        <div class="mob-container">
          <span class="text-allprice-wrapper">
            <span class="text-allprice">Итого</span>
            <span>{{ calculatedPrices.total }} ₽</span>
          </span>          
          <div class="make-order-wrapper">
            <router-link class="make-order-rl" :to="{ name: 'order' }">
              <button class="make-order">Оформить заказ</button>
            </router-link>
          </div>          
        </div>
      </div>
    </div>
  </div>
  <MobileMenu />
</template>

<script setup lang="ts">
import { defineAsyncComponent } from 'vue';
import { onMounted } from 'vue';
const Navbar = defineAsyncComponent(() => import('../components/Navbar.vue'));
import IconTrash from '../components/icons/IconTrash.vue';
const MobileMenu = defineAsyncComponent(() => import('../components/MobileMenu.vue'));
import { useCart } from '../composables/useCart';
import IconMinusBlack from '@/components/icons/IconMinusBlack.vue';
import IconPlusBlack from '@/components/icons/IconPlusBlack.vue';
import IconNoBlack from '@/components/icons/IconNoBlack.vue';

const {
  cartEmpty,
  products,   
  loadCartItems,
  clearCart,
  removeFromCart,
  increment,
  decrement,
  calculatedPrices,
  isMobile,
} = useCart();

onMounted(loadCartItems);
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
  display: flex;
  flex-direction: column;    
}

.empty{
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  height: 100%;
  transform: translateY(150%);
}

.empty :first-child:not(button){
  font-size: 20px;
  font-weight: 400;
  color: #919395;
}

.empty span:not(:first-child){
  font-size: 16px;
  font-weight: 400;
  color: #919395;
  text-align: center;
}

.catalog-button{  
  border: none;
  background-color: #f5f5f5;
}

.catalog-link{
  margin-top: 20px;
  padding: 10px 22px;
  border-radius: 8px;
  border: none;
  background-color: #f5f5f5;
  text-decoration: none;
  color: black
}

.cart-container{
  margin-top: 16px;
  display: grid;
  grid-template-columns: 3fr 1fr;
}

.products-column{
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.name-clean-container{
  display: flex;
  align-items: stretch;
  margin-bottom: 20px;
}

.clean-cart{
  background-color: transparent;
  border:none;
  margin-left: auto;
  opacity: 60%;
}
.clean-cart svg{
  margin-bottom: 4px;
}

.names{
  display: grid;
  gap: 12px;
  grid-template-columns: 80px 3fr 2fr 0.1fr;
}

.cell-text{
  font-size: 12px;
  opacity: 60%;
}

.products-list{
  display: flex;  

}

.product-card-wrapper-mobile{
  display: grid;
  grid-template-columns: 80px 3fr 0.1fr;
  align-items: center;
  justify-content: start;
  margin-top: 16px;
  gap: 12px;
  width: 100%;
  position: relative;
}

.total-price{
  margin-right: 25px;
}

.mobile-wrapper{
  display: flex;
  flex-direction: column;
}

.product-info-mobile{
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;  
}

.del-button-wrapper-mobile{
  position: absolute; 
  top: 0;            
  right: 0;
}

.quantity-wrapper{
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-card{
  display: flex;
  align-items: stretch;
  justify-content: center;
  flex-direction: column;
  width: 100%;
}

.border-line{
  width: 100%;
  background-color: #f5f5f5;
  height: 1px; 
}

.product-card-wrapper{
  display: grid;
  grid-template-columns: 80px 3fr 2fr 0.1fr;
  align-items: center;
  justify-content: start;
  margin-top: 16px;
  gap: 12px;
  width: 100%;
}

.image-container{
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-img{
  width: 80px;
  height: 80px;
  object-fit: cover;
}

.del-button-wrappper{
  display: flex;
  align-items: center;
  justify-content: center;   
}

.del-button{
  background-color: transparent;
  border: none;
}

.del-button svg{
  margin-bottom: 4px;
}

.product-info{
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  margin-right: 12px;
}

.price-quantity-container{ 
  width: 100%;
  height: 100%;
  display: grid;
  align-items: center;
  justify-content: center;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 12px;
}

.wrapper,
.item-price-wrapper,
.total-price-wrapper,
.quantity-control-wrapper{
  display: flex;
  justify-content: center;
  align-items: center;
}

.item-article{
  font-size: 12px;
  opacity: 60%;
}

.quantity-control{
  background-color: #EDEDED;
  color: #fff;
  padding: 8px 16px;
  border-radius: 120px;
  border: none;
  display: flex;
  justify-content: center; 
  align-items: center; 
  height: 30px;   
  width: 85px;
  color: black;
}

.quantity-control button{
  background-color: #EDEDED;
  color: #fff;
  border: none; 
  display: flex; 
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: center;
}

.quantity-control span{
  padding-left: 12px;
  padding-right: 12px;
  display: flex; 
} 

.make-order-buttons{
  display: flex;

}

.mob-container{
  display: flex;
  flex-direction: column;
  align-items: end;
  background-color: #EDEDED;
  border-radius: 8px;
  box-shadow: 0px 0px 8px 0px  rgba(0, 0, 0, 0.2);
  margin-left: 50px;
  padding: 24px 24px;
  width: 100%;
  height: min-content;
  position: sticky;
  margin-top: 114px;
  top: 0px;  
}

.text-allprice-wrapper{
  display: flex;
  width: 100%;
  justify-content: space-between;
  margin-bottom: 12px;
  font-weight: 600;
}

.text-allprice{
  left: 0;
}

.make-order-wrapper{
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: center;
}

.make-order-rl{
  width: 100%;
}

.make-order{
  background-color: #003464;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;  
  margin-top: auto;
  width: 100%;
}

@media (max-width: 440px) {
  .cart-container {
    display: grid;
    grid-template-columns: 1fr; 
    grid-template-rows: auto auto; 
    gap: 8px; 
  }

  .product-card{
    display: none;
  }
  
  .names{
    display: none;
  }

  .item-img{
    width: 70px;
    height: 70px;
  }

  .quantity-control{
    border-radius: 0px;
    background-color: #F8FAFB;
  }

  .quantity-control button{
    background-color: #F8FAFB;
  }

  .name-clean-container{
    margin-bottom: 0px;
  }

  .item-article{
    font-size: 12px;
  }

  .item-name{
    font-size: 16px;
    margin-bottom: 20px;
  }

  .products-column {
    order: 1; 
  }
  
  .make-order-buttons {
    order: 2; 
  }
  
  .mob-container {
    margin-left: 0px; 
    margin-right: 0px; 
    margin-bottom: 60px;
    margin-top: 0;
    width: 100%;
    
  }

  .total-price{
    font-size: 18px;
    font-weight: bold;
    margin-right: -16px;
  }

  .price-quantity-container{
    display: grid;
    grid-template-columns: 1fr; 
    grid-template-rows: auto auto; 
  }
}

@media (min-width: 441px) and (max-width: 767px) {
  .cart-container {
    display: grid;
    grid-template-columns: 1fr; 
    grid-template-rows: auto auto; 
    gap: 16px; 
  }
  
  .products-column {
    order: 1; 
  }
  
  .make-order-buttons {
    order: 2; 
  }
  
  .mob-container {
    margin-left: 0; 
    margin-top: 0; 
    width: 100%; 
  }
  
}

@media (min-width: 768px) and (max-width: 1023px) {
  .cart-container {
    grid-template-columns: 2fr 1fr;    
  }
}

</style>

