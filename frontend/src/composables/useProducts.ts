import { ref, reactive, onMounted, watch, nextTick, computed } from 'vue';
import axios, { AxiosError } from 'axios';
import { useRoute, useRouter } from 'vue-router';
import {fetchCategoryProducts} from './useAPI'
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
  available: boolean;
  quantity: number;
  exists: boolean;
  images: { image: string }[];
  avg_rating?: string;
}

interface CartItem {
  id: number;
  article: string;
  name: string;  
  price: number;
  discount_price?: number;
  images: { image: string }[];
  quantity: number;
  quantity_max: number;
}

interface Cart {
  [id: number]: CartItem;
}

interface SavedFilters {
  filter: string;
  sort: string;
  attributeFilters: Record<string, string>;
  priceMn: string;
  priceMx: string;
}


export function useProducts() {
  const counter = useCounterStore();
  const products = ref<Product[]>([]);
  const pageSize = ref(10);
  const totalPages = ref(1);
  const route = useRoute();
  const filter = ref('');
  const sort = ref<string>('');
  const cart = reactive<Cart>({});
  const availableAttributes = ref<{ name: string, values: string[] }[]>([]);
  const attributeFilters = ref<Record<string, string>>({});
  const currentPage = ref(Number(route.query.page) || 1);
  const router = useRouter();
  const priceMin = ref<string>('');
  const priceMax = ref<string>('');
  const maxPricePlaceholder = ref();
  const priceMinPlaceholder = ref();

  const isPriceFilterDisabled = computed(() => {
    return priceMin.value === '0' && priceMax.value === '0';
  });

  onMounted(() => {
    counter.updateCountFromCart();
    getProducts();
    loadCartFromLocalStorage();
    window.addEventListener('resize', getProducts);
    
  });
  

  function restoreScrollPosition() {
    const scrollY = localStorage.getItem("scrollY");
    if (scrollY) {    
      window.scrollTo(0, parseInt(scrollY));
    }    
  }

  function getProducts() {  
    let categoryID = route.params.categoryID;

  
    if (Array.isArray(categoryID)) {
      categoryID = categoryID[0];
    }

    if (!categoryID) {
      return;
    }

    const savedFilters = localStorage.getItem('savedFilters');
    if (savedFilters) {
      const parsedFilters: SavedFilters = JSON.parse(savedFilters);
      if (parsedFilters.filter) {
        filter.value = parsedFilters.filter;
      }

      if (parsedFilters.sort) {
        sort.value = parsedFilters.sort;
      }

      if (parsedFilters.attributeFilters && Object.keys(parsedFilters.attributeFilters).length > 0) {
        attributeFilters.value = { ...parsedFilters.attributeFilters };
      }
      if (parsedFilters.priceMn){
        priceMin.value = parsedFilters.priceMn;
      }
      if (parsedFilters.priceMx){
        priceMax.value = parsedFilters.priceMx;
      }
    }    

    fetchCategoryProducts(
      categoryID,
      currentPage.value,
      pageSize.value,
      filter.value,
      sort.value,
      window.innerWidth,
      attributeFilters.value,
      priceMin.value !== undefined && priceMin.value !== '' ? Number(priceMin.value) : undefined,
      priceMax.value !== undefined && priceMax.value !== '' ? Number(priceMax.value) : undefined
    )
      .then(data => {      
        products.value = data.results;  
        availableAttributes.value = data.available_attributes; 
        totalPages.value = Math.ceil(data.count / data.page_size);   

        if (data.price_range?.max_price) {
          maxPricePlaceholder.value = data.price_range.max_price;
        }

        if (data.price_range?.min_price) {
          priceMinPlaceholder.value = data.price_range.min_price;
        }

        return nextTick();    
      })
      .then(() => {
        restoreScrollPosition();
      })
      .catch((error: AxiosError) => {
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
        quantity: 1,
        quantity_max: product.quantity
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


  function fetchProducts(page: number) {
    currentPage.value = page;

    router.push({ query: { ...route.query, page: currentPage.value } });

    getProducts();    
  }


  function loadCartFromLocalStorage() {
    const storedCart = JSON.parse(localStorage.getItem('cart') || '{}');
    for (const id in storedCart) {
      if (storedCart.hasOwnProperty(id)) {
        cart[parseInt(id)] = storedCart[id];
      }
    }
  }

  function clearFilter(key: string) {
    delete attributeFilters.value[key];
    localStorage.removeItem("savedFilters")
    localStorage.removeItem("scrollY")
    getProducts();
  }

  const applyPriceFilter = () => {
    localStorage.removeItem("scrollY");
    fetchProducts(1);
  };
 

  const applyPriceFilterDebounced = debounce(() => { 
    applyPriceFilter();
  }, 800);

  function handlePriceMinInput(event: Event) {
    const input = event.target as HTMLInputElement;
    const originalValue = input.value;
    const cleanedValue = originalValue.replace(/[^0-9]/g, '');
    
    if (cleanedValue !== originalValue) {
      priceMin.value = cleanedValue;
      input.value = cleanedValue;
    } else {
      priceMin.value = originalValue;
    }
    
    applyPriceFilterDebounced();
  }

  function handlePriceMaxInput(event: Event) {
    const input = event.target as HTMLInputElement;
    const originalValue = input.value;
    const cleanedValue = originalValue.replace(/[^0-9]/g, '');
    
    if (cleanedValue !== originalValue) {
      priceMax.value = cleanedValue;
      input.value = cleanedValue;
    } else {
      priceMax.value = originalValue;
    }
    
    applyPriceFilterDebounced();
  }


  function debounce<F extends (...args: any[]) => any>(fn: F, delay: number): (...args: Parameters<F>) => void {
    let timeoutId: ReturnType<typeof setTimeout> | null = null;
    
    return function(...args: Parameters<F>) {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      timeoutId = setTimeout(() => fn.apply(null, args), delay);
    };
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
    availableAttributes,
    attributeFilters, 
    clearFilter,
    priceMin,
    priceMax,
    maxPricePlaceholder,
    applyPriceFilter,
    isPriceFilterDisabled,
    priceMinPlaceholder,
    handlePriceMaxInput,
    handlePriceMinInput,
  };
}