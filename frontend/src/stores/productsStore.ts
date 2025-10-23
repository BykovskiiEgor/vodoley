import {defineStore} from 'pinia'

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

interface ProductsState {
    products: Record<string, Product[]>; 
    totalPages: Record<string, number>;  
    currentPage: Record<string, number>; 
    pageSize: number;
    filter: string;
    sort: string;
    attributeFilters: Record<string, Record<string, string>>; 
    priceMin: Record<string, string>; 
    priceMax: Record<string, string>; 
    currentCategory: string | null; 
}

export const useProductsStore = defineStore('products', {
    state: (): ProductsState => ({
        products: {},
        totalPages: {},
        currentPage: {},
        pageSize: 10,
        filter: '',
        sort: '',
        attributeFilters: {},
        priceMin: {},
        priceMax: {},
        currentCategory: null,
    }),

    actions: {
        setProducts(categoryID: string | number, products: Product[], totalPages: number) {
            const catId = String(categoryID); 
            if (!this.products || typeof this.products !== 'object') this.products = {};
            if (!this.totalPages || typeof this.totalPages !== 'object') this.totalPages = {};
            if (!this.currentPage || typeof this.currentPage !== 'object') this.currentPage = {};
            if (!this.attributeFilters || typeof this.attributeFilters !== 'object') this.attributeFilters = {};
            if (!this.priceMin || typeof this.priceMin !== 'object') this.priceMin = {};
            if (!this.priceMax || typeof this.priceMax !== 'object') this.priceMax = {};

            this.products[catId] = products;
            this.totalPages[catId] = totalPages;
            if (!this.currentPage[catId]) this.currentPage[catId] = 1;
        },
        
        setPage(categoryID: string | number, page: number) {
            const catId = String(categoryID);
            if (!this.currentPage || typeof this.currentPage !== 'object') this.currentPage = {};
            this.currentPage[catId] = page;
        },
        
        setCurrentCategory(categoryID: string | number) {
            const catId = String(categoryID);
            this.currentCategory = catId;
            
            if (!this.attributeFilters[catId]) {
                this.attributeFilters[catId] = {};
            }
            if (!this.priceMin[catId]) {
                this.priceMin[catId] = '';
            }
            if (!this.priceMax[catId]) {
                this.priceMax[catId] = '';
            }
        },
        
        setAttributeFilters(filters: Record<string, string>) {
            if (this.currentCategory) {
                this.attributeFilters[this.currentCategory] = filters;
            }
        },
        
        setPriceRange(min: string, max: string) {
            if (this.currentCategory) {
                this.priceMin[this.currentCategory] = min;
                this.priceMax[this.currentCategory] = max;
            }
        },
        
        getAttributeFilters(): Record<string, string> {
            return this.currentCategory ? this.attributeFilters[this.currentCategory] || {} : {};
        },
        
        getPriceRange(): { min: string, max: string } {
            if (this.currentCategory) {
                return {
                    min: this.priceMin[this.currentCategory] || '',
                    max: this.priceMax[this.currentCategory] || ''
                };
            }
            return { min: '', max: '' };
        },
        
        resetCurrentCategoryFilters() {
            if (this.currentCategory) {
                this.attributeFilters[this.currentCategory] = {};
                this.priceMin[this.currentCategory] = '';
                this.priceMax[this.currentCategory] = '';
                this.currentPage[this.currentCategory] = 1;
            }
        },
        
        resetCategory(categoryID: string | number) {
            const catId = String(categoryID);
            this.products[catId] = [];
            this.totalPages[catId] = 1;
            this.currentPage[catId] = 1;
            this.attributeFilters[catId] = {};
            this.priceMin[catId] = '';
            this.priceMax[catId] = '';
        },
        
        reset() {
            this.products = {};
            this.totalPages = {};
            this.currentPage = {};
            this.filter = '';
            this.sort = '';
            this.attributeFilters = {};
            this.priceMin = {};
            this.priceMax = {};
            this.currentCategory = null;
        },
    },

    persist: {
        key: 'products-store',
        storage: sessionStorage,
    },
});