<template>
  <div class="card mb-4">
    <div class="card-header pb-1 align-middle">
      <div class="row">
        <div class="form-control-borderless col h2 m-auto">상품요청관리</div>
      </div>
    </div>
    <div class="card-body py-2">
      <!-- 날짜 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-1 col-form-label">검색어</label>
        <div class="col">
          <div class="row">
            <div class="col-2">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option value="all">전체</option>
                  <option value="paid_date">결제일</option>
                  <option value="shipping_date">발송일</option>
                  <option value="shipped_date">배송완료일</option>
                  <option value="confirmed_date">구매확정일</option>
                  <option value="return_date">반품요청일</option>
                  <option value="exchange_date">교환요청일</option>
                  <option value="refund_date">반품요청일</option>
                </select>
              </div>
              <!-- End Select -->
            </div>
            <div class="col-xl-4 col">
              <input type="text" class="form-control" />
            </div>
          </div>
        </div>
      </div>
      <div class="row mb-2">
        <label for="" class="col-1 col-form-label">카테고리</label>
        <div class="col-xl-4 col">
          <input class="form-control" />
        </div>
      </div>
      <div class="row mb-2">
        <label for="" class="col-1 col-form-label">브랜드</label>
        <div class="col-xl-4 col">
          <input class="form-control" />
        </div>
      </div>
      <!-- 날짜 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-1 col-form-label">날짜</label>
        <div class="col">
          <div class="row">
            <div class="col-2">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option value="all">전체</option>
                  <option value="paid_date">결제일</option>
                  <option value="shipping_date">발송일</option>
                  <option value="shipped_date">배송완료일</option>
                  <option value="confirmed_date">구매확정일</option>
                  <option value="return_date">반품요청일</option>
                  <option value="exchange_date">교환요청일</option>
                  <option value="refund_date">반품요청일</option>
                </select>
              </div>
              <!-- End Select -->
            </div>
            <div class="col-2">
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." data-input />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">-</span>
            <div class="col-2">
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." data-input />
                </div>
              </div>
            </div>
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1">오늘</button>
              <button type="button" class="btn btn-outline-info me-1">일주일</button>
              <button type="button" class="btn btn-outline-info me-1">1개월</button>
              <button type="button" class="btn btn-outline-info me-1">3개월</button>
              <button type="button" class="btn btn-outline-info me-1">6개월</button>
              <button type="button" class="btn btn-outline-info">전체</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-center">
        <button type="button" class="btn btn-sm btn-secondary">검색</button>
        <button type="button" class="btn btn-sm ms-3 btn-outline-secondary">초기화</button>
      </div>
    </div>
  </div>
  <div class="row py-2">
    <div class="col">
      <button type="button" class="btn btn-sm btn-secondary">선택 상품 요청</button>
    </div>
  </div>
  <table class="table table-nowrap table-align-middle card-table">
    <thead class="thead-light">
      <tr>
        <th class="table-column-pe-0">
          <div class="form-check">
            <input id="datatableCheckAll" class="form-check-input" type="checkbox" value="" />
            <label class="form-check-label" for="datatableCheckAll"></label>
          </div>
        </th>
        <th>상품코드</th>
        <th>이미지</th>
        <th>상품명</th>
        <th>공급가</th>
        <th>정상가</th>
        <th>판매가</th>
      </tr>
    </thead>
    <tbody>
      <!-- 회원 검색 결과 목록 테이블 -->
      <!-- TODO: 테이블 데이터 표시 및 검색결과 없을때 표시처리 -->
      <!-- TODO: ex) 1개의 row로 겸색 결과가 없습니다. 문구 표시-->
      <!-- -->

      <tr>
        <td class="table-column-pe-0">
          <div class="form-check">
            <input id="datatableCheckAll1" class="form-check-input" type="checkbox" value="" />
            <label class="form-check-label" for="datatableCheckAll1"></label>
          </div>
        </td>
        <td>상품코드</td>
        <td>
          <div class="avatar">
            <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
          </div>
        </td>
        <td>
          <span class="d-block h5 mb-0">상품명</span>
        </td>
        <td>공급가</td>
        <td>정상가</td>
        <td>판매가</td>
      </tr>
    </tbody>
  </table>
  <!-- Pagination -->
  <div class="d-flex justify-content-center justify-content-sm-end">
    <nav id="datatableWithPaginationPagination" aria-label="Activity pagination"></nav>
  </div>
  <!-- 카탈로그 생성 Modal -->
  <!-- TODO: 회원연결관리 관련 데이터 작업 해야함. -->
  <Modal :id="'makeCatalogueModal'" :title="'카탈로그 추가 예정상품'" :xlarge="true">
    <template #body>
      <table class="table table-nowrap table-align-middle card-table">
        <thead class="thead-light">
          <tr>
            <th class="table-column-pe-0">
              <div class="form-check">
                <input id="datatableCheckAll" class="form-check-input" type="checkbox" value="" />
                <label class="form-check-label" for="datatableCheckAll"></label>
              </div>
            </th>
            <th>상품코드</th>
            <th>이미지</th>
            <th>상품명</th>
            <th>공급가</th>
            <th>정상가</th>
            <th>판매가</th>
          </tr>
        </thead>
        <tbody>
          <!-- 회원 검색 결과 목록 테이블 -->
          <!-- TODO: 테이블 데이터 표시 및 검색결과 없을때 표시처리 -->
          <!-- TODO: ex) 1개의 row로 겸색 결과가 없습니다. 문구 표시-->
          <!-- -->

          <tr>
            <td class="table-column-pe-0">
              <div class="form-check">
                <input id="datatableCheckAll1" class="form-check-input" type="checkbox" value="" />
                <label class="form-check-label" for="datatableCheckAll1"></label>
              </div>
            </td>
            <td>상품코드</td>
            <td>
              <div class="avatar">
                <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
              </div>
            </td>
            <td>
              <span class="d-block h5 mb-0">상품명</span>
            </td>
            <td>공급가</td>
            <td>정상가</td>
            <td>판매가</td>
          </tr>
        </tbody>
      </table>
      <div class="d-flex justify-content-center justify-content-sm-end">
        <nav id="datatableWithPaginationPagination" aria-label="Activity pagination"></nav>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-secondary">카탈로그에 추가하기</button>
      <button type="button" class="btn btn-secondary">선택 상품 빼기</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import { onMounted } from 'vue';

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
});
</script>

<style scoped></style>
