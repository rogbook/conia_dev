<template>
  <PageNavigator :before_link="['쿠폰관리']" :current="'쿠폰 상세'" />
  <div class="card">
    <div class="card-header" :class="{ 'py-2': !coupon.auto }">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">
          <div class="form-control-borderless h2 mb-0">
            쿠폰 상세 정보 <span class="text-danger" v-if="coupon.auto">[{{ coupon.status === 'Y' ? '발행중' : '발행중지' }}]</span>
          </div>
        </div>
        <div class="col-auto" v-if="getUserClassStr.includes('CM') && !coupon.auto">
          <div class="text-end">
            <button type="submit" class="btn btn-primary me-2" @click.prevent="openGiveCouponModal">쿠폰발급</button>
            <button type="submit" class="btn btn-danger" @click.prevent="delCoupon" v-if="coupon.publish_cnt <= 0">쿠폰삭제</button>
          </div>
        </div>
      </div>
    </div>
    <!-- 기본설정 영역 - [CM:읽기/수정, MC:읽기] -->
    <div class="card-body">
      <div class="row col mb-4 align-items-center" v-if="coupon.auto">
        <label class="col-md-1 col-form-label">발행 상태 변경</label>
        <div class="col-auto">
          <div class="form-check form-switch">
            <input type="checkbox" class="form-check-input" @click.prevent="checkClick($event)" :checked="coupon.status === 'Y'" />
          </div>
        </div>
      </div>

      <div class="row col mb-4 align-items-center">
        <label class="col-md-1 col-form-label">쿠폰 이름</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" v-model="coupon.name" readonly />
          </div>
        </div>
      </div>
      <div class="row col mb-4 align-items-center" v-if="coupon.percent">
        <label class="col-md-1 col-form-label">할인율</label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="number" class="form-control" v-model="coupon.percent" readonly />
            <div class="input-group-append input-group-text">
              <i class="bi-percent"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="row col mb-4 align-items-center" v-if="coupon.amount">
        <label class="col-md-1 col-form-label">할인금액</label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="number" class="form-control" v-model="coupon.amount" readonly />
            <div class="input-group-append input-group-text">원</div>
          </div>
        </div>
      </div>

      <div class="row mb-4 align-items-center">
        <label class="col-md-1 col-form-label">사용기한 지정방식</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input id="useMethod_date" type="radio" class="form-check-input" name="useMethod" value="date" :checked="coupon.begin_date && coupon.end_date ? true : false" disabled />
              <label class="form-check-label" for="useMethod_date">기간</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="useMethod_day" type="radio" class="form-check-input" name="useMethod" value="day" :checked="coupon.expire_days ? true : false" disabled />
              <label class="form-check-label" for="useMethod_day">일수</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="useMethod_time" type="radio" class="form-check-input" name="useMethod" value="time" :checked="coupon.begin_time && coupon.end_time ? true : false" disabled />
              <label class="form-check-label" for="useMethod_time">시간</label>
            </div>
          </div>
        </div>
      </div>

      <!-- 사용기간 Datepicker START -->
      <div class="row mb-4 align-items-center" v-if="coupon.begin_date && coupon.end_date">
        <label for="idLabel" class="col-md-1 col-form-label">사용 기한</label>
        <div class="col">
          <div class="row">
            <div class="col-md-3">
              <!-- Form Group -->
              <div class="form-group">
                <div class="js-flatpickr flatpickr-custom input-group">
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" :value="dateTimeFormatConverter(coupon.begin_date)" readonly />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">~</span>
            <div class="col-md-3">
              <!-- Form Group -->
              <div class="form-group">
                <div class="js-flatpickr flatpickr-custom input-group">
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" :value="dateTimeFormatConverter(coupon.end_date)" readonly />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 사용기간 Datepicker END -->
      <div class="row mb-4 align-items-center" v-else-if="coupon.expire_days">
        <label for="idLabel" class="col-md-1 col-form-label">사용 일수</label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="text" class="form-control" :value="coupon.expire_days" readonly />
            <div class="input-group-append input-group-text">일</div>
          </div>
        </div>
      </div>

      <div class="row mb-2 align-items-center" v-else-if="coupon.begin_time && coupon.end_time">
        <label for="idLabel" class="col-md-1 col-form-label">사용 가능 시간대<br /><span style="font-size: 0.7rem" class="text-danger">* 발급 당일 기준</span></label>
        <div class="col">
          <div class="row">
            <div class="col-lg-3">
              <!-- Form Group -->
              <div class="form-group">
                <div id="startTimepicker" class="js-flatpickr flatpickr-custom input-group">
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" v-model="coupon.begin_time" readonly />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">~</span>
            <div class="col-lg-3">
              <!-- Form Group -->
              <div class="form-group">
                <div id="endTimepicker" class="js-flatpickr flatpickr-custom input-group">
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" v-model="coupon.end_time" readonly />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-4 align-items-center">
        <label for="idLabel" class="col-md-1 col-form-label">발급 최대 매수</label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="text" class="form-control" :value="coupon.publish_limit ? coupon.publish_limit : 0" readonly />
            <div class="input-group-append input-group-text">건</div>
          </div>
        </div>
        <div class="col-auto ms-2">
          <label class="col-form-label"><span class="text-danger">* </span>0인 경우 발급최대매수 제한이 없습니다.</label>
        </div>
      </div>
      <div class="row mb-4 align-items-center" v-if="coupon.publish_begin_date || coupon.publish_end_date">
        <label for="idLabel" class="col-md-1 col-form-label">발행 기한</label>
        <div class="col">
          <div class="row">
            <div class="col-md-3">
              <!-- Form Group -->
              <div class="form-group">
                <div class="js-flatpickr flatpickr-custom input-group">
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" :value="dateTimeFormatConverter(coupon.publish_begin_date)" readonly />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">~</span>
            <div class="col-md-3">
              <!-- Form Group -->
              <div class="form-group">
                <div class="js-flatpickr flatpickr-custom input-group">
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" :value="dateTimeFormatConverter(coupon.publish_end_date)" readonly />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row col mb-4 align-items-center">
        <label class="col-md-1 col-form-label">쿠폰적용 상품</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input id="coupon_target_all" type="radio" class="form-check-input" name="coupon_type" value="all" disabled :checked="coupon.target === 'all'" />
              <label class="form-check-label" for="coupon_target_all">전체상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="coupon_target_one" type="radio" class="form-check-input" name="coupon_type" value="one" disabled :checked="coupon.target !== 'all'" />
              <label class="form-check-label" for="coupon_target_one">특정상품</label>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-4 align-items-center" v-if="coupon.target !== 'all'">
        <label class="col-12 col-md-1 col-form-label">쿠폰 적용 대상</label>
        <div class="col-md-11" style="width: 60%">
          <div class="table-responsive">
            <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
              <thead class="thead-light">
                <tr class="text-center">
                  <th>대상</th>
                  <th>상품코드/업체이메일</th>
                  <th>상품명/업체명</th>
                </tr>
              </thead>
              <tbody v-if="coupon.product">
                <tr class="text-center">
                  <td>[상품]</td>
                  <td>
                    <router-link v-if="coupon.product.code" :to="{ path: '/product/detail', state: { id: coupon.product.id } }">{{ coupon.product.code }}</router-link>
                  </td>
                  <td>{{ coupon.product.name }}</td>
                </tr>
              </tbody>
              <tbody v-else>
                <tr class="text-center" v-for="(item, i) in coupon.coupon_target" :key="i">
                  <td>
                    <span v-if="item.product_id">[상품]</span>
                    <span v-else-if="item.member_id">[업체]</span>
                  </td>
                  <td>
                    <span v-if="item.product_id">
                      <router-link :to="{ path: '/product/detail', state: { id: item.product.id } }">{{ item.product.code }}</router-link>
                    </span>
                    <span v-else-if="item.member_id">{{ item.member.email }}</span>
                  </td>
                  <td>
                    <span v-if="item.product_id">{{ item.product.name }}</span>
                    <span v-else-if="item.member_id">{{ item.member.name }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="row col mb-4 align-items-center">
        <label class="col-md-1 col-form-label">쿠폰 이미지 </label>
        <div class="col-md-4">
          <img v-if="coupon.image" class="img-fluid d-block" :src="coupon.image" alt="쿠폰 이미지" />
        </div>
      </div>
      <div class="row col align-items-center">
        <label class="col-md-1 col-form-label">쿠폰 상세 설명</label>
        <div class="col-md-4">
          <div class="input-group">
            <textarea type="text" class="form-control" v-model="coupon.description" readonly></textarea>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="card mt-2">
    <div class="card-header py-3">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">
          <div class="form-control-borderless h2 mb-0">쿠폰 발급 목록</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <!-- 발급일 검색기간 Datepicker -->
      <div class="row mb-2 align-items-center">
        <label for="idLabel" class="col-md-1 col-form-label">검색기간<br />(발급일)</label>
        <div class="col">
          <div class="row">
            <div class="col-md-2">
              <!-- Form Group -->
              <div class="form-group">
                <div
                  id="startDatepickerReg"
                  class="js-flatpickr flatpickr-custom input-group"
                  data-hs-flatpickr-options='{
                    "appendTo": "#startDatepickerReg",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInputReg" placeholder="날짜를 선택해주세요." @change="sDateChangeReg()" v-model="searchCondition.reg_date.sDate" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">-</span>
            <div class="col-md-2">
              <!-- Form Group -->
              <div class="form-group">
                <div
                  id="endDatepickerReg"
                  class="js-flatpickr flatpickr-custom input-group"
                  data-hs-flatpickr-options='{
                    "appendTo": "#endDatepickerReg",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInputReg" placeholder="날짜를 선택해주세요." @change="eDateChangeReg()" v-model="searchCondition.reg_date.eDate" />
                </div>
              </div>
            </div>
            <div class="d-md-none mt-1"></div>
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodReg('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodReg('week')">일주일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodReg('month')">1개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodReg('3month')">3개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodReg('6month')">6개월</button>
              <button type="button" class="btn btn-outline-info mb-1" @click.prevent="setSearchPeriodReg('all')">전체</button>
            </div>
          </div>
        </div>
      </div>
      <!-- End 발급일 검색기간 Datepicker -->

      <!-- 사용일 검색기간 Datepicker -->
      <div class="row mb-2 align-items-center">
        <label for="idLabel" class="col-md-1 col-form-label">검색기간<br />(사용일)</label>
        <div class="col">
          <div class="row">
            <div class="col-md-2">
              <!-- Form Group -->
              <div class="form-group">
                <div
                  id="startDatepickerUse"
                  class="js-flatpickr flatpickr-custom input-group"
                  data-hs-flatpickr-options='{
                    "appendTo": "#startDatepickerUse",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInputUse" placeholder="날짜를 선택해주세요." @change="sDateChangeUse()" v-model="searchCondition.use_date.sDate" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">-</span>
            <div class="col-md-2">
              <!-- Form Group -->
              <div class="form-group">
                <div
                  id="endDatepickerUse"
                  class="js-flatpickr flatpickr-custom input-group"
                  data-hs-flatpickr-options='{
                    "appendTo": "#endDatepickerUse",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInputUse" placeholder="날짜를 선택해주세요." @change="eDateChangeUse()" v-model="searchCondition.use_date.eDate" />
                </div>
              </div>
            </div>
            <div class="d-md-none mt-1"></div>
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodUse('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodUse('week')">일주일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodUse('month')">1개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodUse('3month')">3개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodUse('6month')">6개월</button>
              <button type="button" class="btn btn-outline-info mb-1" @click.prevent="setSearchPeriodUse('all')">전체</button>
            </div>
          </div>
        </div>
      </div>
      <!-- End 사용일 검색기간 Datepicker -->

      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-md-1 col-form-label">세부검색</label>
        <div class="col-md-2">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="d-md-none mt-1"></div>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getPublishedCouponList" />
          </div>
        </div>
      </div>
      <!-- End 세부검색어 입력 -->

      <!-- 사용유무 검색 -->
      <div class="row col">
        <label for="idLabel" class="col-md-1 col-form-label form-label">사용우무</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input id="formInlineRadio2" type="radio" class="form-check-input" name="formInlineRadio" value="Y" v-model="searchCondition.use_yn" />
              <label class="form-check-label" for="formInlineRadio2">사용</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="formInlineRadio3" type="radio" class="form-check-input" name="formInlineRadio" value="N" v-model="searchCondition.use_yn" />
              <label class="form-check-label" for="formInlineRadio3">미사용</label>
            </div>
          </div>
        </div>
      </div>
      <!-- End 사용유무 검색 -->
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getPublishedCouponList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>
  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="publishedCouponList.total > 0">총 : {{ publishedCouponList.total }}개</span>
      <button type="button" class="btn btn-sm btn-outline-info ms-4" @click.prevent="downloadExcel" v-if="publishedCouponList.total > 0">쿠폰발급목록 엑셀다운로드</button>
    </div>
    <!--    <div class="col-auto">-->
    <!--      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />-->
    <!--    </div>-->
  </div>

  <div class="table-responsive tableWrapper">
    <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table" id="publishTable">
      <thead class="thead-light">
        <tr class="text-center">
          <th style="width: 10%">쿠폰코드</th>
          <th style="width: 10%">발급회원</th>
          <th style="width: 10%">발급일</th>
          <th style="width: 10%">사용일</th>
          <th style="width: 10%">사용유무</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(item, i) in publishedCouponList.datas" :key="item.id">
          <td>{{ item.code }}</td>
          <td>{{ item.customer.email }}</td>
          <td>
            {{ dateTimeFormatConverter(item.reg_date) }}
          </td>
          <td>
            {{ item.use_date ? dateTimeFormatConverter(item.use_date) : '-' }}
          </td>
          <td>
            {{ item.use_yn === 'Y' ? '사용' : '미사용' }}
          </td>
        </tr>
        <tr>
          <td colspan="5" class="text-center" v-if="publishedCouponList.total === 0">표시할 항목이 없습니다.</td>
        </tr>
      </tbody>
    </table>
    <!--    <div class="table-footer-area" v-if="publishedCouponList.total > 0">-->
    <!--      <div class="row" v-if="total_page > 1">-->
    <!--        <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />-->
    <!--      </div>-->
    <!--    </div>-->
  </div>

  <!-- 쿠폰 발급 Modal -->
  <Modal :id="'giveCouponModal'" :title="'쿠폰 발급'" :xlarge="true">
    <template #body>
      <GiveCouponModal :coupon_id="coupon_id" :coupon_name="coupon.name" @closeModal="closeModal" />
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { onMounted, reactive, computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import Modal from '@/components/comm/modal.vue';
import { apiResponseCheck, getUserClassStr, dateTimeFormatConverter, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import GiveCouponModal from '@/pages/marketing/coupon/modal/GiveCoupon.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import type { Coupon } from 'CouponInfoModule';
import type { PublishedCouponList } from 'PublishedCouponInfoModule';
import { useCommonStore } from '@/stores/common';
import * as XLSX from 'xlsx';
import type { OrderProduct } from 'SettlementInfoModule';

const route = useRoute();
const router = useRouter();
const isChangeDate = ref(true);
const coupon = ref({} as Coupon);
const publishedCouponList = ref({} as PublishedCouponList);

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(publishedCouponList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getPublishedCouponList();
};

const checkClick = (event: any) => {
  if (!event.target.checked) {
    showConfirm('해당 쿠폰을 [발행중지] 상태로 변경하시겠습니까?', () => {
      apis.coupon.mod_coupon_status(coupon_id.value, '').then(res => {
        apiResponseCheck(res, () => {
          showAlert('쿠폰 발행 상태가 변경되었습니다.', 'success', () => {
            getCouponInfo();
          });
        });
      });
    });
  } else {
    showConfirm('해당 쿠폰을 [발행중] 상태로 변경하시겠습니까?', () => {
      apis.coupon.mod_coupon_status(coupon_id.value, 'Y').then(res => {
        apiResponseCheck(res, () => {
          showAlert('쿠폰 발행 상태가 변경되었습니다.', 'success', () => {
            getCouponInfo();
          });
        });
      });
    });
  }
};

const pageChange = (page: number) => {
  page_no.value = page;
  getPublishedCouponList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const coupon_id = computed(() => {
  return history.state.id;
});

const alertMessage = ref('');

const isUseDate = () => {
  if (coupon.value.expire_days) return true;

  if (coupon.value.begin_date && coupon.value.end_date) {
    const CouponEndDate = new Date(coupon.value.end_date);
    const nowDate = new Date();

    if (CouponEndDate > nowDate) {
      return true;
    } else {
      alertMessage.value = '사용 기한이 지난 쿠폰은 발급이 불가합니다.';
      return false;
    }
  } else if (coupon.value.begin_time && coupon.value.end_time) {
    const nowTime = new Date();
    const [hours, minutes] = coupon.value.end_time.split(':');
    //@ts-ignore
    const CouponEndTime = new Date(nowTime.getFullYear(), nowTime.getMonth(), nowTime.getDate(), hours, minutes);

    if (CouponEndTime > nowTime) {
      return true;
    } else {
      alertMessage.value = '사용 가능 시간대가 지난 쿠폰은 발급이 불가합니다.\n내일 다시 이용해주세요.';
      return false;
    }
  }
};

const searchCondition = reactive({
  reg_date: {
    sDate: '',
    eDate: '',
  },
  use_date: {
    sDate: '',
    eDate: '',
  },
  code: '',
  use_yn: 'Y',
});

const selDetailSearch = reactive({
  items: [{ name: '쿠폰코드', value: 'code' }],
  selectedItem: 'code',
  q: '',
  placeholder: '검색할 쿠폰의 코드를 입력해주세요.',
});
const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'code':
      selDetailSearch.placeholder = '검색할 쿠폰의 코드를 입력해주세요.';
      break;
  }
};

const setSearchPeriodReg = (period: string) => {
  isChangeDate.value = false;
  const today = new Date();
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInputReg'), {});
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInputReg'), {});
  switch (period) {
    case 'today':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(today, true, 'Y-m-d');
      break;
    case 'week':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 7), true, 'Y-m-d');
      break;
    case 'month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 30), true, 'Y-m-d');
      break;
    case '3month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 90), true, 'Y-m-d');
      break;
    case '6month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 180), true, 'Y-m-d');
      break;
    default:
      searchCondition.reg_date.sDate = '';
      searchCondition.reg_date.eDate = '';
      break;
  }
  isChangeDate.value = true;
};

const setSearchPeriodUse = (period: string) => {
  isChangeDate.value = false;
  const today = new Date();
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInputUse'), {});
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInputUse'), {});
  switch (period) {
    case 'today':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(today, true, 'Y-m-d');
      break;
    case 'week':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 7), true, 'Y-m-d');
      break;
    case 'month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 30), true, 'Y-m-d');
      break;
    case '3month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 90), true, 'Y-m-d');
      break;
    case '6month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 180), true, 'Y-m-d');
      break;
    default:
      searchCondition.use_date.sDate = '';
      searchCondition.use_date.eDate = '';
      break;
  }
  isChangeDate.value = true;
};

const sDateChangeReg = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInputReg'), {});

  // @ts-ignore
  const sDate = window.$('#startDatepickerInputReg').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInputReg').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning', () => {
        // @ts-ignore
        sfp.setDate(new Date(eDate), true, 'Y-m-d');
      });
    }
  }
};
const eDateChangeReg = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInputReg'), {});

  // @ts-ignore
  const sDate = window.$('#startDatepickerInputReg').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInputReg').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning', () => {
        // @ts-ignore
        efp.setDate(new Date(sDate), true, 'Y-m-d');
      });
    }
  }
};

const sDateChangeUse = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInputUse'), {});

  // @ts-ignore
  const sDate = window.$('#startDatepickerInputUse').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInputUse').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning', () => {
        // @ts-ignore
        sfp.setDate(new Date(eDate), true, 'Y-m-d');
      });
    }
  }
};
const eDateChangeUse = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInputUse'), {});

  // @ts-ignore
  const sDate = window.$('#startDatepickerInputUse').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInputUse').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning', () => {
        // @ts-ignore
        efp.setDate(new Date(sDate), true, 'Y-m-d');
      });
    }
  }
};

const clearSearchCondition = () => {
  searchCondition.reg_date.sDate = '';
  searchCondition.reg_date.eDate = '';
  searchCondition.use_date.sDate = '';
  searchCondition.use_date.eDate = '';
  searchCondition.use_yn = 'Y';
  selDetailSearch.selectedItem = 'code';
  selDetailSearch.q = '';
  setSearchPeriodReg('month');
  getPublishedCouponList();
};

const openGiveCouponModal = () => {
  if (!isUseDate()) {
    showAlert(alertMessage.value, 'warning');
    return;
  }
  showModal('giveCouponModal');
};

const closeModal = () => {
  hideModal('giveCouponModal');
  getPublishedCouponList();
  getCouponInfo();
};

const getCouponInfo = () => {
  apis.coupon.get_coupon(coupon_id.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      coupon.value = res;
    });
  });
};

const getPublishedCouponList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  //발급일 검색기간
  if (searchCondition.reg_date.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchCondition.reg_date.sDate}` : `s_reg_date=${searchCondition.reg_date.sDate}`);
  }
  if (searchCondition.reg_date.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchCondition.reg_date.eDate}` : `e_reg_date=${searchCondition.reg_date.eDate}`);
  }

  //사용일 검색기간
  if (searchCondition.use_date.sDate) {
    query = query.concat(query ? `&s_use_date=${searchCondition.use_date.sDate}` : `s_use_date=${searchCondition.use_date.sDate}`);
  }
  if (searchCondition.use_date.eDate) {
    query = query.concat(query ? `&e_use_date=${searchCondition.use_date.eDate}` : `e_use_date=${searchCondition.use_date.eDate}`);
  }

  //사용유무
  if (searchCondition.use_yn === 'Y') {
    query = query.concat(query ? `&use_yn=Y` : `use_yn=Y`);
  } else if (searchCondition.use_yn === 'N') {
    query = query.concat(query ? `&use_yn=N` : `use_yn=N`);
  }

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.coupon.get_published_coupon_list(coupon_id.value, query, 0, 5000).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      publishedCouponList.value.datas = res.datas;
      publishedCouponList.value.total = res.total;
    });
  });
};

const delCoupon = () => {
  showConfirm('해당 쿠폰을 삭제하시겠습니까?', () => {
    apis.coupon.del_coupon(coupon_id.value).then(res => {
      apiResponseCheck(res, () => {
        if (res.msg == 'success') {
          showAlert(`쿠폰이 삭제되었습니다.`, 'success');
          router.push('/marketing/coupon');
        }
      });
    });
  });
};

const downloadExcel = async () => {
  // TODO: 정산내역 엑셀 다운로드
  // @ts-ignore
  // 엑셀 파일 생성
  const book = XLSX.utils.book_new();

  // 엑셀에 넣을 데이터 만들기..
  const publishCouponList: any[] = makeExcelData();

  publishCouponList.unshift([]);
  publishCouponList.unshift([]);

  publishCouponList.unshift(['쿠폰명', coupon.value.name]);

  // sheet 생성 - aoa_to_sheet 장식으로
  const worksheetByAoa = XLSX.utils.aoa_to_sheet(publishCouponList);

  // 엑셀 파일에 sheet set (엑셀파일, 시트 데이터, 시트명)
  XLSX.utils.book_append_sheet(book, worksheetByAoa, '정산내역');

  // 엑셀 다운로드
  XLSX.writeFile(book, `[${coupon.value.name}] 쿠폰 발급내역 - ${new Date().getMilliseconds()}.xlsx`);
};

const makeExcelData = (): any[] => {
  const list = [] as any[];
  // TODO: MC, 코니아
  list.push(['쿠폰코드', '발급회원', '발급일', '사용일', '사용유무']);
  for (const c of publishedCouponList.value.datas) {
    const data = [] as any[];
    data.push(c.code); //쿠폰코드
    data.push(`${c.customer.name} (${c.customer.email})`); //발급회원 이름(이메일)
    data.push(`${dateTimeFormatConverter(c.reg_date)}`); //발급일
    data.push(`${c.use_date ? dateTimeFormatConverter(c.use_date) : '-'}`); //사용일
    data.push(`${c.use_yn === 'Y' ? '사용' : '미사용'}`); //사용유무
    list.push(data);
  }
  return list;
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
  setSearchPeriodReg('all');
  setSearchPeriodUse('all');
  limit.value = useCommonStore().getLimit;
  getCouponInfo();

  clearSearchCondition();
  page_no.value > 1 ? getPublishedCouponList(false) : getPublishedCouponList();
});
</script>

<style scoped>
.tableWrapper {
  max-height: 600px;
  overflow-y: auto;
}

#publishTable {
  border-collapse: collapse;
}

#publishTable th {
  position: sticky;
  top: 0px;
}
</style>
