<template>
  <PageNavigator :before_link="['배송비 정산 내역']" :current="'배송비 정산 내역 상세'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">배송비 정산 내역 - [{{ userInfo.name }} {{ userInfo.email ? `(${userInfo.email})` : '' }}]</div>
    </div>
    <div class="card-body">
      <!-- 정산상태 Checkbox -->
      <div class="row align-items-center">
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
            <div class="d-lg-none mt-2"></div>
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
      <div class="row align-items-center justify-content-between">
        <div class="col-auto text-end">
          <span class="text-danger">&#8251; 정산 금액은 실제 지급 금액과 다를 수 있습니다.</span>
        </div>
        <div class="col-auto text-end">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="getSettlementList">검색</button>
        </div>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">조회결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mSettlementList.total > 0">총 : {{ mSettlementList.total }}개</span>
      <button type="button" class="btn btn-sm btn-outline-info ms-4" @click.prevent="downloadExcel" v-if="mSettlementList.total > 0">배송비 정산내역 엑셀 다운로드</button>
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

  <div class="calculate-info-area table-responsive">
    <table class="table table-nowrap table-align-middle card-table table-bordered">
      <thead>
        <tr class="thead-light">
          <th class="text-end" :colspan="getUserClassStr.includes('CM') ? 8 : 6">정산 금액 합계</th>
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
          <td>{{ s.store.title }} ({{ s.store_code }})</td>
          <td class="text-end" v-if="getUserClassStr.includes('CM')">{{ s.target_amount.toLocaleString() }}원</td>
          <td>{{ s.commission_type === 'P' ? `비율 (${s.commission_value}%)` : '고정' }}</td>
          <td class="text-end">
            <a class="text-decoration-underline" href="" @click.prevent="showHistory(s.id, 'ship')" v-if="getUserClassStr.includes('CM')">{{ s.amount.toLocaleString() }}원</a>
            <span v-else>{{ s.amount.toLocaleString() }}원</span>
          </td>
        </tr>
        <tr v-if="mSettlementList.total === 0">
          <td class="text-center" :colspan="getUserClassStr.includes('CM') ? 9 : 7">정산 내역이 없습니다.</td>
        </tr>
      </tbody>
    </table>
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
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showAlert, showConfirm, showConfirmInput, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import apis from '@/apis';
import { useRouter } from 'vue-router';
import type { OrderProduct, SettlementShip, SettlementShipList } from 'SettlementInfoModule';
import Pagination from '@/components/comm/Pagination.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import Modal from '@/components/comm/modal.vue';
import SettlementHistoryModal from '@/pages/settlement/modal/SettlementHistoryModal.vue';
import type { Class, User } from 'UserInfoModule';
import * as XLSX from 'xlsx';

const router = useRouter();
const isChangeDate = ref(true);
const mSettlementList = ref({} as SettlementShipList);

const checkedStatus = ref('R');
const selectReject = ref({} as SettlementShip);
const currentSearchStatus = ref('');
const currentSearchPeriod = ref('');

const refHistory = ref();

const userInfo = reactive({
  id: 0,
  name: '',
  email: '',
  classStr: '',
  company: '',
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

const totalSettlementAmount = computed(() => {
  let total = 0;
  mSettlementList.value.datas?.map(s => {
    total += s.amount;
  });
  return total;
});

const clearSearchCondition = () => {
  initialTarget();
  searchCondition.date.year = new Date().getFullYear();
  searchCondition.date.month = new Date().getMonth() + 1;

  // getSettlementList();
};

const getSettlementList = (init: boolean = true) => {
  if (init) {
    mSelSettlementList.value = [];
  }
  let query = '';
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

const allCheck = ref(false);
const allCheckedClick = () => {
  if (allCheck.value) {
    //@ts-ignore
    mSelSettlementList.value = [...mSettlementList.value.datas];
  } else {
    mSelSettlementList.value = [];
  }
};

const initialTarget = () => {
  // setSearchPeriod('bMonth');
};

// 선택 상품 리스트 (담은 상품)
const mSelSettlementList = ref([]);

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

const showReject = (se: SettlementShip) => {
  selectReject.value = se;

  if (!getUserClassStr.value.includes('CM') && !selectReject.value.reject) {
    showAlert('보류 사유가 없습니다.', 'warning');
    return;
  }
  showModal('rejectModal');
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

const showHistory = (id: number, kind: string) => {
  showModal('settlementHistoryModal');
  refHistory.value.openModal(id, kind);
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

const downloadExcel = async () => {
  // @ts-ignore
  // 엑셀 파일 생성
  const book = XLSX.utils.book_new();

  // 엑셀에 넣을 데이터 만들기..
  const settlementList = makeSettlement();

  settlementList.unshift([]);
  settlementList.unshift([]);

  settlementList.unshift(['이름', userInfo.name], ['이메일', userInfo.email]);
  settlementList.unshift(['업체명', userInfo.company]);
  settlementList.unshift(['조회기간', currentSearchPeriod.value]);

  // sheet 생성 - aoa_to_sheet 장식으로
  const worksheetByAoa = XLSX.utils.aoa_to_sheet(settlementList);

  // 엑셀 파일에 sheet set (엑셀파일, 시트 데이터, 시트명)
  XLSX.utils.book_append_sheet(book, worksheetByAoa, '정산내역');

  // 엑셀 다운로드
  XLSX.writeFile(book, `${userInfo.name} 배송비 정산내역 - ${currentSearchPeriod.value}.xlsx`);
};

const optionStr = (opt: OrderProduct): string => {
  if (opt.product_option.option_title) {
    let optStr = `${opt.product_option.option_title}`;
    if (opt.product_option.option_1) {
      optStr = optStr.concat(` - ${opt.product_option.option_1}`);
    }
    if (opt.product_option.option_2) {
      optStr = optStr.concat(`/${opt.product_option.option_2}`);
    }
    if (opt.product_option.option_3) {
      optStr = optStr.concat(`/${opt.product_option.option_3}`);
    }
    if (opt.product_option.option_4) {
      optStr = optStr.concat(`/${opt.product_option.option_4}`);
    }
    if (opt.product_option.option_5) {
      optStr = optStr.concat(`/${opt.product_option.option_5}`);
    }
    return optStr;
  } else {
    return '없음';
  }
};

const makeSettlement = (): any[] => {
  const list = [] as any[];
  // TODO : PA 데이터
  list.push(['주문번호', '판매상점명(코드)', '정산금액', '정산상태']);

  let tTaxAmount = 0;
  let tTax = 0;
  let total = 0;
  for (const s of mSettlementList.value.datas) {
    const data = [] as any[];
    data.push(s.order_id); //주문번호
    data.push(`${s.store.title}(${s.store_code})`); //판매상점명(코드)
    data.push(s.amount.toLocaleString()); //정산급액
    data.push(convertStatus(s.status)); //정산상태
    tTaxAmount += s.amount;
    list.push(data);
  }
  list.push(['합계', '', tTaxAmount.toLocaleString(), '']);
  return list;
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

const getUserinfo = () => {
  if (getUserClassStr.value.includes('CM')) {
    apis.user.get_user(userInfo.id.toString(), 'member').then(res => {
      apiResponseCheck(res, () => {
        userInfo.company = (res as User).company.name ? (res as User).company.name : '없음';
        userInfo.classStr = getUserClass((res as User).classes);
      });
    });
  } else {
    apis.user.me().then(res => {
      apiResponseCheck(res, () => {
        userInfo.company = (res as User).company.name ? (res as User).company.name : '없음';
        userInfo.classStr = getUserClass((res as User).classes);
      });
    });
  }
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');

  const memberId = history.state.memberId;
  const memberName = history.state.name;
  const memberEmail = history.state.email;

  const s_date = history.state.s_date;
  const e_date = history.state.e_date;

  if (s_date || e_date) {
    searchDate.sDate = s_date;
    searchDate.eDate = e_date;
  } else {
    setSearchPeriod('bMonth');
  }

  if (!memberId || !memberName) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
    return;
  } else {
    userInfo.id = memberId;
    userInfo.name = memberName;
    userInfo.email = memberEmail;
    getUserinfo();
    clearSearchCondition();
  }
  // TODO: 기간 버튼 클릭시 바로 조회 요청시
  getSettlementList();
});
</script>

<style scoped></style>
