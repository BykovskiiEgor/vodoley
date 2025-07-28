import { ref, onMounted, onUnmounted, computed, watch, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { debounce } from 'lodash-es';
import { fetchSearchProductsList } from './useAPI';


interface User {
  email: string;    
  password: string;
  name: string;
  last_name: string;
}

interface Product {
  id: number;
  name: string; 
  quantity: number;
}

export function useNavbar() {
  const searchQuery = ref('');
  const products = ref<Product[]>([]);
  const user = ref<User | null>(null);
  const userNull = ref(true);
  
  const route = useRoute();
  const router = useRouter();
  const cartCount = ref(0);


  onMounted(() => {
    getUser();
  });

  function getUser() {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      user.value = JSON.parse(storedUser) as User;
      userNull.value = false;
    } else {
      userNull.value = true;
    }
    console.log(user.value);
  }

  const onChange = debounce(async () => {
    if (searchQuery.value.trim()) {
      try {
        const response = await fetchSearchProductsList(searchQuery.value);        
        products.value = response.data.results;
        console.log(products.value);
      } catch (error) {
        console.error('Search error:', error);
        products.value = [];
      }
    } else {
      products.value = [];
    }
  }, 300);

  const search = () => {
    if (searchQuery.value.trim()) {
      router.push({ name: 'search', query: { q: searchQuery.value } });
    }
  };

  const goToProduct = (id: number) => {
    router.push({ name: 'ProductDetails', params: { id } });
  };

  function updateCartCount() {
    try {
      const cart: Record<number, Product> = JSON.parse(localStorage.getItem('cart') || '{}');
      cartCount.value = Object.values(cart).reduce((total, product) => total + product.quantity, 0);
    } catch (e) {
      console.error('Ошибка при чтении корзины', e);
      cartCount.value = 0;
    }
  }

  onMounted(() => {
    updateCartCount(); 
    window.addEventListener('storage', updateCartCount); 
  });
  
  onUnmounted(() => {
    window.removeEventListener('storage', updateCartCount);
  });

  const cart = reactive<any[]>(JSON.parse(localStorage.getItem('cart') || '{}'));

  const uniqueCount = computed(() => Object.keys(cart).length);

  watch(cart,() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  });

  return {
    searchQuery,
    products,
    user,
    userNull,
    onChange,
    search,
    goToProduct,
    cartCount,
    uniqueCount
  };
}
