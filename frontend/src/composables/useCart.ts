import { ref, computed, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';


interface Product {
  id: number;
  article: string;
  name: string;  
  price: number;
  discount_price?: number;
  images: { image: string }[];
  quantity: number;
  available: boolean;
  quantity_max: number;
}

interface CalculatedProduct extends Product {
  appliedPrice: number;   
  itemTotal: number;      
}

interface TotalPriceResult {
  items: CalculatedProduct[]; 
  total: number;             
}


export function useCart() {
  const counter = useCounterStore();
  const cartEmpty = ref(false);
  const products = ref<Record<number, Product>>({});
  const isMobile = ref(false);
  const checkScreen = () => {
    isMobile.value = window.innerWidth <= 440;
  };

  onMounted(() => {
    counter.updateCountFromCart();
    checkScreen();
    window.addEventListener('resize', checkScreen);
  });
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
    updateCartEmptyState();
  }
  
  function saveCartItems() {    
    localStorage.setItem('cart', JSON.stringify(products.value));
    updateCartEmptyState();
  }
  
  function clearCart() {
    products.value = {};
    localStorage.removeItem('cart');
    updateCartEmptyState();
  }  
  
  function removeFromCart(id: number) {
    if (products.value[id]) {
      delete products.value[id];
      saveCartItems();
    }
  }
  
  function increment(product: Product){
    if (products.value[product.id]){
      if(products.value[product.id].quantity < product.quantity_max){
        products.value[product.id].quantity += 1;
        saveCartItems();   
      }      
    }
  }
  
  function decrement(product: Product){
    if (products.value[product.id]){
      products.value[product.id].quantity -= 1;
      if (products.value[product.id].quantity <= 0) {
        delete products.value[product.id];
      }
      saveCartItems();
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
  
  function updateCartEmptyState() {
    counter.updateCountFromCart();
    cartEmpty.value = Object.keys(products.value).length === 0;    
  }
  
  const calculatedPrices = computed(() => calculateTotalPrice(products.value));
  return {
    cartEmpty,
    products,
    loadCartItems,
    clearCart,
    removeFromCart,
    calculateTotalPrice,
    increment,
    decrement,
    calculatedPrices,
    isMobile,
  };
}
