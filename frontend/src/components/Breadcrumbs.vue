<template>
  <nav class="breadcrumbs">
    <ul class="crumbs">
      <li v-for="(crumb, index) in breadcrumbs" :key="index" class="flex items-center">
        <router-link
          :to="`/products/${crumb[1]}`"
          class="cr"
        >
          {{ crumb[0] }}
        </router-link>        
        <span v-if="index !== breadcrumbs.length - 1" class="mx-1">/</span>
      </li>
    </ul>
  </nav>
</template>
<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ProductBreadcrumbs',
  props: {
    product: {
      type: Object as () => { breadcrumbs: [string, number][] },
      required: true,
    },
  },
  computed: {
    breadcrumbs() {
      return this.product.breadcrumbs
    },
  },
})
</script>

<style scoped>
.breadcrumbs{
  display: flex;  
}

.crumbs{
  display: flex;
  list-style: none;
  padding-left: 0;
}

.cr{
  color: black
}

.cr:hover{
  color: #003464;
}
</style>
