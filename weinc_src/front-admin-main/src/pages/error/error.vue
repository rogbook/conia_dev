<template>
  <!-- ========== MAIN CONTENT ========== -->
  <main id="content" class="main" role="main">
    <!-- Content -->
    <div class="container">
      <RouterLink class="position-absolute top-0 start-0 end-0 py-4" to="/">
        <img alt="Image Description" class="avatar avatar-xxl avatar-4x3 avatar-centered" data-hs-theme-appearance="default" src="@/assets/images/coniaworld_logo.png" />
      </RouterLink>
      <div class="footer-height-offset d-flex justify-content-center align-items-center flex-column">
        <div class="row justify-content-center align-items-sm-center w-100">
          <div class="col-9 col-sm-6 col-lg-4">
            <div class="text-center text-sm-end me-sm-4 mb-5 mb-sm-0">
              <img alt="Image Description" class="img-fluid" data-hs-theme-appearance="default" src="@/assets/svg/illustrations/oc-thinking.svg" />
            </div>
          </div>
          <!-- End Col -->

          <div class="col-sm-6 col-lg-4 text-center text-sm-start">
            <h1 class="display-1 mb-0">{{ error.statusCode }}</h1>
            <p class="lead">{{ error.message }}</p>
            <button type="button" v-if="error.statusCode === '401'" class="btn btn-primary" @click="handleClearError(error.statusCode)">로그인으로 이동</button>
            <button type="button" v-else class="btn btn-primary" @click="handleClearError(error.statusCode)">홈으로 이동</button>
          </div>
          <!-- End Col -->
        </div>
        <!-- End Row -->
      </div>
    </div>
    <!-- End Content -->
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useErrorStore } from '@/stores/error';
import { storeToRefs } from 'pinia';

const errorStore = useErrorStore();
const { error } = storeToRefs(errorStore);

const router = useRouter();

const handleClearError = (status: string) => {
  errorStore.clearError();
  if (status === '401') {
    router.push('/login');
  } else {
    router.push('/dashboard');
  }
};
</script>

<style lang="scss"></style>
