<template>
  <div>
    <PageNavigator :before_link="[]" :current="'상품조회 및 수정'" />
    <div class="card">
      <div class="card-header py-2">
        <div class="row align-items-center justify-content-between">
          <div class="col-auto">
            <div class="form-control-borderless h2 mb-0">상품조회 및 수정</div>
          </div>
          <div class="col-auto">
            <div class="text-end">
              <button
                type="button"
                class="btn btn-info"
                @click.prevent="
                  useSearchStore().$reset();
                  router.push(`/product/reg`);
                "
                style="float: right"
                v-if="getUserClassStr.includes('CM') || getUserClassStr.includes('PA')">
                상품등록
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="card-body">
        <div class="row mb-2 align-items-center">
          <label for="idLabel" class="col-md-1 col-form-label">공급자(PA)</label>
          <div class="col-md-4">
            <div class="input-group">
              <input type="text" class="form-control" v-model="paInfo.name" placeholder="공급자(PA)를 선택해주세요." aria-label="" disabled />
              <button type="button" class="btn btn-outline-secondary" @click.prevent="openPaSelModal" v-if="paInfo.noPa">검색</button>
            </div>
          </div>
        </div>
        <!-- 상품상태 -->
        <div class="row align-items-center">
          <div class="col-md-1 col-form-label">상품상태</div>
          <div class="col">
            <div class="row form-control border-0">
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="search_p_status_all" class="form-check-input" name="search_p_status" v-model="selDetailSearch.status" value="all" />
                <label class="form-check-label px-1" for="search_p_status_all">전체</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="search_p_status_y" class="form-check-input" name="search_p_status" v-model="selDetailSearch.status" value="Y" />
                <label class="form-check-label px-1" for="search_p_status_y">정상</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="search_p_status_p" class="form-check-input" name="search_p_status" v-model="selDetailSearch.status" value="P" />
                <label class="form-check-label px-1" for="search_p_status_p">판매종료</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="search_p_status_s" class="form-check-input" name="search_p_status" v-model="selDetailSearch.status" value="S" />
                <label class="form-check-label px-1" for="search_p_status_s">품절</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="search_p_status_n" class="form-check-input" name="search_p_status" v-model="selDetailSearch.status" value="N" />
                <label class="form-check-label px-1" for="search_p_status_n">미승인</label>
              </div>
            </div>
          </div>
        </div>
        <!-- 노출여부 -->
        <div class="row align-items-center">
          <div class="col-md-1 col-form-label">노출여부</div>
          <div class="col">
            <div class="row form-control border-0">
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="search_p_view_yn_all" class="form-check-input" name="search_p_view_yn" v-model="selDetailSearch.view_yn" value="all" />
                <label class="form-check-label px-1" for="search_p_view_yn_all">전체</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="search_p_view_yn_y" class="form-check-input" name="search_p_view_yn" v-model="selDetailSearch.view_yn" value="Y" />
                <label class="form-check-label px-1" for="search_p_view_yn_y">노출</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="search_p_view_yn_n" class="form-check-input" name="search_p_view_yn" v-model="selDetailSearch.view_yn" value="N" />
                <label class="form-check-label px-1" for="search_p_view_yn_n">비노출</label>
              </div>
            </div>
          </div>
        </div>
        <!-- 상품유형 radio -->
        <div class="row align-items-center">
          <div class="col-md-1 col-form-label">상품유형</div>
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
        <!-- 결제수단제한 radio -->
        <div class="row align-items-center" v-if="getUserClassStr.includes('CM')">
          <div class="col-md-1 col-form-label">결제수단제한</div>
          <div class="col">
            <div class="row form-control border-0">
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="radio_prod_pg_provider_all" class="form-check-input" name="prod_pg_provider" value="all" v-model="selDetailSearch.pg_provider" />
                <label class="form-check-label px-1" for="radio_prod_pg_provider_all">전체</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="radio_prod_pg_provider_payco" class="form-check-input" name="prod_pg_provider" value="PAYCO" v-model="selDetailSearch.pg_provider" />
                <label class="form-check-label px-1" for="radio_prod_pg_provider_payco">PAYCO</label>
              </div>
            </div>
          </div>
        </div>
        <!-- 검색기간 Datepicker -->
        <div class="row align-items-center">
          <label for="idLabel" class="col-md-1 col-form-label">검색기간<br />(상품등록일)</label>
          <div class="col">
            <div class="row">
              <div class="col-lg-3">
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
              <div class="col-lg-3">
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
              <div class="d-lg-none mt-2"></div>
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
        <div class="row mb-2 align-items-center">
          <label class="col-md-1 col-form-label">카테고리/브랜드</label>
          <div class="col-lg-2">
            <!-- Select -->
            <div class="tom-select-custom">
              <select class="form-select" v-model="selDetailSearch.cateBrand" @change="onChangeCateBrand" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                <option v-text="'카테고리'" value="c"></option>
                <option v-text="'브랜드'" value="b"></option>
              </select>
            </div>
            <!-- End Select -->
          </div>
          <div class="d-lg-none mt-1"></div>
          <div class="col-lg-4">
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
        <div class="row align-items-center">
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
              <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getProducts" />
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer py-2">
        <div class="text-end">
          <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="getProducts">검색</button>
        </div>
      </div>
    </div>

    <span class="divider-center py-4">검색결과</span>
    <div class="row mb-2 align-items-center justify-content-between">
      <div class="col-auto">
        <span v-if="mProductList.total > 0">총 : {{ mProductList.total }}개</span>
        <div class="col-auto align-items-center mt-2" style="font-size: 0.7rem">
          <span class="badge" :style="{ 'background-color': `#9b00ff !important` }">배</span>
          <span class="ms-1 me-2">배송상품</span>
          <span class="badge" :style="{ 'background-color': `#ff6b00 !important` }">티</span>
          <span class="ms-1 me-2">티켓상품</span>
          <span class="badge text-bg-success">E</span>
          <span class="ms-1">E-쿠폰</span>
        </div>
      </div>
      <div class="col-auto">
        <div class="row align-items-center">
          <div class="col-auto" v-if="getUserClassStr.includes('CM')">
            <select class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' v-model="cStatus" @change="selChangeStatus">
              <option value="" disabled>선택상품 일괄상태변경</option>
              <option value="Y">정상</option>
              <option value="P">판매중지</option>
              <option value="S">품절</option>
              <option value="N">미승인</option>
            </select>
          </div>
          <div class="col-auto" v-if="mProductList.datas?.length > 0">
            <button type="button" class="btn btn-sm btn-warning" @click.prevent="downExcel">현재페이지 상품목록 엑셀다운로드</button>
          </div>
          <div class="col-auto">
            <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
          </div>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="table-responsive datatable-custom position-relative">
        <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
          <thead class="thead-light">
            <tr class="text-center">
              <th v-if="getUserClassStr.includes('CM')">
                <input type="checkbox" class="form-check-input" name="cb_add_product" id="cb_p_all" v-model="allCheck" @change="allCheckedClick" />
              </th>
              <th style="width: 5%">상품유형</th>
              <th style="width: 10%">상품코드</th>
              <th style="width: 5%">이미지</th>
              <th>상품명</th>
              <th style="width: 5%">공급자(PA)</th>
              <th>공급가</th>
              <th>정상가</th>
              <th>판매가</th>
              <th v-if="getUserClassStr.includes('CM')">결제수단제한</th>
              <th style="width: 10%">등록일/수정일</th>
              <th style="width: 5%">상태</th>
              <th style="width: 5%">노출</th>
              <th v-if="!getUserClassStr.includes('MC')" style="width: 5%">관리</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="item in mProductList.datas" :key="item.id">
              <td v-if="getUserClassStr.includes('CM')">
                <input type="checkbox" class="form-check-input" name="cb_add_product" v-bind:id="`cb_p_${item.code}`" :value="item" v-model="mSelProductList" />
              </td>
              <td>
                <div v-if="item?.type.startsWith('DP')">
                  <span class="badge" :style="{ 'background-color': `#9b00ff !important` }">배</span>
                </div>
                <div v-else-if="item?.type === 'UP-OF'">
                  <span class="badge" :style="{ 'background-color': `#ff6b00 !important` }">티</span>
                </div>
                <div v-else-if="item?.type === 'UP-EC'">
                  <span class="badge text-bg-success">E</span>
                </div>
              </td>
              <td style="font-size: 0.7rem">{{ item?.code }}</td>
              <td>
                <div class="avatar" v-if="item.photos.length > 0">
                  <img class="avatar-img" :src="item.photos[0].uri" alt="Image Description" />
                </div>
                <div class="avatar" v-if="item.photos.length === 0">
                  <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
                </div>
              </td>
              <td class="text-wrap">
                <span class="d-block h5 mb-0">{{ item.name }}</span>
              </td>
              <td>
                <span class="d-block h5 mb-0">{{ item.member.company?.name }}</span>
              </td>
              <td class="text-end">{{ getPriceInfo(JSON.parse(JSON.stringify(item.options)), 'supply') }}</td>
              <td class="text-end">{{ getPriceInfo(JSON.parse(JSON.stringify(item.options)), 'origin') }}</td>
              <td class="text-end">{{ getPriceInfo(JSON.parse(JSON.stringify(item.options)), 'sell') }}</td>
              <td v-if="getUserClassStr.includes('CM')">{{ item.pg_provider ? `${item.pg_provider}` : '없음' }}</td>
              <td>{{ dateTimeFormatConverter(item.reg_date) }}<br />{{ dateTimeFormatConverter(item.mod_date) }}</td>
              <td>{{ item.status === 'Y' ? '정상' : item.status === 'P' ? '판매중지' : item.status === 'S' ? '품절' : '미승인' }}</td>
              <td>{{ item.view_yn === 'Y' ? '노출' : '비노출' }}</td>
              <td v-if="!getUserClassStr.includes('MC')">
                <!-- TODO: MC가 상품 목록을 검색 시 상품 요청 신청?? -->
                <button type="button" @click.prevent="router.push({ path: `/product/detail`, state: { id: item.id } })" class="btn btn-white btn-sm">수정</button>
              </td>
            </tr>
            <tr>
              <td colspan="12" class="text-center" v-if="mProductList?.datas?.length === 0">표시할 항목이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="table-footer-area" v-if="mProductList.total > 0">
        <div class="row" v-if="total_page > 1">
          <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
        </div>
      </div>
    </div>
  </div>

  <!-- PA 선택 Modal -->
  <Modal :id="'paMemberSelModal'" :title="'공급자(PA) 회원 선택'" :xlarge="true">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">공급자(PA) 회원을 선택합니다.</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <form class="mb-6">
              <div class="row align-items-center mb-2">
                <label class="col-md-2 col-form-label">회원타입</label>
                <div class="col">
                  <div class="row form-control border-0">
                    <div class="col-auto form-check form-check-inline">
                      <input type="radio" id="radio_type_pa" class="form-check-input" name="search_class_type" value="PA" v-model="checkedTypes" />
                      <label class="form-check-label px-1" for="radio_type_pa">PA</label>
                    </div>
                    <div class="col-auto form-check form-check-inline">
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

            <div class="table-responsive">
              <!-- Member List Table -->
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
                      <button type="button" class="btn btn-sm btn-info" @click.prevent="setPaInfo(user)">선택</button>
                    </td>
                  </tr>
                  <tr>
                    <td colspan="6" class="text-center" v-if="searchUserList.data.length === 0">표시할 항목이 없습니다.</td>
                  </tr>
                </tbody>
              </table>
              <!-- Member List Table End-->
            </div>
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

<script lang="ts" setup>
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import apis from '@/apis';
import type { ProductListInfo } from 'ProductListInfoModule';
import Pagination from '@/components/comm/Pagination.vue';
import type { Class, User } from 'UserInfoModule';
import Modal from '@/components/comm/modal.vue';
import { useUserStore } from '@/stores/user';
import { apiResponseCheck, dateTimeFormatConverter, showAlert, getUserClassStr, showLogConsole, showModal, hideModal, showConfirm } from '@/utils/common-utils';
import type { Option as Opt } from 'CatalogProductModule';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useSearchStore } from '@/stores/search';
import { useCommonStore } from '@/stores/common';
import SelectCategoryModal from '@/components/modals/product/SelectCategoryModal.vue';
import SelectBrandModal from '@/components/modals/product/SelectBrandModal.vue';
import * as XLSX from 'xlsx';

const router = useRouter();
const route = useRoute();
const isChangeDate = ref(true);
const mProductList = ref({} as ProductListInfo);
const checkedTypes = ref('PA');
const CategoryModal = ref();
const getPriceInfo = (opts: Opt[], type: string): string | number => {
  const defaultOpt = opts.find(item => item.default_yn === 'Y' && item.status === 'Y');
  if (defaultOpt) {
    switch (type) {
      case 'supply':
        return `${defaultOpt.supply_price.toLocaleString()}원`;
      case 'origin':
        return `${defaultOpt.origin_price.toLocaleString()}원`;
      case 'sell':
        return `${defaultOpt.selling_price.toLocaleString()}원`;
      default:
        return '-';
    }
  } else {
    return '설정필요';
  }
};

// 상품 목록 페이지네이션
const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mProductList.value.total / limit.value));
const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getProducts();
};

// PA 회원 목록 페이지네이션
const user_page_no = ref(1);
const user_offset = computed(() => (user_page_no.value - 1) * user_limit.value);
const user_limit = ref(10);
const user_total_page = computed(() => Math.ceil(searchUserList.value.total / user_limit.value));
const userChangeLimitData = (setLimitNum: number) => {
  user_page_no.value = 1;
  user_limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  searchUser();
};

const searchDate = reactive({
  sDate: '',
  eDate: '',
});

const selDetailSearch = reactive({
  status: 'all',
  type: 'all',
  view_yn: 'all',
  items: [
    { name: '상품명', value: 'name' },
    { name: '상품코드', value: 'code' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 상품의 이름을 입력해주세요.',
  cateBrand: 'c',
  categoryId: 0,
  categoryLabel: '',
  brandId: 0,
  brandName: '',
  pg_provider: 'all',
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

const onChangeCateBrand = () => {
  selDetailSearch.categoryId = 0;
  selDetailSearch.categoryLabel = '';
  selDetailSearch.brandId = 0;
  selDetailSearch.brandName = '';
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

const openPaSelModal = () => {
  user_limit.value = useCommonStore().getLimit;
  // searchUser();
  showModal('paMemberSelModal');
};
const setPaInfo = (user: User) => {
  const paCompany = user?.company?.name ? user?.company?.name : '없음';
  paInfo.id = user.id;
  paInfo.name = `${user.name} ( 업체명 : ${paCompany} )`;
  hideModal('paMemberSelModal');
};

const getProducts = (reset: boolean = true) => {
  mSelProductList.value = [];
  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  if (paInfo.name) {
    query = query.concat(`member_id=${paInfo.id}&member_name=${paInfo.name}`);
  }

  if (selDetailSearch.status !== 'all') {
    query = query.concat(query ? `&status=${selDetailSearch.status}` : `status=${selDetailSearch.status}`);
  }

  if (selDetailSearch.view_yn !== 'all') {
    query = query.concat(query ? `&view_yn=${selDetailSearch.view_yn}` : `view_yn=${selDetailSearch.view_yn}`);
  }

  if (selDetailSearch.type !== 'all') {
    query = query.concat(query ? `&prd_type=${selDetailSearch.type}` : `prd_type=${selDetailSearch.type}`);
  }

  if (selDetailSearch.pg_provider !== 'all') {
    query = query.concat(query ? `&pg_provider=${selDetailSearch.pg_provider}` : `pg_provider=${selDetailSearch.pg_provider}`);
  }

  //검색기간
  if (searchDate.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchDate.sDate}` : `s_reg_date=${searchDate.sDate}`);
  }
  //검색기간
  if (searchDate.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchDate.eDate}` : `e_reg_date=${searchDate.eDate}`);
  }

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
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

  if (query) {
    query = query.concat('&');
  }
  setSearchInfo(query);

  apis.product.getProducts(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      allCheck.value = false;
      mProductList.value.total = res.total;
      mProductList.value.datas = res.datas;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getProducts(false);
  window.scrollTo({ top: 100, left: 0 });
};

const user_pageChange = (page: number) => {
  user_page_no.value = page;
  searchUser(false);
};

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

const searchUserList = ref({
  data: {} as User[],
  total: 0,
});

const getUserClass = (classes: Class[]): string => {
  const types = [];
  if (classes) {
    for (const c of classes) {
      types.push(c.class_code);
    }
  }
  return types.length == 0 ? '-' : types.join(',');
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
const user = useUserStore().user;
const userName = computed(() => {
  return `${useUserStore().user.name}`;
});
const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

const paInfo = reactive({
  id: 0,
  name: '',
  noPa: true,
});

const clearSearchCondition = () => {
  if (userClass.value.includes('PA')) {
    //@ts-ignore
    paInfo.id = parseInt(user.id.toString());
    paInfo.name = userName.value;
    paInfo.noPa = false;
  } else {
    paInfo.id = 0;
    paInfo.name = '';
    paInfo.noPa = true;
  }

  setSearchPeriod('all');
  selDetailSearch.selectedItem = 'name';
  selDetailSearch.q = '';
  selDetailSearch.status = 'all';
  selDetailSearch.view_yn = 'all';
  selDetailSearch.type = 'all';
  selDetailSearch.cateBrand = 'c';
  selDetailSearch.categoryId = 0;
  selDetailSearch.categoryLabel = '';
  selDetailSearch.brandId = 0;
  selDetailSearch.brandName = '';
  selDetailSearch.pg_provider = 'all';
  onChangeDetailSearch();
  getProducts();
};

const searchInfo = ref('');
const setSearchInfo = (query: string) => {
  searchInfo.value = `${query}page_no=${page_no.value}`;
  useSearchStore().setSearchInfo(searchInfo.value);
};

const getSearchInfo = () => {
  if (useSearchStore().getSearchInfo) {
    const paramsArray = JSON.parse(JSON.stringify(useSearchStore().getSearchInfo)).split('&');

    for (const param of paramsArray) {
      const [key, value] = param.split('=');

      switch (key) {
        case 's_reg_date':
          searchDate.sDate = value;
          break;
        case 'e_reg_date':
          searchDate.eDate = value;
          break;
        case 'page_no':
          page_no.value = parseInt(value);
          break;
        case 'status':
          selDetailSearch.status = value;
          break;
        case 'prd_type':
          selDetailSearch.type = value;
          break;
        case 'view_yn':
          selDetailSearch.view_yn = value;
          break;
        case 'name':
        case 'code':
          selDetailSearch.selectedItem = key;
          selDetailSearch.q = value;
          break;
        case 'member_id':
          paInfo.id = value;
          break;
        case 'member_name':
          paInfo.name = value;
          break;
        case 'cateBrand':
          selDetailSearch.cateBrand = value;
          break;
        case 'category':
          selDetailSearch.categoryId = value;
          break;
        case 'categoryLabel':
          selDetailSearch.categoryLabel = value;
          break;
        case 'brand':
          selDetailSearch.brandId = value;
          break;
        case 'brandName':
          selDetailSearch.brandName = value;
          break;
        default:
          break;
      }
    }
  }
};

const downExcel = () => {
  showConfirm(`현재 보여지는 ${limit.value}개의 상품목록을 엑셀다운로드 하시겠습니까?`, () => {
    // 엑셀 파일 생성
    const book = XLSX.utils.book_new();
    const today = dateTimeFormatConverter(new Date());

    // 엑셀 데이터 생성
    const prodList = makeExcelData();

    prodList.unshift([]);
    prodList.unshift([]);
    prodList.unshift(['액셀 생성 날짜', today]);

    // sheet 생성 - aoa_to_sheet 장식으로
    const worksheetByAoa = XLSX.utils.aoa_to_sheet(prodList);

    // 엑셀 파일에 sheet set (엑셀파일, 시트 데이터, 시트명)
    XLSX.utils.book_append_sheet(book, worksheetByAoa, `상품목록`);

    // 엑셀 다운로드
    XLSX.writeFile(book, `상품목록 - ${today}.xlsx`);
  });
};

const makeExcelData = (): any[] => {
  const list = [] as any[];

  list.push(['상품유형', '상품코드', '상품명', '공급자(PA)', '공급가', '정상가', '판매가', '등록일/수정일', '상태', '노출여부']);

  for (const p of mProductList.value.datas) {
    const data = [] as any[];
    data.push(p.type.startsWith('DP') ? '배송상품' : p.type === 'UP-OF' ? '티켓상품' : p.type === 'UP-EC' ? 'E-쿠폰' : '-');
    data.push(p.code);
    data.push(p.name);
    data.push(p.member.company.name ? p.member.company.name : '정보없음');
    data.push(getPriceInfo(JSON.parse(JSON.stringify(p.options)), 'supply'));
    data.push(getPriceInfo(JSON.parse(JSON.stringify(p.options)), 'origin'));
    data.push(getPriceInfo(JSON.parse(JSON.stringify(p.options)), 'sell'));
    data.push(`${dateTimeFormatConverter(p.reg_date)}  /  ${dateTimeFormatConverter(p.mod_date)}`);
    data.push(p.status === 'Y' ? '정상' : p.status === 'P' ? '판매중지' : p.status === 'S' ? '품절' : '미승인');
    data.push(p.view_yn === 'Y' ? '노출' : '비노출');
    list.push(data);
  }

  return list;
};

const cStatus = ref('');
const mSelProductList = ref([]);
const allCheck = ref(false);
const allCheckedClick = () => {
  if (allCheck.value) {
    //@ts-ignore
    mSelProductList.value = [...mProductList.value.datas];
  } else {
    mSelProductList.value = [];
  }
};

const selChangeStatus = () => {
  if (!cStatus.value) {
    return;
  }

  const statusStr = cStatus.value === 'Y' ? '정상' : cStatus.value === 'P' ? '판매중지' : cStatus.value === 'S' ? '품절' : cStatus.value === 'N' ? '미승인' : '';
  if (mSelProductList.value.length === 0) {
    showAlert('선택된 상품이 없습니다.', 'warning', () => {
      cStatus.value = '';
    });
    return;
  } else {
    showConfirm(
      `선택한 상품들을 [${statusStr}] 상태로 일괄변경 하시겠습니까?`,
      () => {
        const list = [];
        mSelProductList.value.map(item => list.push(item.id));
        apis.product.update_status(cStatus.value, list).then(res => {
          apiResponseCheck(
            res,
            () => {
              if (res?.fail_list?.length > 0) {
                let fail = makeFailList(res.fail_list);
                showAlert(`상품상태 일괄변경이 완료되었습니다.<br/>변경 성공건수 : ${res?.success_count}건<br />실패내역은 아래 표와 같습니다.<br /><br />${fail}`, 'warning', () => {
                  getProducts(false);
                  cStatus.value = '';
                });
              } else {
                showAlert(`상품상태 일괄변경이 완료되었습니다.<br/>변경 성공건수 : ${res?.success_count}건`, 'success', () => {
                  getProducts(false);
                  cStatus.value = '';
                });
              }
            },
            () => {
              cStatus.value = '';
            },
          );
        });
      },
      () => {
        cStatus.value = '';
      },
    );
  }
};

const makeFailList = (list: []): string => {
  let fail = `<div class='' style="max-height: 300px; overflow-y: scroll"><table class="table table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th>상품코드</th>
          <th>사유</th>
        </tr>
      </thead>
      <tbody>`;
  for (const f of list) {
    if ((f as []).length > 1) {
      fail = fail.concat(`<tr class="text-center">
          <td>${getProdCode(f[0])}</td>
          <td>${f[1]}</td></tr>`);
    }
  }

  fail = fail.concat(`</tbody></table></div> `);
  return fail;
};

const getProdCode = (id: number): string => {
  let data = mSelProductList.value.filter(item => item.id == id)[0];
  return data?.code;
};

onMounted(() => {
  limit.value = useCommonStore().getLimit;
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
  setSearchPeriod('all');

  if (userClass.value.includes('PA')) {
    //@ts-ignore
    paInfo.id = parseInt(user.id.toString());
    paInfo.name = userName.value;
    paInfo.noPa = false;
  } else {
    paInfo.id = 0;
    paInfo.name = '';
    paInfo.noPa = true;
  }
  getSearchInfo();
  page_no.value > 1 ? getProducts(false) : getProducts();
});
</script>

<style scoped></style>
