<template>
  <div>
    <div class="card">
      <div class="card-header">
        <div class="row align-items-center justify-content-between">
          <div class="col-auto">
            <div class="form-control-borderless h2">재고관리</div>
          </div>
        </div>
      </div>
      <div class="card-body">
        <div class="row mb-2 align-items-center">
          <label for="idLabel" class="col-md-1 col-form-label">공급자(PA)</label>
          <div class="col-md-4">
            <div class="input-group">
              <input type="text" class="form-control" v-model="paInfo.name" placeholder="공급자(PA)를 선택해주세요." aria-label="" disabled />
              <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('paMemberSelModal')" v-if="paInfo.noPa">검색</button>
            </div>
          </div>
        </div>
        <!-- 검색기간 Datepicker -->
        <div class="row mb-2 align-items-center">
          <label for="idLabel" class="col-md-1 col-form-label">검색기간<br />(상품등록일)</label>
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
        <!-- 세부검색어 입력 -->
        <div class="row col">
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
          <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearQuery">초기화</button>

          <button type="button" class="btn btn-sm btn-primary" @click.prevent="getProducts">검색</button>
        </div>
      </div>
    </div>

    <span class="divider-center py-4">검색결과</span>
    <div class="row mb-2 align-items-center justify-content-between">
      <div class="col-auto">
        <span v-if="mProductList.total > 0">총 : {{ mProductList.total }}개</span>
      </div>
    </div>
    <div class="card">
      <div class="table-responsive datatable-custom position-relative">
        <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
          <thead class="thead-light">
            <tr class="text-center">
              <th>상품코드</th>
              <th>이미지</th>
              <th>상품명</th>
              <th>공급자(PA)</th>
              <th>정상가</th>
              <th>판매가</th>
              <th>일괄재고수정</th>
              <th>옵션별재고수정</th>
              <th>상태</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in mProductList.datas" :key="item.id">
              <td>{{ item?.code }}</td>
              <td>
                <div class="avatar" v-if="item.photos.length > 0">
                  <img class="avatar-img" :src="item.photos[0].uri" alt="Image Description" />
                </div>
                <div class="avatar" v-if="item.photos.length === 0">
                  <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
                </div>
              </td>
              <td>
                <span class="d-block h5 mb-0">{{ item.name }}</span>
              </td>
              <td>
                <span class="d-block h5 mb-0">{{ item.member?.company?.name }}</span>
              </td>
              <td>{{ getPriceInfo(JSON.parse(JSON.stringify(item.options)), 'origin') }}<span v-if="getPriceInfo(JSON.parse(JSON.stringify(item.options)), 'origin') !== '설정필요'">원</span></td>
              <td>{{ getPriceInfo(JSON.parse(JSON.stringify(item.options)), 'sell') }}<span v-if="getPriceInfo(JSON.parse(JSON.stringify(item.options)), 'sell') !== '설정필요'">원</span></td>
              <td class="text-center">
                <div class="input-group">
                  <input type="number" class="form-control text-center col border-end-0" value="0" min="0" />
                  <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="">수정</button>
                </div>
              </td>
              <td>
                <button type="button" class="btn btn-sm btn-info" @click.prevent="showModal('showOpStockListModal')">수정</button>
              </td>
              <td>{{ item.status === 'Y' ? '승인' : '미승인' }}</td>
            </tr>
            <tr>
              <td colspan="9" class="text-center" v-if="mProductList.total === 0">표시할 항목이 없습니다.</td>
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
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" id="q" v-model="selDetailSearch2.q" :placeholder="selDetailSearch2.placeholder" />
                    <button type="button" class="btn btn-outline-dark col-md-2" @click.prevent="searchUser">검색</button>
                  </div>
                </div>
              </div>
            </form>
            <!-- Modal Search Form End -->
            <!-- Member List Table -->
            <div class="table-responsive">
              <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table table-nowrap">
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
            </div>
            <!-- Member List Table End-->
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <!-- 개별 옵션별 설정 Modal -->
  <Modal :id="'showOpStockListModal'" :title="'옵션별 재고 설정'" :xlarge="true">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">옵션별 공급가 설정</div>
        <div class="card">
          <div class="card-body">
            <!-- Member List Table -->
            <div class="table-responsive">
              <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
                <thead class="thead-light">
                  <tr class="text-center">
                    <th>옵션명</th>
                    <th>옵션코드</th>
                    <th style="width: 14%">정상가</th>
                    <th style="width: 14%">판매가</th>
                    <th style="width: 24%">재고</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="text-center">
                    <td>옵션명</td>
                    <td>옵션코드</td>
                    <td class="text-center">
                      <div class="input-group">
                        <input type="number" class="form-control text-center" :value="0" />
                        <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="">수정</button>
                      </div>
                    </td>
                    <td>정상가</td>
                    <td>판매가</td>
                  </tr>
                  <tr class="text-center">
                    <td>옵션명</td>
                    <td>옵션코드</td>
                    <td class="text-center">
                      <div class="input-group">
                        <input type="number" class="form-control text-center" :value="0" />
                        <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="">수정</button>
                      </div>
                    </td>
                    <td>정상가</td>
                    <td>판매가</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- Member List Table End-->
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
  <!-- 개별 옵션별 설정 Modal END -->
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import apis from '@/apis';
import type { ProductListInfo } from 'ProductListInfoModule';
import Pagination from '@/components/comm/Pagination.vue';
import type { Class, User } from 'UserInfoModule';
import { AxiosError } from 'axios';
import Modal from '@/components/comm/modal.vue';
import { useUserStore } from '@/stores/user';
import { apiResponseCheck, dateTimeFormatConverter, showAlert, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import type { Option as Opt } from 'CatalogProductModule';
const router = useRouter();
const isChangeDate = ref(true);
const mProductList = ref({} as ProductListInfo);

const getPriceInfo = (opts: Opt[], type: string): string | number => {
  const defaultOpt = opts.find(item => item.default_yn === 'Y' && item.status === 'Y');
  if (defaultOpt) {
    switch (type) {
      case 'supply':
        return defaultOpt.supply_price.toLocaleString();
      case 'origin':
        return defaultOpt.origin_price.toLocaleString();
      case 'sell':
        return defaultOpt.selling_price.toLocaleString();
      default:
        return '-';
    }
  } else {
    return '설정필요';
  }
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mProductList.value.total / limit.value));
const checkedTypes = ref('PA');
const searchDate = reactive({
  sDate: '',
  eDate: '',
});

const selDetailSearch = reactive({
  items: [
    { name: '상품명', value: 'name' },
    { name: '상품코드', value: 'code' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 상품의 이름을 입력해주세요.',
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
  switch (selDetailSearch.selectedItem) {
    case 'name':
      selDetailSearch.placeholder = '검색할 회원의 이름을 입력해주세요.';
      break;
    case 'user_id':
      selDetailSearch.placeholder = '검색할 회원의 아이디(이메일)을 입력해주세요.';
      break;
    case 'mobile':
      selDetailSearch.placeholder = "검색할 회원의 전화번호를 입력해주세요. ('-' 제외)";
      break;
    case 'company_name':
      selDetailSearch.placeholder = '검색할 회원의 회사명을 입력해주세요.';
      break;
  }
};

const getProducts = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  let query = '';

  if (paInfo.name) {
    query = query.concat(`member_id=${paInfo.id}`);
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

  if (query) {
    query = query.concat('&');
  }

  apis.product.getProducts(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mProductList.value.total = res.total;
      mProductList.value.datas = res.datas;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getProducts(false);
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

const searchUser = () => {
  let query = `class_code=${checkedTypes.value}&`;
  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    if (query) {
      query = query.concat(`&${detail}&`);
    } else {
      query = query.concat(`${detail}&`);
    }
  }
  apis.user.get_list(query, 0, 100).then(res => {
    apiResponseCheck(res, () => {
      searchUserList.value.data = res.datas;
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

const setPaInfo = (user: User) => {
  const paCompany = user?.company?.name ? user?.company?.name : '없음';
  paInfo.id = user.id;
  paInfo.name = `${user.name} ( 업체명 : ${paCompany} )`;

  hideModal('paMemberSelModal');
};

const clearQuery = () => {
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
  selDetailSearch.q = '';

  getProducts();
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');

  clearQuery();
});
</script>

<style scoped></style>
