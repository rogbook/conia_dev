<template>
  <PageNavigator :before_link="[]" :current="'코니아 수수료 설정'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">코니아 수수료 설정</div>
    </div>
    <div class="card-body">
      <div class="row col mb-2">
        <label class="col-md-3 col-form-label">기본 수수료율 설정 (0.01% ~ 100%)</label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="text" class="form-control" inputmode="decimal" placeholder="기본 수수료율을 입력해주세요 (0.01% ~ 100%)" v-model="mDefaultCommission" @input="checkCommissionDefault($event)" :disabled="!checkPermission('write:commission_conia')" />
            <span class="input-group-text">%</span>
          </div>
        </div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="modDefaultCommission" v-if="mDefaultCommission.toString() !== mDefaultCommissionOrigin.toString()">저장</button>
        </div>
      </div>
      <div class="row col mb-2">
        <label class="col-md-3 col-form-label">기본 배송비 수수료율 설정 (0.01% ~ 100%)</label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="text" class="form-control" inputmode="decimal" placeholder="기본 배송비 수수료율을 입력해주세요 (0.01% ~ 100%)" v-model="mDefaultShipCommission.value" @input="checkShipCommissionDefault($event)" :disabled="!checkPermission('write:commission_conia')" />
            <span class="input-group-text">%</span>
          </div>
        </div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="modDefaultShipCommission" v-if="mDefaultShipCommission.value.toString() !== mDefaultShipCommissionOrigin.value.toString()">저장</button>
        </div>
      </div>
      <div class="row col-md-6 mb-2">
        <label class="col-md-3 col-form-label">설정된 PG 수수료 목록</label>
        <div class="table-responsive">
          <table class="table table-nowrap table-align-middle card-table col-6">
            <thead class="thead-light">
              <tr class="text-center">
                <th>PG사</th>
                <th>결제방식</th>
                <th>수수료타입 (비율/고정)</th>
                <th>수수료</th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-center" v-for="c in mPgCommissionList" :key="c.id">
                <td>{{ c.pg_provider }}</td>
                <td>{{ c.pg_kind }}</td>
                <td>{{ c.type === 'P' ? '비율' : c.type === 'F' ? '고정' : '-' }}</td>
                <td>{{ c.value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="card-footer py-2" v-if="checkPermission('write:commission_conia')">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning" @click.prevent="showModal('addNewCommission')">개별 설정 추가</button>
      </div>
    </div>
  </div>
  <span class="divider-center py-4">추가 설정된 수수료 목록</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mCommissionList.total > 0">총 : {{ mCommissionList.total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <table class="table table-nowrap table-align-middle card-table">
    <thead class="thead-light">
      <tr class="text-center">
        <th style="width: 10%">상점코드</th>
        <th>상품명</th>
        <th style="width: 20%">수수료율</th>
        <th style="width: 10%" v-if="checkPermission('write:commission_conia')">삭제</th>
      </tr>
    </thead>
    <tbody>
      <!-- 수수료 목록 테이블 -->
      <tr class="text-center" v-for="(commission, i) in mCommissionList.datas" :key="commission.id">
        <td>{{ commission.store ? commission.store.title : '-' }}</td>
        <td v-if="commission.product">
          <div class="row align-items-center justify-content-center">
            <div class="img-area col-auto">
              <div class="avatar" v-if="commission.product.photos.length > 0">
                <img class="avatar-img" :src="commission.product.photos[0].uri" alt="Image Description" />
              </div>
              <div class="avatar" v-if="commission.product.photos.length === 0">
                <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
              </div>
            </div>
            <div class="col-auto">
              {{ commission.product.name }}
            </div>
          </div>
        </td>
        <td v-else>-</td>
        <td style="width: 25%">
          <div class="row align-items-center justify-content-center">
            <div class="col-auto">
              <div class="input-group">
                <input type="text" class="form-control" inputmode="decimal" placeholder="수수료율을 입력해주세요 (0.01% ~ 100%)" v-model="commission.value" @input="checkCurrentCommission($event, i)" :disabled="!checkPermission('write:commission_conia')" />
                <span class="input-group-text">%</span>
              </div>
            </div>
            <div class="col-auto">
              <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="modListCommission(i)" v-if="commission.value !== mCommissionOriginList.datas[i].value">저장</button>
            </div>
          </div>
        </td>
        <td v-if="checkPermission('write:commission_conia')">
          <button type="button" class="btn btn-sm btn-danger" @click.prevent="deleteCommission(commission.id)">삭제</button>
        </td>
      </tr>
      <tr>
        <td colspan="4" class="text-center" v-if="mCommissionList.total == 0">표시할 항목이 없습니다.</td>
      </tr>
    </tbody>
  </table>
  <!-- Pagination -->
  <div class="table-footer-area" v-if="mCommissionList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>
  <!-- End Pagination -->

  <!-- 추가 수수료 등록 Modal -->
  <Modal :id="'addNewCommission'" :title="'추가적인 수수료 설정 등록'">
    <template #body>
      <div class="card">
        <div class="card-body">
          <div class="row col align-items-center mb-2">
            <label class="col-md-3 col-form-label">설정 대상</label>
            <div class="col">
              <div class="row align-items-center form-control border-0">
                <div class="col-auto form-check form-check-inline">
                  <input type="radio" id="radio_status_store" class="form-check-input" name="radio_status" value="store" v-model="newCommissionInfo.kind" />
                  <label class="form-check-label px-1" for="radio_status_store">상점</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input type="radio" id="radio_status_prod" class="form-check-input" name="radio_status" value="prod" v-model="newCommissionInfo.kind" />
                  <label class="form-check-label px-1" for="radio_status_prod">상품</label>
                </div>
              </div>
            </div>
          </div>

          <div class="row col mb-2 align-items-center" v-if="newCommissionInfo.kind === 'store'">
            <label class="col-md-3 col-form-label">대상 상점</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="대상 상점을 선택해주세요." :value="newCommissionInfo.store_title" readonly />
                <button type="button" class="btn btn-outline-info" @click.prevent="openStoreModal">검색</button>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="newCommissionInfo.kind === 'prod'">
            <label class="col-md-3 col-form-label">대상 상품</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="대상 상품을 선택해주세요." :value="newCommissionInfo.product_title" readonly />
                <button type="button" class="btn btn-outline-info" @click.prevent="openProdModal">검색</button>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-3 col-form-label">수수료율 설정 (0.01% ~ 100%)</label>
            <div class="col-auto">
              <div class="input-group">
                <input type="text" class="form-control" inputmode="decimal" placeholder="기본 수수료율을 입력해주세요 (0.01% ~ 100%)" v-model="newCommissionInfo.value" @input="checkNewCommission($event)" />
                <span class="input-group-text">%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="addNewCommission">등록</button>
    </template>
  </Modal>
  <!-- 추가 수수료 등록 Modal END -->

  <!-- 상점 검색 Modal -->
  <Modal :id="'searchStoreModal'" :title="'수수료 설정 대상 상점 선택'" :xlarge="true" :second="true">
    <template #body>
      <AllStoreListModal ref="storeModal" @selectStore="selectStore" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
  <!-- 상점 검색 Modal END -->

  <!-- 상품 검색 Modal -->
  <Modal :id="'searchProdModal'" :title="'수수료 설정 대상 상품 선택'" :xlarge="true" :second="true">
    <template #body>
      <AllProdListModal ref="prodModal" @selectProd="selectProd" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
  <!-- 상품 검색 Modal END -->
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import { useRouter } from 'vue-router';
import { AxiosError } from 'axios';
import Pagination from '@/components/comm/Pagination.vue';
import { apiResponseCheck, dateTimeFormatConverter, showAlert, showConfirm, showLogConsole, showModal, hideModal, checkPermission } from '@/utils/common-utils';
import type { Commission, CommissionList } from 'CommissionInfoModule';
import Modal from '@/components/comm/modal.vue';
import { useUserStore } from '@/stores/user';
import AllStoreListModal from '@/pages/product/commission/modal/AllStoreListModal.vue';
import AllProdListModal from '@/pages/product/commission/modal/AllProdListModal.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import { useCommonStore } from '@/stores/common';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';

const mMemberId = ref(0);

const mStoreInfo = reactive({
  title: '',
  code: '없음',
});

const newCommissionInfo = reactive({
  kind: 'store',
  value: 0.01,
  type: 'P',
  store_code: '',
  store_title: '',
  product_id: 0,
  product_title: '',
  target: 0,
  target_name: '',
  target_type: 'CC',
});

const mCommissionList = ref({} as CommissionList);
const mCommissionOriginList = ref({} as CommissionList);
const mPgCommissionList = ref([] as Commission[]);
const mDefaultCommission = ref(0.0);
const mDefaultCommissionOrigin = ref(0.0);
const mDefaultShipCommission = reactive({ id: 0, value: 0.0 });
const mDefaultShipCommissionOrigin = reactive({ id: 0, value: 0.0 });

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mCommissionList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getCommissionList();
};

const pageChange = (page: number) => {
  page_no.value = page;
  getCommissionList(false);
};

const router = useRouter();

// *** 상점 검색 관련 *** //
const selectStore = (code: string, title: string) => {
  hideModal('searchStoreModal');

  newCommissionInfo.store_code = code;
  newCommissionInfo.store_title = title;
};
const openStoreModal = () => {
  showModal('searchStoreModal');
  storeModal.value.modalOpened();
};
// *** 상점 검색 관련 END *** //

// *** 상품 검색 관련 *** //
const storeModal = ref();
const prodModal = ref();
const openProdModal = () => {
  showModal('searchProdModal');
  prodModal.value.modalOpened();
};
const selectProd = (id: number, name: string) => {
  hideModal('searchProdModal');

  newCommissionInfo.product_id = id;
  newCommissionInfo.product_title = name;
};
// *** 상품 검색 관련 END *** //

const getDefaultCommission = () => {
  apis.commission.get_default_commission(mMemberId.value).then(res => {
    apiResponseCheck(res, () => {
      mDefaultCommission.value = res.default_commission;
      mDefaultCommissionOrigin.value = res.default_commission;
    });
  });
};
const getDefaultShipCommission = () => {
  apis.commission.get_default_commission(mMemberId.value, '&kind=ship').then(res => {
    apiResponseCheck(res, () => {
      mDefaultShipCommission.id = res.id;
      mDefaultShipCommission.value = JSON.parse(JSON.stringify(res.default_commission));
      mDefaultShipCommissionOrigin.id = JSON.parse(JSON.stringify(res.id));
      mDefaultShipCommissionOrigin.value = JSON.parse(JSON.stringify(res.default_commission));
    });
  });
};

const getPgCommissionList = () => {
  apis.commission.get_pg_commission_list().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mPgCommissionList.value = res;
    });
  });
};

const modDefaultCommission = () => {
  if (mDefaultCommission.value === mDefaultCommissionOrigin.value) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  if (!mDefaultCommission.value) {
    showAlert('기본 수수료율을 0%로 설정할 수 없습니다.', 'warning');
    mDefaultCommission.value = mDefaultCommissionOrigin.value;
    return;
  }

  showConfirm(
    '기본 수수료율을 변경하시겠습니까?',
    () => {
      //TODO: 추후 타입에 관한 설정 변경해야함
      apis.commission.mod_default_commission(mMemberId.value, { value: mDefaultCommission.value, type: 'P' }).then(res => {
        apiResponseCheck(res, () => {
          showAlert('기본 수수료율이 변경되었습니다.');
          mDefaultCommissionOrigin.value = mDefaultCommission.value;
        });
      });
    },
    () => {
      mDefaultCommission.value = mDefaultCommissionOrigin.value;
    },
  );
};

const modDefaultShipCommission = () => {
  if (mDefaultShipCommission.value === mDefaultShipCommissionOrigin.value) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  if (!mDefaultShipCommission.value) {
    showAlert('기본 배송비 수수료율을 0%로 설정할 수 없습니다.', 'warning');
    mDefaultShipCommission.value = mDefaultShipCommissionOrigin.value;
    return;
  }

  showConfirm(
    '기본 배송비 수수료율을 변경하시겠습니까?',
    () => {
      //TODO: 추후 타입에 관한 설정 변경해야함
      apis.commission.mod_commission(mDefaultShipCommissionOrigin.id, mDefaultShipCommission.value).then(res => {
        apiResponseCheck(res, () => {
          showAlert('기본 배송비 수수료율이 변경되었습니다.');
          mDefaultShipCommissionOrigin.value = mDefaultShipCommission.value;
        });
      });
    },
    () => {
      mDefaultShipCommission.value = mDefaultShipCommissionOrigin.value;
    },
  );
};

const getCommissionList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  //TODO: 쿼리스트링 작업 예정
  let query = '';

  apis.commission.get_commission_list(mMemberId.value, query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      mCommissionList.value.total = res.total;
      mCommissionList.value.datas = res.datas;

      mCommissionOriginList.value.datas = JSON.parse(JSON.stringify(res.datas));
    });
  });
};

const addNewCommission = () => {
  // 항목 입력 체크
  if (newCommissionInfo.kind === 'store') {
    if (!newCommissionInfo.store_code) {
      showAlert('대상 상점을 선택해주세요.', 'warning');
      return;
    }
  } else if (newCommissionInfo.kind === 'prod') {
    if (!newCommissionInfo.product_title) {
      showAlert('대상 상품을 선택해주세요', 'warning');
      return;
    }
  }

  if (!newCommissionInfo.value) {
    showAlert('수수료는 0%로 설정할 수 없습니다.', 'warning');
    return;
  }

  let data = { value: newCommissionInfo.value, type: newCommissionInfo.type, target: mMemberId.value } as any;
  if (newCommissionInfo.kind === 'store') {
    data['store_code'] = newCommissionInfo.store_code;
  } else if (newCommissionInfo.kind === 'prod') {
    data['product_id'] = newCommissionInfo.product_id;
  }

  showConfirm('수수료 정보를 등록하시겠습니까?', () => {
    apis.commission.add_commission(mMemberId.value, data).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('수수료 정보가 등록되었습니다.');
          hideModal('addNewCommission');
          getCommissionList();
        },
        (num?: number) => {
          if (num === 403) {
            hideModal('addNewCommission');
          }
        },
      );
    });
  });
};

const deleteCommission = (id: number) => {
  showConfirm('해당 수수료 정보를 삭제하시겠습니까?', () => {
    apis.commission.delete_commission(id).then(res => {
      apiResponseCheck(res, () => {
        showAlert('수수료 정보가 삭제되었습니다.');
        getCommissionList();
      });
    });
  });
};

const modListCommission = (idx: number) => {
  if (mCommissionList.value.datas[idx].value === mCommissionOriginList.value.datas[idx].value) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  if (!mCommissionList.value.datas[idx].value) {
    showAlert('수수료율을 0%로 설정할 수 없습니다.', 'warning');
    return;
  }

  showConfirm(
    '해당 수수료율을 변경하시겠습니까?',
    () => {
      apis.commission.mod_commission(mCommissionList.value.datas[idx].id, mCommissionList.value.datas[idx].value).then(res => {
        apiResponseCheck(res, () => {
          showAlert('수수료 정보가 변경되었습니다.');
          getCommissionList();
        });
      });
    },
    () => {
      mCommissionList.value.datas[idx].value = mCommissionOriginList.value.datas[idx].value;
    },
  );
};

const checkCommissionDefault = (e: any) => {
  if (!e.target.value) {
    e.target.value = 0;
    mDefaultCommission.value = 0;
    return;
  }

  if (!checkCommissionValue(e.target.value)) {
    e.target.value = (e.target.value as string).slice(0, e.target.value.length - 1);
    mDefaultCommission.value = e.target.value;
  } else {
    if (e.target.value.startsWith('00') || /0\d$/.test(e.target.value)) {
      e.target.value = parseFloat(e.target.value as string);
    }
  }
};

const checkShipCommissionDefault = (e: any) => {
  if (!e.target.value) {
    e.target.value = 0;
    mDefaultShipCommission.value = 0;
    return;
  }

  if (!checkCommissionValue(e.target.value)) {
    e.target.value = (e.target.value as string).slice(0, e.target.value.length - 1);
    mDefaultShipCommission.value = e.target.value;
  } else {
    if (e.target.value.startsWith('00') || /0\d$/.test(e.target.value)) {
      e.target.value = parseFloat(e.target.value as string);
    }
  }
};

const checkNewCommission = (e: any) => {
  if (!e.target.value) {
    e.target.value = 0;
    newCommissionInfo.value = 0;
    return;
  }

  if (!checkCommissionValue(e.target.value)) {
    e.target.value = (e.target.value as string).slice(0, e.target.value.length - 1);
    newCommissionInfo.value = e.target.value;
  } else {
    if (e.target.value.startsWith('00') || /0\d$/.test(e.target.value)) {
      e.target.value = parseFloat(e.target.value as string);
    }
  }
};

const checkCurrentCommission = (e: any, idx: number) => {
  if (!e.target.value) {
    e.target.value = 0;
    mCommissionList.value.datas[idx].value = 0;
    return;
  }

  if (!checkCommissionValue(e.target.value)) {
    e.target.value = (e.target.value as string).slice(0, e.target.value.length - 1);
    mCommissionList.value.datas[idx].value = e.target.value;
  } else {
    if (e.target.value.startsWith('00') || /0\d$/.test(e.target.value)) {
      e.target.value = parseFloat(e.target.value as string);
    }
  }
};

const checkCommissionValue = (value: any): boolean => {
  if (value > 100 || value < 0) {
    showAlert('0~100 범위의 숫자만 입력 가능합니다.', 'warning');
    return false;
  }

  const pattern = /^(\d{0,10}([.]\d{0,2})?)?$/;
  if (!pattern.test(value)) {
    showAlert('소수점 둘째자리 까지만 입력 가능합니다.', 'warning');
    return false;
  }
  return true;
};

const clearNewCommissionInfo = () => {
  newCommissionInfo.kind = 'store';
  newCommissionInfo.value = 0.01;
  newCommissionInfo.type = 'P';
  newCommissionInfo.store_code = '';
  newCommissionInfo.product_id = 0;
  newCommissionInfo.product_title = '';
  newCommissionInfo.target = 0;
  newCommissionInfo.target_name = '';
  newCommissionInfo.target_type = 'CC';
};

const setModalListener = () => {
  //@ts-ignore
  document.getElementById('addNewCommission').addEventListener('show.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('addNewCommission').addEventListener('hide.bs.modal', function (event) {
    clearNewCommissionInfo();
  });

  //@ts-ignore
  document.getElementById('searchProdModal').addEventListener('show.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('searchProdModal').addEventListener('hide.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('searchStoreModal').addEventListener('show.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('searchStoreModal').addEventListener('hide.bs.modal', function (event) {});
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');

  clearNewCommissionInfo();

  setModalListener();

  if (!checkPermission('read:commission_conia')) {
    showAlert('비정상적인 접근입니다.', 'error', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
  } else {
    mMemberId.value = 1;
    mStoreInfo.code = '없음';
    getDefaultCommission();
    getDefaultShipCommission();
    getPgCommissionList();
    limit.value = useCommonStore().getLimit;
    getCommissionList();
  }
});
</script>

<style scoped></style>
