<template>
  <header class="navbar navbar-expand-lg navbar-fixed navbar-height navbar-container navbar-bordered header-bg" :class="{ 'bg-warning': bgColor === 'DEV', 'bg-white': bgColor === 'PROD' }">
    <div class="navbar-nav-wrap">
      <!-- Logo -->
      <a class="navbar-brand" href="/dashboard" aria-label="Front">
        <img class="navbar-brand-logo" src="@/assets/images/coniaworld_logo.png" alt="Logo" data-hs-theme-appearance="Compact" />
      </a>
      <!-- End Logo -->

      <div class="navbar-nav-wrap-content-start">
        <!-- Navbar Vertical Toggle -->
        <button type="button" class="js-navbar-vertical-aside-toggle-invoker navbar-aside-toggler">
          <i class="bi-arrow-bar-left navbar-toggler-short-align" data-bs-template='<div class="tooltip d-none d-md-block" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>' data-bs-toggle="tooltip" data-bs-placement="right" title="Collapse"></i>
          <i class="bi-arrow-bar-right navbar-toggler-full-align" data-bs-template='<div class="tooltip d-none d-md-block" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>' data-bs-toggle="tooltip" data-bs-placement="right" title="Expand"></i>
        </button>
      </div>

      <div class="navbar-nav-wrap-content-end">
        <!-- Navbar -->
        <ul class="navbar-nav">
          <li class="nav-item">
            <!-- Account -->
            <div class="d-flex align-items-center">
              <div class="server me-3" v-if="bgColor === 'DEV'">[&#8251; 테스트 서버 입니다]</div>
              <div class="avatar avatar-sm avatar-circle justify-content-center">
                <div class="text-center" style="vertical-align: middle">
                  <i class="bi-person" style="font-size: 1.7rem" />
                </div>
              </div>
              <div class="flex-grow-1 ms-1 me-1">
                <h5 class="mb-0" data-bs-toggle="tooltip" data-bs-placement="bottom" :title="`[${userClass}]`">{{ userName }}</h5>
              </div>
            </div>
            <!-- End Account -->
          </li>
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-outline-info me-1" @click="logout">로그아웃</button>
          </div>
        </ul>
        <!-- End Navbar -->
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import api from '@/apis';
import { useAuthStore } from '@/stores/auth';
import { useUserStore } from '@/stores/user';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';

export default defineComponent({
  setup() {
    const bgColor = import.meta.env.VITE_RUN_MODE;
    const isLogin = ref<boolean>();
    const userName = computed(() => {
      return useUserStore().user.name;
    });
    const userClass = computed(() => {
      return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
    });

    const logout = () => {
      showConfirm('로그아웃 하시겠습니까?', () => {
        api.user.logout().then(res => {
          apiResponseCheck(res, () => {
            useAuthStore().logout();
            isLogin.value = false;
            showAlert('로그아웃 되었습니다.', 'success');
          });
        });
      });
    };

    return { isLogin, logout, userName, userClass, bgColor };
  },

  beforeMount() {
    this.isLogin = useAuthStore().isLoggedIn;
  },

  mounted() {
    showLogConsole(useUserStore().user);
  },
});
</script>

<style scoped>
.header-bg {
  background-color: v-bind(bgColor);
}
</style>
