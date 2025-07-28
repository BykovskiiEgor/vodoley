import { ref, reactive, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { requestSearchImage } from "@/composables/useAPI";
import { useProductsStore } from '@/stores/productsByImage';

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
  name: string;
  price: number;
  image: string;
  quantity: number;
}

interface Cart {
  [id: number]: CartItem;
}

export function useSearchByImage() {
  const products = ref<Product[]>([]); 
  const route = useRoute(); 
  const cart = reactive<Cart>({});

  const productsStore = useProductsStore();
  const searchProducts = productsStore.products;

  onMounted(() => {
    products.value = productsStore.products; 
    loadCartFromLocalStorage();  
  });

  watch(() => productsStore.products, (newProducts) => {
    products.value = newProducts;  
  });
  const imageBase64 = ref([]);

  function getProducts() {   
    if (imageBase64.value.length > 0) {
        try {
            const base64Image = imageBase64.value[0];  
            const response = requestSearchImage(base64Image);            
            
        } catch (error) {
            console.error("Error searching by image:", error);
        }
    } else {
        console.log("No image selected");
    }    
    
  }


  function addToCart(product: Product) {
    if (cart[product.id]) {
      cart[product.id].quantity += 1;
    } else {
      cart[product.id] = {
        id: product.id,
        name: product.name,
        price: product.discount_price || product.price,
        image: product.image,
        quantity: 1
      };
    }
    updateLocalStorage();
  }

  function increment(product: Product) {
    cart[product.id].quantity += 1;
    updateLocalStorage();
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
  }


  function loadCartFromLocalStorage() {
    const storedCart = JSON.parse(localStorage.getItem('cart') || '{}');
    for (const id in storedCart) {
      if (storedCart.hasOwnProperty(id)) {
        cart[parseInt(id)] = storedCart[id];
      }
    }
  }

  return {
    products,    
    cart,
    addToCart,
    increment,
    decrement,
    searchProducts,
    productsStore,
  };
}
