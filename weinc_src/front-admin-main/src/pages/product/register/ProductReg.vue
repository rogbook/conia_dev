<template>
  <PageNavigator :before_link="[]" :current="'상품등록'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">상품 신규 등록</div>
    </div>
    <div class="card-body">
      <!-- Step Form -->
      <div class="text-danger mb-3" v-if="mProductId"><b>* 단계별 이동시, 수정내용을 저장하지 않으면 수정하였던 내용은 초기화됩니다.</b></div>
      <div class="text-danger mb-3">
        <b>{{ showWarningText }}</b>
      </div>
      <form
        class="js-step-form"
        data-hs-step-form-options='{
        "progressSelector": "#prodRegStepFormProgress",
        "stepsSelector": "#prodRegStepFormContent",
        "endSelector": "#createProductFinishBtn"
      }'
        v-on:submit.prevent>
        <ul id="prodRegStepFormProgress" class="js-step-progress step step-md step-icon-xs step-inline mb-7" style="font-size: 0.9rem">
          <li class="step-item">
            <a class="step-content-wrapper" href="javascript:;" data-hs-step-form-next-options='{"targetSelector": "#prodBasicInfo"}' @click.prevent="onChangeStep('basic')">
              <span class="step-icon step-icon-soft-dark">1</span>
              <div class="step-content">
                <span class="step-title">기본판매 정보</span>
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" id="stepNotice" href="javascript:;" :class="{ disabled: !mProductId }" data-hs-step-form-next-options='{"targetSelector": "#prodNoticeInfo"}' @click.prevent="onChangeStep('notice')">
              <span class="step-icon step-icon-soft-dark">2</span>
              <div class="step-content">
                <span class="step-title">상품정보제공고시</span>
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" id="stepOption" href="javascript:;" :class="{ disabled: !productState.notice }" data-hs-step-form-next-options='{"targetSelector": "#prodOptionGroupInfo"}' @click.prevent="onChangeStep('option')">
              <span class="step-icon step-icon-soft-dark">3</span>
              <div class="step-content">
                <span class="step-title" v-if="prodType !== 'G'">가격 및 옵션정보</span>
                <span class="step-title" v-else>상품그룹정보</span>
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" id="stepPhoto" href="javascript:;" :class="{ disabled: !productState.option }" data-hs-step-form-next-options='{"targetSelector": "#prodPhotoInfo"}' @click.prevent="onChangeStep('photo')">
              <span class="step-icon step-icon-soft-dark">4</span>
              <div class="step-content">
                <span class="step-title">사진정보</span>
              </div>
            </a>
          </li>
          <li class="step-item" v-if="prodType !== 'G'">
            <a class="step-content-wrapper" id="stepExplain" href="javascript:;" :class="{ disabled: !productState.photo }" data-hs-step-form-next-options='{"targetSelector": "#prodDetailInfo"}' @click.prevent="onChangeStep('explain')">
              <span class="step-icon step-icon-soft-dark">5</span>
              <div class="step-content">
                <span class="step-title">상세정보</span>
              </div>
            </a>
          </li>
          <li class="step-item" v-if="prodType !== 'G'">
            <a class="step-content-wrapper" id="stepCommon" href="javascript:;" :class="{ disabled: !productState.explain }" data-hs-step-form-next-options='{"targetSelector": "#prodCommonInfo"}' @click.prevent="onChangeStep('common')">
              <span class="step-icon step-icon-soft-dark">6</span>
              <div class="step-content">
                <span class="step-title">공통정보</span>
              </div>
            </a>
          </li>
          <li class="step-item" v-if="prodType !== 'G' && prodType.startsWith('DP')">
            <a class="step-content-wrapper" id="stepShippingStore" href="javascript:;" :class="{ disabled: !productState.common }" data-hs-step-form-next-options='{"targetSelector": "#prodShippingStoreInfo"}' @click.prevent="onChangeStep('shippingStore')">
              <span class="step-icon step-icon-soft-dark">7</span>
              <div class="step-content">
                <span class="step-title" v-if="prodType.startsWith('DP')">배송정보</span>
                <!--                <span class="step-title" v-else>매장정보</span>-->
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" id="stepBadge" href="javascript:;" :class="{ disabled: !productState.shipping && !productState.store }" data-hs-step-form-next-options='{"targetSelector": "#prodBadgeInfo"}' @click.prevent="onChangeStep('badge')">
              <span class="step-icon step-icon-soft-dark" v-if="prodType !== 'G' && prodType.startsWith('DP')">8</span>
              <span class="step-icon step-icon-soft-dark" v-if="prodType !== 'G' && prodType.startsWith('UP')">7</span>
              <!--              <span class="step-icon step-icon-soft-dark" v-else>5</span>-->
              <div class="step-content">
                <span class="step-title">상품배지정보</span>
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" id="stepEtc" href="javascript:;" :class="{ disabled: !productState.badge }" data-hs-step-form-next-options='{"targetSelector": "#prodEtcInfo"}' @click.prevent="onChangeStep('etc')">
              <span class="step-icon step-icon-soft-dark" v-if="prodType !== 'G' && prodType.startsWith('DP')">9</span>
              <span class="step-icon step-icon-soft-dark" v-if="prodType !== 'G' && prodType.startsWith('UP')">8</span>
              <!--              <span class="step-icon step-icon-soft-dark" v-else>6</span>-->
              <div class="step-content">
                <span class="step-title">기타정보</span>
              </div>
            </a>
          </li>
          <li class="step-item">
            <a class="step-content-wrapper" id="stepExtra" href="javascript:" :class="{ disabled: !productState.etc }" data-hs-step-form-next-options='{"targetSelector": "#prodExtraInfo"}' @click.prevent="onChangeStep('extra')">
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
            <ProdBasicInfo @setProductId="onSetProductId" @changeType="changeType" :editMode="editMode" :prodId="mProductId" :prodInfo="mProdInfo" ref="basicStep" v-if="!mProductId" />
            <ProdBasicInfoMod @setProductId="onSetProductId" @changedProdInfo="changeProdInfo" :editMode="editMode" :prodId="mProductId" :prodInfo="mProdInfo" ref="basicStep" v-else />
          </div>
          <div id="prodNoticeInfo" style="display: none">
            <ProdNoticeInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" ref="noticeStep" />
          </div>
          <div id="prodOptionGroupInfo" style="display: none">
            <ProdOptionInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :prod-type="mProdInfo.type" :status="mProdInfo?.option_use ? mProdInfo.option_use : 'N'" :product-id="mProductId" ref="optionStep" v-if="prodType !== 'G'" />
            <GroupProductMng @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" ref="groupStep" v-else />
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
            <!--            <ProdStoreInfo v-else-if="prodType.startsWith('UP')" ref="storeStep" @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" :productInfo="mProdInfo" />-->
          </div>
          <div id="prodBadgeInfo" style="display: none">
            <ProdBadgeInfo @saveFinish="saveFinish" :product-id="mProductId" ref="badgeStep" />
          </div>
          <div id="prodEtcInfo" style="display: none">
            <ProdEtcInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :prod-type="prodType" :product-id="mProductId" :productInfo="mProdInfo" ref="etcStep" :reg="true" />
          </div>
          <div id="prodExtraInfo" style="display: none">
            <ProdExtraInfo @saveFinish="saveFinish" @changedProdInfo="changeProdInfo" :product-id="mProductId" ref="extraStep" :reg="true" />
          </div>
        </div>
      </form>
      <!-- End Step Form -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import ProdBasicInfo from '@/pages/product/register/step/ProdBasicInfo.vue';
import ProdBasicInfoMod from '@/pages/product/list/detail/step/ProdBasicInfo.vue';
import ProdOptionInfo from '@/pages/product/list/detail/step/ProdOptionInfo.vue';
import { useRouter } from 'vue-router';
import type { Prod } from 'ProductListInfoModule';
import apis from '@/apis';
import ProdPhotoInfo from '@/pages/product/list/detail/step/ProdPhotoInfo.vue';
import ProdExplainInfo from '@/pages/product/list/detail/step/ProdExplainInfo.vue';
import ProdCommonInfo from '@/pages/product/list/detail/step/ProdCommonInfo.vue';
import ProdShippingInfo from '@/pages/product/list/detail/step/ProdShippingInfo.vue';
import ProdStoreInfo from '@/pages/product/list/detail/step/ProdStoreInfo.vue';
import ProdEtcInfo from '@/pages/product/list/detail/step/ProdEtcInfo.vue';
import ProdNoticeInfo from '@/pages/product/list/detail/step/ProdNoticeInfo.vue';
import { apiResponseCheck, showAlert, showLogConsole } from '@/utils/common-utils';
import ProdBadgeInfo from '@/pages/product/list/detail/step/ProdBadgeInfo.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import GroupProductMng from '@/pages/product/list/detail/step/group/GroupProductMng.vue';
import ProdExtraInfo from '@/pages/product/list/detail/step/ProdExtraInfo.vue';

const router = useRouter();
const mProductId = ref(0);
const mProdInfo = ref({} as Prod);
const editMode = ref(false);

const productState = ref({
  productId: 0,
  basic: false,
  notice: false,
  option: false,
  photo: false,
  explain: false,
  common: false,
  shipping: false,
  store: false,
  badge: false,
  etc: false,
  extra: false,
  group: false,
});

const prodType = ref('DP');
const changeType = (value: string) => {
  prodType.value = value;
};

const showWarningText = computed(() => {
  let text = '';
  if (!productState.value.basic) {
    text = '* 기본 판매정보를 작성하여 상품 기초등록을 진행하여야 다음 단계로 이동할 수 있습니다.';
  } else if (!productState.value.notice) {
    text = '* 상품 정보제공고시 정보를 작성 및 저장 하여야 다음 단계로 이동할 수 있습니다.';
  } else if (!productState.value.option || !productState.value.group) {
    text = prodType.value !== 'G' ? '* 상품 옵션정보를 작성 및 저장 하여야 다음 단계로 이동할 수 있습니다.' : '* 그룹상품을 구성 및 저장 하여야 다음 단계로 이동할 수 있습니다.';
  } else if (!productState.value.photo) {
    text = '* 상품 사진정보를 추가 및 저장 하여야 다음 단계로 이동할 수 있습니다.';
  } else if (!productState.value.explain) {
    text = '* 상품 상세정보를 작성 및 저장 하여야 다음 단계로 이동할 수 있습니다.';
  } else if (!productState.value.common) {
    text = '* 상품 공통정보를 선택 및 저장 하여야 다음 단계로 이동할 수 있습니다.';
  } else if (!productState.value.shipping || !productState.value.store) {
    text = prodType.value.startsWith('DP') ? '* 상품 배송정보를 선택 및 저장 하여야 다음 단계로 이동할 수 있습니다.' : '* 상품 매장정보를 선택 및 저장 하여야 다음 단계로 이동할 수 있습니다.';
  } else if (!productState.value.badge) {
    text = '* 상품 배지정보를 선택 및 저장 하여야 다음 단계로 이동할 수 있습니다.';
  } else if (!productState.value.etc) {
    text = '* 상품 기타정보를 작성 및 저장 하여야 상품등록 작업이 완전히 완료됩니다.';
  } else if (!productState.value.extra) {
    text = '* 상품 추가 정보는 필수 등록사항이 아닙니다. 상품등록이 완료되었습니다.';
  } else {
    text = '';
  }
  return text;
});

// Step Info
const basicStep = ref();
const noticeStep = ref();
const groupStep = ref();
const optionStep = ref();
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
  productState.value.productId = id;
  productState.value.basic = true;
  editMode.value = true;
  changeProdInfo();
  //@ts-ignore
  window.$('#stepNotice').get(0).click();
};

const saveFinish = (step: string = '') => {
  switch (step) {
    case 'notice':
      productState.value.notice = true;
      //@ts-ignore
      window.$('#stepOption').get(0).click();
      break;
    case 'option':
    case 'group':
      productState.value.option = true;
      productState.value.group = true;
      //@ts-ignore
      window.$('#stepPhoto').get(0).click();
      break;
    case 'photo':
      productState.value.photo = true;
      if (prodType.value !== 'G') {
        //@ts-ignore
        window.$('#stepExplain').get(0).click();
      } else {
        productState.value.explain = true;
        productState.value.common = true;
        productState.value.shipping = true;
        productState.value.store = true;
        //@ts-ignore
        window.$('#stepBadge').get(0).click();
      }
      break;
    case 'explain':
      productState.value.explain = true;
      //@ts-ignore
      window.$('#stepCommon').get(0).click();
      break;
    case 'common':
      productState.value.common = true;
      if (prodType.value.startsWith('DP')) {
        //@ts-ignore
        window.$('#stepShippingStore').get(0).click();
      } else {
        productState.value.shipping = true;
        productState.value.store = true;
        //@ts-ignore
        window.$('#stepBadge').get(0).click();
      }
      break;
    case 'shipping':
    case 'store':
      productState.value.shipping = true;
      productState.value.store = true;
      //@ts-ignore
      window.$('#stepBadge').get(0).click();
      break;
    case 'badge':
      productState.value.badge = true;
      //@ts-ignore
      window.$('#stepEtc').get(0).click();
      break;
    case 'etc':
      productState.value.etc = true;
      //@ts-ignore
      window.$('#stepExtra').get(0).click();
      break;
    case 'extra':
      productState.value.extra = true;
      finishCreateProduct();
      break;
    default:
      break;
  }
};

const finishCreateProduct = () => {
  showAlert('상품 등록이 완료되었습니다.', 'success', () => {
    router.push('/product/list');
  });
};

const getProdInfo = () => {
  apis.product.getProduct(mProductId.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mProdInfo.value = res;
      editMode.value = true;
    });
  });
};

onMounted(() => {
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
  }
};

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
