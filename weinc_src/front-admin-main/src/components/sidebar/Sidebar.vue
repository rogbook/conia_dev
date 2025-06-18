<template>
  <aside class="js-navbar-vertical-aside navbar navbar-vertical-aside navbar-vertical navbar-vertical-fixed navbar-expand-xl navbar-bordered bg-white">
    <div class="navbar-vertical-container">
      <div class="navbar-vertical-footer-offset">
        <button type="button" class="js-navbar-vertical-aside-toggle-invoker navbar-aside-toggler">
          <i class="bi-arrow-bar-left navbar-toggler-short-align" data-bs-template='<div class="tooltip d-none d-md-block" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>' data-bs-toggle="tooltip" data-bs-placement="right" title="Collapse"></i>
          <i class="bi-arrow-bar-right navbar-toggler-full-align" data-bs-template='<div class="tooltip d-none d-md-block" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>' data-bs-toggle="tooltip" data-bs-placement="right" title="Expand"></i>
        </button>

        <SidebarLogo /> <SidebarMenu />
      </div>
    </div>
  </aside>
</template>

<script lang="ts">
import SidebarMenu from '@/components/sidebar/menu/SidebarMenu.vue';
import SidebarLogo from '@/components/sidebar/SidebarLogo.vue';
import { defineComponent } from 'vue';

export default defineComponent({
  components: { SidebarLogo, SidebarMenu },
});
</script>

<style scoped></style>
