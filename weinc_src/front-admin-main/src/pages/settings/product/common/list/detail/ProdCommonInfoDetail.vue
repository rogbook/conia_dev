<template>
  <PageNavigator :before_link="['상품공통정보관리']" :current="commonInfoId ? '상품공통정보관리 상세' : '신규 상품공통정보 생성'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center" v-if="commonInfoId">
        <div class="col-auto">
          <div class="form-control-borderless h2">상품공통정보관리</div>
          <div class="form-control-borderless h4">상품공통정보명 : [{{ commonInfo.name }}]</div>
        </div>
      </div>
      <div class="row justify-content-between align-items-center" v-else>
        <div class="col-auto">
          <div class="form-control-borderless h2">신규 상품공통정보 생성</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="row col mb-4 align-items-center" v-if="!commonInfoId && getUserClassStr.includes('CM')">
        <label class="col-md-1 col-form-label">템플릿 여부</label>
        <div class="col-auto">
          <div class="form-check form-check-inline">
            <input id="radio_template_y" type="radio" class="form-check-input" name="radio_template_yn" value="Y" v-model="isTemplate" />
            <label class="form-check-label" for="radio_template_y">예</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-check form-check-inline">
            <input id="radio_template_n" type="radio" class="form-check-input" name="radio_template_yn" value="N" v-model="isTemplate" />
            <label class="form-check-label" for="radio_template_n">아니오</label>
          </div>
        </div>
      </div>
      <div class="row col mb-4 align-items-center" v-if="!commonInfoId && isTemplate === 'N' && getUserClassStr.includes('CM')">
        <label class="col-md-1 col-form-label">공급자(PA)</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" v-model="paInfo.name" placeholder="공급자(PA)를 선택해주세요." aria-label="" disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('paMemberSelModal')">검색</button>
          </div>
        </div>
      </div>
      <div class="row col mb-4 align-items-center">
        <label class="col-md-1 col-form-label">상폼공통정보명</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="상폼공통정보명 입력해주세요." v-model.trim="commonInfo.name" />
          </div>
        </div>
      </div>
      <div class="row col mb-2 align-items-center" v-if="commonInfoId">
        <label class="col-md-1 col-form-label text-nowrap">사용여부</label>
        <div class="col-auto">
          <div class="form-check form-check-inline">
            <input id="radio_status_y" type="radio" class="form-check-input" name="radio_status" value="Y" v-model="commonInfo.status" />
            <label class="form-check-label" for="radio_status_y">사용</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-check form-check-inline">
            <input id="radio_status_n" type="radio" class="form-check-input" name="radio_status" value="N" v-model="commonInfo.status" />
            <label class="form-check-label" for="radio_status_n">사용안함</label>
          </div>
        </div>
      </div>
      <div class="common-info-contents">
        <label class="col-2 col-form-label text-nowrap">상품공통정보 내용</label>
        <CKEditorCustom @receiveData="receiveData" ref="ckeditorCustom" :removeItems="removeItems" :editorData="editorData" />
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="row align-items-center justify-content-center">
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="saveClick" v-if="!commonInfoId">상품공통정보 등록</button>
          <button type="button" class="btn btn-sm btn-warning" @click.prevent="saveClick" v-else>상품공통정보 수정</button>
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
                    <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                      <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
                    </select>
                  </div>
                  <!-- End Select -->
                </div>
                <div class="d-md-none mt-1"></div>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="searchUser" />
                    <button type="button" class="btn btn-outline-dark col-md-2" @click.prevent="searchUser">검색</button>
                  </div>
                </div>
              </div>
            </form>
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
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import CKEditorCustom from '@/pages/settings/product/common/list/detail/CKEditorCustom.vue';
import apis from '@/apis';
import type { Class, User } from 'UserInfoModule';
import type { ProdCommonInfo } from 'ProdCommonInfoListModule';
import { useUserStore } from '@/stores/user';
import { apiResponseCheck, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import Modal from '@/components/comm/modal.vue';

const router = useRouter();
const commonInfoId = ref();
const commonInfo = ref({} as ProdCommonInfo);
const originCommonInfo = ref({} as ProdCommonInfo);

const isTemplate = ref('N');

const ckeditorCustom = ref();
const removeItems = ref(['imageUpload']);
const editorData = ref('');
const checkedTypes = ref('PA');
const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

const getCommonInfo = () => {
  apis.common.get_prod_common_info(commonInfoId.value).then(res => {
    apiResponseCheck(res, () => {
      commonInfo.value = res;
      originCommonInfo.value = JSON.parse(JSON.stringify(res));
      editorData.value = commonInfo.value.contents;
    });
  });
};

const saveClick = () => {
  ckeditorCustom.value.saveClicked();
};

const receiveData = (data: string) => {
  if (!commonInfo.value.name) {
    showAlert('상품공통정보명을 입력해주세요.', 'warning');
    return;
  }
  if (!data.trim()) {
    showAlert('상품공통정보 내용을 입력해주세요.', 'warning');
    return;
  }

  if (commonInfoId.value) {
    //수정
    let modData = {} as any;
    if (originCommonInfo.value.name !== commonInfo.value.name) {
      modData['name'] = commonInfo.value.name;
    }

    if (originCommonInfo.value.status !== commonInfo.value.status) {
      modData['status'] = commonInfo.value.status;
    }

    if (originCommonInfo.value.contents !== data) {
      modData['contents'] = data;
    }

    if (Object.keys(modData).length === 0) {
      showAlert('변경 사항이 없습니다.', 'warning');
      return;
    }

    showConfirm('상품공통정보를 수정하시겠습니까?', () => {
      apis.common.mod_prod_common_info(commonInfoId.value, modData).then(res => {
        apiResponseCheck(res, () => {
          showAlert('수정 되었습니다.', 'success', () => {
            if (window.history.length > 1) {
              router.back();
            } else {
              router.replace('/');
            }
          });
        });
      });
    });
  } else {
    if (getUserClassStr.value.includes('CM')) {
      if (isTemplate.value === 'N' && !paInfo.id) {
        showAlert('공급자(PA)를 선택해주세요.', 'warning');
        return;
      }
    }
    //등록
    showConfirm('상품공통정보를 등록하시겠습니까?', () => {
      const obj: any = { name: commonInfo.value.name, contents: data };
      if (!userClass.value.includes('CM')) {
        obj['member_id'] = useUserStore().user.id;
      } else {
        if (isTemplate.value === 'N') {
          obj['member_id'] = paInfo.id;
        }
      }
      apis.common.reg_prod_common_info(obj).then(res => {
        apiResponseCheck(res, () => {
          showAlert('등록 되었습니다.', 'success', () => {
            if (window.history.length > 1) {
              router.back();
            } else {
              router.replace('/');
            }
          });
        });
      });
    });
  }
};

// 공금자(PA) 관련
const paInfo = reactive({
  id: 0,
  name: '',
  noPa: true,
});

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
      showLogConsole(res.datas);
      searchUserList.value.data = res.datas;
    });
  });
};

const setPaInfo = (user: User) => {
  if (!user.company) {
    showAlert('사업자 정보가 없는 공급자(PA) 회원입니다.\n 사업자 정보를 확인해주세요.', 'warning', () => {
      return;
    });
  } else {
    const paCompany = user?.company?.name ? user?.company?.name : '없음';
    paInfo.id = user.id;
    paInfo.name = `${user.name} ( 업체명 : ${paCompany} )`;

    hideModal('paMemberSelModal');
  }
};

onMounted(() => {
  const id = history.state.id;

  if (id) {
    commonInfoId.value = id;

    getCommonInfo();
  }
});
</script>

<style scoped></style>
