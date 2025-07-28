<template>
  <header>
    <Navbar />
  </header>
  <div class="container">
    <div class="order-container">
      <div class="data-column">  
        <div class="products-wrapper">
          <div class="products-container">
            <span class="data-names">Позиций – {{ productsCountTotal }}</span>  
              <div class="image-wrapper">
                <span v-for="product in products">
                  <div class="image-container">
                    <img class="item-img" :src="product.images.length ? product.images[0].image : '/images/vodoley.jpg'" :alt="`Image for ${product.name}`"/>
                    <span class="quantity-iic">{{ product.quantity }} шт.</span>
                  </div>
                </span>                
              </div>   
              <div>
                <span style="font-weight: 600;">Итого – {{ calculatedPrices.total }} ₽</span>
              </div>                  
          </div>
        </div>      
        <form id="order-form" @submit.prevent="submitOrder">
          <div class="data-wrapper">
            <div class="data-backgraound">             
              <span class="block-name">Получатель</span>
              <div class="form-input-wrapper"> 
                <span class="data-names">Почта</span>                       
                <input 
                  type="email" 
                  class="form-input" 
                  id="email" 
                  v-model="formData.email" 
                  placeholder="Email@email.ru" 
                  @blur="handleBlur('email')"
                  :class="{ 'is-invalid': shouldShowError('email') }">
                <div class="invalid-feedback" v-if="shouldShowError('email')">
                  {{ formErrors.email }}
                </div>
              </div>                        
              <div class="form-input-wrapper"> 
                <span class="data-names">Имя</span>             
                <input 
                  type="text" 
                  class="form-input" 
                  id="firstName" 
                  v-model="formData.firstName" 
                  placeholder="Иван" 
                  @blur="handleBlur('firstName')"
                  :class="{ 'is-invalid': shouldShowError('firstName') }">
                <div class="invalid-feedback" v-if="shouldShowError('firstName')">
                  {{ formErrors.firstName }}
                </div>
              </div>
              <div class="form-input-wrapper">
                <span class="data-names">Фамилия</span>   
                <input 
                  type="text" 
                  class="form-input" 
                  id="lastName" 
                  v-model="formData.lastName" 
                  placeholder="Иванов" 
                  @blur="handleBlur('lastName')"
                  :class="{ 'is-invalid': shouldShowError('lastName') }">
                <div class="invalid-feedback" v-if="shouldShowError('lastName')">
                  {{ formErrors.lastName }}
                </div>
              </div>                       
              <div class="form-input-wrapper">
                <span class="data-names">Номер телефона</span>   
                <input 
                  type="tel" 
                  class="form-input" 
                  id="phoneNumber" 
                  v-maska:argument.modifier="'+7(###) ###-##-##'"
                  v-model="formData.phoneNumber"                   
                  placeholder="+7(___) ___-__-__"
                  @blur="handleBlur('phoneNumber')"
                  :class="{ 'is-invalid': shouldShowError('phoneNumber') }">
                <div class="invalid-feedback" v-if="shouldShowError('phoneNumber')">
                  {{ formErrors.phoneNumber }}
                </div>
              </div>                            
              <div class="form-input-wrapper" style="position: relative;">
                <span class="data-names">Адрес</span>   
                <input 
                  type="text" 
                  class="form-input" 
                  id="address" 
                  v-model="formData.address" 
                  placeholder="Город, улица, дом, квартира" 
                  @blur="handleBlur('address')"
                  @input="handleAddressInput(formData.address)"
                  @focus="showSuggestions = true"
                  :class="{ 'is-invalid': shouldShowError('address') }">
                <div class="invalid-feedback" v-if="shouldShowError('address')">
                  {{ formErrors.address }}
                </div>
                <div 
                  v-show="showSuggestions && (addressSuggestions.length > 0 || isLoadingSuggestions)" 
                  class="suggestions-container">
                  <div v-if="isLoadingSuggestions" class="suggestion-item text-muted">
                    Загрузка...
                  </div>
                  <template v-else>
                    <div 
                      v-for="suggestion in addressSuggestions" 
                      :key="suggestion.value" 
                      class="suggestion-item"
                      @mousedown="selectAddress(suggestion)">
                      {{ suggestion.value }}
                    </div>
                  </template>
                </div>
              </div> 
              <div>
                <span class="data-names" style="color: #d5d4d4">*Данные нужны для создания личного кабинета, в котором Вы узнаете об изменении статуса и обработке заказа</span>
              </div> 
            </div>            
          </div> 
        </form>
      </div> 
      <div class="confirm-button">
        <div class="mob-container">                  
          <div class="make-order-wrapper">
            <button 
              form="order-form"
              type="button" 
              class="make-order"
              :disabled="!isFormValid || cartEmpty"
              @click="submitOrder()">
              Оформить заказ
            </button>
            <span class="agreement">
              Нажимая кнопку, я даю согласие на обработку персональных данных, в соответствии с Политикой, и соглашаюсь с Правилами
            </span>
          </div>          
        </div>
      </div>
    </div>
  </div>  
</template>

<script setup lang="ts">
import Footer from '@/components/Footer.vue';
import {useOrder} from '../composables/useOrder';
import Navbar from '@/components/Navbar.vue';

const {
  products,
  submitOrder,
  formData,
  handleBlur,
  shouldShowError,  
  formErrors,
  isFormValid,
  cartEmpty,
  fetchAddressSuggestions,
  showSuggestions,
  addressSuggestions,
  isLoadingSuggestions,
  selectAddress,
  handleAddressInput,
  productsCountTotal,
  calculatedPrices,
} = useOrder();
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

.order-container{
  margin-top: 16px;
  display: grid;
  grid-template-columns: 2fr 1fr;
}

.data-column{
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.products-wrapper{
  display: flex;

}

.image-wrapper{
  display: flex;
  flex-direction: row;
}

.image-container{
  display: flex;
  flex-direction: column;
  align-items: center;
}

.item-img{
  width: 40px;
  height: 40px;
  object-fit: cover;
}

.quantity-iic{
  font-size: 10px;
}

.products-container{
  border-radius: 8px;
  box-shadow: 0px 0px 8px 0px  rgba(0, 0, 0, 0.2);
  padding: 24px;
  width: 100%;
  display: flex;
  flex-direction: column;  
  gap: 18px;
}

.data-wrapper{
  display: flex;
  flex-direction: column;  
}

.block-name{
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
}

.info-bn{
  font-size: 12px;
  font-weight: 300;
}

.form-input-wrapper{
  display: flex;
  flex-direction: column;
}

.data-backgraound{
  border-radius: 8px;
  box-shadow: 0px 0px 8px 0px  rgba(0, 0, 0, 0.2);
  padding: 24px;
  width: 100%;
  display: flex;
  flex-direction: column;  
  gap: 18px;
}

.data-header{
  display: flex;
  flex-direction: column;
}

.data-names{
  font-size: 14px;
  margin-bottom: 4px;
}

.form-input{
  border: 1px solid #d5d4d4;
  border-radius: 4px;
  padding: 4px 8px;
  height: 45px;
}

.form-input::placeholder{
  opacity: 0.3;
}

.confirm-button{
  display: flex;
}

.mob-container{
  display: flex;
  flex-direction: column;
  align-items: end;
  border-radius: 8px;
  box-shadow: 0px 0px 8px 0px  rgba(0, 0, 0, 0.2);
  margin-left: 50px;
  padding: 24px 24px;
  width: 100%;
  height: min-content;
  position: sticky;
  top: 0px;  
}

.make-order-wrapper{
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: center;
  flex-direction: column;
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

.agreement{
  font-size: 8px;
}

.suggestions-container {
  position: absolute;
  top: 100%; 
  left: 0;
  right: 0;
  z-index: 1000;
  max-height: 200px;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.suggestion-item:hover {
  background-color: #f8f9fa;
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

@media (max-width: 440px) {
  .order-container{
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;
  }

  .order-container{
    order: 1
  }

  .confirm-button{
    order: 2
  }

  .mob-container{
    margin-left: 0;
    margin-top: 18px;
    margin-bottom: 18px;
  }

  .block-name{
    margin-bottom: 0;
  }
  .data-backgraound{
    gap: 14px
  }

  .data-names{
    margin-bottom: 0;
    font-size: 12px;
  }

}
</style>
