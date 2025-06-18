<template>
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">상품 기타 정보</h4>
          <small>상품의 기타정보를 등록/수정합니다.</small>
        </div>
        <div class="nav-item ms-auto">
          <button type="button" class="btn btn-warning" @click.prevent="saveEtcInfo">저장</button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card mb-4">
        <div class="card-header">[판매설정]</div>
        <div class="card-body">
          <div class="row align-items-center mb-2">
            <div class="col-md-2 col-form-label">1인당 구매횟수 제한</div>
            <div class="col row align-items-center">
              <div class="col-md-2">
                <input type="number" class="form-control" placeholder="1인당 구매횟수" v-model.lazy="prodInfo.user_limit" oninput="this.value.length > 11 ? this.value = this.value.slice(0,11) : this.value = this.value" @input="checkNumber($event)" />
              </div>
              <div class="col-auto ms-2">
                <label class="col-form-label"><span class="text-danger">* </span>0을 입력하면 <span class="text-danger">1인당</span> 구매 횟수 제한이 없습니다.</label>
              </div>
            </div>
          </div>
          <div class="row align-items-center mb-2">
            <div class="col-md-2 col-form-label">1인당 구매횟수 제한 초기화 주기</div>
            <div class="col">
              <div class="row form-control border-0 align-items-center">
                <div class="col-auto form-check form-check-inline">
                  <div class="row align-items-center">
                    <div class="col-auto">
                      <input type="radio" id="u_limit_reset_type_m" class="form-check-input" name="u_limit_reset_type" v-model="mUserLimitReset.type" value="month" @change="onChangeLimitReset" />
                      <label class="form-check-label px-1" for="u_limit_reset_type_m">매월</label>
                    </div>
                    <div class="col-md-auto ps-0 pe-0" v-if="mUserLimitReset.type === 'month'">
                      <div class="tom-select-custom">
                        <select class="form-select" v-model="mUserLimitReset.value" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                          <option v-for="i in 31" :key="i" :value="i">{{ i }}</option>
                        </select>
                      </div>
                    </div>
                    <div class="col-md-auto" v-if="mUserLimitReset.type === 'month'">일 마다</div>
                  </div>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <div class="row align-items-center">
                    <div class="col-auto">
                      <input type="radio" id="u_limit_reset_type_w" class="form-check-input" name="u_limit_reset_type" v-model="mUserLimitReset.type" value="week" @change="onChangeLimitReset" />
                      <label class="form-check-label px-1" for="u_limit_reset_type_w">매주</label>
                    </div>
                    <div class="col-md-auto ps-0 pe-0" v-if="mUserLimitReset.type === 'week'">
                      <div class="tom-select-custom">
                        <select class="form-select" v-model="mUserLimitReset.value" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                          <option value="1">월</option>
                          <option value="2">화</option>
                          <option value="3">수</option>
                          <option value="4">목</option>
                          <option value="5">금</option>
                          <option value="6">토</option>
                          <option value="0">일</option>
                        </select>
                      </div>
                    </div>
                    <div class="col-md-auto" v-if="mUserLimitReset.type === 'week'">요일 마다</div>
                  </div>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input type="radio" id="u_limit_reset_type_n" class="form-check-input" name="u_limit_reset_type" v-model="mUserLimitReset.type" value="" />
                  <label class="form-check-label px-1" for="u_limit_reset_type_n">사용안함</label>
                </div>
              </div>
            </div>
          </div>
          <div class="row align-items-center mb-2">
            <div class="col-md-2 col-form-label">1회당 최소 구매수량 제한</div>
            <div class="col row align-items-center">
              <div class="col-md-2">
                <input type="number" class="form-control" placeholder="1회당 최소 구매횟수" v-model.lazy="prodInfo.min_purchase_limit" oninput="this.value.length > 11 ? this.value = this.value.slice(0,11) : this.value = this.value" @input="checkNumber($event)" />
              </div>
              <div class="col-auto ms-2">
                <label class="col-form-label"><span class="text-danger">* </span>0을 입력하면 1회당 <span class="text-danger">최소</span> 구매 수량 제한이 없습니다.</label>
              </div>
            </div>
          </div>
          <div class="row align-items-center mb-2">
            <div class="col-md-2 col-form-label">1회당 최대 구매수량 제한</div>
            <div class="col row align-items-center">
              <div class="col-md-2">
                <input type="number" class="form-control" placeholder="1회당 최대 구매횟수" v-model.lazy="prodInfo.max_purchase_limit" oninput="this.value.length > 11 ? this.value = this.value.slice(0,11) : this.value = this.value" @input="checkNumber($event)" />
              </div>
              <div class="col-auto ms-2">
                <label class="col-form-label"><span class="text-danger">* </span>0을 입력하면 1회당 <span class="text-danger">최대</span> 구매 수량 제한이 없습니다.</label>
              </div>
            </div>
          </div>
          <!-- 판매기간 Datepicker -->
          <div class="row mb-2 align-items-center">
            <label for="idLabel" class="col-md-2 col-form-label">판매 기간 설정</label>
            <div class="col">
              <div class="row">
                <div class="col-lg-3">
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
                <div class="col-lg-3">
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
                <div class="d-lg-none mt-2"></div>
                <div class="col">
                  <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
                  <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">일주일</button>
                  <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('month')">1개월</button>
                  <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('3month')">3개월</button>
                  <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('6month')">6개월</button>
                  <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('all')">상시판매</button>
                </div>
              </div>
            </div>
          </div>
          <!-- 구매가능시간 Timepicker -->
          <div class="row mb-2 align-items-center">
            <label for="idLabel" class="col-md-2 col-form-label">구매가능 시간설정</label>
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
                  <button type="button" class="btn btn-outline-info me-1" @click.prevent="setSearchPeriod('all', true)">상시판매</button>
                </div>
              </div>
            </div>
          </div>

          <div class="row align-items-center" v-if="props.prodType.startsWith('UP')">
            <div class="col-md-2 col-form-label"><span v-if="props.prodType === 'UP-EC'" class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 사용기한 지정방식</div>
            <div class="col">
              <div class="row form-control border-0">
                <div class="col-auto form-check form-check-inline">
                  <input type="radio" id="use_end_type_period" class="form-check-input" name="use_end_type" v-model="use_end_type" value="period" />
                  <label class="form-check-label px-1" for="use_end_type_period">일수</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input type="radio" id="use_end_type_date" class="form-check-input" name="use_end_type" v-model="use_end_type" value="date" />
                  <label class="form-check-label px-1" for="use_end_type_date">기한</label>
                </div>
                <div class="col-auto form-check form-check-inline" v-if="props.prodType !== 'UP-EC'">
                  <input type="radio" id="use_end_type_none" class="form-check-input" name="use_end_type" v-model="use_end_type" value="none" />
                  <label class="form-check-label px-1" for="use_end_type_none">사용안함</label>
                </div>
              </div>
            </div>
          </div>

          <div class="row align-items-center mb-2" v-if="props.prodType.startsWith('UP') && use_end_type == 'period'">
            <div class="col-md-2 col-form-label"><span v-if="props.prodType === 'UP-EC'" class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 사용기한 지정(일수)</div>
            <div class="col row align-items-center">
              <div class="col-md-3">
                <input type="number" class="form-control" inputmode="decimal" placeholder="일수를 입력해주세요. (최소 1일)" v-model="prodInfo.use_end_period" @input="checkNumber($event, false)" />
              </div>
            </div>
          </div>

          <div class="row align-items-center mb-2" v-show="props.prodType.startsWith('UP') && use_end_type == 'date'">
            <div class="col-md-2 col-form-label"><span v-if="props.prodType === 'UP-EC'" class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 사용기한 지정(기한)</div>
            <div class="col row align-items-center">
              <div class="col-md-3">
                <div class="form-group">
                  <div
                    id="useEndDatepicker"
                    class="js-flatpickr flatpickr-custom input-group"
                    data-hs-flatpickr-options='{
                      "appendTo": "#useEndDatepicker",
                      "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                    }'>
                    <div class="input-group-prepend input-group-text" data-bs-toggle>
                      <i class="bi-calendar-week"></i>
                    </div>
                    <input type="text" class="flatpickr-custom-form-control form-control" id="useEndDatepickerInput" placeholder="날짜를 선택해주세요." v-model="useDate.eDate" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="row align-items-center">
            <div class="col-md-2 col-form-label">판매종료시간 노출여부</div>
            <div class="col">
              <div class="row form-control border-0">
                <div class="col-auto form-check form-check-inline">
                  <input type="radio" id="radio_view_end_y" class="form-check-input" name="view_end_yn" v-model="prodInfo.view_end_time" value="Y" />
                  <label class="form-check-label px-1" for="radio_view_end_y">노출</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input type="radio" id="radio_view_end_n" class="form-check-input" name="view_end_yn" v-model="prodInfo.view_end_time" value="N" />
                  <label class="form-check-label px-1" for="radio_view_end_n">미노출</label>
                </div>
              </div>
            </div>
          </div>

          <div class="row align-items-center">
            <div class="col-md-2 col-form-label">쿠폰 사용 가능 여부</div>
            <div class="col">
              <div class="row form-control border-0">
                <div class="col-auto form-check form-check-inline">
                  <input type="radio" id="radio_coupon_y" class="form-check-input" name="coupon_yn" v-model="prodInfo.coupon_yn" value="Y" />
                  <label class="form-check-label px-1" for="radio_coupon_y">사용가능</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input type="radio" id="radio_coupon_n" class="form-check-input" name="coupon_yn" v-model="prodInfo.coupon_yn" value="N" />
                  <label class="form-check-label px-1" for="radio_coupon_n">사용불가</label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-4" v-if="props.prodType === 'UP-EC'">
        <div class="card-header">[E-쿠폰 설정]</div>
        <div class="card-body">
          <div class="row align-items-center mb-2">
            <div class="col-sm-2 col-form-label">이용가능 매장</div>
            <div class="col row align-items-center">
              <div class="col-sm-4">
                <input type="text" class="form-control" v-model.lazy="prodInfo.use_place" placeholder="이용가능 매장을 입력해 주세요." />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-4" v-if="getUserClassStr.includes('CM')">
        <div class="card-header">[결제수단관리]</div>
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-md-1 col-form-label">결제수단 제한</div>
            <div class="col form-control border-0">
              <div class="row align-items-center">
                <div class="col-auto">
                  <input type="checkbox" id="check_pg_kcp" class="form-check-input" name="check_pg_provider" value="KCP" disabled />
                  <label class="form-check-label px-1" for="check_pg_kcp">KCP</label>
                </div>
                <div class="col-auto">
                  <input type="checkbox" id="check_pg_payco" class="form-check-input" name="check_pg_provider" value="PAYCO" v-model="currentPgProvider" />
                  <label class="form-check-label px-1" for="check_pg_payco">PAYCO</label>
                </div>
                <div class="col-md form-control border-0 text-danger">&#8251;선택된 결제업체는 본상품 결제시 결제수단으로 이용 불가합니다.</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">[메모]</div>
        <div class="card-body">
          <textarea class="form-control" placeholder="상점에 표시될 상품의 추가적인 메모를 입력해주세요." v-model.trim="prodInfo.memo" style="min-height: 100px; max-height: 300px" maxlength="255" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import type { Prod } from 'ProductListInfoModule';
import { apiResponseCheck, getUserClassStr, isAdmin, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import type { IProduct } from '@/apis/api.product';
import { useUserStore } from '@/stores/user';

const props = defineProps<{ prodType: string; productId: number; productInfo: Prod | null; reg: boolean }>();
const emits = defineEmits(['saveFinish', 'changedProdInfo']);

const prodInfo = ref({} as Prod);
const originProdInfo = ref({} as Prod);

const currentPgProvider = ref([] as string[]);
const originPgProvider = ref([] as string[]);

// 사용기한 설정 관련
const use_end_type = ref('period');
const origin_use_end_type = ref('period');
const useDate = reactive({
  eDate: '',
});

const saleDate = reactive({
  sDate: '',
  eDate: '',
  sTime: '',
  eTime: '',
});

interface UserLimitReset {
  type: string;
  value: number;
}

const mUserLimitReset = ref({} as UserLimitReset);
const onChangeLimitReset = () => {
  if (originProdInfo.value.user_limit_reset) {
    const origin = JSON.parse(originProdInfo.value.user_limit_reset);
    if (mUserLimitReset.value.type === origin.type) {
      mUserLimitReset.value = origin;
    } else {
      mUserLimitReset.value.value = 1;
    }
  } else {
    mUserLimitReset.value.value = 1;
  }
};

const sfp = ref();
const efp = ref();
const stfp = ref();
const etfp = ref();
const uefp = ref();

const checkNumber = (event: any, zero: boolean = true) => {
  if (event.target.value) {
    //E쿠폰의 경우 365일 제한
    if (props.prodType === 'UP-EC' && event.target.value > 365) {
      showAlert('최대 365일까지만 지정 가능합니다.', 'warning', () => {
        prodInfo.value.use_end_period = 1;
        event.target.focus();
      });
      return;
    }
    if (event.target.value > 99999999.99) {
      showAlert('최대 1억 미만 까지 입력할 수 있습니다.', 'warning', () => {
        event.target.focus();
      });
      return;
    } else if (event.target.value < 0) {
      showAlert('음수는 입력할 수 없습니다.', 'warning', () => {
        event.target.focus();
      });
      return;
    }

    if (event.target.value.startsWith('0') && event.target.value.length > 1 && zero) {
      event.target.value = event.target.value.slice(1);
    } else if (event.target.value.startsWith('0') && !zero) {
      event.target.value = event.target.value.slice(1);
    } else {
      event.target.value = event.target.value.replace(/[^0-9]/g, '');
    }
  }
};

const saveEtcInfo = () => {
  let data = {} as IProduct;
  if (prodInfo.value.user_limit !== originProdInfo.value.user_limit) {
    data.user_limit = prodInfo.value.user_limit;
  }
  if (prodInfo.value.min_purchase_limit !== originProdInfo.value.min_purchase_limit) {
    data.min_purchase_limit = prodInfo.value.min_purchase_limit;
  }
  if (prodInfo.value.max_purchase_limit !== originProdInfo.value.max_purchase_limit) {
    data.max_purchase_limit = prodInfo.value.max_purchase_limit;
  }
  if (prodInfo.value.memo !== originProdInfo.value.memo) {
    data.memo = prodInfo.value.memo;
  }
  if (prodInfo.value.coupon_yn !== originProdInfo.value.coupon_yn) {
    data.coupon_yn = prodInfo.value.coupon_yn;
  }
  if (prodInfo.value.use_place !== originProdInfo.value.use_place) {
    data.use_place = prodInfo.value.use_place;
  }

  if (prodInfo.value.view_end_time !== originProdInfo.value.view_end_time) {
    data.view_end_time = prodInfo.value.view_end_time;
  }

  if (!originProdInfo.value.sale_start_date && saleDate.sDate) {
    data.sale_start_date = saleDate.sDate;
  } else if (originProdInfo.value.sale_start_date && !saleDate.sDate) {
    data.sale_start_date = '_null_';
  } else {
    if (originProdInfo.value.sale_start_date != null && saleDate.sDate !== originProdInfo.value.sale_start_date) {
      data.sale_start_date = saleDate.sDate;
    }
  }
  if (!originProdInfo.value.sale_end_date && saleDate.eDate) {
    data.sale_end_date = saleDate.eDate;
  } else if (originProdInfo.value.sale_end_date && !saleDate.eDate) {
    data.sale_end_date = '_null_';
  } else {
    if (originProdInfo.value.sale_end_date != null && saleDate.eDate !== originProdInfo.value.sale_end_date) {
      data.sale_end_date = saleDate.eDate;
    }
  }

  if (!originProdInfo.value.sale_start_time && saleDate.sTime) {
    data.sale_start_time = saleDate.sTime;
  } else if (originProdInfo.value.sale_start_time && !saleDate.sTime) {
    data.sale_start_time = '_null_';
  } else {
    if (originProdInfo.value.sale_start_time != null && saleDate.sTime !== originProdInfo.value.sale_start_time) {
      data.sale_start_time = saleDate.sTime;
    }
  }
  if (!originProdInfo.value.sale_end_time && saleDate.eTime) {
    data.sale_end_time = saleDate.eTime;
  } else if (originProdInfo.value.sale_end_time && !saleDate.eTime) {
    data.sale_end_time = '_null_';
  } else {
    if (originProdInfo.value.sale_end_time != null && saleDate.eTime !== originProdInfo.value.sale_end_time) {
      data.sale_end_time = saleDate.eTime;
    }
  }
  // 비실물 오프라인 상품인 경우 사용기한
  if (props.prodType.startsWith('UP')) {
    if (use_end_type.value === 'period') {
      // 일수 제한 체크
      if (!prodInfo.value.use_end_period) {
        showAlert('사용기한 일수를 입력해주세요.', 'warning');
        return;
      }
      if (prodInfo.value.use_end_period > 99999999.99 || prodInfo.value.use_end_period < 1) {
        showAlert('사용기한 지정(일수) 데이터를 확인해주세요.', 'warning');
        return;
      }

      // 기존과 동일 여부 체크
      if (prodInfo.value.use_end_period !== originProdInfo.value.use_end_period) {
        data.use_end_period = prodInfo.value.use_end_period;
        data.use_end_date = '_null_';
      }
    } else if (use_end_type.value === 'date') {
      // 기한 제한 체크
      if (!useDate.eDate) {
        showAlert('사용기한 날짜를 선택해주세요.', 'warning');
        return;
      }
      // 현재 일자보다 큰지 체크
      const now = new Date();
      const todayStr = `${now.getFullYear()}-${('0' + (now.getMonth() + 1)).slice(-2)}-${('0' + now.getDate()).slice(-2)} 00:00`;
      if (todayStr > useDate.eDate) {
        showAlert('사용기한은 오늘보다 이전 날짜일 수 없습니다.', 'warning');
        return;
      }
      if (originProdInfo.value?.use_end_date?.length > 17) {
        if (originProdInfo.value?.use_end_date?.replace('T', ' ').slice(0, -3) !== useDate.eDate) {
          data.use_end_period = 0;
          data.use_end_date = useDate.eDate;
        }
      } else {
        if (originProdInfo.value.use_end_date !== useDate.eDate) {
          data.use_end_period = 0;
          data.use_end_date = useDate.eDate;
        }
      }
    } else {
      if (origin_use_end_type.value !== 'none') {
        // 사용 안함
        data.use_end_date = '_null_';
        data.use_end_period = 0;
      }
    }
  }

  // 결제수단 제한
  if (currentPgProvider.value.toString() !== originPgProvider.value.toString()) {
    // 변경사항 있음
    if (currentPgProvider.value.length > 0) {
      data.pg_provider = currentPgProvider.value.join('|');
    } else {
      data.pg_provider = '_null_';
    }
  }

  // 1인당 구매횟수 제한 초기화
  const currentULR: string = JSON.stringify(mUserLimitReset.value);
  console.log(currentULR);
  if (currentULR !== originProdInfo.value.user_limit_reset) {
    if (mUserLimitReset.value.type) {
      data.user_limit_reset = currentULR;
    } else {
      //사용안함
      if (originProdInfo.value.user_limit_reset) {
        data.user_limit_reset = '_null_';
      }
    }
  }

  if (Object.keys(data).length === 0) {
    if (props.reg) {
      emits('saveFinish', 'etc');
      return;
    }
    showAlert('변경 사항이 없습니다.', 'warning');
    return;
  }

  showLogConsole(data);

  showConfirm('저장하시겠습니까?', () => {
    apis.product.updateBaseInfo(props.productId, data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 기타 정보가 저장되었습니다.', 'success');
        emits('changedProdInfo');
        emits('saveFinish', 'etc');
        valueRefresh(data);
      });
    });
  });
};

const onStepActive = () => {
  if (props.productId && props.productInfo) {
    prodInfo.value = JSON.parse(JSON.stringify(props.productInfo));
    originProdInfo.value = JSON.parse(JSON.stringify(props.productInfo));

    if (!prodInfo.value.min_purchase_limit) {
      prodInfo.value.min_purchase_limit = '0';
      originProdInfo.value.min_purchase_limit = '0';
    }
    if (!prodInfo.value.max_purchase_limit) {
      prodInfo.value.max_purchase_limit = '0';
      originProdInfo.value.max_purchase_limit = '0';
    }
    if (!prodInfo.value.user_limit) {
      prodInfo.value.user_limit = 0;
      originProdInfo.value.user_limit = 0;
    }

    if (prodInfo.value.sale_start_date) {
      saleDate.sDate = prodInfo.value.sale_start_date.replace('T', ' ').slice(0, -3);
      sfp.value.setDate(prodInfo.value.sale_start_date);
    }

    if (prodInfo.value.sale_end_date) {
      saleDate.eDate = prodInfo.value.sale_end_date.replace('T', ' ').slice(0, -3);
      efp.value.setDate(prodInfo.value.sale_end_date);
    }

    if (prodInfo.value.sale_start_time) {
      saleDate.sTime = prodInfo.value.sale_start_time.slice(0, -3);
      stfp.value.setDate(prodInfo.value.sale_start_time);
    }
    if (prodInfo.value.sale_end_time) {
      saleDate.eTime = prodInfo.value.sale_end_time.slice(0, -3);
      etfp.value.setDate(prodInfo.value.sale_end_time);
    }

    // 사용기한 지정방식 초기화
    // 사용기한 지정방식 종류에 따른 (일수,기한) 들 초기화
    if (props.prodType.startsWith('UP')) {
      if (prodInfo.value.use_end_period === 0) {
        prodInfo.value.use_end_period = originProdInfo.value.use_end_period = '';
      }
      if (prodInfo.value.use_end_period) {
        use_end_type.value = 'period';
      } else if (prodInfo.value.use_end_date) {
        use_end_type.value = 'date';
        useDate.eDate = prodInfo.value.use_end_date.replace('T', ' ').slice(0, -3);
      } else {
        if (props.prodType === 'UP-EC') {
          use_end_type.value = 'period';
        } else {
          use_end_type.value = 'none';
        }
      }
      origin_use_end_type.value = `${use_end_type.value}`;
    }

    // 결제수단제한
    if (prodInfo.value.pg_provider) {
      originPgProvider.value = `${prodInfo.value.pg_provider}`.split('|');
      currentPgProvider.value = `${prodInfo.value.pg_provider}`.split('|');
    }

    // 1인당 구매횟수 재한 초기화
    if (originProdInfo.value.user_limit_reset) {
      mUserLimitReset.value = JSON.parse(originProdInfo.value.user_limit_reset);
    } else {
      mUserLimitReset.value.type = '';
      mUserLimitReset.value.value = 1;
    }
  }
};

const valueRefresh = (data: IProduct) => {
  originPgProvider.value = [];
  currentPgProvider.value = [];
  for (const key of Object.keys(data)) {
    //@ts-ignore
    prodInfo.value[key] = data[key] === '_null_' ? null : data[key];
    //@ts-ignore
    originProdInfo.value[key] = data[key] === '_null_' ? null : data[key];
  }

  if (prodInfo.value.pg_provider) {
    originPgProvider.value = `${prodInfo.value.pg_provider}`.split('|');
    currentPgProvider.value = `${prodInfo.value.pg_provider}`.split('|');
  }

  origin_use_end_type.value = `${use_end_type.value}`;
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
    case '3month':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 90).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case '6month':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 180).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
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
      showAlert('검색 종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      efp.value.setDate(new Date(), true, 'Y-m-d H:i');
    }
  }
};

const useEndDateChange = () => {
  if (props.prodType !== 'UP-EC') {
    return;
  }
  // @ts-ignore
  const useEndfp = window.$('#useEndDatepickerInput').val() as string;
  const timeDifference = new Date().getTime() - new Date(useEndfp).getTime();
  const daysDifference = Math.abs(timeDifference / (1000 * 3600 * 24));

  if (daysDifference > 365) {
    showAlert('사용 기한은 오늘로부터 1년 이내로만 지정 가능합니다.', 'warning');
    useDate.eDate = '';
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
      showAlert('검색 시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      sfp.value.setDate(new Date(), true, 'H:i');
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
      showAlert('검색 종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      efp.value.setDate(new Date(), true, 'H:i');
    }
  }
};

defineExpose({ onStepActive });

onMounted(() => {
  //@ts-ignore
  sfp.value = flatpickr(document.querySelector('#startDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => sDateChange() });
  //@ts-ignore
  efp.value = flatpickr(document.querySelector('#endDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => eDateChange() });

  //@ts-ignore
  stfp.value = flatpickr(document.querySelector('#startTimepickerInput'), { noCalendar: true, enableTime: true, time_24hr: true, onClose: () => sTimeChange() });
  //@ts-ignore
  etfp.value = flatpickr(document.querySelector('#endTimepickerInput'), { noCalendar: true, enableTime: true, time_24hr: true, onClose: () => eTimeChange() });

  //@ts-ignore
  uefp.value = flatpickr(document.querySelector('#useEndDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => useEndDateChange() });

  setSearchPeriod('all');
  setSearchPeriod('all', true);
});
</script>

<style scoped></style>
