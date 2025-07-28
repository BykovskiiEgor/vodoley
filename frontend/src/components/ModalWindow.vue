<template>
  <div v-if="visible" class="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Оформить под заказ</h5>
          <button type="button" class="btn-close" @click="hide"></button>
        </div>
        <div class="modal-body">
          <form>            
            <div class="form-group">
              <label for="phone">Номер телефона</label>
              <input type="text" class="form-control" id="phone" v-model="phoneNumber" placeholder="+79173642794">  
              <span v-if="formErrors.phoneNumber" class="error">{{ formErrors.phoneNumber }}</span>                  
              <label for="quantity">Необходимое количество</label>
              <input type="text" class="form-control" id="quantity" v-model="quantity">
              <label for="Comment">Комментарий к заказу</label>
              <input type="text" class="form-control" id="Comment" v-model="comment">              
            </div>
          </form>
        </div>
        <div class="modal-footer" style="display: flex; justify-content: center;">
          <button type="button" class="btn btn-secondary" style="display: flex; align-items: center;" @click="submitOrder">Заказать</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { defineProps} from 'vue';

interface Product {
  id: number;
  name: string;
  price: number;
}


const props = defineProps<{
  visible: boolean;
  product: Product | null;
  hide: () => void;
}>();

const phoneRegex = /^(\+7|8)?\d{10}$/;
const formErrors = ref<{ phoneNumber?: string }>({});

const phoneNumber = ref<string>('');
const quantity = ref<string>('');
const comment = ref<string>('');


const submitOrder = async (): Promise<void> => {
  if (!props.product) {
    console.error('No product selected.');
    return;
  }

  if (!phoneNumber.value) {
    alert('Пожалуйста, укажите номер телефона.');
    return;
  }

  if (!phoneRegex.test(phoneNumber.value)) {
    formErrors.value.phoneNumber = 'Некорректный номер телефона.';
    return;
  }

  const order = {
    phone: phoneNumber.value,
    quantity: quantity.value,
    comment: comment.value,
    product: {
      id: props.product.id,
      name: props.product.name,
      price: props.product.price,
    },
  };

  try {
    const response = await axios.post('https://vodoley-belebey.ru/api/preorder/', order);
    console.log('Order submitted successfully:', response.data);
    alert('Заказ успешно оформлен, с вами свяжутся для уточнения деталей заказа.');
    props.hide();   
  } catch (error) {
    console.error('Error submitting order:', error);
    alert(error || 'Error submitting order. Please try again later.');
  }
};
</script>

  <style scoped>
  .modal {
    display: block;
    background-color: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    z-index: 1050;
  }
  .modal-dialog {
    margin: 10% auto;
    max-width: 500px;
  }
  .modal-content {
    padding: 20px;
  }
  </style>
  