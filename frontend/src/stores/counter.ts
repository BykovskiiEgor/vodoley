import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
  }),
  actions: {
    updateCountFromCart() {
      const cart = JSON.parse(localStorage.getItem('cart') || '{}');
      this.count = Object.keys(cart).length; 
    },
    increment() {
      this.count++;
    },
    decrement() {
      if (this.count > 0) this.count--;
    },
    empty() {
      this.count = 0;
    },
  },
});