<template>
  <form class="js-validate needs-validation col-lg-8" novalidate>
    <div id="addUserStepFormContent">
      <div class="text-end mb-2">
        <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="showModal('showBasicInfo')">가입기본정보보기</button>
      </div>
      <div id="addUserStepBillingAddress" class="card">
        <!-- Body -->
        <div class="card-body">
          <div class="mb-4 mb-xl-6">
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" v-model="joinType" name="P" id="P" value="P" />
              <label class="form-check-label" for="P">개인</label>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" v-model="joinType" name="B" id="B" value="B" />
              <label class="form-check-label" for="B">법인사업자</label>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" v-model="joinType" name="PB" id="PB" value="PB" />
              <label class="form-check-label" for="PB">개인사업자(일반)</label>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" v-model="joinType" name="PBS" id="PBS" value="PBS" />
              <label class="form-check-label" for="PBS">개인사업자(간이과세)</label>
            </div>
          </div>
          <div class="col-12 border py-md-6 px-md-4 mb-md-6 py-3 px-3 mb-3">
            <template v-if="joinType === 'B'">
              CONIA ADMIN
              <p class="fw-bold fs-3">법인 사업자 회원</p>
              법인사업자가 있는 법인회원
            </template>
            <template v-else-if="joinType === 'PB'">
              CONIA ADMIN
              <p class="fw-bold fs-3">개인 사업자(일반) 회원</p>
              일반 사업자가 있는 개인회원
            </template>
            <template v-else-if="joinType === 'PBS'">
              CONIA ADMIN
              <p class="fw-bold fs-3">개인 사업자(간이과세) 회원</p>
              간이과세 사업자가 있는 개인회원
            </template>
            <template v-else>
              CONIA ADMIN
              <p class="fw-bold fs-3">개인회원</p>
              사업자가 없는 개인회원
            </template>
          </div>
          <div class="px-sm-4 px-3">
            <JoinPersonal @nextStep="nextStep" :bankList="bankList" :joinType="joinType" :user="user" v-if="joinType === 'P'" />
            <JoinCompany @nextStep="nextStep" :bankList="bankList" :joinType="joinType" :user="user" v-else />
          </div>
        </div>

        <!-- End Body -->

        <!-- Footer -->
        <!--        <div class="card-footer d-flex align-items-center">-->
        <!--          <div class="ms-auto">-->
        <!--            <button ref="submitRef" class="btn btn-primary" type="submit">Next <i class="bi-chevron-right"></i></button>-->
        <!--          </div>-->
        <!--        </div>-->
        <!-- End Footer -->
      </div>
    </div>
  </form>

  <Modal :id="'showBasicInfo'" :title="'가입기본정보보기'">
    <template #body>
      <div class="card">
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-3 col-form-label">이메일(아이디)</label>
            <div class="col">
              <div class="input-group">
                <span class="form-control">{{ userInfo.email }}</span>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-3 col-form-label">이름</label>
            <div class="col">
              <div class="input-group">
                <span class="form-control">{{ userInfo.name }}</span>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-3 col-form-label">휴대폰번호</label>
            <div class="col">
              <div class="input-group">
                <span class="form-control">{{ userInfo.mobile }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, readonly, ref } from 'vue';
import { loadScript, unloadScript } from '@/utils/standaloneImport';
import JoinPersonal from '@/components/user/join/JoinPersonal.vue';
import JoinCompany from '@/components/user/join/JoinCompany.vue';
import { useCommonStore } from '@/stores/common';
import type { IBankList, TJoinType } from '@/components/user/type';
import { useUserStore } from '@/stores/user';
import Modal from '@/components/comm/modal.vue';
import type { User } from 'UserInfoModule';
import apis from '@/apis';
import { showLogConsole, showModal, hideModal } from '@/utils/common-utils';

const user = readonly(useUserStore().user);
const bankList = readonly<IBankList[]>(useCommonStore().bankList);

const userInfo = ref({} as User);
const getUserInfo = () => {
  apis.user.me().then(res => {
    showLogConsole(res);
    userInfo.value = res;
  });
};

/**
 * 회원가입 종류
 */
const joinType = ref<TJoinType>('P');

const emits = defineEmits(['nextStep']);

/**
 * Daum Map api
 */
const installList = readonly(['//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js']);
onMounted(() => {
  getUserInfo();
  installList.map(path => {
    loadScript(path);
  });
});

onUnmounted(() => {
  installList.map(path => {
    unloadScript(path);
  });
});

const nextStep = () => {
  emits('nextStep');
};
</script>

<style scoped></style>
