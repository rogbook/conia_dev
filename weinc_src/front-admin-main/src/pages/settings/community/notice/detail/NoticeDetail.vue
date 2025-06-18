<template>
  <PageNavigator :before_link="['공지사항 관리']" :current="'공지사항 상세'" />
  <div class="card col-lg-8">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center" v-if="noticeId">
        <div class="col-auto">
          <div class="form-control-borderless h2">공지사항</div>
          <div class="form-control-borderless h4">제목 : [{{ noticeInfo.title }}]</div>
        </div>
      </div>
      <div class="row justify-content-between align-items-center" v-else>
        <div class="col-auto">
          <div class="form-control-borderless h2">공지사항 신규등록</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card col">
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-3 col-form-label">노출대상</label>
            <div class="col">
              <div class="tom-select-custom col-auto">
                <select class="form-select" v-model="selectedTarget" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option value="0" disabled>노출대상을 선택해주세요</option>
                  <option v-for="target in commonInfoList" :key="JSON.stringify(target)" v-text="target.name" :value="target.value"></option>
                </select>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="selectedTarget === 'partner'">
            <label class="col-md-3 col-form-label">파트너 대상</label>
            <div class="col-auto" v-for="item in classList">
              <div class="form-check form-check-inline">
                <input :id="`partner_class${item.code}`" type="radio" class="form-check-input" name="partner_class" :value="item.code === 'partner' ? item.code : `partner_${item.code}`" v-model="partnerClass" />
                <label class="form-check-label" :for="`partner_class${item.code}`">{{ item.name }}</label>
              </div>
            </div>
          </div>
          <!-- 상점(몰) 검색 -->
          <div class="row col mb-2" v-if="selectedTarget === 'customer'">
            <label class="col-md-3 col-form-label">상점 선택</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="운영중인 상점을 선택해주세요." v-model="selectedStoreInfo.name" readonly />
                <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="showModal('findStoreModal')">상점 선택</button>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-3 col-form-label">공지사항 상단고정</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_open_y" type="radio" class="form-check-input" name="radio_store_open" value="Y" v-model="noticeInfo.pin" />
                <label class="form-check-label" for="radio_open_y">상단고정</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_open_n" type="radio" class="form-check-input" name="radio_store_open" value="N" v-model="noticeInfo.pin" />
                <label class="form-check-label" for="radio_open_n">일반</label>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="false">
            <label class="col-md-3 col-form-label">우선순위</label>
            <div class="col">
              <div class="input-group">
                <input type="number" class="form-control" placeholder="1-99 까지의 숫자만 입력해주세요." v-model="noticeInfo.sort" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-3 col-form-label">공지 제목</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="공지사항 제목을 입력해주세요." v-model.trim="noticeInfo.title" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-3 col-form-label">공지 내용</label>
            <div class="col">
              <CKEditorCustom @receiveData="newReceiveData" ref="newCkeditorCustom" :removeItems="removeItems" :editor-data="editorData" />
            </div>
          </div>
        </div>
        <div class="card-footer py-2" v-if="noticeId">
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-primary" @click.prevent="modNoticeInfo">공지사항 저장</button>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2" v-if="!noticeId">
      <div class="row align-items-center justify-content-center">
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="addNoticeInfo">공지사항 등록</button>
        </div>
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
                <label class="col-1 col-form-label text-nowrap">상점검색</label>
                <div class="col-2"></div>
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
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import CKEditorCustom from '@/pages/settings/product/common/list/detail/CKEditorCustom.vue';
import Modal from '@/components/comm/modal.vue';
import type { StoreList } from 'StoreListInfoModule';
import { useUserStore } from '@/stores/user';
import PageNavigator from '@/components/title/PageNavigator.vue';

const router = useRouter();

const noticeId = ref();
const memberId = ref(useUserStore().user.id as number);
const noticeInfo = reactive({
  title: '',
  contents: '',
  target: '',
  pin: 'N',
  sort: 99,
  reg_date: '',
  mod_date: '',
  store_code: '',
});

const selectedStoreInfo = reactive({
  name: '',
  code: '',
});

const store_title = ref('');
const storeList = ref({} as StoreList);
const classList = ref([
  {
    code: '',
    name: '',
    description: '',
  },
]);
const partnerClass = ref('');

const setStore = (title: string, code: string) => {
  hideModal('findStoreModal');
  selectedStoreInfo.name = title;
  selectedStoreInfo.code = code;
  noticeInfo.store_code = code;

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

const newCkeditorCustom = ref();
const removeItems = ref(['imageUpload']);
const editorData = ref('');

const selectedTarget = ref('admin');
const commonInfoList = ref([
  { name: '관리자', value: 'admin' },
  { name: '파트너', value: 'partner' },
  { name: '일반회원', value: 'customer' },
]);

const newReceiveData = (data: string) => {
  noticeInfo.contents = data;
};

const getNoticeInfo = () => {
  apis.community.get_notice(noticeId.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      noticeInfo.title = res.title;
      noticeInfo.target = res.target;
      selectedTarget.value = res.target;
      noticeInfo.contents = res.contents;
      editorData.value = res.contents;
      noticeInfo.pin = res.pin;
      noticeInfo.sort = res.sort;
      noticeInfo.reg_date = res.reg_date;
      noticeInfo.mod_date = res.mod_date;
      if (res.store_code) {
        noticeInfo.store_code = res.store_code;
        selectedStoreInfo.code = res.store?.code;
        selectedStoreInfo.name = res.store?.title;
      }

      if (selectedTarget.value.startsWith('partner')) {
        selectedTarget.value = 'partner';
        partnerClass.value = res.target;
      }
    });
  });
};

const getClassList = () => {
  apis.user.get_class().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      for (let i in res) {
        if (res[i].code === 'CM') {
          res.splice(i, 1);
          break;
        }
      }
      classList.value = res;
      classList.value.unshift({ code: 'partner', name: '파트너 전체', description: '' });
    });
  });
};

const addNoticeInfo = () => {
  newCkeditorCustom.value.saveClicked();

  if (selectedTarget.value === 'partner' && !partnerClass.value) {
    showAlert('파트너 대상을 선택해주세요.', 'warning');
    return;
  }

  if (!noticeInfo.title) {
    showAlert('공지사항 제목을 입력해주세요.', 'warning');
    return;
  }

  if (!noticeInfo.contents) {
    showAlert('공지사항 내용을 입력해주세요.', 'warning');
    return;
  }

  showConfirm('공지사항을 등록하시겠습니까?', () => {
    const data: any = { title: noticeInfo.title, contents: noticeInfo.contents, pin: noticeInfo.pin, target: selectedTarget.value, status: 'Y', member_id: memberId.value };
    if (selectedTarget.value === 'customer' && selectedStoreInfo.code) {
      data['store_code'] = selectedStoreInfo.code;
    }
    if (selectedTarget.value === 'partner') {
      data['target'] = partnerClass.value;
    }

    apis.community.add_notice(data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('공지사항이 등록되었습니다.', 'success', () => {
          if (window.history.length > 1) {
            router.back();
          } else {
            router.replace('/');
          }
        });
      });
    });
  });
};

const modNoticeInfo = () => {
  newCkeditorCustom.value.saveClicked();

  if (!noticeInfo.title) {
    showAlert('공지사항 제목을 입력해주세요.', 'warning');
    return;
  }

  if (!noticeInfo.contents) {
    showAlert('공지사항 내용을 입력해주세요.', 'warning');
    return;
  }

  showConfirm('공지사항을 수정하시겠습니까?', () => {
    const data: any = { title: noticeInfo.title, contents: noticeInfo.contents, category: noticeInfo.category, target: selectedTarget.value };
    if (selectedTarget.value === 'customer' && selectedStoreInfo.code) {
      data['store_code'] = selectedStoreInfo.code;
    }
    if (selectedTarget.value === 'partner') {
      data['target'] = partnerClass.value;
    }

    apis.community.mod_notice(noticeId.value, data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('공지사항이 수정되었습니다.', 'success', () => {
          if (window.history.length > 1) {
            router.back();
          } else {
            router.replace('/');
          }
        });
      });
    });
  });
};

onMounted(() => {
  const id = history.state.id;
  getClassList();
  if (id) {
    noticeId.value = id;
    getNoticeInfo();
  }
});
</script>

<style scoped></style>
