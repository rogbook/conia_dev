<template>
  <div class="container d-flex align-items-center justify-content-center vh-100">
    <!-- Message Body -->
    <div id="successMessageContent">
      <div class="text-center">
        <img alt="Image Description" class="img-fluid mb-3" data-hs-theme-appearance="default" src="@/assets/svg/illustrations/oc-hi-five.svg" style="max-width: 15rem" />
        <div class="mb-4">
          <h2>관리자가 승인여부를 처리 중입니다.</h2>
        </div>

        <div class="d-flex justify-content-center">
          <button type="button" @click.prevent="logout" class="btn btn-primary">확인</button>
        </div>
      </div>
    </div>
    <!-- End Message Body -->
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
// import { showAlert, showConfirm } from '@/utils/common-utils';

const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.logout();
  //   showAlert('로그아웃 되었습니다.', 'success');
};
</script>

<style scoped></style>
