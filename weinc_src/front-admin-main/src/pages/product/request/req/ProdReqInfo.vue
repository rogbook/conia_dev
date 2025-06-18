<template>
  <div class="card col-md-8">
    <div class="card-header">
      <div class="form-control-borderless h2">상품 요청</div>
    </div>
    <div class="card-body">
      <!-- 상점(몰) 검색 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label">상점 선택</label>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="운영중인 상점을 선택해주세요." v-model="reqProdInfo.store.store_name" readonly />
            <button v-if="getUserClassStr.includes('CM')" type="button" class="btn btn-sm btn-outline-info" @click.prevent="showModal('findStoreModal')">상점 선택</button>
          </div>
        </div>
      </div>
      <!-- 요청 내용 입력 -->
      <div class="row col mb-3">
        <label class="col-md-2 col-form-label">상품 요청 내용</label>
        <div class="col">
          <textarea type="text" class="form-control" maxlength="255" placeholder="요청할 내용을 입력해주세요" v-model="reqProdInfo.memo" style="height: 200px" />
        </div>
      </div>
      <!-- 상품 선택 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label">요청 상품 대상 목록</label>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="showModal('selProdModal')">상품 조회</button>
        </div>
      </div>
      <div class="table-responsive datatable-custom position-relative">
        <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
          <thead class="thead-light">
            <tr class="text-center">
              <th>상품코드</th>
              <th>이미지</th>
              <th>상품명</th>
              <th>삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in selectedProdList" :key="item.id">
              <td>{{ item.code }}</td>
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
                <button type="button" class="btn btn-sm border-0 p-0" @click.prevent="removeProdList(i)"><i class="bi-x-circle text-danger"></i></button>
              </td>
            </tr>
            <tr class="text-center" v-if="selectedProdList.length === 0">
              <td colspan="4">선택된 상품이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="card-footer py-3">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="reqProduct">상품요청</button>
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
            <div class="table-responsive">
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

  <Modal :id="'selProdModal'" :title="'요청할 상품 검색'" :xlarge="true">
    <template #header> </template>
    <template #body>
      <SelectProdReq @selectedProd="selectedProd" />
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import Modal from '@/components/comm/modal.vue';
import { apiResponseCheck, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import apis from '@/apis';
import { AxiosError } from 'axios';
import type { StoreList } from 'StoreListInfoModule';
import SelectProdReq from '@/pages/product/request/req/SelectProdReq.vue';
import type { Prod } from 'ProductListInfoModule';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const reqProdInfo = reactive({
  store: {
    store_code: '',
    store_name: '',
  },
  title: '',
  memo: '',
  product_id: [] as number[],
});

const store_title = ref('');
const storeList = ref({} as StoreList);

const selectedProdList = ref([] as Prod[]);

const reqStoreList = () => {
  if (!store_title.value) {
    if (getUserClassStr.value.includes('CM')) {
      //검색어 입력함.
      apis.store.get_list(`title=${store_title.value}&`).then(res => {
        apiResponseCheck(res, () => {
          showLogConsole(res);
          storeList.value = res;
        });
      });
    } else {
      //검색어 입력안함.
      showAlert('검색할 상점의 이름을 입력해주세요.', 'warning');
      return;
    }
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

const removeProdList = (idx: number) => {
  selectedProdList.value.splice(idx, 1);
};

const setStore = (title: string, code: string) => {
  hideModal('findStoreModal');
  reqProdInfo.store.store_name = title;
  reqProdInfo.store.store_code = code;

  store_title.value = '';
  storeList.value = {} as StoreList;
};

const selectedProd = (list: Prod[]) => {
  hideModal('selProdModal');

  for (const prod of list) {
    if (selectedProdList.value.some(item => item.id === prod.id)) {
      // DO Nothing
    } else {
      selectedProdList.value.push(prod);
    }
  }
};

const reqProduct = () => {
  if (!reqProdInfo.store.store_code) {
    showAlert('운영중인 상점을 선택해주세요.', 'warning');
    return;
  }

  if (selectedProdList.value.length === 0) {
    showAlert('요청할 상품을 선택해주세요.', 'warning');
    return;
  }

  reqProdInfo.title = selectedProdList.value.length > 1 ? `${selectedProdList.value[0].name} 외 ${selectedProdList.value.length - 1}건` : selectedProdList.value[0].name;
  for (const prod of selectedProdList.value) {
    reqProdInfo.product_id.push(prod.id);
  }

  showConfirm('상품을 요청하시겠습니까?', () => {
    const data: { store_code: string; title: string; memo?: string; product_ids: number[] } = { store_code: reqProdInfo.store.store_code, title: reqProdInfo.title, product_ids: reqProdInfo.product_id };
    if (reqProdInfo.memo) {
      data['memo'] = reqProdInfo.memo;
    }
    apis.product.reqProdReq(data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 요청이 완료되었습니다.', 'success');
        router.push('/product/req/list');
      });
    });
  });
};

const getStoreInfo = (storeCode: string) => {
  apis.store.get_store(storeCode).then(res => {
    apiResponseCheck(res, () => {
      reqProdInfo.store.store_name = res.title;
      reqProdInfo.store.store_code = res.code;
    });
  });
};

onMounted(() => {
  if (!getUserClassStr.value.includes('CM')) {
    // @ts-ignore
    const myStore: any[] = useUserStore().user.organization?.my_store as any[];
    if (myStore.length > 0) {
      getStoreInfo(myStore[0]);
    }
  }
});
</script>

<style scoped></style>
