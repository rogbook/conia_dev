<template>
  <PageNavigator :before_link="[]" :current="'주문관리'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">주문현황</div>
    </div>
    <div class="card-body py-2">
      <!-- 주문상태 Checkbox -->
      <div class="row mb-2">
        <label for="idLabel" class="col-sm-2 col-md-1 col-lg-1 col-form-label form-label">[주문상태]</label>
        <div class="col-sm col-md col-lg">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_all" class="form-check-input" name="status_type" value="all" v-model="searchCondition.status" />
              <label class="form-check-label px-1" for="radio_status_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_wait" class="form-check-input" name="status_type" value="PW" v-model="searchCondition.status" />
              <label class="form-check-label px-1" for="radio_status_wait">입금대기</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_paid" class="form-check-input" name="status_type" value="PD" v-model="searchCondition.status" />
              <label class="form-check-label px-1" for="radio_status_paid">결제완료</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_shippingB" class="form-check-input" name="status_type" value="DW" v-model="searchCondition.status" />
              <label class="form-check-label px-1" for="radio_status_shippingB">상품준비중</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_shippingO" class="form-check-input" name="status_type" value="DN" v-model="searchCondition.status" />
              <label class="form-check-label px-1" for="radio_status_shippingO">배송중</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_shippingC" class="form-check-input" name="status_type" value="DC" v-model="searchCondition.status" />
              <label class="form-check-label px-1" for="radio_status_shippingC">배송완료</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_orderC" class="form-check-input" name="status_type" value="CP" v-model="searchCondition.status" />
              <label class="form-check-label px-1" for="radio_status_orderC">구매확정</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_cancel" class="form-check-input" name="status_type" value="CD" v-model="searchCondition.status" />
              <label class="form-check-label px-1" for="radio_status_cancel">결제취소</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 결제수단 Checkbox -->
      <div class="row mb-2">
        <label for="idLabel" class="col-sm-2 col-md-1 col-lg-1 col-xl-1 col-form-label form-label">[결제수단]</label>
        <div class="col-sm col-md col-lg">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_payment_all" class="form-check-input" name="pay_type" value="all" v-model="searchCondition.payment" />
              <label class="form-check-label px-1" for="radio_payment_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_payment_card" class="form-check-input" name="pay_type" value="card" v-model="searchCondition.payment" />
              <label class="form-check-label px-1" for="radio_payment_card">신용카드</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_payment_virtual" class="form-check-input" name="pay_type" value="vbank" v-model="searchCondition.payment" />
              <label class="form-check-label px-1" for="radio_payment_virtual">가상계좌</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_payment_transfer" class="form-check-input" name="pay_type" value="bank" v-model="searchCondition.payment" />
              <label class="form-check-label px-1" for="radio_payment_transfer">실시간이체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_payment_payco" class="form-check-input" name="pay_type" value="payco" v-model="searchCondition.payment" />
              <label class="form-check-label px-1" for="radio_payment_payco">페이코</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 주문상품유형 Checkbox -->
      <div class="row mb-2">
        <label for="idLabel" class="col-sm-2 col-md-2 col-lg-1 col-form-label form-label">[주문상품유형]</label>
        <div class="col-sm col-md col-lg">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_all" class="form-check-input" name="prod_type" value="all" v-model="searchCondition.type" />
              <label class="form-check-label px-1" for="radio_prod_type_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_DP" class="form-check-input" name="prod_type" value="DP" v-model="searchCondition.type" />
              <label class="form-check-label px-1" for="radio_prod_type_DP">배송상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_UP_OF" class="form-check-input" name="prod_type" value="UP-OF" v-model="searchCondition.type" />
              <label class="form-check-label px-1" for="radio_prod_type_UP_OF">티켓상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_UP_EC" class="form-check-input" name="prod_type" value="UP-EC" v-model="searchCondition.type" />
              <label class="form-check-label px-1" for="radio_prod_type_UP_EC">E-쿠폰</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 상점 검색 -->
      <div class="row mb-2">
        <label class="col-md-1 col-form-label">[상점선택]</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" v-model="searchCondition.store.name" placeholder="조회할 상점을 선택하세요." aria-label="조회할 상점을 선택하세요." disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('findStoreModal')" v-if="userClass.includes('PA') || userClass.includes('CM')">검색</button>
          </div>
        </div>
      </div>

      <!-- 공급자 선택 -->
      <div class="row mb-2 align-items-center">
        <label for="idLabel" class="col-md-1 col-form-label">[공급자(PA)]</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" v-model="paInfo.name" placeholder="공급자(PA)를 선택해주세요." aria-label="" disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="openPaSelModal" v-if="paInfo.noPa">검색</button>
          </div>
        </div>
      </div>

      <!-- 검색기간 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-sm-2 col-m-1 col-lg-1 col-form-label">[검색기간]</label>
        <div class="col-sm col-md col-lg">
          <div class="row">
            <div class="col-sm-4 col-md-2 col-lg-2 mb-1">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" v-model="searchCondition.date.type" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option value="order">주문일자</option>
                  <!--                  <option value="pay">결제일자</option>-->
                </select>
              </div>
              <!-- End Select -->
            </div>
            <div class="col-sm-6 col-md-2 col-lg-2 mb-1">
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." v-model="searchCondition.date.sDate" @change="sDateChange" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center mb-1">-</span>
            <div class="col-sm-6 col-md-2 col-lg-2 mb-1">
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." v-model="searchCondition.date.eDate" @change="eDateChange" />
                </div>
              </div>
            </div>
            <div class="col-sm col-md col-lg">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('yesterday')">전일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">일주일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('month')">1개월</button>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <label class="col-sm-2 col-md-1 col-lg-1 col-form-label">[세부검색]</label>
        <div class="col-sm col-md col-lg">
          <div class="row">
            <div class="col-sm-4 col-md-2 col-lg-2 mb-1">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" v-model="searchCondition.q.type" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option value="order_name">주문자</option>
                  <option value="order_email">주문자 아이디(이메일)</option>
                  <option value="order_id">주문번호</option>
                  <option value="prd_name">상품명</option>
                  <option value="prd_code">상품코드</option>
                </select>
              </div>
              <!-- End Select -->
            </div>
            <div class="col-sm-6 col-md-4 col-lg-4 mb-1">
              <div class="input-group">
                <input type="text" class="form-control" :placeholder="searchCondition.placeholder" id="q" v-model="searchCondition.q.value" @keypress.enter.prevent="getOrderList" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-2" @click.prevent="clearSearchCondition()">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getOrderList()">검색</button>
      </div>
    </div>
  </div>
  <span class="divider-center py-4">검색결과</span>
  <div class="row align-items-center mb-3 justify-content-between" v-if="mOrderList.total > 0">
    <div class="col-auto">
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
      <button type="button" class="btn btn-sm btn-warning p-2" @click.prevent="selectStatusDW()" v-if="checkPD && (getUserClassStr.includes('PA') || getUserClassStr.includes('CM'))">선택 상품 [상품준비중] 일괄 변경</button>
    </div>
  </div>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span>총 : {{ mOrderList.total }}개</span>
    </div>
    <div class="col-auto row align-items-center">
      <div class="col-auto">
        <button type="button" class="btn btn-sm btn-outline-info me-2" v-if="getUserClassStr.includes('CM') || getUserClassStr.includes('PA')" @click.prevent="openExcelShip">송장번호 일괄등록</button>
        <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="downloadExcel">조회내역 엑셀다운로드</button>
      </div>
      <div class="col-auto">
        <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
      </div>
    </div>
  </div>

  <div class="list-area table-responsive-sm">
    <table class="table table-sm table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th style="width: 5%" v-if="getUserClassStr.includes('PA') || getUserClassStr.includes('CM')">선택</th>
          <th style="width: 5%">주문상품유형</th>
          <th style="width: 10%">주문일자</th>
          <th style="width: 10%">주문번호</th>
          <th style="width: 5%">주문자</th>
          <th style="width: 5%">공급사</th>
          <th style="width: 5%">상점</th>
          <th style="width: 20%">주문상품</th>
          <th style="width: 5%">주문수량</th>
          <th>주문금액</th>
          <th style="width: 10%">결제일자</th>
          <th style="width: 5%">결제수단</th>
          <th style="width: 5%">상태</th>
          <th style="width: 5%">상세보기</th>
        </tr>
      </thead>
      <tbody>
        <!-- 회원 검색 결과 목록 테이블 -->
        <!-- TODO: 테이블 데이터 표시 및 검색결과 없을때 표시처리 -->
        <!-- TODO: ex) 1개의 row로 겸색 결과가 없습니다. 문구 표시-->
        <tr class="text-center" v-for="order in mOrderList.datas" :key="order.id">
          <td v-if="getUserClassStr.includes('PA') || getUserClassStr.includes('CM')">
            <input type="checkbox" class="form-check-input" name="cb_add_product" v-bind:id="`cb_o_${order.id}`" :value="order.id" v-model="mSelOrderProdList" v-if="order.type?.startsWith('DP') && (order.status === 'PD' || order.status === 'DD')" />
          </td>
          <td class="text-center">
            <div v-if="order.order_shipping_id">
              <span class="badge" :style="{ 'background-color': `#9b00ff !important` }">배</span>
            </div>
            <div v-else>
              <span v-if="order.type === 'UP-OF'" class="badge" :style="{ 'background-color': `#ff6b00 !important` }">티</span>
              <span v-else-if="order.type === 'UP-EC'" class="badge text-bg-success">E</span>
            </div>
          </td>
          <td style="font-size: 0.8rem">{{ dateTimeFormatConverter(order.order_date) }}</td>
          <td>
            <div class="" style="font-size: 0.85rem">{{ order.order_id }}</div>
            <div class="" v-if="order.origin_order_id">
              <router-link :to="{ name: 'orderDetail', state: { orderId: order.origin_order_id } }" style="font-size: 0.7rem">(원주문번호 : {{ order.origin_order_id }})</router-link>
            </div>
          </td>
          <td>{{ order.user_name }}</td>
          <td>{{ order.seller_title }}</td>
          <td class="text-wrap">{{ order.store_name }}</td>
          <td class="text-center text-wrap">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-auto">
                  <img :src="order.product_thumbnail" style="width: 50px" />
                </div>
                <div class="col-sm col-md col-lg text-start">
                  <div class="mb-1">
                    <b>{{ order.product_name }}</b>
                  </div>
                  <div class="">{{ order.product_option_name }}</div>
                </div>
              </div>
            </div>
          </td>
          <td>{{ order.ea }}</td>
          <td class="text-end">{{ order.amount.toLocaleString() }}원</td>
          <td style="font-size: 0.8rem">{{ order.pg_date ? dateTimeFormatConverter(order.pg_date) : dateTimeFormatConverter(order.order_date) }}</td>
          <td>{{ order.pg_kind ? convertPgType(order.pg_kind) : '교환주문건' }}</td>
          <td>{{ convertOrderStatus(order.status) }}</td>
          <td>
            <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ name: 'orderDetail', state: { orderId: order.order_id } })">상세</button>
          </td>
        </tr>
        <tr>
          <td colspan="14" class="text-center" v-if="mOrderList.total === 0">표시할 항목이 없습니다.</td>
        </tr>
      </tbody>
    </table>
    <div class="table-footer-area" v-if="mOrderList.total > 0">
      <div class="row" v-if="total_page > 1">
        <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
      </div>
    </div>
  </div>

  <!-- 상점검색 Modal -->
  <Modal :id="'findStoreModal'" :title="'상점 검색'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">상점을 검색해주세요.</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <div class="mb-6">
              <div class="row col align-items-center">
                <label class="col-md-1 col-form-label text-nowrap">상점검색</label>
                <div class="col-md-2"></div>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" id="store_title" v-model="store_title" placeholder="검색할 상점의 이름을 입력해주세요." @submit.stop.prevent="reqStoreList()" @keypress.enter.prevent="reqStoreList()" />
                    <button type="button" class="btn btn-outline-info" @click.prevent="reqStoreList()">검색</button>
                  </div>
                </div>
              </div>
            </div>
            <!-- Member List Table -->
            <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
              <thead class="thead-light">
                <tr class="text-center">
                  <th>상점</th>
                  <th style="width: 10%">선택</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center" v-for="(store, i) in storeList.datas" :key="JSON.stringify(store)">
                  <td>{{ store.title }}</td>
                  <td>
                    <button type="button" class="btn btn-sm btn-info" @click.prevent="setStore(store.title as string, store.code as string)">선택</button>
                  </td>
                </tr>
                <tr v-if="!storeList.datas || storeList.datas.length === 0">
                  <td colspan="2" class="text-center">검색 결과가 없습니다.</td>
                </tr>
              </tbody>
            </table>
            <!-- Member List Table End-->
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

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

  <!-- 송장번호 일괄등록 Modal -->
  <Modal :id="'shipExcelModal'" :title="'송장번호 일괄등록'">
    <template #body>
      <!-- Nav -->
      <div class="text-start">
        <ul class="nav nav-tabs mb-4 pb-1" role="tablist">
          <li class="nav-item">
            <a class="nav-link active" id="nav-one-eg1-tab" href="#nav-one-down" data-bs-toggle="pill" data-bs-target="#nav-one-down" role="tab" aria-controls="nav-one-down" aria-selected="true">엑셀 다운로드</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" id="nav-two-eg1-tab" href="#nav-two-upload" data-bs-toggle="pill" data-bs-target="#nav-two-upload" role="tab" aria-controls="nav-two-upload" aria-selected="false">엑셀 업로드</a>
          </li>
        </ul>
      </div>
      <!-- Tab Content -->
      <div class="tab-content">
        <div class="tab-pane fade show active" id="nav-one-down" role="tabpanel" aria-labelledby="nav-one-eg1-tab">
          <ShipExcelDown />
        </div>

        <div class="tab-pane fade" id="nav-two-upload" role="tabpanel" aria-labelledby="nav-two-eg1-tab">
          <ShipExcelUpload />
        </div>
      </div>
      <!-- End Tab Content -->
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import { computed, onMounted, reactive, ref } from 'vue';
import { apiResponseCheck, convertOrderStatus, dateTimeFormatConverter, showAlert, showConfirm, showLogConsole, showModal, hideModal, convertPgType, getUserClassStr } from '@/utils/common-utils';
import type { StoreList } from 'StoreListInfoModule';
import apis from '@/apis';
import type { OrderList } from 'OrderInfoModule';
import { useRouter, useRoute } from 'vue-router';
import Pagination from '@/components/comm/Pagination.vue';
import { useUserStore } from '@/stores/user';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';
import type { Class, User } from 'UserInfoModule';
import ShipExcelDown from '@/pages/order/list/excel/ShipExcelDown.vue';
import ShipExcelUpload from '@/pages/order/list/excel/ShipExcelUpload.vue';

const router = useRouter();
const route = useRoute();
const isChangeDate = ref(true);
const currentQueryStr = ref('');

const searchCondition = reactive({
  q: {
    type: 'order_name',
    value: '',
  },
  status: 'all',
  payment: 'all',
  type: 'all',
  date: {
    type: 'order',
    sDate: '',
    eDate: '',
  },
  store: {
    name: '',
    code: '',
  },
  placeholder: '주문자를 입력해주세요.',
});

// 선택 상품 리스트 (담은 상품)
const mSelOrderProdList = ref([] as number[]);

const mOrderList = ref({} as OrderList);

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mOrderList.value.total / limit.value));
const user = useUserStore().user;
const userName = computed(() => {
  return `${useUserStore().user.name}`;
});
const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getOrderList();
};

const store_title = ref('');
const storeList = ref({} as StoreList);

const storeCode = ref(useUserStore().user.store_code);
const checkPD = computed(() => {
  let result = false;
  mOrderList.value.datas.map(item => {
    if (item.status === 'PD') result = true;
  });
  return result;
});

const paInfo = reactive({
  id: 0,
  name: '',
  noPa: true,
});
const checkedTypes = ref('PA');
const searchUserList = ref({
  data: {} as User[],
  total: 0,
});
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
const user_pageChange = (page: number) => {
  user_page_no.value = page;
  searchUser(false);
};

const onChangeDetailSearch = () => {
  switch (searchCondition.q.type) {
    case 'order_name':
      searchCondition.placeholder = '주문자를 입력해주세요.';
      break;
    case 'order_email':
      searchCondition.placeholder = '주문자 아이디(이메일)을 입력해주세요.';
      break;
    case 'order_id':
      searchCondition.placeholder = '주문번호를 입력해주세요. (숫자만 입력)';
      break;
    case 'prd_name':
      searchCondition.placeholder = '상품명을 입력해주세요.';
      break;
    case 'prd_code':
      searchCondition.placeholder = '상품코드를 입력해주세요.';
      break;
  }
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

const setStore = (title: string, code: string) => {
  hideModal('findStoreModal');
  searchCondition.store.name = title;
  searchCondition.store.code = code;

  store_title.value = '';
  storeList.value = {} as StoreList;
};

const reqStoreList = () => {
  if (!store_title.value) {
    //검색어 입력안함.
    showAlert('검색할 상점의 이름을 입력해주세요.', 'warning');
  } else {
    //검색어 입력함.
    apis.store.get_list(`title=${store_title.value}&`).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        storeList.value = res;
      });
    });
  }
};

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

  searchCondition.q.type = 'order_name';
  searchCondition.q.value = '';
  searchCondition.status = 'all';
  searchCondition.payment = 'all';
  searchCondition.type = 'all';
  searchCondition.date.type = 'order';
  setSearchPeriod('today');
  searchCondition.store.code = '';
  searchCondition.store.name = '';
  currentQueryStr.value = '';
  onChangeDetailSearch();
  getOrderList();
};

const getOrderList = (reset: boolean = true) => {
  const date1 = new Date(searchCondition.date.sDate);
  const date2 = new Date(searchCondition.date.eDate);
  const timeDiff = Math.abs(date2.getTime() - date1.getTime());
  const diffMonths = Math.ceil(timeDiff / (1000 * 3600 * 24 * 31));

  if (diffMonths > 1) {
    showAlert('검색기간은 1개월 이하로만 조회가 가능합니다.', 'warning');
    setSearchPeriod('today');
    return;
  }

  if (searchCondition.q.type === 'order_id' && searchCondition.q.value) {
    if (!/^[0-9]+$/.test(searchCondition.q.value)) {
      showAlert('주문번호는 숫자로만 검색 가능합니다.', 'warning');
      return;
    }
  }

  mSelOrderProdList.value = [];
  if (reset) {
    page_no.value = 1;
  }
  let query = '';

  if (!getUserClassStr.value.includes('CM')) {
    if (getUserClassStr.value.includes('PA')) {
      query = query.concat(query ? `&pa_id=${useUserStore().user.id}` : `pa_id=${useUserStore().user.id}`);
    }
    if (getUserClassStr.value.includes('MC')) {
      query = query.concat(query ? `&store_code=${storeCode.value}` : `store_code=${storeCode.value}`);
    }
  }

  if (searchCondition.store.code && !getUserClassStr.value.includes('MC')) {
    query = query.concat(query ? `&store_code=${searchCondition.store.code}&store_name=${searchCondition.store.name}` : `store_code=${searchCondition.store.code}&store_name=${searchCondition.store.name}`);
  }

  if (paInfo.name && !getUserClassStr.value.includes('PA')) {
    query = query.concat(`pa_id=${paInfo.id}&pa_name=${paInfo.name}`);
  }

  if (searchCondition.status !== 'all') {
    query = query.concat(query ? `&status=${searchCondition.status}` : `status=${searchCondition.status}`);
  }

  if (searchCondition.payment !== 'all') {
    query = query.concat(query ? `&pg_type=${searchCondition.payment}` : `pg_type=${searchCondition.payment}`);
  }

  if (searchCondition.type !== 'all') {
    query = query.concat(query ? `&prd_type=${searchCondition.type}` : `prd_type=${searchCondition.type}`);
  }

  // 검색기간 시작날짜
  if (searchCondition.date.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchCondition.date.sDate}` : `s_reg_date=${searchCondition.date.sDate}`);
  }
  // 검색기간 종료날짜
  if (searchCondition.date.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchCondition.date.eDate}` : `e_reg_date=${searchCondition.date.eDate}`);
  }

  // 세부 검색
  if (searchCondition.q.value) {
    query = query.concat(query ? `&${searchCondition.q.type}=${searchCondition.q.value}` : `${searchCondition.q.type}=${searchCondition.q.value}`);
  }

  if (query) {
    query = query.concat('&');
  }
  currentQueryStr.value = query;
  setSearchInfo(query);

  apis.order.get_order_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mOrderList.value = res;
    });
  });
};

/** 검색조건 pinia 유지 관련 */
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
          searchCondition.date.sDate = value;
          break;
        case 'e_reg_date':
          searchCondition.date.eDate = value;
          break;
        case 'page_no':
          page_no.value = parseInt(value);
          break;
        case 'status':
          searchCondition.status = value;
          break;
        case 'pg_type':
          searchCondition.payment = value;
          break;
        case 'prd_type':
          searchCondition.type = value;
          break;
        case 'order_name':
        case 'order_email':
        case 'order_id':
        case 'prd_code':
        case 'prd_name':
          searchCondition.q.type = key;
          searchCondition.q.value = value;
          break;
        case 'store_code':
          searchCondition.store.code = value;
          break;
        case 'store_name':
          searchCondition.store.name = value;
          break;
        case 'pa_id':
          paInfo.id = value;
          break;
        case 'pa_name':
          paInfo.name = value;
          break;
        default:
          break;
      }
    }
  }
};
/** */

const selectStatusDW = () => {
  showConfirm('선택한 주문상품들에 대해 [상품준비중] 상태로 \n일괄 변경하시겠습니까?<br/> <span style="color: red">&#8251; 묶음배송인 주문건에도 모두 일괄 적용 됩니다.</span>', () => {
    apis.order.delivery_wait_update_select('DW', mSelOrderProdList.value).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        showAlert('[상품준비중] 상태로 일괄 변경되었습니다.');
        mSelOrderProdList.value = [];
        getOrderList();
      });
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getOrderList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const sDateChange = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInput'), {});
  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;
  const timeDiff = Math.abs(new Date(eDate).getTime() - new Date(sDate).getTime());
  const diffMonths = Math.ceil(timeDiff / (1000 * 3600 * 24 * 31));

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning', () => {
        // @ts-ignore
        sfp.setDate(new Date(eDate), true, 'Y-m-d');
      });
      return;
    }
    if (diffMonths > 1) {
      showAlert('최대 검색기간을 초과하여 자동으로 조정되었습니다.<br/>(최대 검색기간 1개월)', 'warning', () => {
        // @ts-ignore
        const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});
        // @ts-ignore
        efp.setDate(new Date(sDate).getTime() + 1000 * 60 * 60 * 24 * 31, true, 'Y-m-d');
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
  const timeDiff = Math.abs(new Date(eDate).getTime() - new Date(sDate).getTime());
  const diffMonths = Math.ceil(timeDiff / (1000 * 3600 * 24 * 31));

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning', () => {
        // @ts-ignore
        efp.setDate(new Date(sDate), true, 'Y-m-d');
      });
      return;
    }

    if (diffMonths > 1) {
      showAlert('최대 검색기간을 초과하여 자동으로 조정되었습니다.<br/>(최대 검색기간 1개월)', 'warning', () => {
        // @ts-ignore
        const sfp = flatpickr(document.querySelector('#startDatepickerInput'), {});
        // @ts-ignore
        sfp.setDate(new Date(eDate).getTime() - 1000 * 60 * 60 * 24 * 31, true, 'Y-m-d');
      });
    }
  }
};
const setSearchPeriod = (period: string) => {
  isChangeDate.value = false;
  const today = new Date();
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInput'), {});
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});
  switch (period) {
    case 'yesterday':
      // @ts-ignore
      efp.setDate(new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1), true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1), true, 'Y-m-d');
      break;
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
    default:
      searchCondition.date.sDate = '';
      searchCondition.date.eDate = '';
      break;
  }
  isChangeDate.value = true;
};

const downloadExcel = () => {
  showConfirm('현재 조회된 주문 내역을 다운로드 하시겠습니까?', () => {
    const now = new Date();
    apis.order.order_list_excel(currentQueryStr.value).then(res => {
      apiResponseCheck(res, async () => {
        const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `주문 내역 목록-${now.getFullYear()}${now.getMonth() + 1}${now.getDate()}${now.getHours()}${now.getMinutes()}${now.getSeconds()}.xlsx`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      });
    });
  });
};

const openExcelShip = () => {
  showModal('shipExcelModal');
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');

  setSearchPeriod('today');

  //매출현황에서 진입시
  if (history.state.orderDate) {
    searchCondition.date.sDate = history.state.orderDate;
    searchCondition.date.eDate = history.state.orderDate;
  }

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
  limit.value = useCommonStore().getLimit;
  page_no.value > 1 ? getOrderList(false) : getOrderList();
});
</script>

<style scoped></style>
