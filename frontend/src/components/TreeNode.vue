<template>
  <div>
    <ul v-if="children && children.length">
      <li v-for="(child, index) in visibleChildren" :key="child.id">
        <div class="category-item">        
            <router-link class="subcategory-link" :to="`/products/${child.id}`">{{ child.name }}</router-link>    
          <button 
            class="collapse-button" 
            v-if="child.children.length" 
            @click="toggleCollapse(child.id)"
          >
            <IconDown v-if="collapsedCategories.includes(child.id)" />
            <IconDown v-else style="transform: rotate(0.5turn);" />
          </button>
        </div>
        <TreeNode 
          v-if="child.children && child.children.length && !collapsedCategories.includes(child.id)"
          :children="child.children" 
          :collapsed-categories="collapsedCategories"
          @toggle-collapse="toggleCollapse"
        />
      </li>
      <button
        style="margin-left: 10px;"
        class="collapse-button" 
        v-if="showMoreButton" 
        @click="showMore"
      >
        <p >Ещё</p>
      </button>
      <button 
        style="margin-left: 10px;"
        class="collapse-button" 
        v-if="showLessButton" 
        @click="showLess"
      >
        <p>Свернуть</p>
      </button>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import IconUp from '@/components/icons/IconUp.vue';
import IconDown from '@/components/icons/IconDown.vue';

interface Category {
  id: number;
  name: string;
  parent: string | null;
  children: Category[];
}

const props = defineProps<{
  children: Category[];
  max?: number;
  collapsedCategories: number[]; 
}>();

const emit = defineEmits<{
  (event: 'toggle-collapse', categoryId: number): void;
}>();

const showAll = ref(false);

const visibleChildren = computed(() => {
  if (props.max && !showAll.value) {
    return props.children.slice(0, props.max); 
  }
  return props.children; 
});

const showMoreButton = computed(() => {
  return props.max && props.children.length > props.max && !showAll.value;
});

const showLessButton = computed(() => {
  return props.max && props.children.length > props.max && showAll.value;
});

const showMore = () => {
  showAll.value = true;
};

const showLess = () => {
  showAll.value = false;
};

const toggleCollapse = (categoryId: number) => {
  emit('toggle-collapse', categoryId); 
};
</script>

<style scoped>
ul{
  list-style: none;
  padding-left: 0;
}

li{
  padding-left: 10px;
}

.subcategory-link {
  text-decoration: none;
  color: inherit;
  padding-bottom: 4px;  
  font-weight: 350;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.collapse-button {
  background-color: transparent;
  border: none; 
  padding: 0; 
  cursor: pointer; 
  display: flex;
}

.collapse-button:focus {
  outline: none; 
}
</style>
