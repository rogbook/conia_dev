<template>
  <PageNavigator :before_link="[]" :current="'PG 배송비 정산내역'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">PG 배송비 정산내역 - [{{ userInfo.name }}{{ userInfo.email ? ` (${userInfo.email})` : '' }}]</div>
    </div>
    <div class="card-body">
      <!-- 정산상태 Checkbox -->
      <div class="row align-items-center mb-2">
        <label for="idLabel" class="col-md-1 col-form-label form-label">정산상태</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_r" class="form-check-input" name="search_status" value="R" v-model="checkedStatus" />
              <label class="form-check-label px-1" for="radio_status_r">대기</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_c" class="form-check-input" name="search_status" value="C" v-model="checkedStatus" />
              <label class="form-check-label px-1" for="radio_status_c">확정</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_p" class="form-check-input" name="search_status" value="P" v-model="checkedStatus" />
              <label class="form-check-label px-1" for="radio_status_p">입금완료</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_j" class="form-check-input" name="search_status" value="J" v-model="checkedStatus" />
              <label class="form-check-label px-1" for="radio_status_j">보류</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 가입기간 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-md-1 col-form-label">검색기간</label>
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." @change="sDateChange()" v-model="searchDate.sDate" />
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." @change="eDateChange()" v-model="searchDate.eDate" />
                </div>
              </div>
            </div>
            <div class="d-md-none mt-1"></div>
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('bMonth')">전월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">일주일</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getSettlementList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">조회결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mSettlementList.total > 0">총 : {{ mSettlementList.total }}개</span>
    </div>
    <div class="col">
      <div class="row align-items-center justify-content-end" v-if="getUserClassStr.includes('CM')">
        <div class="col-auto px-0 ms-2">
          <button type="button" class="btn btn-sm btn-outline-info" v-if="currentSearchStatus === 'J'" @click.prevent="changeStatus('R')">선택항목 [대기] 처리</button>
        </div>
        <div class="col-auto px-0 ms-2">
          <button type="button" class="btn btn-sm btn-outline-info" v-if="currentSearchStatus !== 'C' && currentSearchStatus !== 'P'" @click.prevent="changeStatus('C')">선택항목 [확정] 처리</button>
        </div>
        <div class="col-auto px-0 ms-2">
          <button type="button" class="btn btn-sm btn-outline-info" v-if="currentSearchStatus === 'C'" @click.prevent="changeStatus('P')">선택항목 [입금완료] 처리</button>
        </div>
        <div class="col-auto px-0 ms-2">
          <button type="button" class="btn btn-sm btn-outline-info" v-if="currentSearchStatus !== 'J' && currentSearchStatus !== 'P'" @click.prevent="changeStatus('J')">선택항목 [보류] 처리</button>
        </div>
      </div>
    </div>
  </div>

  <div class="calculate-info-area table-responsive-md" style="overflow-x: auto">
    <table class="table table-nowrap table-align-middle card-table table-bordered">
      <thead>
        <tr class="thead-light">
          <th class="text-end" :colspan="getUserClassStr.includes('CM') ? 8 : 7">정산 금액 합계</th>
          <th class="text-end text-danger">{{ mSettlementList.total_sum?.toLocaleString() ? mSettlementList.total_sum?.toLocaleString() : '-' }}원</th>
        </tr>
      </thead>
      <thead class="thead-light">
        <tr class="text-center">
          <th v-if="getUserClassStr.includes('CM')">
            <input type="checkbox" class="form-check-input" name="cb_select_settlement" id="cb_ss_all" v-model="allCheck" @change="allCheckedClick" />
          </th>
          <th>정산일자</th>
          <th>처리일자</th>
          <th>정산상태</th>
          <th>주문번호</th>
          <th>판매상점명(코드)</th>
          <th v-if="getUserClassStr.includes('CM')">정산대상금액</th>
          <th>수수료율(%) 또는 고정금액</th>
          <th>정산금액</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="s in mSettlementList.datas" :key="s.id">
          <td v-if="getUserClassStr.includes('CM')">
            <input type="checkbox" class="form-check-input" name="cb_select_settlement" v-bind:id="`cb_ss_${s.id}`" :value="s" v-model="mSelSettlementList" />
          </td>
          <td>{{ dateTimeFormatConverter(s.reg_date).slice(0, 13) }}</td>
          <td>{{ dateTimeFormatConverter(s.mod_date).slice(0, 13) }}</td>
          <td>
            <div class="">
              {{ convertStatus(s.status) }}
              <button type="button" class="btn badge bg-danger ms-2" v-if="currentSearchStatus === 'J'" @click.prevent="showReject(s)">사유</button>
            </div>
          </td>
          <td>
            <button type="button" class="btn btn-sm btn-outline-info" style="font-weight: bold" @click.prevent="router.push({ name: 'orderDetail', state: { orderId: s.order_id } })">{{ s.order_id }}</button>
          </td>
          <td>{{ s.store_code }}</td>
          <td class="text-end" v-if="getUserClassStr.includes('CM')">{{ s.target_amount.toLocaleString() }}원</td>
          <td>{{ s.commission_type === 'P' ? `비율 (${s.commission_value}%)` : '고정' }}</td>
          <td class="text-end">
            <a class="text-decoration-underline" href="" @click.prevent="showHistory(s.id, 'ship')" v-if="getUserClassStr.includes('CM')">{{ s.amount.toLocaleString() }}원</a>
            <span v-else>{{ s.amount.toLocaleString() }}원</span>
          </td>
        </tr>
        <tr v-if="mSettlementList.total === 0">
          <td class="text-center" :colspan="getUserClassStr.includes('CM') ? 9 : 8">정산 내역이 없습니다.</td>
        </tr>
      </tbody>
    </table>
    <div class="table-footer-area" v-if="false">
      <div class="row" v-if="total_page > 1">
        <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
      </div>
    </div>
  </div>
  <!-- 정산근거  Modal -->
  <Modal :id="'settlementHistoryModal'" :title="'정산 근거'" :xlarge="true" :centered="true">
    <template #body>
      <SettlementHistoryModal ref="refHistory" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
  <!-- 정산근거 Modal END -->

  <!-- 정산보류사유  Modal -->
  <Modal :id="'rejectModal'" :title="'정산 보류 사유'" :centered="true">
    <template #body>
      <div class="card">
        <div class="card-body">
          <div class="row mb-2 align-items-center">
            <label class="col-md-3 col-form-label">보류 사유</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="보류 사유를 입력해주세요." v-model="selectReject.reject" :readonly="!getUserClassStr.includes('CM')" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-sm btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-sm btn-warning" @click.prevent="modReject(selectReject)" v-if="getUserClassStr.includes('CM')">수정</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, hideModal, showAlert, showConfirm, showConfirmInput, showLogConsole, showModal } from '@/utils/common-utils';
import apis from '@/apis';
import { useRouter } from 'vue-router';
import type { SettlementShip, SettlementShipList } from 'SettlementInfoModule';
import Pagination from '@/components/comm/Pagination.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import Modal from '@/components/comm/modal.vue';
import SettlementHistoryModal from '@/pages/settlement/modal/SettlementHistoryModal.vue';

const router = useRouter();
const isChangeDate = ref(true);
const currentSearchStatus = ref('');
const currentSearchPeriod = ref('');
const selectReject = ref({} as SettlementShip);

// 선택 상품 리스트 (담은 상품)
const mSelSettlementList = ref([]);

const checkedStatus = ref('R');
const allCheck = ref(false);

const mSettlementList = ref({} as SettlementShipList);
const allCheckedClick = () => {
  if (allCheck.value) {
    //@ts-ignore
    mSelSettlementList.value = [...mSettlementList.value.datas];
  } else {
    mSelSettlementList.value = [];
  }
};
const refHistory = ref();

const userInfo = reactive({
  id: 0,
  name: '',
  email: '',
});

const searchDate = reactive({
  sDate: '',
  eDate: '',
});

const searchCondition = reactive({
  date: {
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
  },
});

const page_no = ref(1);
const limit = ref(10);
const offset = computed(() => (page_no.value - 1) * limit.value);
const total_page = computed(() => Math.ceil(mSettlementList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getSettlementList();
};

const pageChange = (page: number) => {
  page_no.value = page;
  getSettlementList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const totalSettlementAmount = computed(() => {
  let total = 0;
  mSettlementList.value.datas?.map(s => {
    total += s.amount;
  });
  return total;
});

const convertStatus = (s: string): string => {
  switch (s) {
    case 'R':
      return '대기';
    case 'C':
      return '확정';
    case 'P':
      return '입금완료';
    case 'J':
      return '보류';
    default:
      return '-';
  }
};

const clearSearchCondition = () => {
  initialTarget();

  getSettlementList();
};

const getSettlementList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  mSelSettlementList.value = [];
  let query = '&kind=PG';

  query = query.concat(`&status=${checkedStatus.value}`);
  //검색기간
  if (searchDate.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchDate.sDate}` : `&s_reg_date=${searchDate.sDate}`);
  }
  //검색기간
  if (searchDate.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchDate.eDate}` : `&e_reg_date=${searchDate.eDate}`);
  }

  apis.settlement.get_ship_list(userInfo.id, query).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mSettlementList.value.total = res.total;
      mSettlementList.value.datas = res.datas;
      mSettlementList.value.total_sum = res.total_sum;
      currentSearchStatus.value = checkedStatus.value;
      currentSearchPeriod.value = `${searchDate.sDate}~${searchDate.eDate}`;
    });
  });
};

const initialTarget = () => {
  setSearchPeriod('bMonth');
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

const setSearchPeriod = (period: string) => {
  isChangeDate.value = false;
  const today = new Date();
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInput'), {});
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});
  switch (period) {
    case 'bMonth':
      // @ts-ignore
      efp.setDate(new Date(today.getFullYear(), today.getMonth(), 0), true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getFullYear(), today.getMonth() - 1, 1), true, 'Y-m-d');
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

const showHistory = (id: number, kind: string) => {
  showModal('settlementHistoryModal');
  refHistory.value.openModal(id, kind);
};

const showReject = (se: SettlementShip) => {
  selectReject.value = se;

  if (!getUserClassStr.value.includes('CM') && !selectReject.value.reject) {
    showAlert('보류 사유가 없습니다.', 'warning');
    return;
  }
  showModal('rejectModal');
};

const modReject = (se: SettlementShip) => {
  if (!se.reject) {
    showAlert('보류 사유를 입력해주세요.', 'warning');
    return;
  }
  showConfirm('보류사유를 수정하시겠습니까?', () => {
    const data = { ids: [se.id], reject: se.reject };
    modSettlement(data);
  });
};

const modSettlement = (data: { ids: number[]; status?: string; date_range?: string; reject?: string }) => {
  apis.settlement.mod_ship_settlements(data).then(res => {
    apiResponseCheck(res, () => {
      const msg = data.status ? `[${convertStatus(data.status)}] 처리 되었습니다.` : '수정되었습니다.';
      showAlert(msg, 'success', () => {
        getSettlementList();
        if (!data.status) {
          hideModal('rejectModal');
        }
      });
    });
  });
};

const changeStatus = (status: string) => {
  if (mSelSettlementList.value.length === 0) {
    showAlert('선택한 항목이 없습니다.', 'warning');
    return;
  }

  if (status === 'J') {
    showConfirmInput(`선택한 항목을 [${convertStatus(status)}] 처리 하시겠습니까?`, '보류 사유를 입력해주세요.', (res: string) => {
      const date_range = `${searchDate.sDate} ~ ${searchDate.eDate}`;
      const ids: number[] = [];
      mSelSettlementList.value.map(item => {
        ids.push((item as SettlementShip).id);
      });
      const data = { ids: ids, status: status, date_range: date_range, reject: res };
      modSettlement(data);
    });
  } else {
    showConfirm(`선택한 항목을 [${convertStatus(status)}] 처리 하시겠습니까?`, () => {
      const date_range = `${searchDate.sDate} ~ ${searchDate.eDate}`;
      const ids: number[] = [];
      mSelSettlementList.value.map(item => {
        ids.push((item as SettlementShip).id);
      });
      const data = { ids: ids, status: status, date_range: date_range };
      modSettlement(data);
    });
  }
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');

  limit.value = useCommonStore().getLimit;
  const memberId = history.state.memberId;
  const memberName = history.state.name;
  const memberEmail = history.state.email;

  if (!memberId || !memberName) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
  } else {
    userInfo.id = memberId;
    userInfo.name = memberName;
    userInfo.email = memberEmail;
    clearSearchCondition();
  }
});
</script>

<style scoped></style>
