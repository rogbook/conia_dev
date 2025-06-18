<template>
  <!-- ========== MAIN CONTENT ========== -->
  <main id="content" class="main" role="main">
    <!-- Content -->
    <div class="content container-fluid">
      <div class="row justify-content-lg-center">
        <!-- Step -->
        <ul id="addUserStepFormProgress" class="py-md-5 col-lg-8 justify-content-lg-center row js-step-progress step step-sm step-icon-sm step step-inline step-item-between mb-3 mb-md-5">
          <li class="step-item" :class="{ active: page.step === STEP.BASE_INFO }">
            <a class="step-content-wrapper" data-hs-step-form-next-options='{"targetSelector": "#addUserStepProfile"}' href="javascript:">
              <span class="step-icon step-icon-soft-dark">1</span>
              <div class="step-content"><span class="step-title">기본정보</span></div>
            </a>
          </li>

          <li class="step-item" :class="{ active: page.step === STEP.ADMIN_INFO }">
            <a
              class="step-content-wrapper"
              data-hs-step-form-next-options='{
                    "targetSelector": "#addUserStepBillingAddress"}'
              href="javascript:">
              <span class="step-icon step-icon-soft-dark">2</span>
              <div class="step-content">
                <span class="step-title">추가정보</span>
              </div>
            </a>
          </li>

          <li class="step-item" :class="{ active: page.step === STEP.COMPLETE }">
            <a class="step-content-wrapper" data-hs-step-form-next-options='{"targetSelector": "#addUserStepConfirmation"}' href="javascript:">
              <span class="step-icon step-icon-soft-dark">3</span>
              <div class="step-content">
                <span class="step-title">승인요청</span>
              </div>
            </a>
          </li>
        </ul>
        <!-- End Step -->
        <!-- Step Form -->
        <JoinBase @nextStep="nextStep" v-if="page.step === STEP.BASE_INFO" />
        <JoinAdditional @nextStep="nextStep" v-else-if="page.step === STEP.ADMIN_INFO" />
        <JoinRequest @nextStep="nextStep" v-else-if="page.step === STEP.COMPLETE" />
        <!-- End Step Form -->
      </div>
    </div>
    <!-- End Content -->

    <!-- Footer -->
    <div class="footer">
      <div class="row justify-content-between align-items-center">
        <div class="col">
          <p class="fs-6 mb-0">
            <span class="d-none d-sm-inline-block">Copyright © ConiaLab Corp. All rights reserved.</span>
          </p>
        </div>
      </div>
      <!-- End Row -->
    </div>
    <!-- End Footer -->
  </main>
  <!-- ========== END MAIN CONTENT ========== -->
</template>

<script setup lang="ts">
import { onMounted, reactive, readonly } from 'vue';
import { STEP } from '@/models/users/join';
import { useRoute } from 'vue-router';
import JoinBase from '@/pages/user/join/joinBase.vue';
import JoinAdditional from '@/pages/user/join/joinAdditional.vue';
import JoinRequest from '@/pages/user/join/joinRequest.vue';
const page = reactive({ step: (useRoute().meta.step as STEP) || STEP.BASE_INFO });

const nextStep = () => {
  page.step = page.step + 1;
};
onMounted(() => {
  // @ts-ignore
  new HSTogglePassword('.js-toggle-password');

  // INITIALIZATION OF FORM SEARCH
  // =======================================================
  // @ts-ignore
  new HSFormSearch('.js-form-search');

  // INITIALIZATION OF BOOTSTRAP DROPDOWN
  // =======================================================
  // @ts-ignore
  HSBsDropdown.init();

  // INITIALIZATION OF FILE ATTACH
  // =======================================================
  // @ts-ignore
  new HSFileAttach('.js-file-attach');

  // INITIALIZATION OF STEP FORM
  // =======================================================
  // @ts-ignore
  new HSStepForm('.js-step-form', {
    finish: () => {
      // @ts-ignore
      document.getElementById('addUserStepFormProgress').style.display = 'none';
      // @ts-ignore
      document.getElementById('addUserStepProfile').style.display = 'none';
      // @ts-ignore
      document.getElementById('addUserStepBillingAddress').style.display = 'none';
      // @ts-ignore
      document.getElementById('addUserStepConfirmation').style.display = 'none';
      // @ts-ignore
      document.getElementById('successMessageContent').style.display = 'block';
      scrollToTop('#header');
      const formContainer = document.getElementById('formContainer');
    },
    onNextStep: function () {
      scrollToTop();
    },
    onPrevStep: function () {
      scrollToTop();
    },
  });

  function scrollToTop(el = '.js-step-form') {
    // @ts-ignore
    el = document.querySelector(el);
    window.scrollTo({
      // @ts-ignore
      top: el.getBoundingClientRect().top + window.scrollY - 30,
      left: 0,
      behavior: 'smooth',
    });
  }

  // INITIALIZATION OF ADD FIELD
  // =======================================================
  // @ts-ignore
  new HSAddField('.js-add-field', {
    // @ts-ignore
    addedField: field => {
      // @ts-ignore
      HSCore.components.HSTomSelect.init(field.querySelector('.js-select-dynamic'));
      // @ts-ignore
      HSCore.components.HSMask.init(field.querySelector('.js-input-mask'));
    },
  });

  // INITIALIZATION OF SELECT
  // =======================================================
  // @ts-ignore
  HSCore.components.HSTomSelect.init('.js-select', {
    render: {
      // @ts-ignore
      option: function (data, escape) {
        return data.optionTemplate || `<div>${data.text}</div>>`;
      },
      // @ts-ignore
      item: function (data, escape) {
        return data.optionTemplate || `<div>${data.text}</div>>`;
      },
    },
  });

  // INITIALIZATION OF INPUT MASK
  // =======================================================
  // @ts-ignore
  HSCore.components.HSMask.init('.js-input-mask');
});
</script>

<style scoped>
* {
  transition: unset !important;
}

body {
  opacity: 0;
}
</style>
