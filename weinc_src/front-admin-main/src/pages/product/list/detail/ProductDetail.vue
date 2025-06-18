<template>
  <PageNavigator :before_link="['상품조회 및 수정']" :current="'상품 상세'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">상품 상세 정보</div>
      <span v-if="getUserClassStr.includes('CM')"><MobilePushLink :title="`상품 [ ${mProdInfo.name} ]`" :nextValue="`product/${mProdInfo.id}`" /></span>
    </div>
    <div class="card-body">
      <!-- Step Form -->
      <div class="text-danger mb-3"><b>* 단계별 이동시, 수정내용을 저장하지 않으면 수정하였던 내용은 초기화됩니다.</b></div>
      <form
        class="js-step-form"
        data-hs-step-form-options='{
        "progressSelector": "#prodRegStepFormProgress",
        "stepsSelector": "#prodRegStepFormContent",
        "endSelector": "#createProductFinishBtn"
      }'
        v-on:submit.prevent>
        <!-- Step -->
        <ul id="prodRegStepFormProgress" class="js-step-progress step step-md step-icon-xs step-inline mb-4" style="font-size: 0.9rem">
          <li class="step-item">
            <a class="step-content-wrapper" href="javascript:" data-hs-step-form-next-options='{"targetSelector": "#prodBasicInfo"}' @click.prevent="onChangeStep('basic')">
              <span class="step-icon step-icon-soft-dark">1</span>
              <div class="step-content">
                <span class="step-title">기본판매 정보</span>
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" href="javascript:" data-hs-step-form-next-options='{"targetSelector": "#prodNoticeInfo"}' @click.prevent="onChangeStep('notice')">
              <span class="step-icon step-icon-soft-dark">2</span>
              <div class="step-content">
                <span class="step-title">상품정보제공고시</span>
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" href="javascript:" data-hs-step-form-next-options='{"targetSelector": "#prodOptionGroupInfo"}' @click.prevent="onChangeStep('option')">
              <span class="step-icon step-icon-soft-dark">3</span>
              <div class="step-content">
                <span class="step-title" v-if="prodType !== 'G'">가격 및 옵션정보</span>
                <span class="step-title" v-else>상품그룹정보</span>
              </div>
            </a>
          </li>
          <li class="step-item col-auto">
            <a class="step-content-wrapper" href="javascript:" data-hs-step-form-next-options='{"targetSelector": "#prodPhotoInfo"}' @click.prevent="onChangeStep('photo')">
              <span class="step-icon step-icon-soft-dark">4</span>
              <div class="step-content">
                <span class="step-title">사진정보</span>
              </div>
            </a>
          </li>
          <li class="step-item" v-if="prodType !== 'G'">
            <a class="step-content-wrapper" href="javascript:" data-hs-step-form-next-options='{"targetSelector": "#prodDetailInfo"}' @click.prevent="onChangeStep('explain')">
              <span class="step-icon step-icon-soft-dark">5</span>
              <div class="step-content">
                <span class="step-title">상세정보</span>
              </div>
            </a>
          </li>
          <li class="step-item" v-if="prodType !== 'G'">
            <a class="step-content-wrapper" href="javascript:" data-hs-step-form-next-options='{"targetSelector": "#prodCommonInfo"}' @click.prevent="onChangeStep('common')">
              <span class="step-icon step-icon-soft-dark">6</span>
              <div class="step-content">
                <span class="step-title">공통정보</span>
              </div>
            </a>
          </li>
          <li class="step-item" v-if="prodType !== 'G' && !prodType.startsWith('UP')">
            <a class="step-content-wrapper" href="javascript:" data-hs-step-form-next-options='{"targetSelector": "#prodShippingStoreInfo"}' @click.prevent="onChangeStep('shippingStore')">
              <span class="step-icon step-icon-soft-dark">7</span>
              <div class="step-content">
                <span class="step-title" v-if="prodType.startsWith('DP')">배송정보</span>
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" href="javascript:" data-hs-step-form-next-options='{"targetSelector": "#prodBadgeInfo"}' @click.prevent="onChangeStep('badge')">
              <span class="step-icon step-icon-soft-dark" v-if="prodType !== 'G' && prodType.startsWith('DP')">8</span>
              <span class="step-icon step-icon-soft-dark" v-if="prodType !== 'G' && prodType.startsWith('UP')">7</span>
              <!--              <span class="step-icon step-icon-soft-dark" v-else>5</span>-->
              <div class="step-content">
                <span class="step-title">상품배지정보</span>
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" href="javascript:" data-hs-step-form-next-options='{"targetSelector": "#prodEtcInfo"}' @click.prevent="onChangeStep('etc')">
              <span class="step-icon step-icon-soft-dark" v-if="prodType !== 'G' && prodType.startsWith('DP')">9</span>
              <span class="step-icon step-icon-soft-dark" v-if="prodType !== 'G' && prodType.startsWith('UP')">8</span>
              <!--              <span class="step-icon step-icon-soft-dark" v-else>6</span>-->
              <div class="step-content">
                <span class="step-title">기타정보</span>
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" href="javascript:" data-hs-step-form-next-options='{"targetSelector": "#prodExtraInfo"}' @click.prevent="onChangeStep('extra')">
              <span class="step-icon step-icon-soft-dark" v-if="prodType !== 'G' && prodType.startsWith('DP')">10</span>
              <span class="step-icon step-icon-soft-dark" v-if="prodType !== 'G' && prodType.startsWith('UP')">9</span>
              <!--              <span class="step-icon step-icon-soft-dark" v-else>6</span>-->
              <div class="step-content">
                <span class="step-title">추가정보</span>
              </div>
            </a>
          </li>
        </ul>
        <!-- End Step -->

        <!-- Content Step Form -->
        <div id="prodRegStepFormContent">
          <div id="prodBasicInfo" class="active">
            <ProdBasicInfo @setProductId="onSetProductId" @changedProdInfo="changeProdInfo" :editMode="editMode" :prodId="mProductId" :prodInfo="mProdInfo" ref="basicStep" />
          </div>
          <div id="prodNoticeInfo" style="display: none">
            <ProdNoticeInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" ref="noticeStep" />
          </div>
          <div id="prodOptionGroupInfo" style="display: none">
            <ProdOptionInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :prod-type="mProdInfo.type" :status="mProdInfo?.option_use ? mProdInfo.option_use : 'N'" :product-id="mProductId" ref="optionStep" v-if="prodType !== 'G'" />
            <GroupProductMng @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" :paId="mProdInfo.member_id" ref="groupStep" v-else />
          </div>
          <div id="prodPhotoInfo" style="display: none">
            <ProdPhotoInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" ref="photoStep" />
          </div>
          <div id="prodDetailInfo" style="display: none" v-if="prodType !== 'G'">
            <ProdExplainInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" ref="explainStep" :contents="mProdInfo.contents ? mProdInfo.contents : ''" />
          </div>
          <div id="prodCommonInfo" style="display: none" v-if="prodType !== 'G'">
            <ProdCommonInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" :prod-member-id="mProdInfo.member_id" :prod-member="mProdInfo.member" ref="commonStep" :commonId="mProdInfo.common_info_id ? mProdInfo.common_info_id : 0" />
          </div>
          <div id="prodShippingStoreInfo" style="display: none" v-if="prodType !== 'G' && prodType.startsWith('DP')">
            <ProdShippingInfo v-if="prodType.startsWith('DP')" @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" :prod-member-id="mProdInfo.member_id" ref="shippingStep" :shippingId="mProdInfo.shipping_info_id ? mProdInfo.shipping_info_id : 0" />
            <!--            <ProdStoreInfo v-else-if="prodType.startsWith('UP')" ref="storeStep" :product-id="mProductId" :productInfo="mProdInfo" />-->
          </div>
          <div id="prodBadgeInfo" style="display: none">
            <ProdBadgeInfo @saveFinish="saveFinish" :product-id="mProductId" ref="badgeStep" />
          </div>
          <div id="prodEtcInfo" style="display: none">
            <ProdEtcInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :prod-type="prodType" :product-id="mProductId" :productInfo="mProdInfo" ref="etcStep" />
          </div>
          <div id="prodExtraInfo" style="display: none">
            <ProdExtraInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" ref="extraStep" />
          </div>
        </div>
        <!-- End Content Step Form -->
      </form>
      <!-- End Step Form -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import ProdBasicInfo from '@/pages/product/list/detail/step/ProdBasicInfo.vue';
import ProdOptionInfo from '@/pages/product/list/detail/step/ProdOptionInfo.vue';
import { useRoute, useRouter } from 'vue-router';
import type { Prod } from 'ProductListInfoModule';
import apis from '@/apis';
import ProdPhotoInfo from '@/pages/product/list/detail/step/ProdPhotoInfo.vue';
import ProdExplainInfo from '@/pages/product/list/detail/step/ProdExplainInfo.vue';
import ProdCommonInfo from '@/pages/product/list/detail/step/ProdCommonInfo.vue';
import ProdShippingInfo from '@/pages/product/list/detail/step/ProdShippingInfo.vue';
import ProdStoreInfo from '@/pages/product/list/detail/step/ProdStoreInfo.vue';
import ProdEtcInfo from '@/pages/product/list/detail/step/ProdEtcInfo.vue';
import ProdNoticeInfo from '@/pages/product/list/detail/step/ProdNoticeInfo.vue';
import { apiResponseCheck, showAlert, showLogConsole, getUserClassStr } from '@/utils/common-utils';
import ProdBadgeInfo from '@/pages/product/list/detail/step/ProdBadgeInfo.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import GroupProductMng from '@/pages/product/list/detail/step/group/GroupProductMng.vue';
import ProdExtraInfo from '@/pages/product/list/detail/step/ProdExtraInfo.vue';
import MobilePushLink from '@/components/comm/MobilePushLink.vue';

const router = useRouter();
const mProductId = ref(0);
const mProdInfo = ref({} as Prod);
const editMode = ref(false);
const prodType = ref('');

// Step Info
const basicStep = ref();
const noticeStep = ref();
const optionStep = ref();
const groupStep = ref();
const photoStep = ref();
const explainStep = ref();
const commonStep = ref();
const shippingStep = ref();
const storeStep = ref();
const badgeStep = ref();
const etcStep = ref();
const extraStep = ref();

const onSetProductId = (id: number) => {
  mProductId.value = id;
  editMode.value = true;
};

const getProdInfo = () => {
  apis.product.getProduct(mProductId.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mProdInfo.value = res;
      prodType.value = mProdInfo.value.type;
      editMode.value = true;
    });
  });
};

onMounted(() => {
  if (history.state.id === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }

  mProductId.value = history.state.id;
  getProdInfo();

  // INITIALIZATION OF STEP FORM
  //@ts-ignore
  new HSStepForm('.js-step-form', {
    // @ts-ignore
    finish($el) {
      const $successMessageTempalte = $el.querySelector('.js-success-message').cloneNode(true);

      $successMessageTempalte.style.display = 'block';

      $el.style.display = 'none';
      $el.parentElement.appendChild($successMessageTempalte);
    },
  });
});

const onChangeStep = (step: string) => {
  switch (step) {
    case 'basic':
      changeProdInfo();
      basicStep.value.onStepActive();
      break;
    case 'notice':
      noticeStep.value.onStepActive();
      break;
    case 'option':
      if (prodType.value !== 'G') {
        optionStep.value.onStepActive();
      } else {
        groupStep.value.onStepActive();
      }
      break;
    case 'photo':
      photoStep.value.onStepActive();
      break;
    case 'explain':
      explainStep.value.onStepActive();
      break;
    case 'common':
      commonStep.value.onStepActive();
      break;
    case 'shippingStore':
      if (prodType.value.startsWith('DP')) {
        shippingStep.value.onStepActive();
      } else {
        storeStep.value.onStepActive();
      }
      break;
    case 'badge':
      badgeStep.value.onStepActive();
      break;
    case 'etc':
      etcStep.value.onStepActive();
      break;
    case 'extra':
      extraStep.value.onStepActive();
      break;
  }
};

const saveFinish = (type: string = '') => {};

const changeProdInfo = () => {
  getProdInfo();
};
</script>

<style scoped>
a.disabled {
  pointer-events: none;
  cursor: default;
}

.step-title::after {
  display: none !important;
}
</style>
