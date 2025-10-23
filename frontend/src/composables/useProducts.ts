import { ref, reactive, onMounted, onBeforeUnmount, watch, computed, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { fetchCategoryProducts } from './useAPI';
import { useCounterStore } from '@/stores/counter';
import { useProductsStore } from '@/stores/productsStore';

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

export function useProducts() {
  const counter = useCounterStore();
  const cart = reactive<Cart>({});
  const availableAttributes = ref<{ name: string; values: string[] }[]>([]);
  const maxPricePlaceholder = ref<number>();
  const priceMinPlaceholder = ref<number>();

  const route = useRoute();
  const router = useRouter();
  const store = useProductsStore();

  const currentAttributeFilters = computed(() => store.getAttributeFilters());
  const currentPriceRange = computed(() => store.getPriceRange());
  
  const isPriceFilterDisabled = computed(() => 
    currentPriceRange.value.min === '0' && currentPriceRange.value.max === '0'
  );

  function getCurrentCategoryID() {
    return Array.isArray(route.params.categoryID)
      ? route.params.categoryID[0]
      : route.params.categoryID;
  }

  function debounce<F extends (...args: any[]) => any>(fn: F, delay: number): (...args: Parameters<F>) => void {
    let timeoutId: ReturnType<typeof setTimeout> | null = null;
    return function(...args: Parameters<F>) {
      if (timeoutId) clearTimeout(timeoutId);
      timeoutId = setTimeout(() => fn.apply(null, args), delay);
    };
  }

  function loadCartFromLocalStorage() {
    const storedCart = JSON.parse(localStorage.getItem('cart') || '{}');
    for (const id in storedCart) {
      if (storedCart.hasOwnProperty(id)) cart[parseInt(id)] = storedCart[id];
    }
  }

  function updateLocalStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
    counter.updateCountFromCart();
  }

  function addToCart(product: Product) {
    if (cart[product.id]) cart[product.id].quantity += 1;
    else
      cart[product.id] = {
        id: product.id,
        article: product.article,
        name: product.name,
        price: product.price,
        discount_price: product.discount_price,
        images: product.images,
        quantity: 1,
        quantity_max: product.quantity,
      };
    updateLocalStorage();
  }

  function increment(product: Product) {
    if (cart[product.id]?.quantity < product.quantity) {
      cart[product.id].quantity += 1;
      updateLocalStorage();
    }
  }

  function decrement(product: Product) {
    if (cart[product.id]?.quantity > 1) cart[product.id].quantity -= 1;
    else delete cart[product.id];
    updateLocalStorage();
  }

  async function getProducts() {
    const categoryID = getCurrentCategoryID();
    if (!categoryID) return;

    store.setCurrentCategory(categoryID);

    const currentPage = store.currentPage?.[categoryID] || 1;
    const attributeFilters = currentAttributeFilters.value;
    const priceRange = currentPriceRange.value;

    try {
      const data = await fetchCategoryProducts(
        categoryID,
        currentPage,
        store.pageSize,
        store.filter,
        store.sort,
        window.innerWidth,
        attributeFilters, 
        priceRange.min ? Number(priceRange.min) : undefined,
        priceRange.max ? Number(priceRange.max) : undefined
      );

      store.setProducts(categoryID, data.results, Math.ceil(data.count / data.page_size));
      availableAttributes.value = data.available_attributes || [];

      if (data.price_range?.max_price) maxPricePlaceholder.value = data.price_range.max_price;
      if (data.price_range?.min_price) priceMinPlaceholder.value = data.price_range.min_price;

    } catch (error) {
      console.error('Fetch products error', error);
      store.setProducts(categoryID, [], 1);
    }
  }

  function fetchProducts(page: number) {
    const categoryID = getCurrentCategoryID();
    store.setPage(categoryID, page);
    router.push({ query: { ...route.query, page } });
    getProducts();
  }

  const applyPriceFilter = () => {
    fetchProducts(1);
  };

  const applyPriceFilterDebounced = debounce(applyPriceFilter, 800);

  function handlePriceMinInput(event: Event) {
    const input = event.target as HTMLInputElement;
    const cleanedValue = input.value.replace(/[^0-9]/g, '');
    
    const priceRange = currentPriceRange.value;
    store.setPriceRange(cleanedValue, priceRange.max);
    
    input.value = cleanedValue;
    applyPriceFilterDebounced();
  }

  function handlePriceMaxInput(event: Event) {
    const input = event.target as HTMLInputElement;
    const cleanedValue = input.value.replace(/[^0-9]/g, '');
    
    const priceRange = currentPriceRange.value;
    store.setPriceRange(priceRange.min, cleanedValue);
    
    input.value = cleanedValue;
    applyPriceFilterDebounced();
  }

  function clearFilter(key: string) {
    const categoryID = getCurrentCategoryID();
    if (categoryID && store.attributeFilters[categoryID]) {
      const updatedFilters = { ...currentAttributeFilters.value };
      delete updatedFilters[key];
      store.setAttributeFilters(updatedFilters);
    }
    fetchProducts(1);
  }

  function updateAttributeFilters(filters: Record<string, string>) {
    store.setAttributeFilters(filters);
    fetchProducts(1);
  }

  function resetAllFilters() {
    store.resetCurrentCategoryFilters();
    fetchProducts(1);
  }

  const currentCategoryID = computed(() => getCurrentCategoryID());
  
  const currentPage = computed({
    get: () => store.currentPage?.[currentCategoryID.value] ?? 1,
    set: (val: number) => store.setPage(currentCategoryID.value, val),
  })

  const totalPages = computed(() => store.totalPages?.[currentCategoryID.value] ?? 1)

  const handleResize = debounce(getProducts, 300);

  onMounted(async () => {
    counter.updateCountFromCart();
    loadCartFromLocalStorage();
    await nextTick();

    const categoryID = getCurrentCategoryID();
    if (!categoryID) return;

    store.setCurrentCategory(categoryID);

    if (!store.currentPage?.[categoryID]) store.setPage(categoryID, 1);
    if (!store.totalPages?.[categoryID]) store.totalPages[categoryID] = 1;

    getProducts();
    window.addEventListener('resize', handleResize);
  });

  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize);
  });  

  watch(() => route.params.categoryID, (newCategory, oldCategory) => {
    if (newCategory !== oldCategory) {
      const categoryID = getCurrentCategoryID();
      
      store.setCurrentCategory(categoryID);
      
      store.setPage(categoryID, 1);    
      router.replace({ query: { ...route.query, page: 1 } });
      getProducts();
    }
  });

  return {
    store,
    cart,
    addToCart,
    increment,
    decrement,
    fetchProducts,
    availableAttributes,
    clearFilter,
    updateAttributeFilters, 
    resetAllFilters, 
    applyPriceFilter,
    isPriceFilterDisabled,
    handlePriceMaxInput,
    handlePriceMinInput,
    maxPricePlaceholder,
    priceMinPlaceholder,
    currentPage,
    totalPages,
    currentAttributeFilters, 
    currentPriceRange, 
  };
}