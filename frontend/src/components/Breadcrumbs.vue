<template>
  <nav v-if="breadcrumbs.length" class="breadcrumb">
    <ul>
      <li v-for="(bc, index) in breadcrumbs" :key="index">
        <router-link v-if="index < breadcrumbs.length - 1" :to="bc.path">
          {{ bc.label }}
        </router-link>
        <span v-else>{{ bc.label }}</span>
      </li>
    </ul>
  </nav>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

interface Breadcrumb {
  label: string;
  path: string;
}

const route = useRoute();
const router = useRouter();

const breadcrumbs = computed<Breadcrumb[]>(() => {
  const matched = route.matched.filter(r => r.meta?.breadcrumb);
  return matched.map(r => ({
    label: r.meta.breadcrumb as string,
    path: r.path,
  }));
});
</script>

<style scoped>
.breadcrumb ul {
  display: flex;
  gap: 0.5rem;
}
.breadcrumb li::after {
  content: '>';
  margin: 0 0.5rem;
}
.breadcrumb li:last-child::after {
  content: '';
}
</style>
