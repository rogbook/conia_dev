<template>
  <div class="card">
    <div class="card-header py-2 text-black h4">구성된 카탈로그 상품</div>
    <div class="card-body">
      <!-- 공급자(PA) 선택 -->
      <div class="row mb-2 align-items-center">
        <label for="idLabel" class="col-md-2 col-form-label">공급자(PA)</label>
        <div class="col-md-6">
          <div class="input-group">
            <input type="text" class="form-control" v-model="paInfo.name" placeholder="공급자(PA)를 선택해주세요." aria-label="" disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="openPaSelModal" v-if="paInfo.noPa">검색</button>
          </div>
        </div>
      </div>
      <!-- 상품상태 -->
      <div class="row align-items-center">
        <div class="col-md-2 col-form-label">상품상태</div>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_cp_status_all" class="form-check-input" name="search_cp_status" v-model="selDetailSearch.status" value="all" />
              <label class="form-check-label px-1" for="search_cp_status_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_cp_status_y" class="form-check-input" name="search_cp_status" v-model="selDetailSearch.status" value="Y" />
              <label class="form-check-label px-1" for="search_cp_status_y">정상</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_cp_status_p" class="form-check-input" name="search_cp_status" v-model="selDetailSearch.status" value="P" />
              <label class="form-check-label px-1" for="search_cp_status_p">판매종료</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_cp_status_s" class="form-check-input" name="search_cp_status" v-model="selDetailSearch.status" value="S" />
              <label class="form-check-label px-1" for="search_cp_status_s">품절</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_cp_status_n" class="form-check-input" name="search_cp_status" v-model="selDetailSearch.status" value="N" />
              <label class="form-check-label px-1" for="search_cp_status_n">미승인</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 상품유형 radio -->
      <div class="row align-items-center mb-2">
        <div class="col-md-2 col-form-label">상품유형</div>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_all" class="form-check-input" name="prod_type" value="all" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_DP" class="form-check-input" name="prod_type" value="DP" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_DP">배송상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_UP_OF" class="form-check-input" name="prod_type" value="UP-OF" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_UP_OF">티켓상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_UP_EC" class="form-check-input" name="prod_type" value="UP-EC" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_UP_EC">E-쿠폰</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 검색기간 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-md-2 col-form-label">검색기간</label>
        <div class="col">
          <div class="row mb-2">
            <div class="col-md">
              <!-- Form Group -->
              <div class="form-group">
                <div
                  id="startDatepicker"
                  class="js-flatpickr flatpickr-custom input-group"
                  data-hs-flatpickr-options='{
                    "appendTo": "#startDatepicker",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." @change="sDateChange()" v-model="searchDate.sDate" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">-</span>
            <div class="col-md">
              <!-- Form Group -->
              <div class="form-group">
                <div
                  id="endDatepicker"
                  class="js-flatpickr flatpickr-custom input-group"
                  data-hs-flatpickr-options='{
                    "appendTo": "#endDatepicker",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." @change="eDateChange()" v-model="searchDate.eDate" />
                </div>
              </div>
            </div>
          </div>
          <div class="d-md-none mt-1"></div>
          <div class="row">
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">일주일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('month')">1개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('3month')">3개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('6month')">6개월</button>
              <button type="button" class="btn btn-outline-info mb-1" @click.prevent="setSearchPeriod('all')">전체</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 카테고리/브랜드 선택 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label">카테고리/브랜드</label>
        <div class="col-md-3">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.cateBrand" @change="onChangeCateBrand" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-text="'카테고리'" value="c"></option>
              <option v-text="'브랜드'" value="b"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="d-md-none mt-1"></div>
        <div class="col">
          <div class="input-group" v-if="selDetailSearch.cateBrand === 'c'">
            <input type="text" class="form-control" v-model="selDetailSearch.categoryLabel" placeholder="카테고리를 선택해주세요." aria-label="" disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="openCategoryModal">검색</button>
          </div>
          <div class="input-group" v-if="selDetailSearch.cateBrand === 'b'">
            <input type="text" class="form-control" v-model="selDetailSearch.brandName" placeholder="브랜드를 선택해주세요." aria-label="" disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('SelBrandModal')">검색</button>
          </div>
        </div>
      </div>
      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label">세부검색</label>
        <div class="col-md-3">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="d-md-none mt-1"></div>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getCatalogProdList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getCatalogProdList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between" v-if="cProductList.total > 0">
    <div class="col-auto">
      <span>총 : {{ cProductList.total }}개</span>
      <div class="col-auto align-items-center mt-2" style="font-size: 0.7rem">
        <span class="badge" :style="{ 'background-color': `#9b00ff !important` }">배</span>
        <span class="ms-1 me-2">배송상품</span>
        <span class="badge" :style="{ 'background-color': `#ff6b00 !important` }">티</span>
        <span class="ms-1 me-2">티켓상품</span>
        <span class="badge text-bg-success">E</span>
        <span class="ms-1">E-쿠폰</span>
      </div>
    </div>
    <div class="d-md-none mt-1"></div>
    <div class="col-auto">
      <button type="button" class="btn btn-sm btn-warning col-auto" @click.prevent="showModal('allVariationModal')">판매가 보정 일괄 수정</button>
    </div>
  </div>
  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto"></div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <div class="table-responsive">
    <table class="table table-borderless table-thead-bordered table-align-middle">
      <thead class="thead-light">
        <tr class="text-center text-nowrap">
          <th>
            <input type="checkbox" class="form-check-input" name="cb_add_product" id="cb_p_all" v-model="allCheck" @change="allCheckedClick" />
          </th>
          <th class="px-0" style="width: 5%">상품<br />유형</th>
          <th style="width: 10%">상품코드</th>
          <th style="width: 5%">이미지</th>
          <th style="width: 15%">상품명</th>
          <th style="width: 15%">공급가</th>
          <th style="width: 15%">정상가</th>
          <th style="width: 15%">판매가</th>
          <th style="width: 5%">상품상태</th>
          <th style="width: 10%">판매가 보정</th>
        </tr>
      </thead>
      <tbody class="text-wrap">
        <tr class="text-center" v-for="(c, i) in cProductList.datas" :key="c.id">
          <td>
            <input type="checkbox" class="form-check-input" name="cb_add_product" v-bind:id="`cb_p_${c.product.code}`" :value="c" v-model="mSelProductList" />
          </td>
          <td style="font-size: 0.6rem">
            <div v-if="c.product.type.startsWith('DP')">
              <span class="badge" :style="{ 'background-color': `#9b00ff !important` }">배</span>
            </div>
            <div v-else-if="c.product.type === 'UP-OF'">
              <span class="badge" :style="{ 'background-color': `#ff6b00 !important` }">티</span>
            </div>
            <div v-else-if="c.product.type === 'UP-EC'">
              <span class="badge text-bg-success">E</span>
            </div>
          </td>
          <td class="p-0" style="font-size: 0.6rem">
            <router-link :to="{ path: `/product/detail`, state: { id: c.product.id } }" style="font-size: 0.6rem">{{ c.product.code }}</router-link>
          </td>
          <td>
            <div class="avatar" v-if="c.product.photos.length > 0">
              <img class="avatar-img" :src="c.product.photos[0].uri" alt="Image Description" />
            </div>
            <div class="avatar" v-if="c.product.photos.length === 0">
              <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
            </div>
          </td>
          <td class="p-0" style="font-size: 0.8rem; width: 15%">
            {{ c.product.name }}
          </td>
          <td class="ps-1 pe-1 text-end">{{ getPriceInfo(c.product.options, 'supply') }}</td>
          <td class="ps-1 pe-1 text-end">{{ getPriceInfo(c.product.options, 'origin') }}</td>
          <td class="ps-1 pe-1 text-end">{{ getPriceInfo(c.product.options, 'sell') }}</td>
          <td class="text-nowrap">{{ c.product.status === 'Y' ? '정상' : c.product.status === 'P' ? '판매중지' : c.product.status === 'S' ? '품절' : '미승인' }}</td>
          <td class="p-0">
            <input
              type="number"
              class="form-control text-center px-0"
              v-if="c.product.type !== 'G'"
              v-model="c.variation"
              placeholder="숫자만입력"
              :class="{ 'text-primary': c.variation < 0, 'text-danger': c.variation > 0 }"
              @change="checkVariationRange(i, c.variation, c.product.options, $event)" />
            <!-- TODO : 그룹상품유형 페지 (추후 삭제 요망) -->
            <!--          <input-->
            <!--            type="number"-->
            <!--            class="form-control text-center px-0"-->
            <!--            v-else-->
            <!--            v-model="c.variation"-->
            <!--            placeholder="숫자만입력"-->
            <!--            :class="{ 'text-primary': c.variation < 0, 'text-danger': c.variation > 0 }"-->
            <!--            @change="checkVariationRangeGroup(i, c.variation, $event, c.product?.up_min, c.product?.up_max)" />-->
          </td>
        </tr>
        <tr class="text-center" v-if="cProductList.total === 0">
          <td colspan="10">검색 결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-footer-area" v-if="cProductList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChangeC" />
    </div>
    <div class="text-end">
      <button type="button" class="btn btn-sm btn-danger col-auto" @click.prevent="removeProdToCatalog">선택상품삭제</button>
    </div>
  </div>

  <!-- PA 선택 Modal -->
  <Modal :id="'paMemberSelModalC'" :title="'공급자(PA) 회원 선택'" :xlarge="true">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">공급자(PA) 회원을 선택합니다.</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <form class="mb-6">
              <div class="row align-items-center mb-2">
                <label class="col-md-2 col-form-label">회원타입</label>
                <div class="col form-control border-0">
                  <div class="row">
                    <div class="col-auto">
                      <input type="radio" id="radio_type_pa" class="form-check-input" name="search_class_type" value="PA" v-model="checkedTypes" />
                      <label class="form-check-label px-1" for="radio_type_pa">PA</label>
                    </div>
                    <div class="col-auto">
                      <input type="radio" id="radio_type_pa-s" class="form-check-input" name="search_class_type" value="PA-S" v-model="checkedTypes" />
                      <label class="form-check-label px-1" for="radio_type_pa-s">PA-S</label>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row col">
                <label class="col-md-2 col-form-label">회원검색</label>
                <div class="col-md-2">
                  <!-- Select -->
                  <div class="tom-select-custom">
                    <select class="form-select" v-model="selDetailSearch2.selectedItem" @change="onChangeDetailSearch2" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                      <option v-for="detail in selDetailSearch2.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
                    </select>
                  </div>
                  <!-- End Select -->
                </div>
                <div class="d-md-none mt-1"></div>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" id="q" v-model="selDetailSearch2.q" :placeholder="selDetailSearch2.placeholder" @keypress.enter.prevent="searchUser" />
                    <button type="button" class="btn btn-outline-dark col-md-2" @click.prevent="searchUser">검색</button>
                  </div>
                </div>
              </div>
            </form>
            <!-- Modal Search Form End -->

            <div class="row mb-2 align-items-center justify-content-between">
              <div class="col-auto"></div>
              <div class="col-auto">
                <PageLimitCustom v-if="user_limit" :limit="user_limit" @changeLimitData="userChangeLimitData" />
              </div>
            </div>

            <!-- Member List Table -->
            <div class="table-responsive">
              <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
                <thead class="thead-light">
                  <tr class="text-center">
                    <th>회원타입</th>
                    <th>사업자명</th>
                    <th>이름</th>
                    <th>아이디</th>
                    <th>휴대전화</th>
                    <th>선택</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="text-center" v-for="(user, i) in searchUserList.data" :key="user.id">
                    <td>{{ getUserClass(user.classes) }}</td>
                    <td>{{ user?.company?.name ? user?.company?.name : '사업자정보 없음' }}</td>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.mobile }}</td>
                    <td>
                      <button type="button" class="btn btn-sm btn-info" @click.prevent="setPaInfoC(user)">선택</button>
                    </td>
                  </tr>
                  <tr>
                    <td colspan="6" class="text-center" v-if="searchUserList.data.length === 0">표시할 항목이 없습니다.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- Member List Table End-->
          </div>
          <div class="table-footer-area" v-if="searchUserList.total > 0">
            <div class="row" v-if="user_total_page > 1">
              <Pagination :currentPage="user_page_no" :totalPages="user_total_page" :pageChange="user_pageChange" />
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <!-- 일괄 수정 Modal -->
  <Modal :id="'allVariationModal'" :title="'판매가 보정 일괄 설정'" :xlarge="false">
    <template #body>
      <div class="row">
        <div class="text-start mb-1">
          <p>
            현재 검색된
            <span class="text-danger bold">
              <b>총 {{ cProductList.total }}개</b>
            </span>
            상품에 대해 판매가 보정 수치를 일괄 설정합니다.
          </p>
        </div>

        <div class="text-start mb-4">
          <p>
            카탈로그에 담긴 모든 상품의 판매가 보정 수치가 <span class="text-danger"><b>모두 동일한 값</b></span> 으로 설정되니 유의해주세요.
          </p>
        </div>
        <div class="card">
          <div class="card-body">
            <div class="row col mb-2 align-items-center">
              <label class="col-md-4 col-form-label text-center">판매가 보정<br />({{ minMaxVariation.min }} 이상)</label>

              <div class="col">
                <div class="input-group">
                  <input type="number" class="form-control text-center col border-end-0" v-model="allVariation" @input="checkMaxValue($event)" />
                  <button type="button" class="btn btn-sm btn-danger" @click.prevent="reqAllVariation">수정</button>
                </div>
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
  <!-- 일괄 수정 Modal END -->

  <!-- 카테고리 선택-->
  <Modal :id="'SelCategoryModal'" :title="'카테고리 선택'">
    <template #body>
      <SelectCategoryModal @closeModal="closeCategoryModal" ref="CategoryModal" />
    </template>
  </Modal>

  <!-- 브랜드 선택-->
  <Modal :id="'SelBrandModal'" :title="'브랜드 선택'">
    <template #body>
      <SelectBrandModal @closeModal="closeBrandModal" />
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import Pagination from '@/components/comm/Pagination.vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useRoute, useRouter } from 'vue-router';
import type { CatalogProductList, Option as Opt } from 'CatalogProductModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import Modal from '@/components/comm/modal.vue';
import SelectCategoryModal from '@/components/modals/product/SelectCategoryModal.vue';
import SelectBrandModal from '@/components/modals/product/SelectBrandModal.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import type { Class, User } from 'UserInfoModule';

const catalogId = ref();
const cProductList = ref({} as CatalogProductList);
const cOriginList = ref({} as CatalogProductList);
const isChangeDate = ref(true);
// 선택 상품 리스트 (담은 상품)
const mSelProductList = ref([]);
const CategoryModal = ref();
const minMaxVariation = reactive({
  min: 0,
  max: 0,
});

const allVariation = ref(0);

const getMinMaxVariation = () => {
  let min = -999999999;
  let max = 999999999;
  if (cProductList.value.total > 0) {
    for (const c of cProductList.value.datas) {
      const defaultOpt = c.product.options.find(item => item.default_yn === 'Y' && item.status === 'Y');
      if (defaultOpt) {
        const tmpMin = defaultOpt.selling_price * -1;
        const tmpMax = defaultOpt.origin_price - defaultOpt.selling_price;
        if (max > tmpMax) {
          max = tmpMax;
        }
        if (min < tmpMin) {
          min = tmpMin;
        }
      } else {
        if (c.product.up_min && c.product.up_max) {
          if (max > c.product.up_max) {
            max = c.product.up_max;
          }
          if (min < c.product.up_min) {
            min = c.product.up_min;
          }
        }
      }
    }
  }
  minMaxVariation.max = max;
  minMaxVariation.min = min + 100;
};

const allCheck = ref(false);
const allCheckedClick = () => {
  if (allCheck.value) {
    //@ts-ignore
    mSelProductList.value = [...cProductList.value.datas];
  } else {
    mSelProductList.value = [];
  }
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(cProductList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getCatalogProdList();
};

const selDetailSearch = reactive({
  items: [
    { name: '상품명', value: 'name' },
    { name: '상품코드', value: 'code' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 상품 이름을 입력해주세요.',
  type: 'all',
  cateBrand: 'c',
  categoryId: 0,
  categoryLabel: '',
  brandId: 0,
  brandName: '',
  status: 'all',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'name':
      selDetailSearch.placeholder = '검색할 상품의 이름을 입력해주세요.';
      break;
    case 'code':
      selDetailSearch.placeholder = '검색할 상품의 코드를 입력해주세요.';
      break;
  }
};

const getPriceInfo = (opts: Opt[], type: string): string | number => {
  const defaultOpt = opts.find(item => item.default_yn === 'Y' && item.status === 'Y');
  if (defaultOpt) {
    switch (type) {
      case 'supply':
        return defaultOpt.supply_price.toLocaleString() + '원';
      case 'origin':
        return defaultOpt.origin_price.toLocaleString() + '원';
      case 'sell':
        return defaultOpt.selling_price.toLocaleString() + '원';
      default:
        return '-';
    }
  } else {
    return '-';
  }
};

const onChangeCateBrand = () => {
  selDetailSearch.categoryId = 0;
  selDetailSearch.categoryLabel = '';
  selDetailSearch.brandId = 0;
  selDetailSearch.brandName = '';
};

const clearSearchCondition = () => {
  setSearchPeriod('all');
  paInfo.id = 0;
  paInfo.name = '';
  paInfo.company = '';
  selDetailSearch.type = 'all';
  selDetailSearch.selectedItem = 'name';
  selDetailSearch.q = '';
  selDetailSearch.cateBrand = 'c';
  selDetailSearch.categoryId = 0;
  selDetailSearch.categoryLabel = '';
  selDetailSearch.brandId = 0;
  selDetailSearch.brandName = '';
  selDetailSearch.status = 'all';
  getCatalogProdList();
};
const openCategoryModal = () => {
  showModal('SelCategoryModal');
  CategoryModal.value.openModal();
};

const closeCategoryModal = (cateId: number, cateLabel: string) => {
  hideModal('SelCategoryModal');
  selDetailSearch.categoryId = cateId;
  selDetailSearch.categoryLabel = cateLabel;
};

const closeBrandModal = (brandId: number, brandName: string) => {
  hideModal('SelBrandModal');
  selDetailSearch.brandId = brandId;
  selDetailSearch.brandName = brandName;
};

const getCatalogProdList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  // PA 검색
  if (paInfo.name) {
    query = query.concat(query ? `&member_id=${paInfo.id}` : `member_id=${paInfo.id}`);
  }

  // 상품유형
  if (selDetailSearch.type !== 'all') {
    query = query.concat(query ? `&prd_type=${selDetailSearch.type}` : `prd_type=${selDetailSearch.type}`);
  }
  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }
  //검색기간
  if (searchDate.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchDate.sDate}` : `s_reg_date=${searchDate.sDate}`);
  }
  //검색기간
  if (searchDate.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchDate.eDate}` : `e_reg_date=${searchDate.eDate}`);
  }
  //카테고리 선택 체크
  if (selDetailSearch.categoryId) {
    query = query.concat(query ? `&category=${selDetailSearch.categoryId}&categoryLabel=${selDetailSearch.categoryLabel}` : `category=${selDetailSearch.categoryId}&categoryLabel=${selDetailSearch.categoryLabel}`);
  }
  //브랜드 선택 체크
  if (selDetailSearch.brandId) {
    query = query.concat(query ? `&cateBrand=${selDetailSearch.cateBrand}` : `cateBrand=${selDetailSearch.cateBrand}`);
    query = query.concat(query ? `&brand=${selDetailSearch.brandId}&brandName=${selDetailSearch.brandName}` : `brand=${selDetailSearch.brandId}&brandName=${selDetailSearch.brandName}`);
  }

  if (selDetailSearch.status !== 'all') {
    query = query.concat(query ? `&status=${selDetailSearch.status}` : `status=${selDetailSearch.status}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.catalog.get_catalog_prod(query, catalogId.value, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      allCheck.value = false;
      if (res.total) {
        cProductList.value.datas = res.datas;
        cProductList.value.total = res.total;
        cOriginList.value.datas = JSON.parse(JSON.stringify(res.datas));
        getMinMaxVariation();
      } else {
        cProductList.value.datas = [];
        cProductList.value.total = 0;
        cOriginList.value.datas = [];
        minMaxVariation.max = 0;
        minMaxVariation.min = 0;
      }
    });
  });
};

const removeProdToCatalog = () => {
  if (mSelProductList.value.length === 0) {
    showAlert('선택한 상품이 없습니다.', 'warning');
    return;
  }

  //@ts-ignore
  const arrProdId: number[] = [];
  // @ts-ignore
  mSelProductList.value.map(item => arrProdId.push(item.product.id));
  showConfirm('선택한 상품을 카탈로그에서 삭제하시겠습니까?', () => {
    apis.catalog.delete_prod_to_catalog(catalogId.value, arrProdId).then(res => {
      apiResponseCheck(res, () => {
        showAlert('카탈로그에서 삭제되었습니다.', 'success');
        // page_no.value = 1;
        mSelProductList.value = [];
        page_no.value > 1 ? getCatalogProdList(false) : getCatalogProdList();
        // window.location.reload();
      });
    });
  });
};

const pageChangeC = (page: number) => {
  page_no.value = page;
  getCatalogProdList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const searchDate = reactive({
  sDate: '',
  eDate: '',
});
const setSearchPeriod = (period: string) => {
  isChangeDate.value = false;
  const today = new Date();
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInput'), {});
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});
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
      searchDate.sDate = '';
      searchDate.eDate = '';
      break;
  }
  isChangeDate.value = true;
};
const sDateChange = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInput'), {});

  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

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
const eDateChange = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});

  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

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

const checkVariationRange = (idx: number, value: number, opts: Opt[], event: any) => {
  const defaultOpt = opts.find(item => item.default_yn === 'Y' && item.status === 'Y');
  if (defaultOpt) {
    const max = defaultOpt.origin_price - defaultOpt.selling_price;
    const min = defaultOpt.selling_price * -1 + 100;

    // TODO: 2023. 11. 07. 보정수치 상한선 제거
    // if (value > max) {
    //   showAlert(`${max} 보다 작거나 같은값을 입력해주세요.`, 'warning');
    //   event.target.focus();
    //   return;
    // }

    if (value < min) {
      showAlert(`${min} 이상의 값을 입력해주세요.`, 'warning', () => {
        event.target.focus();
      });
      return;
    }

    if (!event.target.value) {
      showAlert(`숫자를 입력해주세요.`, 'warning', () => {
        event.target.focus();
      });
      return;
    }

    showConfirm('판매가 보정 수치를 수정하시겠습니까?', () => {
      const pIds = [];
      pIds.push(cProductList.value.datas[idx].product.id);
      apis.catalog.mod_catalog_prod_variation(catalogId.value, parseInt(event.target.value), pIds).then(res => {
        apiResponseCheck(res, () => {
          showAlert('판매가 보정 수치가 변경되었습니다.', 'success');
        });
      });
    });
  } else {
    showAlert(`상품에 대한 옵션 설정이 올바르지 않습니다. 해당 상품의 옵션정보를 확인해주세요.`, 'warning');
    return;
  }
};

const checkMaxValue = (event: any) => {
  const n: number = parseInt(event.target.value);
  if (n < minMaxVariation.min) {
    showAlert(`${minMaxVariation.min} 이상의 값을 입력해주세요.`, 'warning', () => {
      event.target.focus();
    });
    event.target.value = minMaxVariation.min;
    allVariation.value = minMaxVariation.min;
  }
};

const reqAllVariation = () => {
  showConfirm('판매가 보정 수치를 일괄 수정 하시겠습니까?', () => {
    apis.catalog.mod_all_catalog_variation(catalogId.value, allVariation.value).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('판매가 보정 수치가 일괄 적용되었습니다.', 'success');
          getCatalogProdList();
          hideModal('allVariationModal');
        },
        (num?: number) => {
          if (num === 403) {
            hideModal('allVariationModal');
          }
        },
      );
    });
  });
};

const setModalListener = () => {
  //@ts-ignore
  document.getElementById('allVariationModal').addEventListener('show.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('allVariationModal').addEventListener('hide.bs.modal', function (event) {
    allVariation.value = 0;
  });
};

const refreshCatalogProdList = () => {
  page_no.value > 1 ? getCatalogProdList(false) : getCatalogProdList();
};

// PA 검색 관련 START
const paInfo = reactive({
  id: 0,
  name: '',
  company: '',
  noPa: true,
});

const searchUserList = ref({
  data: {} as User[],
  total: 0,
});
const checkedTypes = ref('PA');
const user_page_no = ref(1);
const user_offset = computed(() => (user_page_no.value - 1) * user_limit.value);
const user_limit = ref(10);
const user_total_page = computed(() => Math.ceil(searchUserList.value.total / user_limit.value));

const openPaSelModal = () => {
  user_limit.value = useCommonStore().getLimit;
  // searchUser();
  showModal('paMemberSelModalC');
};
const setPaInfoC = (user: User) => {
  const paCompany = user?.company?.name ? user?.company?.name : '없음';
  paInfo.id = user.id;
  paInfo.name = `${user.name} ( 업체명 : ${paCompany} )`;
  paInfo.company = user.company.name;
  hideModal('paMemberSelModalC');
};

const selDetailSearch2 = reactive({
  items: [
    { name: '이름', value: 'name' },
    { name: '아이디', value: 'user_id' },
    { name: '전화번호', value: 'mobile' },
    { name: '회사명', value: 'company_name' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 회원의 이름을 입력해주세요.',
});

const onChangeDetailSearch2 = () => {
  switch (selDetailSearch2.selectedItem) {
    case 'name':
      selDetailSearch2.placeholder = '검색할 회원의 이름을 입력해주세요.';
      break;
    case 'user_id':
      selDetailSearch2.placeholder = '검색할 회원의 아이디(이메일)을 입력해주세요.';
      break;
    case 'mobile':
      selDetailSearch2.placeholder = "검색할 회원의 전화번호를 입력해주세요. ('-' 제외)";
      break;
    case 'company_name':
      selDetailSearch2.placeholder = '검색할 회원의 회사명을 입력해주세요.';
      break;
  }
};

const searchUser = (reset: boolean = true) => {
  if (reset) {
    user_page_no.value = 1;
  }

  let query = `class_code=${checkedTypes.value}&`;
  // 세부검색어 체크
  if (selDetailSearch2.q) {
    const detail = `${selDetailSearch2.selectedItem}=${selDetailSearch2.q}`;
    if (query) {
      query = query.concat(`${detail}&`);
    } else {
      query = query.concat(`${detail}&`);
    }
  }

  apis.user.get_list(query, user_offset.value, user_limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      searchUserList.value.data = res.datas;
      searchUserList.value.total = res.total;
    });
  });
};

const userChangeLimitData = (setLimitNum: number) => {
  user_page_no.value = 1;
  user_limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  searchUser();
};

const getUserClass = (classes: Class[]): string => {
  const types = [];
  if (classes) {
    for (const c of classes) {
      types.push(c.class_code);
    }
  }
  return types.length == 0 ? '-' : types.join(',');
};

const user_pageChange = (page: number) => {
  user_page_no.value = page;
  searchUser(false);
};
// PA 검색 관련 END

onMounted(() => {
  catalogId.value = history.state.id;
  limit.value = useCommonStore().getLimit;
  if (catalogId.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }
  setModalListener();
  setSearchPeriod('all');

  page_no.value > 1 ? getCatalogProdList(false) : getCatalogProdList();
});

defineExpose({ refreshCatalogProdList });
</script>

<style scoped></style>
