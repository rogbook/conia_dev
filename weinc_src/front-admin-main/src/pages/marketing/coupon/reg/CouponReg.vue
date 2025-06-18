<template>
  <PageNavigator :before_link="['쿠폰관리']" :current="'쿠폰 등록'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center">
        <div class="col-auto">
          <div class="form-control-borderless h2">쿠폰 생성</div>
        </div>
      </div>
    </div>
    <!-- 기본설정 영역 - [CM:읽기/수정, MC:읽기] -->
    <div class="card-body">
      <div class="row col mb-4 align-items-center">
        <label class="col-md-1 col-form-label">쿠폰 이름 <span class="text-danger">*</span></label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="쿠폰 이름을 입력해주세요." v-model.trim="coupon.name" maxlength="20" />
          </div>
        </div>
      </div>

      <div class="row mb-4 align-items-center">
        <label class="col-md-1 col-form-label">할인방식</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input id="discountMethod_per" type="radio" class="form-check-input" name="discountMethod" value="per" v-model="discountMethod" />
              <label class="form-check-label" for="discountMethod_per">퍼센트</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="discountMethod_amount" type="radio" class="form-check-input" name="discountMethod" value="amount" v-model="discountMethod" />
              <label class="form-check-label" for="discountMethod_amount">고정금액</label>
            </div>
          </div>
        </div>
      </div>

      <div class="row col mb-4 align-items-center" v-if="discountMethod === 'per'">
        <label class="col-md-1 col-form-label">할인율 <span class="text-danger">*</span></label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="number" class="form-control" placeholder="할인율을 입력해주세요." v-model.lazy="coupon.percent" oninput="this.value.length > 2 ? this.value = this.value.slice(0,2) : this.value = this.value" />
            <div class="input-group-append input-group-text">
              <i class="bi-percent"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="row col mb-4 align-items-center" v-else>
        <label class="col-md-1 col-form-label">할인금액 <span class="text-danger">*</span></label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="number" class="form-control" placeholder="할인금액을 입력해주세요." v-model.lazy="coupon.amount" oninput="this.value.length > 6 ? this.value = this.value.slice(0,6) : this.value = this.value" />
            <div class="input-group-append input-group-text">원</div>
          </div>
        </div>
      </div>

      <div class="row mb-4 align-items-center">
        <label class="col-md-1 col-form-label">사용기한 지정방식</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input id="useMethod_date" type="radio" class="form-check-input" name="useMethod" value="date" v-model="useMethod" />
              <label class="form-check-label" for="useMethod_date">기간</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="useMethod_day" type="radio" class="form-check-input" name="useMethod" value="day" v-model="useMethod" />
              <label class="form-check-label" for="useMethod_day">일수</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="useMethod_time" type="radio" class="form-check-input" name="useMethod" value="time" v-model="useMethod" />
              <label class="form-check-label" for="useMethod_time">시간</label>
            </div>
          </div>
        </div>
      </div>

      <div class="row col mb-4 align-items-center" v-if="useMethod === 'day'">
        <label class="col-md-1 col-form-label">사용 일수 설정</label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="number" class="form-control" placeholder="사용 일수를 입력해주세요." v-model.lazy="coupon.expire_days" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" />
            <div class="input-group-append input-group-text">일</div>
          </div>
        </div>
      </div>

      <!-- 사용기간 Datepicker START -->
      <div class="row mb-4 align-items-center" v-if="useMethod === 'date'">
        <label for="idLabel" class="col-md-1 col-form-label">사용 기간 설정</label>
        <div class="col">
          <div class="row">
            <div class="col-md-3">
              <!-- Form Group -->
              <div class="form-group">
                <div id="startDatepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#startDatepicker","dateFormat": "Y-m-d H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." v-model="saleDate.sDate" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">~</span>
            <div class="col-md-3">
              <!-- Form Group -->
              <div class="form-group">
                <div id="endDatepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#endDatepicker","dateFormat": "Y-m-d H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." v-model="saleDate.eDate" />
                </div>
              </div>
            </div>
            <div class="d-mb-none mt-1"></div>
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('three')">3일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">7일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('month')">30일</button>
            </div>
          </div>
        </div>
      </div>
      <!-- 사용기간 Datepicker END -->

      <div class="row mb-2 align-items-center" v-show="useMethod === 'time'">
        <label for="idLabel" class="col-md-1 col-form-label">사용 가능 시간대<br /><span style="font-size: 0.7rem" class="text-danger">* 발급 당일 기준</span></label>
        <div class="col">
          <div class="row">
            <div class="col-lg-3">
              <!-- Form Group -->
              <div class="form-group">
                <div id="startTimepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#startTimepicker","dateFormat": "H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startTimepickerInput" placeholder="시간을 선택해주세요." v-model="saleDate.sTime" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">~</span>
            <div class="col-lg-3">
              <!-- Form Group -->
              <div class="form-group">
                <div id="endTimepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#endTimepicker","dateFormat": "H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endTimepickerInput" placeholder="시간을 선택해주세요." v-model="saleDate.eTime" />
                </div>
              </div>
            </div>
            <div class="d-lg-none mt-2"></div>
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1" @click.prevent="setSearchPeriod('all', true)">초기화</button>
            </div>
          </div>
        </div>
      </div>

      <div class="row col mb-4 align-items-center">
        <label class="col-md-1 col-form-label">발급 최대 매수</label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="number" class="form-control" placeholder="발급최대매수를 입력해주세요." v-model.lazy="coupon.publish_limit" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" />
            <div class="input-group-append input-group-text">개</div>
          </div>
        </div>
        <div class="col-auto ms-2">
          <label class="col-form-label"><span class="text-danger">* </span>0을 입력하면 발급최대매수 제한이 없습니다.</label>
        </div>
      </div>

      <div class="row col mb-4 align-items-center">
        <label class="col-md-1 col-form-label">쿠폰적용 상품선택</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input id="coupon_target_all" type="radio" class="form-check-input" name="coupon_target" value="all" v-model="coupon.target" />
              <label class="form-check-label" for="coupon_target_all">전체상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="coupon_target_one" type="radio" class="form-check-input" name="coupon_target" value="one" v-model="coupon.target" />
              <label class="form-check-label" for="coupon_target_one">특정상품</label>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-4 align-items-center" v-if="coupon.target !== 'all'">
        <label class="col-12 col-md-1 col-form-label">특정 상품 대상</label>
        <div class="col-12 col-md-11">
          <div class="input-group">
            <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="showModal('selProdModal')">상품 또는 업체선택</button>
          </div>
        </div>

        <div class="row mt-2" v-if="couponTargets.length">
          <div class="col-md-1"></div>
          <div class="col-md-11" style="width: 60%">
            <div class="text-end mb-1" v-if="couponTargets.length > 0">선택된 항목 수 : {{ couponTargets.length }}</div>
            <div class="table-responsive" style="max-height: 500px; overflow-y: auto">
              <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
                <thead class="thead-light">
                  <tr class="text-center">
                    <th>대상</th>
                    <th>상품코드/업체이메일</th>
                    <th>상품명/업체명</th>
                    <th>삭제</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="text-center" v-for="(item, i) in couponTargets" :key="i">
                    <td>
                      <span v-if="item.product_id">[상품]</span>
                      <span v-else-if="item.member_id">[업체]</span>
                    </td>
                    <td>{{ item.code ? item.code : '' }}</td>
                    <td>{{ item.name }}</td>
                    <td>
                      <button type="button" class="btn btn-sm border-0 p-0" @click.prevent="removeTargetList(i)"><i class="bi-x-circle text-danger"></i></button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="row col mb-4 align-items-center">
        <label class="col-md-1 col-form-label">쿠폰 이미지</label>
        <div class="col-md-4">
          <div class="input-group" v-if="!coupon.image">
            <UploadImage
              class="form-control"
              @change="
                () => {
                  uploadImg.check = uploadImg.value.length > 0;
                }
              "
              @upload="onRegistComRegPhoto"
              :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
              :placeholder="'이미지를 선택해 주세요.'"
              disabled />
          </div>
          <div v-else>
            <img class="img-fluid img-thumbnail d-block" :src="coupon.image" alt="쿠폰 이미지" />
            <div class="mt-3">
              <button type="button" class="btn btn-outline-info me-2 btn-sm" @click="coupon.image = ''">수정</button>
            </div>
          </div>
        </div>
      </div>
      <div class="row col align-items-center">
        <label class="col-md-1 col-form-label">쿠폰 상세 설명 <span class="text-danger">*</span></label>
        <div class="col-md-4">
          <div class="input-group">
            <textarea type="text" class="form-control" placeholder="쿠폰 상세 설명을 입력해주세요." v-model.trim="coupon.description" maxlength="255" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="row align-items-center justify-content-end">
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="regCoupon">생성</button>
        </div>
      </div>
    </div>
  </div>

  <!-- 상품 / 업체 선택 Modal -->
  <Modal :id="'selProdModal'" :title="'상품 또는 업체 검색'" :xlarge="true">
    <template #body>
      <SelProdModal ref="SelProdModalChildRef" @selectCheckedProd="selectCheckedProd" @selectCheckedPa="selectCheckedPa" @openCateMoal="openCateMoal" />
    </template>
  </Modal>

  <!-- PA 선택 Modal -->
  <Modal :id="'selPaModal'" :title="'공급자(PA) 회원 선택'" :second="true" :xlarge="true">
    <template #body>
      <SelPaModal @selectPa="selectPa" />
    </template>
  </Modal>

  <!-- 카테고리 선택-->
  <Modal :id="'SelCategoryModal'" :title="'카테고리 선택'" :second="true">
    <template #body>
      <SelectCategoryModal @closeModal="closeCategoryModal" ref="CategoryModal" />
    </template>
  </Modal>

  <!-- 브랜드 선택-->
  <Modal :id="'SelBrandModal'" :title="'브랜드 선택'" :second="true">
    <template #body>
      <SelectBrandModal @closeModal="closeBrandModal" />
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { onMounted, reactive, computed, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import apis from '@/apis';
import { apiResponseCheck, showAlert, showConfirm, showModal, hideModal } from '@/utils/common-utils';
import UploadImage from '@/components/comm/uploadImage.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import Modal from '@/components/comm/modal.vue';
import SelProdModal from '@/pages/marketing/coupon/modal/SelProd.vue';
import SelPaModal from '@/pages/marketing/coupon/modal/SelPa.vue';
import SelectCategoryModal from '@/components/modals/product/SelectCategoryModal.vue';
import SelectBrandModal from '@/components/modals/product/SelectBrandModal.vue';
import type { Coupon, RegCouponTarget } from 'CouponInfoModule';

const router = useRouter();
const coupon = ref({} as Coupon);
const newCoupon = ref({} as Coupon);

const couponTargets = ref([] as RegCouponTarget[]);

const SelProdModalChildRef = ref();
const CategoryModal = ref();
const useMethod = ref('date');
const discountMethod = ref('per');

watch(
  () => useMethod.value,
  () => {
    coupon.value.expire_days = 1;
    saleDate.sDate = '';
    saleDate.eDate = '';
    saleDate.sTime = '';
    saleDate.eTime = '';
  },
);

const openCateMoal = () => {
  showModal('SelCategoryModal');
  CategoryModal.value.openModal();
};

const selectPa = (id: number, name: string) => {
  hideModal('selPaModal');
  SelProdModalChildRef.value.setPaInfo(id, name);
};
const closeCategoryModal = (cateId: number, cateLabel: string) => {
  hideModal('SelCategoryModal');
  SelProdModalChildRef.value.setCate(cateId, cateLabel);
};
const closeBrandModal = (brandId: number, brandName: string) => {
  hideModal('SelBrandModal');
  SelProdModalChildRef.value.setBrand(brandId, brandName);
};

const sfp = ref();
const efp = ref();
const stfp = ref();
const etfp = ref();
const saleDate = reactive({
  sDate: '',
  eDate: '',
  sTime: '',
  eTime: '',
});

const selectCheckedProd = (prod: any) => {
  for (const value of prod) {
    if (couponTargets.value.some(item => item.product_id === value.id)) {
      // DO Nothing
    } else {
      //code : 상품코드 , name : 상품명
      couponTargets.value.push({ product_id: value.id, member_id: 0, code: value.code, name: value.name });
    }
  }
  hideModal('selProdModal');
};

const selectCheckedPa = (pa: any) => {
  for (const value of pa) {
    if (couponTargets.value.some(item => item.member_id === value.id)) {
      // DO Nothing
    } else {
      //code : 업체이메일 , name : 업체명
      couponTargets.value.push({ product_id: 0, member_id: value.id, code: value.email, name: value.company.name });
    }
  }
  hideModal('selProdModal');
};

const removeTargetList = (idx: number) => {
  couponTargets.value.splice(idx, 1);
};

const regCoupon = () => {
  if (!checkValidation()) return;
  setReqObj();
  showConfirm('쿠폰을 생성하시겠습니까?', () => {
    apis.coupon.reg_coupon(newCoupon.value).then(res => {
      apiResponseCheck(res, () => {
        if (res.id) {
          showAlert('쿠폰이 생성되었습니다.', 'success', () => {
            router.push('/marketing/coupon');
          });
        }
      });
    });
  });
};

const setReqObj = () => {
  newCoupon.value.name = coupon.value.name;
  if (discountMethod.value === 'per') {
    newCoupon.value.percent = coupon.value.percent;
  } else {
    newCoupon.value.amount = coupon.value.amount;
  }
  newCoupon.value.description = coupon.value.description;
  if (coupon.value.image) {
    newCoupon.value.image = coupon.value.image;
  }

  if (coupon.value.target !== 'all') {
    let hasMemberId = false;
    let hasProductId = false;

    for (let value of couponTargets.value) {
      if (value.product_id) {
        hasProductId = true;
      } else if (value.member_id) {
        hasMemberId = true;
      }
    }

    let target = '';
    if (hasMemberId && hasProductId) {
      target = 'PM';
    } else if (hasMemberId) {
      target = 'M';
    } else if (hasProductId) {
      target = 'P';
    }

    newCoupon.value.target = target;
    newCoupon.value.type = 'product';
    //@ts-ignore
    newCoupon.value.coupon_target = couponTargets.value;
  } else {
    newCoupon.value.target = 'all';
  }
  if (useMethod.value === 'date') {
    newCoupon.value.begin_date = saleDate.sDate;
    newCoupon.value.end_date = saleDate.eDate;
  }
  if (useMethod.value === 'day') {
    newCoupon.value.expire_days = coupon.value.expire_days;
  }
  if (useMethod.value === 'time') {
    if (saleDate.sTime && saleDate.eTime) {
      newCoupon.value.begin_time = saleDate.sTime;
      newCoupon.value.end_time = saleDate.eTime;
    }
  }

  if (coupon.value.publish_limit) {
    newCoupon.value.publish_limit = coupon.value.publish_limit;
  } else {
    newCoupon.value.publish_limit = 0;
  }

  newCoupon.value.type = 'product';
  // newCoupon.value.issuer = member_id.value;
  newCoupon.value.issuer = 1;
};

const checkValidation = () => {
  if (!coupon.value.name) {
    showAlert('쿠폰이름을 입력해 주세요.', 'warning');
    return;
  }
  if (discountMethod.value === 'per' && !coupon.value.percent) {
    showAlert('할인율을 입력해 주세요.', 'warning');
    return;
  }
  if (discountMethod.value === 'amount' && !coupon.value.amount) {
    showAlert('할인금액을 입력해 주세요.', 'warning');
    return;
  }
  if (useMethod.value === 'date' && (!saleDate.sDate || !saleDate.eDate)) {
    showAlert('사용 기간을 설정해주세요.', 'warning');
    return;
  }

  if (useMethod.value === 'time') {
    if (!saleDate.sTime || !saleDate.eTime) {
      showAlert('사용 가능 시간대를 입력해주세요.', 'warning');
      return;
    }
    if (saleDate.sTime > saleDate.eTime) {
      showAlert('사용 가능 시간대의 시작 시간이 <br/> 종료시간보다 이후 시간일 수 없습니다.', 'warning');
      return;
    }
    if (saleDate.sTime === saleDate.eTime) {
      showAlert('사용 가능 시간대의 시작시간과 <br/> 종료시간의 값을 다르게 입력해주세요.', 'warning');
      return;
    }
  }

  if (useMethod.value === 'day' && !coupon.value.expire_days) {
    showAlert('사용 일수를 설정해주세요.', 'warning');
    return;
  }
  if (coupon.value.publish_limit !== 0 && !coupon.value.publish_limit) {
    showAlert('발급최대매수를 입력해주세요.', 'warning');
    return;
  }
  if (coupon.value.target !== 'all' && !couponTargets.value.length) {
    showAlert('상품 또는 업체를 선택해 주세요.', 'warning');
    return;
  }
  if (!coupon.value.description) {
    showAlert('쿠폰 상세 설명을 입력해 주세요.', 'warning');
    return;
  }
  return true;
};

// 이미지
const uploadImg = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});

const onRegistComRegPhoto = (files: File) => {
  apis.common.upload_photo(files, 'coupon/').then(res => {
    apiResponseCheck(res, () => {
      coupon.value.image = res.uri;
      uploadImg.value = files.name;
      uploadImg.fileData = files;
    });
  });
};

const setSearchPeriod = (period: string, time: boolean = false) => {
  const today = new Date();
  switch (period) {
    case 'today':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(today.setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'three':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 3).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'week':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 7).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'month':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 30).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    default:
      if (time) {
        saleDate.sTime = '';
        saleDate.eTime = '';
      } else {
        saleDate.sDate = '';
        saleDate.eDate = '';
      }
      break;
  }
};

const sDateChange = () => {
  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      sfp.value.setDate(new Date(), true, 'Y-m-d H:i');
    }
  }
};
const eDateChange = () => {
  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      efp.value.setDate(new Date(), true, 'Y-m-d H:i');
    }
  }
};

const sTimeChange = () => {
  // @ts-ignore
  const sTime = window.$('#startTimepickerInput').val() as string;
  // @ts-ignore
  const eTime = window.$('#endTimepickerInput').val() as string;

  if (sTime === eTime || !sTime || !eTime) {
    return;
  } else {
    if (sTime > eTime) {
      showAlert('시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning');
      setSearchPeriod('all', true);
    }
  }
};
const eTimeChange = () => {
  // @ts-ignore
  const sTime = window.$('#startTimepickerInput').val() as string;
  // @ts-ignore
  const eTime = window.$('#endTimepickerInput').val() as string;

  if (sTime === eTime || !sTime || !eTime) {
    return;
  } else {
    if (sTime > eTime) {
      showAlert('종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning');
      setSearchPeriod('all', true);
    }
  }
};

onMounted(() => {
  coupon.value.target = 'all';
  coupon.value.publish_limit = 0;
  //@ts-ignore
  sfp.value = flatpickr(document.querySelector('#startDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => sDateChange() });
  //@ts-ignore
  efp.value = flatpickr(document.querySelector('#endDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => eDateChange() });

  //@ts-ignore
  stfp.value = flatpickr(document.querySelector('#startTimepickerInput'), { noCalendar: true, enableTime: true, time_24hr: true, onClose: () => sTimeChange() });
  //@ts-ignore
  etfp.value = flatpickr(document.querySelector('#endTimepickerInput'), { noCalendar: true, enableTime: true, time_24hr: true, onClose: () => eTimeChange() });
  // setSearchPeriod('today');
});
</script>

<style scoped></style>
