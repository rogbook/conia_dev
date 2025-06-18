<template>
  <main id="content" role="main" class="main">
    <div class="position-fixed top-0 end-0 start-0 bg-img-start login-bg">
      <!-- Shape -->
      <div class="shape shape-bottom zi-1">
        <svg
            preserveAspectRatio="none"
            xmlns="http://www.w3.org/2000/svg"
            x="0px"
            y="0px"
            viewBox="0 0 1921 273"
        >
          <polygon fill="#fff" points="0,273 1921,273 1921,0 "/>
        </svg>
      </div>
      <!-- End Shape -->
    </div>

    <div class="content container-fluid py-5 py-sm-7">
      <slot/>
    </div>
  </main>
</template>

<script lang="ts" setup>
import {onBeforeMount} from "vue";

onBeforeMount(() => {
  document.body.classList.remove(...document.body.classList);
});

</script>

<style scoped>
.login-bg {
  height: 32rem;
  background-image: url('@/assets/svg/components/card-6.svg');
}
</style>
