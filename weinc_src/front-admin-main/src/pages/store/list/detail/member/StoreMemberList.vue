<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세'] : ['상점 관리', '상점관리 상세']" :current="'이용자 관리'" />
  <div class="card mb-4">
    <div class="card-header py-2">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">
          <div class="form-control-borderless h2 mb-0">이용자 관리</div>
        </div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-warning" @click.prevent="openCustomerUpload">이용자 일괄 등록</button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <!-- 회원타입 Checkbox -->
      <div class="row align-items-center">
        <label for="idLabel" class="col-md-1 col-form-label form-label">승인여부</label>
        <div class="col form-control border-0">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_all" class="form-check-input" name="search_class_type" value="all" v-model="selDetailSearch.confirm" />
              <label class="form-check-label px-1" for="radio_status_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_y" class="form-check-input" name="search_class_type" value="Y" v-model="selDetailSearch.confirm" />
              <label class="form-check-label px-1" for="radio_status_y">승인</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_n" class="form-check-input" name="search_class_type" value="N" v-model="selDetailSearch.confirm" />
              <label class="form-check-label px-1" for="radio_status_n">미승인</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 세부검색어 입력 -->
      <div class="row col">
        <label class="col-md-1 col-form-label">세부검색</label>
        <div class="col-md-2 mb-1">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="reqUserList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="reqUserList">검색</button>
      </div>
    </div>
  </div>
  <span class="divider-center py-4">검색결과</span>
  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="total > 0">총 : {{ total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <div class="table-responsive">
    <table class="table table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th>이름</th>
          <th>아이디</th>
          <th>가입일시</th>
          <th v-if="mAbleTarget !== 'N'">회원식별값 (예:사번 등)</th>
          <th style="width: 10%">승인여부</th>
          <th style="width: 10%">추천인</th>
          <th style="width: 10%">삭제</th>
        </tr>
      </thead>
      <tbody>
        <!-- 회원 검색 결과 목록 테이블 -->
        <tr class="text-center" v-for="(user, i) in userList" :key="user.id">
          <td>{{ user.customer.name }}</td>
          <td>{{ user.customer.email }}</td>
          <td>{{ dateTimeFormatConverter(user.reg_date) }}</td>
          <td v-if="mAbleTarget !== 'N'">
            <div class="col-auto">
              <div class="input-group">
                <input type="text" class="form-control" v-model="user.value" placeholder="회원식별값을 입력해주세요." disabled />
              </div>
            </div>
          </td>
          <td style="min-width: 120px">
            <div class="col-auto">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" v-model="user.confirm" @change="customerConfirmChange(i)" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option value="Y">승인</option>
                  <option value="N">미승인</option>
                </select>
              </div>
              <!-- End Select -->
            </div>
          </td>
          <td>{{ user.recommander_member === null ? '없음' : `${user.recommander_member.name} [${user.recommander_member.email}]` }}</td>
          <td>
            <button type="button" class="btn btn-sm btn-danger" @click.prevent="deleteStoreUser(user)">삭제</button>
          </td>
        </tr>
        <tr>
          <td colspan="7" class="text-center" v-if="total == 0">표시할 항목이 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- TODO: 페이징 처리 추가 요망 -->
  <div class="table-footer-area" v-if="total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>
  <!-- End Pagination -->

  <!-- 송장번호 일괄등록 Modal -->
  <Modal :id="'customerExcelModal'" :title="'상점 이용자 일괄등록'">
    <template #body>
      <div class="mb-2">상점 이용자를 등록할 엑셀 파일을 업로드합니다.</div>
      <span class="text-danger mb-4">&#8251; 등록할 데이터가 많을 경우 시간이 다소 걸릴 수 있습니다.</span>

      <div class="row col mb-4 align-items-center mt-4">
        <div class="col-md-auto">
          <UploadExcel class="form-control" @upload="excelSelect" :btn="{ btnName: '엑셀 파일 선택', btnClass: 'btn btn-sm btn-info' }" />
        </div>
        <div class="col-md-auto mt-1" v-if="uploadFile">파일명 : {{ uploadFile.name }}</div>
        <div class="col-md-auto mt-1" v-else>[선택된 파일이 없습니다.]</div>
      </div>
      <a class="text-decoration-underline" href="" @click.prevent="downloadExcel">업로드 양식 엑셀 다운로드</a>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-sm btn-danger" @click.prevent="uploadExcelInfo">엑셀파일 업로드</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import type { UserList, User } from 'StoreMemberInfoModule';
import apis from '@/apis';
import { useRoute, useRouter } from 'vue-router';
import Pagination from '@/components/comm/Pagination.vue';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, hideModal, showAlert, showConfirm, showLogConsole, showModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import Modal from '@/components/comm/modal.vue';
import UploadExcel from '@/components/comm/UploadExcel.vue';
import * as XLSX from 'xlsx';

const storeCode = ref();
const mAbleTarget = ref('N');

const userList = ref({} as UserList['datas']);
const total = ref({} as UserList['total']);

const userListOrigin = ref({} as UserList['datas']);

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(total.value / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  reqUserList();
};

const selDetailSearch = reactive({
  items: [
    { name: '이름', value: 'name' },
    { name: '아이디', value: 'email' },
    { name: '추천인', value: 'recommend' },
  ],
  selectedItem: 'name',
  confirm: 'all',
  q: '',
  placeholder: '검색할 회원의 이름을 입력해주세요.',
});

const router = useRouter();

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'name':
      selDetailSearch.placeholder = '검색할 회원의 이름을 입력해주세요.';
      break;
    case 'email':
      selDetailSearch.placeholder = '검색할 회원의 아이디(이메일)을 입력해주세요.';
      break;
    case 'recommend':
      selDetailSearch.placeholder = '검색할 회원의 추천인을 입력해주세요.';
      break;
  }
};

const pageChange = (page: number) => {
  page_no.value = page;
  reqUserList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const clearSearchCondition = () => {
  selDetailSearch.selectedItem = 'name';
  selDetailSearch.q = '';
  selDetailSearch.confirm = 'all';
  reqUserList();
};

const reqUserList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  if (selDetailSearch.confirm !== 'all') {
    query = query.concat(query ? `&confirm=${selDetailSearch.confirm}` : `confirm=${selDetailSearch.confirm}`);
  }

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.store.get_store_user_list(storeCode.value, query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      userList.value = res.datas;
      total.value = res.total;
      userListOrigin.value = JSON.parse(JSON.stringify(res.datas));
    });
  });
};

const customerConfirmChange = (idx: number) => {
  const confirm = userList.value[idx].confirm === 'Y' ? '승인' : '미승인';
  showConfirm(
    `회원의 승인 여부를 ${confirm} 상태로 변경하시겠습니까?`,
    () => {
      apis.store.mod_store_user_status(storeCode.value, userList.value[idx].id, userList.value[idx].confirm).then(res => {
        apiResponseCheck(res, () => {
          showAlert('회원의 승인여부 상태가 변경되었습니다.');
          userListOrigin.value[idx].confirm = userList.value[idx].confirm;
        });
      });
    },
    () => {
      userList.value[idx].confirm = userListOrigin.value[idx].confirm;
    },
  );
};

const deleteStoreUser = (user: User) => {
  showConfirm(`[${user.customer.name} (${user.customer.email})] 회원을 상점에서 삭제하시겠습니까?`, () => {
    apis.store.delete_store_user(storeCode.value, user.id).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상점 이용 회원 목록에서 삭제되었습니다.');
        reqUserList();
      });
    });
  });
};

const openCustomerUpload = () => {
  showModal('customerExcelModal');
};

// 파일 업로드
const uploadFile = ref(null as File | null);

const excelSelect = (file: File) => {
  console.log(file);
  uploadFile.value = file;
};

const uploadExcelInfo = () => {
  if (!uploadFile.value) {
    showAlert('업로드할 엑셀 파일을 선택해주세요', 'warning');
    return;
  }

  showConfirm('엑셀 파일을 업로드 하시겠습니까?<br/><span class="text-danger">&#8251; 등록할 데이터가 많을 경우 시간이 다소 걸릴 수 있습니다.</span> ', () => {
    apis.customer.add_store_customer_list(storeCode.value, uploadFile.value!).then(res => {
      apiResponseCheck(res, () => {
        if (res?.fail_list?.length > 0) {
          let fail = makeFailList(res.fail_list);
          showAlert(`엑셀 파일이 성공적으로 업로드 되었습니다.<br/>등록 성공건수 : ${res?.success_count}건<br />실패내역은 아래 표와 같습니다.<br /><br />${fail}`, 'warning', () => {
            hideModal('customerExcelModal');
            reqUserList();
          });
        } else {
          showAlert(`엑셀 파일이 성공적으로 업로드 되었습니다.<br/>등록 성공건수 : ${res?.success_count}건`, 'success', () => {
            hideModal('customerExcelModal');
            reqUserList();
          });
        }
      });
    });
  });
};

const makeFailList = (list: []): string => {
  let fail = `<div class='' style="max-height: 300px; overflow-y: scroll"><table class="table table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th>대상</th>
          <th>사유</th>
        </tr>
      </thead>
      <tbody>`;
  for (const f of list) {
    console.log(f);
    if ((f as []).length > 1) {
      fail = fail.concat(`<tr class="text-center">
          <td>${f[0]}</td>
          <td>${f[1]}</td></tr>`);
    }
  }

  fail = fail.concat(`</tbody></table></div> `);
  return fail;
};

const clearUploadInfo = () => {
  uploadFile.value = null;
};

const downloadExcel = async () => {
  // @ts-ignore
  // 엑셀 파일 생성
  const book = XLSX.utils.book_new();

  // 엑셀에 넣을 데이터 만들기..
  const data = [] as any;
  data.unshift(['이메일', '이름']);

  // sheet 생성 - aoa_to_sheet 장식으로
  const worksheetByAoa = XLSX.utils.aoa_to_sheet(data);

  // 엑셀 파일에 sheet set (엑셀파일, 시트 데이터, 시트명)
  XLSX.utils.book_append_sheet(book, worksheetByAoa, '이용자 목록');

  // 엑셀 다운로드
  XLSX.writeFile(book, `이용자 일괄등록 업로드용 템플릿.xlsx`);
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');

  limit.value = useCommonStore().getLimit;
  storeCode.value = history.state.code;
  if (storeCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }

  const able = history.state.able;
  if (able) {
    mAbleTarget.value = able;
  }

  page_no.value > 1 ? reqUserList(false) : reqUserList();

  //@ts-ignore
  document.getElementById('customerExcelModal').addEventListener('show.bs.modal', function (event) {
    clearUploadInfo();
  });
});
</script>

<style scoped></style>
