<template>
  <component :is="layout">
    <slot />
  </component>
</template>

<script lang="ts">
import { computed, markRaw, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import Default from '@/layouts/default.vue';
import NoneLayout from '@/layouts/noneLayout.vue';
import LoginLayout from '@/layouts/loginLayout.vue';

export default {
  name: 'rootLayout',
  components: {
    Default,
    NoneLayout,
    LoginLayout,
  },
  setup() {
    const route = useRoute();
    const layout = computed(() => route.meta.layout || Default);
    return {
      layout,
    };
  },
};
</script>

<style scoped></style>
