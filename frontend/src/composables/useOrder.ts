import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import MobileMenu from '../components/MobileMenu.vue';
import router from '@/router';import { requestCreateOrder } from './useAPI';
;


interface Product {
  id: number;
  article: string;
  name: string;  
  price: number;
  discount_price?: number;
  images: { image: string }[];
  quantity: number;
  available: boolean;
}

interface CalculatedProduct extends Product {
  appliedPrice: number;   
  itemTotal: number;      
}

interface TotalPriceResult {
  items: CalculatedProduct[]; 
  total: number;             
}

interface User {
  email?: string;
  first_name?: string;
  last_name?: string;
  phone_number?: string;   
}

export function useOrder(){
    const products = ref<Record<number, Product>>({});
    const formData = ref({
      email: '',
      firstName: '',
      lastName: '',
      address: '',
      phoneNumber: ''
    });
    
    
    const touchedFields = ref({
        email: false,
        firstName: false,
        lastName: false,
        address: false,
        phoneNumber: false
      });
      
    
    const addressSuggestions = ref<any[]>([]);
    const showSuggestions = ref(false);
    const isLoadingSuggestions = ref(false);
    const cartEmpty = ref(true); 
    
    const DADATA_TOKEN = import.meta.env.VITE_DATA_TOKEN;    
    const debounceTimeout = ref<any | null>(null);

    const productsCountTotal = Object.keys(JSON.parse(localStorage.getItem('cart') || '{}')).length;
    
    const selectedAddress = ref<string | null>(null);

    const isAddressValid = computed(() => {
      return addressSuggestions.value.some(suggestion => suggestion.value === formData.value.address);
    });
    
    const user = ref<User>({});    

    const validationRules = {
      email: [
        { 
          condition: (value: string) => !value.trim(), 
          message: 'Поле email обязательно для заполнения' 
        },
        { 
          condition: (value: string) => !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value), 
          message: 'Некорректный формат email' 
        }
      ],
      firstName: [
        { 
          condition: (value: string) => !value.trim(), 
          message: 'Поле имени обязательно для заполнения' 
        },
        { 
          condition: (value: string) => value.trim().length < 2, 
          message: 'Имя должно содержать минимум 2 символа' 
        },
        { 
          condition: (value: string) => !/^[a-zA-Zа-яА-ЯёЁ\- ]+$/.test(value), 
          message: 'Имя может содержать только буквы и дефисы' 
        }
      ],
      lastName: [
        { 
          condition: (value: string) => !value.trim(), 
          message: 'Поле фамилии обязательно для заполнения' 
        },
        { 
          condition: (value: string) => value.trim().length < 2, 
          message: 'Фамилия должна содержать минимум 2 символа' 
        },
        { 
          condition: (value: string) => !/^[a-zA-Zа-яА-ЯёЁ\- ]+$/.test(value), 
          message: 'Фамилия может содержать только буквы и дефисы' 
        }
      ],
      address: [
        { 
          condition: (value: string) => !value.trim(), 
          message: 'Поле адреса обязательно для заполнения' 
        },
        { 
          condition: () => !isAddressValid.value, 
          message: 'Выберите адрес из списка' 
        }
      ],
      phoneNumber: [
        { 
          condition: (value: string) => !value.trim(), 
          message: 'Поле телефона обязательно для заполнения' 
        },
        { 
          condition: (value: string) => !/^\+?\d{10,14}$/.test(value.replace(/\D/g, '')), 
          message: 'Некорректный номер телефона' 
        }
      ]
    };
    
    const formErrors = computed(() => {
      const errors: Record<string, string> = {};
      
      for (const [field, rules] of Object.entries(validationRules)) {
        const value = formData.value[field as keyof typeof formData.value];
        for (const rule of rules) {
          if (rule.condition(value)) {
            errors[field] = rule.message;
            break;
          }
        }
      }
      
      return errors;
    });
    
    const isFormValid = computed(() => {
      return Object.keys(formErrors.value).length === 0;
    });
    
    onMounted(() => {
      loadCartItems();
      loadUserFromLocalStorage();
      cartEmpty.value = Object.keys(products.value).length === 0;
    });


    function loadUserFromLocalStorage() {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
          try {
              const user = JSON.parse(storedUser);
              formData.value.email = user.user.email || '';
              formData.value.firstName = user.user.first_name || '';
              formData.value.lastName = user.user.last_name || '';
              formData.value.phoneNumber = user.user.phone_number || '';

              const savedAddress = user.user?.addresses?.find((addr: { isPrimary: boolean; }) => addr.isPrimary)?.address || user.user?.addresses?.at(-1)?.address ;
              formData.value.address = savedAddress;

              if (savedAddress) {
                addressSuggestions.value.push({ value: savedAddress });
              }

          } catch (error) {
              console.error('Error parsing user data:', error);
          }
      }
  }
    
    function loadCartItems() {
      try {
        const storedProducts = JSON.parse(localStorage.getItem('cart') || '{}');
        if (typeof storedProducts === 'object' && storedProducts !== null) {
          products.value = storedProducts;
        } else {
          products.value = {};
        }
      } catch (error) {
        console.error('Failed to parse cart items from localStorage', error);
        products.value = {};
      }
    }
    
    function calculateTotalPrice(products: Record<string, Product>):TotalPriceResult  {
      const result: TotalPriceResult = {
        items: [], 
        total: 0,  
      };
    
      result.items = Object.values(products).map(product => {
        const price = product.discount_price ?? product.price; 
        const priceInCents = Math.round(price * 100);
        const totalInCents = priceInCents * product.quantity;
        const total = totalInCents / 100; 
    
        return {
          ...product,
          appliedPrice: price,       
          itemTotal: total,         
        };
      });
    
      const totalInCents = result.items.reduce((sum, item) => {
        return sum + Math.round(item.appliedPrice * 100) * item.quantity;
      }, 0);
    
      result.total = totalInCents / 100; 
    
      return result;
    }

    const calculatedPrices = computed(() => calculateTotalPrice(products.value));
    
    function handleBlur(field: keyof typeof touchedFields.value) {
      touchedFields.value[field] = true;
    }
    
    function shouldShowError(field: keyof typeof touchedFields.value) {
      return touchedFields.value[field] && formErrors.value[field];
    }
    
    async function fetchAddressSuggestions(query: string) {   
      if (query.length < 3) {
        addressSuggestions.value = [];
        return;
      }
    
      isLoadingSuggestions.value = true;
      showSuggestions.value = true;
      
      try {
        const response = await fetch('https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Token ${DADATA_TOKEN}`
          },
          body: JSON.stringify({ query: query, count: 5 })
        });
        
        const data = await response.json();
        addressSuggestions.value = data.suggestions || [];
      } catch (error) {
        console.error('Error fetching address suggestions:', error);
        addressSuggestions.value = [];
      } finally {
        isLoadingSuggestions.value = false;
      }
    }
    
    function selectAddress(suggestion: any) {
      formData.value.address = suggestion.value;
      showSuggestions.value = false;
    }
    
    async function submitOrder() {
      for (const field in touchedFields.value) {
        touchedFields.value[field as keyof typeof touchedFields.value] = true;
      }
      
      if (!isFormValid.value) {
        alert('Пожалуйста, исправьте ошибки в форме');
        return;
      }
      
      if (cartEmpty.value) {
        alert('Ваша корзина пуста. Пожалуйста, добавьте товары перед оформлением заказа.');
        return;
      }
    
      const order = {
        email: formData.value.email,
        first_name: formData.value.firstName,
        last_name: formData.value.lastName,
        address: formData.value.address,
        phone_number: formData.value.phoneNumber,
        total_price: calculatedPrices.value.total,
        products: products.value,
      };
    
      try {
        const response = requestCreateOrder(order);        
        alert('Заказ успешно оформлен, для отслеживания изменения статуса авторизируйтесь в личном кабинете');
        localStorage.removeItem('cart');
        router.push('/');
      } catch (error) {
        console.error('Error submitting order:', error);
        alert('Произошла ошибка при оформлении заказа. Пожалуйста, попробуйте позже.');
      }
    }

    function handleAddressInput(query: string) {
      if (debounceTimeout.value) {
        clearTimeout(debounceTimeout.value);
      }
      
      debounceTimeout.value = setTimeout(() => {
        fetchAddressSuggestions(query);
      }, 1500); 
    }

    

    return{
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
    }
}

