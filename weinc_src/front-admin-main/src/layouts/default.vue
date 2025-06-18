<template>
  <Header />
  <SidebarLayout />
  <main id="content" role="main" class="main">
    <div class="content container-fluid has-navbar-vertical-aside navbar-vertical-aside-show-xl footer-offset">
      <div class="m-2">
        <slot />
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';
import Header from '@/components/header/Header.vue';
import SidebarLayout from '@/components/sidebar/Sidebar.vue';
import { toggleBodyClass } from '@/utils/bodyManager';

onMounted(() => {
  toggleBodyClass('addClass', 'has-navbar-vertical-aside');
  toggleBodyClass('addClass', 'navbar-vertical-aside-show-xl');
  toggleBodyClass('addClass', 'footer-offset');

  // template initialize
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  // eslint-disable-next-line no-undef
  window.hs_config = {
    layoutBuilder: { extend: { switcherSupport: true }, header: { layoutMode: 'default', containerMode: 'container-fluid' }, sidebarLayout: 'default' },
  };
});
onUnmounted(() => {
  // toggleBodyClass('removeClass', 'has-navbar-vertical-aside');
  // toggleBodyClass('removeClass', 'navbar-vertical-aside-show-xl');
  // toggleBodyClass('removeClass', 'footer-offset');
});
</script>

<style scoped></style>
