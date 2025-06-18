<template>
  <PageNavigator :before_link="[]" :current="'배송비 수수료 설정'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">배송비 수수료 설정</div>
    </div>
    <div class="card-body">
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
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="reqUserList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="reqUserList">검색</button>
      </div>
    </div>
  </div>
  <span class="divider-center py-4">검색결과</span>
  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="userList.total > 0">총 : {{ userList.total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>
  <div class="table-responsive">
    <table class="table table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th>회원타입</th>
          <th>이름</th>
          <th>아이디</th>
          <th>사업자명</th>
          <th>가입일시</th>
          <th style="width: 10%">수수료 설정</th>
        </tr>
      </thead>
      <tbody>
        <!-- 회원 검색 결과 목록 테이블 -->
        <tr class="text-center" v-for="(user, i) in userList.data" :key="user.id">
          <td>{{ getUserClass(user.classes) }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user?.company?.name ? user?.company?.name : '사업자정보 없음' }}</td>
          <td>{{ dateTimeFormatConverter(user.reg_date) }}</td>
          <td>
            <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ name: 'paShipCommission', state: { memberId: user.id, memberInfo: { email: user.email, name: user.name, company: user.company.name } } })">설정</button>
          </td>
        </tr>
        <tr>
          <td colspan="6" class="text-center" v-if="userList.total == 0">표시할 항목이 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-footer-area" v-if="userList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>
  <!-- End Pagination -->
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import type { User, Class } from 'UserInfoModule';
import apis from '@/apis';
import { useRouter } from 'vue-router';
import Pagination from '@/components/comm/Pagination.vue';
import { apiResponseCheck, checkPermission, dateTimeFormatConverter, showAlert, showLogConsole } from '@/utils/common-utils';
import { useUserStore } from '@/stores/user';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

const userList = ref({
  data: {} as User[],
  total: 0,
});

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(userList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  reqUserList();
};

const selDetailSearch = reactive({
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

const router = useRouter();

const onChangeDetailSearch = () => {
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

const pageChange = (page: number) => {
  page_no.value = page;
  reqUserList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const reqUserList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  let query = '';
  query = query.concat(`class_code=PA`);

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.user.get_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      userList.value.data = res.datas;
      userList.value.total = res.total;
    });
  });
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

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
  limit.value = useCommonStore().getLimit;
  if (checkPermission('read:commission_conia')) {
    reqUserList();
  } else {
    showAlert('비정상적인 접근입니다.', 'error', () => {
      useRouter().back();
    });
  }
});
</script>

<style scoped></style>
