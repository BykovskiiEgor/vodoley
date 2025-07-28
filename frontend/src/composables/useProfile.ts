import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { fetchOrders, requestEditEmail, requestEditPhone } from './useAPI';
import router from '@/router';

interface User {
    email?: string;
    first_name?: string;
    last_name?: string;
    phone_number?: string;   
}

interface OrderItem {
    name: string;
    quantity: number;
}

interface Order {
    id: number;
    status: string;
    order_date: string;
    total_price: string;
    orderitem_set: OrderItem[];
    address: Address[];
}

interface Address {
  id: number;
  address: string;
  isPrimary: boolean;
}


export function useProfile() {
    const edit = ref(false);
    const editPhone = ref(false);
    const user = ref<User>({});    
    const data = ref<{
        orders: Order[];
    }>({
        orders: []
    });
    const activeTab = ref<string>('orders');

    const orders = computed(() => data.value.orders);

    const addressSuggestions = ref<any[]>([]);
    const showSuggestions = ref(false);
    const isLoadingSuggestions = ref(false);
    const DADATA_TOKEN = import.meta.env.VITE_DATA_TOKEN; 
    const filter = ref('');

    const formData = ref({
        email: '', 
        address: '',
        phone: '',       
      });

    const touchedFields = ref({
        email: false, 
        phoneNumber: false,
        address: false,       
    });
    
    const addresses = ref<Address[]>([]);

    const debounceTimeout = ref<any | null>(null);

    onMounted(() => {
        loadUserFromLocalStorage();
        if (user.value.email) {
            getOrders(user.value.email);
        }        
    });

    function loadUserFromLocalStorage() {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            try {
                const userData = JSON.parse(storedUser);
                addresses.value = userData?.user?.addresses || [];
                if (userData?.user) {
                    user.value = {
                        email: userData.user.email,
                        first_name: userData.user.first_name,
                        last_name: userData.user.last_name,
                        phone_number: userData.user.phone_number,
                    };
                }
            } catch (error) {
                console.error('Error parsing user data:', error);
            }
        }
    }
      
    async function getOrders(email: string) {
        try {
            const response = await fetchOrders(email, filter.value);
            data.value = response;
        } catch (error) {
            console.error('Error loading orders:', error);
        }
    }
    
    function formatDate(dateString: string): string {
        const options: Intl.DateTimeFormatOptions = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        return new Date(dateString).toLocaleDateString('ru-RU', options);
    }

    function quantityStatusClass(status: string) {
        switch (status) {
            case 'В ожидании': return 'yellow';
            case 'Обработан':
            case 'Собран': return 'blue';
            case 'Доставлен': return 'green';
            default: return '';
        }
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
    }

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

    async function submitEditEmail() {
        if (!isFormValid.value) {
            alert('Пожалуйста, исправьте ошибки в форме');
            return;
        }
        const email = formData.value.email
        try {
            const response = await requestEditEmail(email)
            alert(response.message);
            updateEmailInLocalStorage(email)
            edit.value = false
        }
        catch (error) {
            console.error('Error submitting order:', error);
            alert('Произошла ошибка при изменении Email.');
        }

    }

    async function submitEditPhone() {      
      const phone = formData.value.phone
      try{
        const response = await requestEditPhone(phone)
        alert(response.message);
        updatePhoneInLocalStorage(phone)
        editPhone.value = false
      }
      catch (error) {
            console.error('Error submitting phone change:', error);
            alert('Произошла ошибка при изменении номера.');
        }
    }

    function updateEmailInLocalStorage(newEmail: string) {      
        const userDataString = localStorage.getItem('user');
        
        if (userDataString) {
          try {
            const userData = JSON.parse(userDataString);            
            if (userData.user && userData.user.email) {
              userData.user.email = newEmail;                
              const updatedUserDataString = JSON.stringify(userData);                      
              localStorage.setItem('user', updatedUserDataString);
              console.log('Email успешно обновлен в localStorage');
              loadUserFromLocalStorage()
            } else {
              console.error('Структура данных пользователя неверна');
            }
          } catch (e) {
            console.error('Ошибка при парсинге данных пользователя:', e);
          }
        } else {
          console.error('Данные пользователя не найдены в localStorage');
        }
    }

    function updatePhoneInLocalStorage(newPhone: string) {      
        const userDataString = localStorage.getItem('user');
        
        if (userDataString) {
          try {
            const userData = JSON.parse(userDataString);            
            if (userData.user && userData.user.phone_number) {
              userData.user.phone_number = newPhone;                
              const updatedUserDataString = JSON.stringify(userData);                      
              localStorage.setItem('user', updatedUserDataString);
              console.log('Номер успешно обновлен в localStorage');
              loadUserFromLocalStorage()
            } else {
              console.error('Структура данных пользователя неверна');
            }
          } catch (e) {
            console.error('Ошибка при парсинге данных пользователя:', e);
          }
        } else {
          console.error('Данные пользователя не найдены в localStorage');
        }
    }

    function shouldShowError(field: keyof typeof touchedFields.value) {
      return touchedFields.value[field] && formErrors.value[field];
    }

    function handleBlur(field: keyof typeof touchedFields.value) {
      touchedFields.value[field] = true;
    }

    function getFilters(){
      if (user.value.email)
        {
          getOrders(user.value.email);
        }  
    }

    function dellAddress(id: number) {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        const user = JSON.parse(storedUser);
        
        if (user.user?.addresses) {
          user.user.addresses = user.user.addresses.filter(
            (address: { id: number }) => address.id !== id
          );
          
          localStorage.setItem('user', JSON.stringify(user));
          loadUserFromLocalStorage();
        }
      }
    }

    function selectAddress(suggestion: any) {
      formData.value.address = suggestion.value;
      showSuggestions.value = false;
    }

    function handleAddressInput(query: string) {
      if (debounceTimeout.value) {
        clearTimeout(debounceTimeout.value);
      }
      
      debounceTimeout.value = setTimeout(() => {
        fetchAddressSuggestions(query);
      }, 1500); 
    }

    function addAddress(address: string){
      const storedUser = localStorage.getItem('user');
      if (storedUser){
        const user = JSON.parse(storedUser);  
        if (user.user.addresses.length > 0 ){
          const addressExists = user.user.addresses.some(
          (addr: { address: string; }) => addr.address.toLowerCase() === address.toLowerCase()
        );
        if (addressExists) {
          alert('Этот адрес уже существует');
          throw new Error('Этот адрес уже существует');
        }
      }      
        
        const newAddress = {
          id: Date.now(), 
          address: address.trim(),
          isPrimary: user.user.addresses?.length === 0
        };
        user.user.addresses.push(newAddress);
        localStorage.setItem('user', JSON.stringify(user));
        loadUserFromLocalStorage();
      }

    }

    function setPrimaryAddress(id: number) {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        const user = JSON.parse(storedUser);
        
        if (user.user?.addresses) {        
          user.user.addresses = user.user.addresses.map((addr: Address) => ({
            ...addr,
            isPrimary: addr.id === id
          }));
          
          localStorage.setItem('user', JSON.stringify(user));
          loadUserFromLocalStorage();
        }
      }
    }

    function exit(){
      const isConfirmed = window.confirm('Вы уверены, что хотите выйти из аккаунта?');
      
      if (isConfirmed){
        localStorage.removeItem('user');
        localStorage.removeItem('cart');
        router.push('/auth');
      }
      
    }

    return {
        edit,
        editPhone,
        data,
        user,
        orders,
        formatDate,
        activeTab,   
        quantityStatusClass, 
        fetchAddressSuggestions,
        submitEditEmail,
        submitEditPhone,
        handleBlur,
        formData,
        shouldShowError,
        formErrors,
        getOrders,
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
        exit,
    };
}