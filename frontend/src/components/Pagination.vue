<template>
  <div class="pagination justify-content-center">
    <button 
      class="btn btn-outline-dark pagination-btn" 
      @click="goToPage(currentPage - 1), clearYposition()" 
      :disabled="isFirstPage">
      <prev-icon />
    </button>

    <button 
      class="btn btn-outline-dark pagination-btn" 
      @click="goToPage(1), clearYposition()" 
      :disabled="isFirstPage">1
    </button>

    <span class="pagination-info">Страница {{ currentPage }} из {{ totalPages }}</span>

    <button 
      class="btn btn-outline-dark pagination-btn" 
      @click="goToPage(totalPages), clearYposition()" 
      :disabled="isLastPage">{{ totalPages }}
    </button>

    <button 
      class="btn btn-outline-dark pagination-btn" 
      @click="goToPage(currentPage + 1), clearYposition()" 
      :disabled="isLastPage">
      <next-icon />
    </button>
  </div>
</template>

<script>
import PrevIcon from './icons/prevIcon.vue';
import NextIcon from './icons/nextIcon.vue';

export default {
  components: {
    PrevIcon,
    NextIcon
  },
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    }
  },
  computed: {
    isFirstPage() {
      return this.currentPage === 1;
    },
    isLastPage() {
      return this.currentPage === this.totalPages;
    }
  },
  methods: {
    goToPage(page) {
      this.$emit('page-changed', page);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    clearYposition() {
      localStorage.removeItem("scrollY")
    }
    
  }
};
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 30px;
}

.pagination-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.pagination-info {
  margin: 0 10px;
}

.pagination-btn svg {
  width: 20px;
  height: 20px;
}
</style>
