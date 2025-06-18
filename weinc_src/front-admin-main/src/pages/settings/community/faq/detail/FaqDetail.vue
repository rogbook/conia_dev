<template>
  <PageNavigator :before_link="['FAQ 관리']" :current="faqId ? 'FAQ 상세' : 'FAQ 신규 등록'" />
  <div class="card col-lg-6">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center" v-if="faqId">
        <div class="col">
          <div class="form-control-borderless h2">자주하는질문</div>
          <div class="form-control-borderless h4">제목: [{{ faqInfo.title }}]</div>
        </div>
        <div class="col-auto">
          <div class="text-end">
            <button class="btn btn-sm btn-outline-danger" @click.prevent="delFaqInfo">삭제</button>
          </div>
        </div>
      </div>
      <div class="row justify-content-between align-items-center" v-else>
        <div class="col-auto">
          <div class="form-control-borderless h2">자주하는질문 신규등록</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card col">
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-3 col-form-label">질문분류</label>
            <div class="col">
              <div class="tom-select-custom col-auto">
                <select class="form-select" v-model="selectedCate" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option value="" disabled>질문분류를 선택해주세요</option>
                  <option v-for="target in faqCateList" :key="target.id" v-text="target.category" :value="target.category"></option>
                </select>
              </div>
            </div>
          </div>
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
            <label class="col-md-3 col-form-label">제목(질문내용)</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="제목(질문내용)을 입력해주세요." v-model.trim="faqInfo.title" maxlength="30" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-3 col-form-label">내용(질문답변)</label>
            <div class="col">
              <CKEditorCustom @receiveData="newReceiveData" ref="newCkeditorCustom" :removeItems="removeItems" :editor-data="editorData" />
            </div>
          </div>
        </div>
        <div class="card-footer py-2" v-if="faqId">
          <div class="text-end">
            <button class="btn btn-sm btn-primary" @click.prevent="modFaqInfo">자주하는질문 저장</button>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2" v-if="!faqId">
      <div class="row align-items-center justify-content-center">
        <div class="col-auto">
          <button class="btn btn-sm btn-primary" @click.prevent="addFaqInfo">자주하는질문 등록</button>
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
import type { FaqInfo } from 'BoardInfoModule';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import CKEditorCustom from '@/pages/settings/product/common/list/detail/CKEditorCustom.vue';
import Modal from '@/components/comm/modal.vue';
import type { StoreList } from 'StoreListInfoModule';
import PageNavigator from '@/components/title/PageNavigator.vue';

interface FaqCate {
  id: number;
  category: string;
  sort: number;
}

const router = useRouter();

const faqId = ref();
const faqInfo = reactive({
  title: '',
  contents: '',
  category: '',
  target: '',
  reg_date: '',
  mod_date: '',
  store_code: '',
});

const originFaq = ref({} as FaqInfo);

const selectedStoreInfo = reactive({
  name: '',
  code: '',
});

const store_title = ref('');
const storeList = ref({} as StoreList);

const setStore = (title: string, code: string) => {
  hideModal('findStoreModal');
  selectedStoreInfo.name = title;
  selectedStoreInfo.code = code;
  faqInfo.store_code = code;

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
const removeItems = ref(['imageUpload', 'insertTable']);
const editorData = ref('');

const selectedTarget = ref('admin');
const commonInfoList = ref([
  { name: '관리자', value: 'admin' },
  { name: '파트너', value: 'partner' },
  { name: '일반회원', value: 'customer' },
]);

const newReceiveData = (data: string) => {
  faqInfo.contents = data;
};

const getFaqInfo = () => {
  apis.community.get_faq(faqId.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      originFaq.value = JSON.parse(JSON.stringify(res));
      faqInfo.title = res.title;
      faqInfo.target = res.target;
      faqInfo.category = res.category;
      selectedCate.value = res.category;
      faqInfo.contents = res.contents;
      editorData.value = res.contents;
      faqInfo.reg_date = res.reg_date;
      faqInfo.mod_date = res.mod_date;
      if (res.store_code) {
        faqInfo.store_code = res.store_code;
        selectedStoreInfo.code = res.store_code;
      }
    });
  });
};

const addFaqInfo = () => {
  newCkeditorCustom.value.saveClicked();
  if (!selectedCate.value) {
    showAlert('질문 분류를 선택해주세요.', 'warning');
    return;
  }

  if (!faqInfo.title) {
    showAlert('제목(질문내용)을 입력해주세요.', 'warning');
    return;
  }

  if (!faqInfo.contents) {
    showAlert('내용(질문답변)을 입력해주세요.', 'warning');
    return;
  }

  showConfirm('자주하는질문을 등록하시겠습니까?', () => {
    const data: any = { title: faqInfo.title, contents: faqInfo.contents, category: selectedCate.value, target: selectedTarget.value };
    if (selectedTarget.value === 'customer' && selectedStoreInfo.code) {
      data['store_code'] = selectedStoreInfo.code;
    }
    apis.community.add_faq(data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('자주하는질문이 등록되었습니다.', 'success', () => {
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

const modFaqInfo = () => {
  newCkeditorCustom.value.saveClicked();
  if (!selectedCate.value) {
    showAlert('질문 분류를 선택해주세요.', 'warning');
    return;
  }

  if (!faqInfo.title) {
    showAlert('제목(질문내용)을 입력해주세요.', 'warning');
    return;
  }

  if (!faqInfo.contents) {
    showAlert('내용(질문답변)을 입력해주세요.', 'warning');
    return;
  }

  let data: any = {};
  if (faqInfo.target !== originFaq.value.target) {
    data['target'] = faqInfo.target;
  }

  if (selectedCate.value !== originFaq.value.category) {
    data['category'] = selectedCate.value;
  }

  if (faqInfo.title !== originFaq.value.title) {
    data['title'] = faqInfo.title;
  }

  if (faqInfo.contents !== originFaq.value.contents) {
    data['contents'] = faqInfo.contents;
  }

  if (selectedTarget.value === 'customer' && faqInfo.store_code !== originFaq.value.store_code) {
    data['store_code'] = faqInfo.store_code;
  }

  if (Object.keys(data).length === 0) {
    showAlert('변경된 내용이 없습니다.', 'warning');
    return;
  }

  showConfirm('자주하는질문을 수정하시겠습니까?', () => {
    apis.community.mod_faq(faqId.value, data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('자주하는질문이 등록되었습니다.', 'success', () => {
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

const delFaqInfo = () => {
  showConfirm('해당 자주하는질문을 삭제하시겠습니까?', () => {
    apis.community.del_faq(faqId.value).then(res => {
      apiResponseCheck(res, () => {
        showAlert('자주하는질문에서 삭제되었습니다.', 'success', () => {
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

const faqCateList = ref([] as FaqCate[]);
const selectedCate = ref('');

const getFaqCategory = () => {
  apis.community.faq_cate_list().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      faqCateList.value = res;
    });
  });
};

onMounted(() => {
  getFaqCategory();
  const id = history.state.id;
  if (id) {
    faqId.value = id;
    getFaqInfo();
  }
});
</script>

<style scoped></style>
