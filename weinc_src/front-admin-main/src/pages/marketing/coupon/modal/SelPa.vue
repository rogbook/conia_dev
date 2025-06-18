<template>
  <div class="row">
    <div class="text-start mb-4">공급자(PA) 회원을 선택합니다.</div>
    <div class="card">
      <div class="card-body">
        <!-- Modal Search Form -->
        <div class="row align-items-center mb-2">
          <label class="col-md-2 col-form-label">회원타입</label>
          <div class="col form-control border-0">
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
        <div class="row col mb-4">
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
              <input type="text" class="form-control" id="q" v-model="selDetailSearch2.q" :placeholder="selDetailSearch2.placeholder" />
              <button type="button" class="btn btn-outline-dark col-md-2" @click.prevent="searchUser">검색</button>
            </div>
          </div>
        </div>
        <!-- Modal Search Form End -->
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

<script lang="ts" setup>
import { onMounted, reactive, ref, watch } from 'vue';
import apis from '@/apis';
import type { Class, User } from 'UserInfoModule';
import { apiResponseCheck } from '@/utils/common-utils';

const emits = defineEmits(['selectPa']);
const checkedTypes = ref('PA');
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
    case 'compnay_name':
      selDetailSearch2.placeholder = '검색할 회원의 회사명을 입력해주세요.';
      break;
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
  if (selDetailSearch2.q) {
    const detail = `${selDetailSearch2.selectedItem}=${selDetailSearch2.q}`;
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
const paInfo = reactive({
  id: 0,
  name: '',
  noPa: true,
});

const setPaInfo = (user: User) => {
  const paCompany = user?.company?.name ? user?.company?.name : '없음';
  paInfo.id = user.id;
  paInfo.name = `${user.name} ( 업체명 : ${paCompany} )`;

  emits('selectPa', paInfo.id, paInfo.name);
};
onMounted(() => {});
</script>
