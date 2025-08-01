import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await api.post('/token/refresh/', {
          refresh: refreshToken
        });
        
        localStorage.setItem('access_token', response.data.access);
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
        return api(originalRequest);
      } catch (err) {        
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');        
        return Promise.reject(err);
      }
    }
    
    return Promise.reject(error);
  }
);

// Функция для получения одного продукта по артикулу
export async function fetchProduct(id: number) {
  try {
    const response = await api.get(`/current-items/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Ошибка загрузки продукта:', error);
    throw error;
  }
}

// Функция для получения всех продуктов
export async function fetchAllProducts() {
  try {
    const response = await api.get('/items/');
    return response.data;
  } catch (error) {
    console.error('Ошибка загрузки продуктов:', error);
    throw error;
  }
}

// Функция для получения рекомендованных продуктов
export async function fetchRecommendedProducts(page: number, pageSize: number, screenWidth: number) {
  try {
    const response = await api.get('/recommendations/', {
      params: {
        page: page,
        page_size: pageSize,       
        screen_width: screenWidth
      }
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка загрузки рекомендованных продуктов:', error);
    throw error;
  }
}

// Функция для получения продуктов со скидкой
export async function fetchDiscountedProducts(page: number, pageSize: number) {
  try {
    const response = await api.get('/discounts/', {
      params: {
        page,
        page_size: pageSize,
        screen_width: window.innerWidth
      }
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка загрузки продуктов со скидкой:', error);
    throw error;
  }
}

// Функция для получения заказов пользователя
export async function fetchOrders(email: string, filter: string) {
  try {
    const response = await api.post('/get-orders/', { email }, 
      {
        params: {
          filter: filter,
        }
      });
    return response.data;     
  } catch (error) {
    console.error('Error fetching orders:', error);
    throw error;
  } 
}

// Функция для отправки запроса на получение временного пароля
export async function requestPassword(email: string): Promise<void> {
  try {
    const response = await api.post('/get-password/', { email });
    console.log('Temporary password sent:', response.data);
    alert('Временный пароль для входа отправлен на указанную почту.');
  } catch (error) {
    console.error('Error requesting password:', error);
    alert('Error requesting password. Please try again later.');
    throw error;
  }
}

// Функция для получения товаров по поиску
export async function fetchSearchProducts(query: string, page: number, pageSize: number, filter: string, sort: string, screenWidth: number) {
  try {
    const response = await api.get('/search/', {
      params: {
        q: query,
        page: page,
        page_size: pageSize,
        filter: filter,
        sort: sort,
        screen_width: screenWidth
      }
    });
    return response.data;
  } catch (error) {
    console.error('Fetch products error:', error);
    throw error;
  }
}


// Функция для получения списка товаров по поиску
export async function fetchSearchProductsList(query: string){
  try {
    const response = await api.get(`/search/?q=${encodeURIComponent(query)}`);
    return response;
  } catch (error) {
    console.error('Fetch products error:', error);
    throw error;
  }
}


// Функция для получения товаров по категориям 
export async function fetchCategoryProducts(categoryID: string, page: number, pageSize: number, filter: string, sort: string, screenWidth: number, attributeFilters:Record<string, string>, priceMin: number=0, priceMax: number=0) {
  try {
    const response = await api.get(`/items/category/${categoryID}`, {
      params: {             
        page: page,
        page_size: pageSize,
        filter: filter,
        sort: sort,
        screen_width: screenWidth,
        attributeFilters: attributeFilters,
        priceMin: priceMin,
        priceMax: priceMax,
        }
    });    
    sessionStorage.removeItem("savedFilters")    
    return response.data;
  } catch (error) {
    console.error('Fetch products error:', error);
    throw error;
  }
}


// Функция для получения категорий товаров
export async function fetchCategory(){
  try {
    const response = await api.get('/categories/');
    return response.data;
  } catch (error) {
    console.error('Fetch categories error:', error);
    throw error;
    }
}


// Функция для изменения почты
export async function requestEditEmail(email: string){
  try {
    const response = await api.patch('/update-email/', {email});
    return response.data;
  } catch (error) {
    console.error('Edit email error:', error);
    throw error;
    }
}

// Функция для изменения номера
export async function requestEditPhone(phone_number: string){
  try {
    const response = await api.patch('/update-phone/', {phone_number});
    return response.data;
  } catch (error) {
    console.error('Edit email error:', error);
    throw error;
    }
}

// Функция для оценки товара
export async function requestRateItem(productId: number, rate: number){
  try {
    const response = await api.post('/rate-item/', { productId, rate});
    return response.data;
  } catch (error) {
    console.error('Rate error:', error);
    throw error;
    }
}

export async function requestSearchImage(image: string){
  try{    
    const response = await api.post('/search-photo/', { image }); 
    return response.data;
  } catch(error){
    throw error;
  }
}

export async function requestCreateOrder(order: any){
  try{
    const response = await api.post('/create_order/', {order});
    return response.data
  }catch(error){
    throw error;
  }
}


export async function requestLogin(user: any){
  try{
    const response = await api.post('/login/', user);
    return response
  }catch(error){
    throw error;
  }
}