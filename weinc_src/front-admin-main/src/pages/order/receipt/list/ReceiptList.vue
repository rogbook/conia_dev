<template>
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">매출증빙관리</div>
    </div>
    <div class="card-body py-2">
      <!-- 검색기간 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-md-1 col-form-label">입금일</label>
        <div class="col">
          <div class="row">
            <div class="col-md-2">
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
            <div class="col-md-2">
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
            <div class="d-md-none mt-1"></div>
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1 mb-1">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1">일주일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1">1개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1">3개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1">6개월</button>
              <button type="button" class="btn btn-outline-info mb-1">전체</button>
            </div>
          </div>
        </div>
      </div>
      <!-- 검색기간 Datepicker END -->
      <!-- 증빙서류 / 신청구분 Checkbox -->
      <div class="row mb-2">
        <!-- 증빙서류 Checkbox -->
        <div class="row col">
          <label for="idLabel" class="col-md-2 col-form-label form-label">증빙서류</label>
          <div class="col form-control border-0">
            <div class="row">
              <div class="col-auto">
                <input type="checkbox" id="check_proof_all" class="form-check-input" name="check_proof" value="all" checked />
                <label class="form-check-label px-1" for="check_proof_all">전체</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_proof_receipt" class="form-check-input" name="check_proof" value="receipt" />
                <label class="form-check-label px-1" for="check_proof_receipt">매출전표</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_proof_tax" class="form-check-input" name="check_proof" value="tax" />
                <label class="form-check-label px-1" for="check_proof_tax">세금계산서</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_proof_cash" class="form-check-input" name="check_proof" value="cash" />
                <label class="form-check-label px-1" for="check_proof_cash">현금영수증</label>
              </div>
            </div>
          </div>
        </div>
        <!-- 신청구분 Checkbox -->
        <div class="row col">
          <label for="idLabel" class="col-md-2 col-form-label form-label">신청구분</label>
          <div class="col form-control border-0">
            <div class="row">
              <div class="col-auto">
                <input type="checkbox" id="check_req_from_all" class="form-check-input" name="check_req_from" value="all" checked />
                <label class="form-check-label px-1" for="check_req_from_all">전체</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_req_from_mc" class="form-check-input" name="check_req_from" value="mc" />
                <label class="form-check-label px-1" for="check_req_from_mc">MC</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_req_from_pa" class="form-check-input" name="check_req_from" value="pa" />
                <label class="form-check-label px-1" for="check_req_from_pa">PA</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_req_from_cu" class="form-check-input" name="check_req_from" value="cu" />
                <label class="form-check-label px-1" for="check_req_from_cu">일반</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_req_from_cm" class="form-check-input" name="check_req_from" value="cm" />
                <label class="form-check-label px-1" for="check_req_from_cm">관리자</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_req_from_self" class="form-check-input" name="check_req_from" value="self" />
                <label class="form-check-label px-1" for="check_req_from_self">자진발급</label>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 증빙서류 / 신청구분 Checkbox END -->
      <!-- 결제여부 / 반품유무 Checkbox -->
      <div class="row mb-2">
        <!-- 결제여부 Checkbox -->
        <div class="row col">
          <label for="idLabel" class="col-md-2 col-form-label form-label">결제여부</label>
          <div class="col form-control border-0">
            <div class="row">
              <div class="col-auto">
                <input type="checkbox" id="check_pay_state_all" class="form-check-input" name="check_pay_state" value="all" checked />
                <label class="form-check-label px-1" for="check_pay_state_all">전체</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_pay_state_y" class="form-check-input" name="check_pay_state" value="y" />
                <label class="form-check-label px-1" for="check_pay_state_y">입금</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_pay_state_n" class="form-check-input" name="check_pay_state" value="n" />
                <label class="form-check-label px-1" for="check_pay_state_n">미입금</label>
              </div>
            </div>
          </div>
        </div>
        <!-- 반품유무 Checkbox -->
        <div class="row col">
          <label for="idLabel" class="col-md-2 col-form-label form-label">반품유무</label>
          <div class="col form-control border-0">
            <div class="row">
              <div class="col-auto">
                <input type="checkbox" id="check_refund_all" class="form-check-input" name="check_refund" value="all" checked />
                <label class="form-check-label px-1" for="check_refund_all">전체</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_refund_y" class="form-check-input" name="check_refund" value="y" />
                <label class="form-check-label px-1" for="check_refund_y">있음</label>
              </div>
              <div class="col-auto">
                <input type="checkbox" id="check_refund_n" class="form-check-input" name="check_refund" value="n" />
                <label class="form-check-label px-1" for="check_refund_n">없음</label>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 결제여부 / 반품유무 Checkbox END -->
      <!-- 증빙상태 Checkbox -->
      <div class="row mb-2">
        <label for="idLabel" class="col-md-1 col-form-label form-label">증빙상태</label>
        <div class="col form-control border-0">
          <div class="row">
            <div class="col-auto">
              <input type="checkbox" id="check_receipt_status_all" class="form-check-input" name="check_receipt_status" value="all" checked />
              <label class="form-check-label px-1" for="check_receipt_status_all">전체</label>
            </div>
            <div class="col-auto">
              <input type="checkbox" id="check_receipt_status_wait" class="form-check-input" name="check_receipt_status" value="wait" />
              <label class="form-check-label px-1" for="check_receipt_status_wait">대기중</label>
            </div>
            <div class="col-auto">
              <input type="checkbox" id="check_receipt_status_done_y" class="form-check-input" name="check_receipt_status_done_y" value="done_y" />
              <label class="form-check-label px-1" for="check_receipt_status_done_y">완료(연동)</label>
            </div>
            <div class="col-auto">
              <input type="checkbox" id="check_receipt_status_done_n" class="form-check-input" name="check_receipt_status_done_n" value="done_n" />
              <label class="form-check-label px-1" for="check_receipt_status_done_n">완료(미연동)</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 증빙상태 Checkbox END -->
      <!-- 세부검색어 입력 -->
      <div class="row col">
        <label class="col-md-1 col-form-label">세부검색</label>
        <div class="col-md-2">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option value="all">전체</option>
              <option value="order">주문자</option>
              <option value="order_id">주문자아이디</option>
              <option value="order_code">주문번호</option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="검색어를 입력하세요." id="q" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button class="btn btn-sm btn-primary">검색</button>
      </div>
    </div>
  </div>
  <span class="divider-center py-4">검색결과</span>
  <table class="table table-nowrap table-align-middle card-table table-bordered">
    <thead class="thead-light">
      <tr class="text-center">
        <th rowspan="3" style="width: 3%">
          <div class="col-auto">
            <input type="checkbox" id="check_list_item_all" class="form-check-input" name="check_list_item" value="all" />
          </div>
        </th>
        <th rowspan="2" colspan="5">주문</th>
        <th colspan="8">매출증빙</th>
        <th rowspan="2">반품</th>
        <th rowspan="3">메모</th>
      </tr>
      <tr class="text-center">
        <th colspan="4">1.신청</th>
        <th colspan="2">2.처리</th>
        <th colspan="2">3.결과</th>
      </tr>
      <tr class="text-center">
        <th>주문번호<br />주문일</th>
        <th>상점</th>
        <th>주문자</th>
        <th>결제금액</th>
        <th>결제상태</th>
        <th>신청자<br />신청일</th>
        <th>신청정보</th>
        <th>증빙자료</th>
        <th>증빙금액</th>
        <th>처리확정일</th>
        <th>처리방법</th>
        <th>전송로그</th>
        <th>처리상태</th>
        <th>반품번호</th>
      </tr>
    </thead>
    <tbody>
      <!-- 회원 검색 결과 목록 테이블 -->
      <!-- TODO: 테이블 데이터 표시 및 검색결과 없을때 표시처리 -->
      <!-- TODO: ex) 1개의 row로 겸색 결과가 없습니다. 문구 표시-->
      <!-- -->
      <!--  <ProductListItem v-for="(item, index) in productList" :item="item" :key="index" />-->
    </tbody>
  </table>
  <!-- Pagination -->
  <div class="d-flex justify-content-center justify-content-sm-end">
    <nav id="datatableWithPaginationPagination" aria-label="Activity pagination"></nav>
  </div>

  <!-- 회원 연결 관리 Modal -->
  <!-- TODO: 회원연결관리 관련 데이터 작업 해야함. -->
  <Modal :id="'findPaModal'" :title="'파트너 검색'" :xlarge="true">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">파트너를 검색해주세요.</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <form class="mb-6">
              <div class="row col">
                <label class="col-md-2 col-form-label">파트너검색</label>
                <div class="col-md-2">
                  <!-- Select -->
                  <div class="tom-select-custom">
                    <select class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                      <option value="name">이름</option>
                      <option value="id">아이디</option>
                      <option value="mobile">전화번호</option>
                    </select>
                  </div>
                  <!-- End Select -->
                </div>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" id="q" />
                    <button type="button" class="btn btn-outline-dark col-2">검색</button>
                  </div>
                </div>
              </div>
            </form>
            <!-- Modal Search Form End -->
            <!-- Member List Table -->
            <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
              <thead class="thead-light">
                <tr>
                  <th class="table-column-pe-0">
                    <div class="form-check">
                      <input id="datatableCheckAll" class="form-check-input" type="checkbox" value="" />
                      <label class="form-check-label" for="datatableCheckAll"></label>
                    </div>
                  </th>
                  <th>선택</th>
                  <th>회원타입</th>
                  <th>이름</th>
                  <th>아이디</th>
                  <th>휴대전화</th>
                  <th>가입일시</th>
                </tr>
              </thead>
              <tbody>
                <!-- 회원 검색 결과 목록 테이블 -->
                <!-- TODO: 테이블 데이터 표시 및 검색결과 없을때 표시처리 -->
                <!-- -->
                <!--  <ProductListItem v-for="(item, index) in productList" :item="item" :key="index" />-->
              </tbody>
            </table>
            <!-- Member List Table End-->
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary">선택</button>
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
