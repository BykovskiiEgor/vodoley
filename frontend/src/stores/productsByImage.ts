import { defineStore } from 'pinia';
import { ref } from 'vue';

interface SearchProducts{
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

export const useProductsStore = defineStore('products', () => {
    const products = ref<SearchProducts[]>([]);

    const setProducts = (searchProducts: SearchProducts[]) => {
        products.value = searchProducts;
    };
    

    return {
        products,
        setProducts
    };
});
