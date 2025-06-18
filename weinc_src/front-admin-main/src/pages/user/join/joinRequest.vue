<template>
  <div>
    <!-- Message Body -->
    <div id="successMessageContent">
      <div class="text-center">
        <img alt="Image Description" class="img-fluid mb-3" data-hs-theme-appearance="default" src="@/assets/svg/illustrations/oc-hi-five.svg" style="max-width: 15rem" />
        <div class="mb-4">
          <h2>WELCOM TO CONIA</h2>
          <p>
            회원가입 신청을 감사드립니다!
            <br />
            <small class="fw-semibold text-dark pt-6">관리자의 승인이 완료된 후 사용이 가능합니다.</small>
            <br />
            <small class="fw-semibold text-dark">감사합니다</small>
          </p>
        </div>

        <div class="d-flex justify-content-center">
          <button type="button" @click.prevent.stop="onClickGobackToLogin" class="btn btn-primary"><i class="bi-person-plus-fill me-1"></i> 로그인 이동</button>
        </div>
      </div>
    </div>
    <!-- End Message Body -->
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
const authStore = useAuthStore();
const router = useRouter();
authStore.logout(false);
const onClickGobackToLogin = () => {
  router.push('/login');
};
</script>

<style scoped></style>
