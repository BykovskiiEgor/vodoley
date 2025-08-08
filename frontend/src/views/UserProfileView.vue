<template>
    <header>
        <Navbar />
    </header>
    <div class="container">
        <div class="content-wrapper">
            <div class="tabs">
                <button 
                    @click="activeTab = 'orders'"
                    :class="{ active: activeTab === 'orders' }">
                    Заказы
                </button>
                <button 
                    @click="activeTab = 'profile'"
                    :class="{ active: activeTab === 'profile' }">
                    Профиль
                </button>
            </div>
            <div class="tab-content">                
                <div v-if="activeTab === 'orders'" class="orders-tab">   
                    <div class="sort-container">
                        <form class="sort" @change="getFilters()">              
                            <select v-model="filter" class="form-select">
                                <option disabled value="">Статус</option>
                                <option>Все</option>
                                <option value="1">в ожидании</option>
                                <option value="2">Обработан</option>
                                <option value="3">Собран</option>
                                <option value="4">Доставлен</option>
                            </select>                      
                        </form>    
                    </div>                      
                    <div class="order-card" v-for="order in orders" :key="order.id">
                        <div class="order-header">
                            <span>Заказ №{{ order.id }} - <span :class="quantityStatusClass(order.status)">{{ order.status }}</span></span>
                            <span>Дата заказа: {{ formatDate(order.order_date as string) }}</span>
                        </div>            
                        <div class="order-items">
                            <div v-for="(item, index) in order.orderitem_set" :key="index" class="order-item">
                            <span>{{ item.name }}</span>
                            <span class="quantity">{{ item.quantity }} шт</span>
                            </div>
                        </div>                
                        <div class="order-total">
                            Общая сумма: <span class="bold-text">{{ order.total_price }} руб.</span> 
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="activeTab === 'profile'" class="profile-tab">                        
                <div class="profile-info">
                    <div class="info-section-header">
                        <span class="lk-icon"><LkIcon/></span>                       
                        <span class="name-header">{{user?.first_name }} {{ user?.last_name }}</span>
                        <span class="exit-container" title="Выйти из аккаунта">
                            <button class="exit-btn" @click="exit()"><IconExit/></button>
                        </span>
                        <span class="change-icon"><ChangeIcon/></span>                        
                    </div>
            
                    <div class="info-section" v-if="!edit">
                        <label>Адрес электронной почты</label>
                        <div class="info-value">
                            <span class="info-value-input">{{ user.email }}</span>
                            <button class="add-btn"
                                @click="edit = true">
                                Изменить
                            </button>
                        </div>
                    </div>
                    <div v-if="edit">
                        <label>Адрес электронной почты</label>
                        <div class="info-value">
                            <span class="edit-form">
                                <div class="edit-form-wrapper">
                                    <input class="add-value-input"
                                    type="email" 
                                    v-model="formData.email" 
                                    placeholder="email@email.ru" 
                                    @blur="handleBlur('email')"
                                    :class="{ 'is-invalid': shouldShowError('email') }">
                                    <button style="margin-right: 8px;" class="edit-btn"
                                        @click="submitEditEmail()">
                                        <IconYes/>
                                    </button>
                                    <button class="edit-btn"
                                        @click="edit = false">
                                        <IconNo/>
                                    </button>
                                </div>                                
                                <div  class="invalid-feedback" :class="{ 'show': shouldShowError('email') }">
                                {{ formErrors.email }}
                                </div>
                            </span>                                                        
                        </div>
                    </div>
                    
                    <div class="info-section" v-if="!editPhone">
                        <label>Номер телефона</label>
                        <div class="info-value">
                            <span class="info-value-input">{{ user.phone_number }}</span>
                            <button class="add-btn" @click="editPhone = true">Изменить</button>
                        </div>
                    </div>
                    <div v-if="editPhone">
                        <label>Номер телефона</label>
                        <div class="info-value">
                            <span class="edit-form">
                                <div class="edit-form-wrapper">
                                    <input 
                                        type="tel" 
                                        class="add-value-input"
                                        id="phoneNumber" 
                                        v-maska:argument.modifier="'+7(###) ###-##-##'"
                                        v-model="formData.phone"                   
                                        placeholder="+7(___) ___-__-__"                                       
                                        :class="{ 'is-invalid': shouldShowError('phoneNumber') }">
                                    <button style="margin-right: 8px;" class="edit-btn"
                                        @click="submitEditPhone()">
                                        <IconYes/>
                                    </button>
                                    <button class="edit-btn"
                                        @click="editPhone = false">
                                        <IconNo/>
                                    </button>
                                </div>                                                               
                            </span>                                                        
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <label>Адрес доставки</label>
                        <div style="padding-bottom: 8px; position: relative;" class="info-value">
                            <input 
                                class="add-value-input"
                                type="text" 
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
                            <button class="add-btn" @click="addAddress(formData.address)">Добавить</button>
                        </div>
                        <div class="info-value-address">                            
                            <div class="address-list-container" v-for="address  in addresses" v-if="addresses">                                                            
                                <span class="address-from-list" >{{ address.address }} <span v-if="address.isPrimary">★</span></span>
                                    <button style="margin-right: 8px;" title="Сделать адрес предпочтительным" class="edit-btn"
                                        @click="setPrimaryAddress(address.id)">
                                        <IconYes/>
                                    </button>
                                    <button class="edit-btn" style="width: 38px; height: 42px; padding: 13px 13px;"
                                        @click="dellAddress(address.id)">
                                        <IconTrashWhite style="margin-bottom: 8px;"/>
                                    </button>
                            </div> 
                        </div>                        
                    </div>
                </div>
            </div>   
        </div>     
    </div>
</template>

<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const Navbar = defineAsyncComponent(() => import('../components/Navbar.vue'));
import {useProfile} from '../composables/useProfile';
import ChangeIcon from '@/components/icons/ChangeIcon.vue';
import LkIcon from '@/components/icons/LkIcon.vue';
import IconYes from '@/components/icons/IconYes.vue';
import IconNo from '@/components/icons/IconNo.vue';
import IconTrashWhite from '../components/icons/IconTrashWhite.vue';
import IconExit from '@/components/icons/IconExit.vue';

const {
    edit,
    orders,
    user,
    formatDate,
    activeTab,
    quantityStatusClass,
    submitEditEmail,
    handleBlur,
    formData,
    shouldShowError,
    formErrors,
    filter,
    getFilters,
    addresses,
    dellAddress,
    isLoadingSuggestions,
    showSuggestions,
    addressSuggestions,
    selectAddress,
    handleAddressInput,
    addAddress,
    setPrimaryAddress,
    editPhone,
    submitEditPhone,
    exit,
}=useProfile();

</script>

<style scoped>
.green{
    color: #217F0E;
    opacity: 1 !important;
}
.blue{
    color: #0891B2;
    opacity: 1 !important;
}
.yellow{
    color: #C8790B;
    opacity: 1 !important;
}

.order-header span{
    font-size: 14px;
    opacity: 60%;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
  display: flex;
  flex-direction: column;    
}

.content-wrapper{
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  margin-right: 10px;
  position: relative;
}

.tabs button.active {
  font-weight: bold;
  color: #003464;
}

.tabs button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #003464;
}

.order-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.order-items {
  margin-bottom: 15px;
  font-size: 18px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;  
}

.quantity{
    font-size: 18px;
    font-weight: bold;
}

.order-total {  
    border-top:  1px solid #eee;
    padding-top: 12px;
    text-align: left;
}

.bold-text{
    font-weight: bold;
}

.profile-info {
    display: flex;
    flex-direction: column;
    gap: 12px;
    background: #fff;
    border-radius: 6px;
    padding: 20px;
    border: 1px solid #ddd;
}

.info-section-header {
    display: flex; 
    align-items: center;       
    padding-bottom: 20px;
    border-bottom: 1px solid #ddd;
}

.lk-icon{   
    max-width: max-content;
    margin-right: 20px;
}

.name-header{    
    text-align: left;
    font-size: 22px;
    font-weight: 600;
    color: #334155
}

.change-icon{
    margin-left: auto;
    text-align: right;
}


.info-section label {
  display: block;
  margin-bottom: 5px;
  color: #0F172A;
  font-size: 16px;
  font-weight: 400;
}

.info-section {
  display: flex;
  flex-direction: column;
  color: #666;
  font-size: 14px;
  border-radius: 6px;
}

.info-value {
  display: flex;
  justify-content: space-between;
  align-items: center;    
}

.info-value-address{
    display: flex;
    flex-direction: column;
    border-radius: 6px;
    color: #666;
    
}

.info-value-input{
    background: #F8FAFC;
    border-radius: 4px;
    color: #0F172A;
    width: 100%;
    height: 100%;
    padding: 10px;
    margin-right: 8px;
}

.add-value-input{
    background: #F8FAFC;
    border-radius: 4px;
    color: #0F172A;
    width: 100%;
    height: 100%;
    padding: 10px;
    margin-right: 8px;
    border: none;
}

.address-list-container{
    display: flex; 
    justify-content: space-between;   
    align-items: center;
    margin-bottom: 8px;    
}

.address-from-list{
    background: #F8FAFC;
    border-radius: 4px;
    color: #0F172A;
    width: 100%;
    height: 100%;
    padding: 10px;
    margin-right: 8px;
}

.edit-btn {
  background: #334155;
  color: white;
  border: none;
  padding: 10px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  
}

.edit-btn:hover {
  background: #4d5a6d;
}

.add-btn{
    background: #334155;
    color: white;
    border: none;
    padding: 10px 11px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.add-btn:hover {
  background: #4d5a6d;
}

.edit-form{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.edit-form-wrapper{
    display: flex;    
}

.invalid-feedback.show {
  display: inline;
}

.sort-container{
  display: flex;
  flex-direction: row;
  justify-content: end;
  margin-bottom: 10px;
}

.sort{
  display: flex;
  gap: 4px;
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

.exit-container{
    margin-left: 10px;
}

.exit-container:hover{
    cursor: pointer;
}

.exit-btn{
    background-color: transparent;
    border: none;
    color: transparent;
}
</style>
