<template>
  <PageNavigator :before_link="['배송비 수수료 설정']" :current="'배송비 수수료 상세 설정'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">배송비 수수료 설정 - [{{ mMemberInfo.name }}{{ mMemberInfo.email ? ` (${mMemberInfo.email})` : '' }}]</div>
    </div>
    <div class="card-body">
      <div class="row col mb-2 align-items-center">
        <label class="col-md-3 col-form-label">회원에게 부과할 수수료율 설정 (0.01% ~ 100%)</label>
        <div class="col-md-2">
          <div class="input-group">
            <input type="text" class="form-control" inputmode="decimal" placeholder="배송비 수수료율을 입력해주세요 (0.01% ~ 100%)" v-model="mDefaultCommission.value" @input="checkCommissionDefault($event)" :disabled="!checkPermission('write:commission_conia')" />
            <span class="input-group-text">%</span>
          </div>
        </div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="modDefaultCommission" v-if="mDefaultCommission.value.toString() !== mDefaultCommissionOrigin.value.toString()">
            {{ mDefaultCommissionOrigin.id !== 0 ? '저장' : '신규등록' }}
          </button>
        </div>
      </div>
    </div>
    <div class="card-footer py-2" v-if="false">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning" @click.prevent="openNewCommission">개별 설정 추가</button>
      </div>
    </div>
  </div>
  <div class="" v-if="false">
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
          <th>상점코드</th>
          <th>상품명</th>
          <th>수수료율</th>
          <th>삭제</th>
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
                  <input type="text" class="form-control" inputmode="decimal" placeholder="수수료율을 입력해주세요 (0.01% ~ 100%)" v-model="commission.value" @input="checkCurrentCommission($event, i)" />
                  <span class="input-group-text">%</span>
                </div>
              </div>
              <div class="col-auto">
                <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="modListCommission(i)" v-if="commission.value !== mCommissionOriginList.datas[i].value">저장</button>
              </div>
            </div>
          </td>
          <td>
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
  </div>

  <!-- 추가 수수료 등록 Modal -->
  <Modal :id="'addNewCommission'" :title="'추가적인 수수료 설정 등록'" v-if="checkPermission('write:sub_commission') || getUserClassStr.includes('CM')">
    <template #body>
      <div class="card">
        <div class="card-body">
          <div class="row col align-items-center mb-2">
            <label class="col-md-3 col-form-label">설정 대상</label>
            <div class="col-auto">
              <div class="row align-items-center">
                <div class="col-auto">
                  <input type="radio" id="radio_status_store" class="form-check-input" name="radio_status" value="store" v-model="newCommissionInfo.kind" />
                  <label class="form-check-label px-1" for="radio_status_store">상점</label>
                </div>
                <div class="col-auto">
                  <input type="radio" id="radio_status_prod" class="form-check-input" name="radio_status" value="prod" v-model="newCommissionInfo.kind" />
                  <label class="form-check-label px-1" for="radio_status_prod">상품</label>
                </div>
                <div class="col-auto" v-if="false">
                  <input type="radio" id="radio_status_member" class="form-check-input" name="radio_status" value="member" v-model="newCommissionInfo.kind" />
                  <label class="form-check-label px-1" for="radio_status_member">회원</label>
                </div>
              </div>
            </div>
          </div>

          <div class="row col mb-2 align-items-center" v-if="newCommissionInfo.kind === 'store'">
            <label class="col-md-3 col-form-label">대상 상점</label>
            <div class="col-md-6">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" id="sel_sub_store" v-model="selSubStoreList.selectedItem" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "상점을 선택해주세요."}'>
                  <option v-for="detail in selSubStoreList.items" :key="JSON.stringify(detail)" v-text="detail.title" :value="detail.store_code"></option>
                </select>
              </div>
              <!-- End Select -->
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
          <div class="row col mb-2 align-items-center" v-if="newCommissionInfo.kind === 'member'">
            <label class="col-md-3 col-form-label">대상 회원</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="대상 회원을 선택해주세요." :value="newCommissionInfo.target_name" readonly />
                <button type="button" class="btn btn-outline-info" @click.prevent="openMemberModal">검색</button>
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

  <!-- 상품 검색 Modal -->
  <Modal :id="'searchProdModal'" :title="'수수료 설정 대상 상품 선택'" :xlarge="true" :second="true">
    <template #body>
      <SelectCatalogProd :store-code="mStoreInfo.code" ref="storeModal" @selectedProd="selectedProd" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
  <!-- 상품 검색 Modal END -->

  <!-- 회원 검색 Modal -->
  <Modal :id="'searchMemberModal'" :title="'수수료 설정 대상 회원 선택'" :xlarge="true" :second="true">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">수수료 설정 대상 회원을 선택합니다.</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <form class="mb-6">
              <div class="row col">
                <label class="col-md-2 col-form-label">회원검색</label>
                <div class="col-md-2">
                  <!-- Select -->
                  <div class="tom-select-custom">
                    <select class="form-select" v-model="selDetailSearchMember.selectedItem" @change="onChangeDetailSearchMember" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                      <option v-for="detail in selDetailSearchMember.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
                    </select>
                  </div>
                  <!-- End Select -->
                </div>
                <div class="d-md-none mt-1"></div>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" id="q" v-model="selDetailSearchMember.q" :placeholder="selDetailSearchMember.placeholder" />
                    <button type="button" class="btn btn-outline-dark col-md-2" @click.prevent="reqUserList">검색</button>
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
                    <th>이름</th>
                    <th>아이디</th>
                    <th>휴대전화</th>
                    <th>선택</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="text-center" v-for="(user, i) in searchUserList.data" :key="user.id">
                    <td>{{ getUserClass(user.classes) }}</td>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.mobile }}</td>
                    <td>
                      <button type="button" class="btn btn-sm btn-info" @click.prevent="setMemberInfo(user)">선택</button>
                    </td>
                  </tr>
                  <tr>
                    <td colspan="5" class="text-center" v-if="searchUserList.data.length === 0">표시할 항목이 없습니다.</td>
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
  <!-- 회원 검색 Modal END -->
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import type { User, Class } from 'UserInfoModule';
import apis from '@/apis';
import { useRouter } from 'vue-router';
import { AxiosError } from 'axios';
import Pagination from '@/components/comm/Pagination.vue';
import { apiResponseCheck, checkPermission, dateTimeFormatConverter, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import type { CommissionList } from 'CommissionInfoModule';
import Modal from '@/components/comm/modal.vue';
import SelectCatalogProd from '@/pages/product/commission/modal/SelectCatalogProd.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

const mMemberId = ref(0);
const mMemberInfo = ref({} as { name: string; email: string });
const isExistChild = ref(false);

const mStoreInfo = reactive({
  title: '',
  code: '없음',
});

const newCommissionInfo = reactive({
  kind: 'store',
  value: 0.01,
  type: 'P',
  store_code: '',
  product_id: 0,
  product_title: '',
  target: 0,
  target_name: '',
  target_type: 'CC',
});

const mCommissionList = ref({} as CommissionList);
const mCommissionOriginList = ref({} as CommissionList);
const mDefaultCommission = reactive({ id: 0, value: 0.0 });
const mDefaultCommissionOrigin = reactive({ id: 0, value: 0.0 });

const searchUserList = ref({
  data: {} as User[],
  total: 0,
});

const router = useRouter();

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
  window.scrollTo({ top: 100, left: 0 });
};

const openNewCommission = () => {
  if (isExistChild.value) {
    showModal('addNewCommission');
  } else {
    showAlert('하위 상점이 존재하지 않습니다.', 'warning');
  }
};

// *** 상점 검색 관련 *** //
const selSubStoreList = reactive({
  items: [],
  selectedItem: '',
});
// *** 상점 검색 관련 END *** //

// *** 상품 검색 관련 *** //
const storeModal = ref();
const openProdModal = () => {
  showModal('searchProdModal');
  storeModal.value.modalOpened();
};
const selectedProd = (id: number, name: string) => {
  hideModal('searchProdModal');

  newCommissionInfo.product_id = id;
  newCommissionInfo.product_title = name;
};
// *** 상품 검색 관련 END *** //

// *** 회원 검색 관련 *** //
const openMemberModal = () => {
  showModal('searchMemberModal');
};
const selDetailSearchMember = reactive({
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
const onChangeDetailSearchMember = () => {
  switch (selDetailSearchMember.selectedItem) {
    case 'name':
      selDetailSearchMember.placeholder = '검색할 회원의 이름을 입력해주세요.';
      break;
    case 'user_id':
      selDetailSearchMember.placeholder = '검색할 회원의 아이디(이메일) 입력해주세요.';
      break;
    case 'mobile':
      selDetailSearchMember.placeholder = '검색할 회원의 전화번호를 입력해주세요.';
      break;
    case 'company_name':
      selDetailSearchMember.placeholder = '검색할 회원의 회사명을 입력해주세요.';
      break;
  }
};
const reqUserList = () => {
  let query = '';

  // 세부검색어 체크
  if (selDetailSearchMember.q) {
    const detail = `${selDetailSearchMember.selectedItem}=${selDetailSearchMember.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.user.get_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      searchUserList.value.data = res.datas;
      searchUserList.value.total = res.total;
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
const setMemberInfo = (user: User) => {
  newCommissionInfo.target_name = `${user.name} [${user.email}]`;
  newCommissionInfo.target = user.id;
  hideModal('searchMemberModal');
};
// *** 회원 검색 관련 END *** //

const getSubStores = () => {
  apis.store.get_sub_store_list(mMemberId.value).then(res => {
    apiResponseCheck(res, () => {
      selSubStoreList.items = res;
      if (res.length === 0) {
        isExistChild.value = false;
      } else {
        isExistChild.value = true;

        //@ts-ignore
        setTimeout(function () {
          //@ts-ignore
          let select = document.getElementById('sel_sub_store');
          //@ts-ignore
          let instance = select.tomselect;
          instance.refreshItems();
          instance.sync();
        }, 500);
      }

      getDefaultCommission();
      getCommissionList();
    });
  });
};

const getDefaultCommission = () => {
  apis.commission.get_default_commission(mMemberId.value, '&kind=ship').then(res => {
    apiResponseCheck(res, () => {
      mDefaultCommission.id = res.id;
      mDefaultCommission.value = JSON.parse(JSON.stringify(res.default_commission));
      mDefaultCommissionOrigin.id = JSON.parse(JSON.stringify(res.id));
      mDefaultCommissionOrigin.value = JSON.parse(JSON.stringify(res.default_commission));
    });
  });
};

const modDefaultCommission = () => {
  if (mDefaultCommissionOrigin.id === 0) {
    // 신규 배송비 수수료 등록
    if (!mDefaultCommission.value) {
      showAlert('배송비 수수료율을 0%로 설정할 수 없습니다.', 'warning');
      mDefaultCommission.value = mDefaultCommissionOrigin.value;
      return;
    }

    showConfirm(
      '배송비 수수료율을 신규 등록하시겠습니까?',
      () => {
        apis.commission.add_commission(mMemberId.value, { target: 1, member_id: mMemberId.value, type: 'P', value: mDefaultCommission.value, kind: 'ship', default: 'N' }).then(res => {
          apiResponseCheck(res, () => {
            showAlert('배송비 수수료율이 등록되었습니다.', 'success', () => {
              getDefaultCommission();
            });
          });
        });
      },
      () => {},
    );
  } else {
    // 기존 배송비 수수료 수정
    if (mDefaultCommission.value === mDefaultCommissionOrigin.value) {
      showAlert('변경사항이 없습니다.', 'warning');
      return;
    }

    if (!mDefaultCommission.value) {
      showAlert('배송비 수수료율을 0%로 설정할 수 없습니다.', 'warning');
      mDefaultCommission.value = mDefaultCommissionOrigin.value;
      return;
    }

    showConfirm(
      '배송비 수수료율을 변경하시겠습니까?',
      () => {
        //TODO: 추후 타입에 관한 설정 변경해야함
        apis.commission.mod_commission(mDefaultCommissionOrigin.id, mDefaultCommission.value).then(res => {
          apiResponseCheck(res, () => {
            showAlert('배송비 수수료율이 변경되었습니다.');
            mDefaultCommissionOrigin.value = mDefaultCommission.value;
          });
        });
      },
      () => {
        mDefaultCommission.value = mDefaultCommissionOrigin.value;
      },
    );
  }
};

const getCommissionList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  //TODO: 쿼리스트링 작업 예정
  let query = '';

  apis.commission.get_commission_list(mMemberId.value, query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mCommissionList.value.total = res.total;
      mCommissionList.value.datas = res.datas;
      mCommissionOriginList.value.datas = JSON.parse(JSON.stringify(res.datas));
    });
  });
};

const addNewCommission = () => {
  // 항목 입력 체크
  if (newCommissionInfo.kind === 'store') {
    if (!selSubStoreList.selectedItem) {
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
    data['store_code'] = selSubStoreList.selectedItem;
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
    showAlert('숫자만 입력 가능 하며 소수점 둘째자리 까지만 입력 가능합니다.', 'warning');
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
  selSubStoreList.selectedItem = '';
};

const setModalListener = () => {
  //@ts-ignore
  document.getElementById('addNewCommission').addEventListener('show.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('addNewCommission').addEventListener('hide.bs.modal', function (event) {
    clearNewCommissionInfo();
  });

  //@ts-ignore
  document.getElementById('searchMemberModal').addEventListener('show.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('searchMemberModal').addEventListener('hide.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('searchProdModal').addEventListener('show.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('searchProdModal').addEventListener('hide.bs.modal', function (event) {});
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');

  limit.value = useCommonStore().getLimit;
  clearNewCommissionInfo();

  if (checkPermission('write:sub_commission') || getUserClassStr.value.includes('CM')) setModalListener();

  const memberId = history.state.memberId;
  const memberInfo = history.state.memberInfo;
  const storeCode = history.state.storeCode;

  if (!memberId) {
    showAlert('비정상적인 접근입니다.', 'error', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
  } else {
    mMemberId.value = memberId;
    mMemberInfo.value = memberInfo;
    mStoreInfo.code = storeCode ? storeCode : '없음';

    if (checkPermission('write:sub_commission') || getUserClassStr.value.includes('CM')) getSubStores();
  }
});
</script>

<style scoped></style>
