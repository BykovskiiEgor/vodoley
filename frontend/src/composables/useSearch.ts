import { ref, reactive, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import {fetchSearchProducts} from './useAPI'
import { useCounterStore } from '@/stores/counter';


interface Product {
  id: number;
  article: string;
  name: string;
  description: string;
  price: number;
  discount_price: number;
  discount_percent: number;
  image: string;
  quantity: number;
  available: boolean
  exists: boolean;
  images: { image: string }[];
}

interface CartItem {
  id: number;
  article: string;
  name: string;  
  price: number;
  discount_price?: number;
  images: { image: string }[];
  quantity: number;
}

interface Cart {
  [id: number]: CartItem;
}

export function useSearch() {
  const counter = useCounterStore();
  const products = ref<Product[]>([]);
  const currentPage = ref(1);
  const pageSize = ref(10);
  const totalPages = ref(1);
  const route = useRoute();
  const filter = ref('');
  const sort = ref('');
  const cart = reactive<Cart>({});
  const availableAttributes = ref<{ name: string, values: string[] }[]>([]);
  const attributeFilters = ref<Record<string, string>>({});

  onMounted(() => {
    counter.updateCountFromCart();
    getProducts();
    loadCartFromLocalStorage();
    window.addEventListener('resize', updatePageSize);
    updatePageSize();
  });

  watch(() => route.query.q, () => {
    currentPage.value = 1;
    getProducts();
  });

  function getProducts() {
    const query = route.query.q as string;
    if (!query) {
      return;
    }
    fetchSearchProducts(query, currentPage.value, pageSize.value, filter.value, sort.value, window.innerWidth)
    .then(data => {
      products.value = data.results;
      console.log(products.value)
      totalPages.value = Math.ceil(data.count / pageSize.value);
    })
    .catch(error => {
      console.error('Fetch products error:', error.message);
      products.value = [];
    });
  }


  function addToCart(product: Product) {
    if (cart[product.id]) {
      cart[product.id].quantity += 1;
    } else {
      cart[product.id] = {        
        id: product.id,
        article: product.article,
        name: product.name,
        price: product.price,
        discount_price: product.discount_price,
        images: product.images,
        quantity: 1
      };
    }
    updateLocalStorage();
  }

  function increment(product: Product) { 
    if (cart[product.id]) 
      {
        if (cart[product.id].quantity < product.quantity)
          {
            cart[product.id].quantity += 1;
            updateLocalStorage();
          }
      }
  }

  function decrement(product: Product) {
    if (cart[product.id].quantity > 1) {
      cart[product.id].quantity -= 1;
    } else {
      delete cart[product.id];
    }
    updateLocalStorage();    
  }

  function updateLocalStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
    counter.updateCountFromCart();
  }

  function updatePageSize() {
    if (window.innerWidth < 600) {
      pageSize.value = 5;
    } else if (window.innerWidth < 1200) {
      pageSize.value = 10;
    } else {
      pageSize.value = 20;
    }
    fetchProducts(currentPage.value);
  }

  function fetchProducts(page: number) {
    currentPage.value = page;
    getProducts();
  }

  watch([filter, sort], () => {
    currentPage.value = 1;
    getProducts();
  });

  function loadCartFromLocalStorage() {
    const storedCart = JSON.parse(localStorage.getItem('cart') || '{}');
    for (const id in storedCart) {
      if (storedCart.hasOwnProperty(id)) {
        cart[parseInt(id)] = storedCart[id];
      }
    }
  }

  function clearFilter(key: string) {
    attributeFilters.value[key] = '';
    getProducts();
  }

  return {
    products,
    currentPage,
    pageSize,
    totalPages,
    filter,
    sort,
    cart,
    addToCart,
    increment,
    decrement,
    fetchProducts,
    clearFilter,
    availableAttributes,
    attributeFilters,
  };
}
