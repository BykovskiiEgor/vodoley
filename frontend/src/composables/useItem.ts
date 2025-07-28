import { ref, onMounted, watch, reactive, onUnmounted, nextTick} from 'vue';
import { useRoute } from 'vue-router';
import { fetchProduct, requestRateItem } from './useAPI';
import { useCounterStore } from '@/stores/counter';

interface Product {
  id: number;
  article: string;
  name: string;
  description: string;
  price: number;
  discount_price?: number;
  image: string;
  available: boolean;
  exists: boolean;
  images: { image: string }[];
  attributes: { attribute: { name: string }; value: string }[];
  avg_rating?: string;
  user_rating?: number;
  quantity: number;
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

interface User {
  email?: string;
  first_name?: string;
  last_name?: string;
  phone_number?: string;   
}

export function useItem() {
  const counter = useCounterStore();
  const products = ref<Product[]>([]);
  const route = useRoute();
  const productId = ref<number>(parseInt(route.params.id as string, 10));
  const cart = reactive<Cart>({});
  const isRequestFormVisible = ref(false);  
  const currentIndex = reactive<{ [key: number]: number }>({});
  const textToCopy = ref<HTMLElement | null>(null);
  const isCopied = ref(false);
  const startIndex = ref(0);
  const imageStyle = ref({
    transform: 'scale(1)',
    transformOrigin: 'center',
    transition: 'transform 0.2s ease-out',
  });
  const zoomVisible = ref(false);
  const zoomPosition = reactive({ x: 0, y: 0 });
  const zoomBackground = ref('');
  const scaleImage = ref(false);
  const isSticky = ref(false);
  let observer: IntersectionObserver | null = null;
  const isExpanded = ref(false);
  const isDesktop = ref(window.innerWidth >= 1024);
  const user = ref<User>({});    
  const isUser = ref(false);
    

  onMounted(() => {
    loadProduct(productId.value);
    loadCartFromLocalStorage();  
    loadUserFromLocalStorage();
    counter.updateCountFromCart();
   
    const waitForSentinel = setInterval(() => {
      const sentinel = document.querySelector('.sticky-sentinel');
      if (sentinel) {  
        observer = new IntersectionObserver(
          ([entry]) => {
            isSticky.value = !entry.isIntersecting;
          },
          {
            root: null,
            threshold: 0, 
          }
        );
  
        observer.observe(sentinel);
        clearInterval(waitForSentinel);
        updateStickyPosition
      }
    }, 500);
  });

  onUnmounted(() => {
    if (observer) {
      observer.disconnect();
    }
  });

  watch(
    () => route.params.id,
    (newId) => {
      const newProductId = parseInt(newId as string, 10);
      if (newProductId !== productId.value) {
        productId.value = newProductId;
        loadProduct(newProductId);
      }
    }
  );

  function loadUserFromLocalStorage() {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
        try {
            const userData = JSON.parse(storedUser);
            if (userData?.user) {
                isUser.value = true;
                user.value = {
                    email: userData.user.email,
                    first_name: userData.user.first_name,
                    last_name: userData.user.last_name,
                    phone_number: userData.user.phone_number
                };
                console.log('User loaded from localStorage:', user.value);
            }
        } catch (error) {
            console.error('Error parsing user data:', error);
        }
    }
}

  async function loadProduct(id: number) {
    try {
      const productData = await fetchProduct(id);
      products.value = [productData];
      currentIndex[productData.id] = 0;
    } catch (error) {
      console.error('Ошибка загрузки продукта:', error);
    }
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
    if (cart[product.id]) {
      if (cart[product.id].quantity < product.quantity) {
        cart[product.id].quantity += 1;}
      updateLocalStorage();
    }
  }

  function decrement(product: Product) {
    if (cart[product.id]) {
      if (cart[product.id].quantity > 1) {
        cart[product.id].quantity -= 1;
      } else {
        delete cart[product.id];
      }
      updateLocalStorage();
      
    }
  }

  function updateLocalStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
    counter.updateCountFromCart();
  }

  function loadCartFromLocalStorage() {
    const storedCart = JSON.parse(localStorage.getItem('cart') || '{}');
    for (const id in storedCart) {
      cart[parseInt(id, 10)] = storedCart[id];
    }
  }

  function showRequestForm(){
    isRequestFormVisible.value = true;
  }

  function hideRequestForm(){
    isRequestFormVisible.value = false;
  }

  const currentImage = (product: Product) => {
    return product.images[currentIndex[product.id]]?.image || product.image;
  };

  const changeImage = (productId: number, index: number) => {
    currentIndex[productId] = index;
  };

  const copyText = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      isCopied.value = true; 
  
      setTimeout(() => {
        isCopied.value = false;
      }, 2000);
    } catch (error) {
      console.error('Ошибка при копировании текста:', error);
    }
  };

  const scrollImages = (productId: number, direction: number) => {
    const product = products.value.find(p => p.id === productId);
    if (!product) return;
  
    const maxIndex = product.images.length - 1;
    let newIndex = (currentIndex[productId] ?? 0) + direction;
  
    if (newIndex > maxIndex) {
      newIndex = 0; 
    } else if (newIndex < 0) {
      newIndex = maxIndex; 
    }
  
    currentIndex[productId] = newIndex;
  
    if (newIndex < startIndex.value) {
      startIndex.value = newIndex;
    } else if (newIndex >= startIndex.value + 5) {
      startIndex.value = newIndex - 4;
    }
  };
  
  const showMoreImages = (direction: number, productId: number) => {
    scrollImages(productId, direction);
  };

  const handleMouseMove = (event: MouseEvent, product: Product) => {
    if (!scaleImage.value) return;
    zoomVisible.value = true;
    const container = event.currentTarget as HTMLElement;
    const img = container.querySelector('.zoom-image') as HTMLImageElement;
    if (!img) return;
  
    const { offsetX: mouseX, offsetY: mouseY } = event;
    const { offsetWidth: containerWidth, offsetHeight: containerHeight } = container;
  
    const xPercent = (mouseX / containerWidth) * 100;
    const yPercent = (mouseY / containerHeight) * 100;
  
    zoomPosition.x = mouseX;
    zoomPosition.y = mouseY;
  
    zoomBackground.value = `url(${currentImage(product)})`;
    imageStyle.value = {
      transform: `scale(3)`,
      transformOrigin: `${xPercent}% ${yPercent}%`,
      transition: 'transform 0.2s ease-out'
    };
  };
  
  const handleMouseLeave = () => {
    zoomVisible.value = false;
    imageStyle.value = {
      transform: 'scale(1)',
      transformOrigin:'',
      transition: 'transform 0.2s ease-out'
    };
  };

  const ScaleImage = () =>{
    scaleImage.value = true;

    if (scaleImage){
      scaleImage.value = false;
    }
  }   

  function updateStickyPosition() {  
    if (!isDesktop.value) {
      isSticky.value = false;
      return;
    }  
    const container = document.querySelector('.container') as HTMLImageElement;
    const stickyBox = document.querySelector('.product-info-box.sticky') as HTMLImageElement;
  
    if (!container || !stickyBox) return;
  
    const containerRect = container.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
  
    const maxRight = viewportWidth - containerRect.right + 15;
    stickyBox.style.right = `${Math.max(0, maxRight)}px`;
    stickyBox.style.visibility = `visible`; 
  }
    
  
  window.addEventListener('resize', updateStickyPosition);
  window.addEventListener('scroll', updateStickyPosition);
  updateStickyPosition();

  window.addEventListener('resize', () => {
    isDesktop.value = window.innerWidth >= 1024;
  });

  function showFullAtt() {
    isExpanded.value = !isExpanded.value;
  }

  async function handleRatingSelected(rating: number){
    try {
      const response = await requestRateItem(productId.value, rating)
      
    } catch (error) {
      console.error('Ошибка оценки продукта:', error);
    }
  }
    
  return {
    products,
    cart,
    addToCart,
    increment,
    decrement,    
    isRequestFormVisible, 
    showRequestForm,   
    hideRequestForm,
    currentImage,
    changeImage, 
    currentIndex, 
    copyText, 
    isCopied, 
    textToCopy,
    scrollImages,
    showMoreImages,
    startIndex,
    handleMouseMove,
    handleMouseLeave,
    imageStyle,
    ScaleImage,
    scaleImage,
    isSticky,
    showFullAtt,
    isExpanded,
    isUser,
    handleRatingSelected,
  };
}
