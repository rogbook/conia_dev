<template>
  <PageNavigator :before_link="['배송그룹설정']" :current="shippingId ? '배송그룹 상세' : '신규 배송그룹 생성'" />
  <div class="card" :class="{ 'col-md-6': shippingId === undefined }">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center" v-if="shippingId">
        <div class="col-auto">
          <div class="form-control-borderless h2">배송그룹관리</div>
          <div class="form-control-borderless h4">배송그룹명 : [{{ shipping.name }}]</div>
        </div>
      </div>
      <div class="row justify-content-between align-items-center" v-else>
        <div class="col-auto">
          <div class="form-control-borderless h2">신규 배송그룹 생성</div>
        </div>
      </div>
    </div>
    <!-- 기본설정 영역 - [CM:읽기/수정, MC:읽기] -->
    <div class="card-body">
      <div class="row">
        <div class="card" :class="{ 'col-md-4 me-4': shippingId !== undefined }">
          <div class="card-header py-3">
            <span class="icon icon-xs icon-dark icon-circle" style="width: 0.5rem; height: 0.5rem"></span>
            기본정보
          </div>
          <div class="card-body">
            <div class="row col mb-2 align-items-center" v-if="getUserClassStr.includes('CM') && !shippingId">
              <label class="col-md-3 col-form-label">공급자(PA)</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="공급자(PA)를 선택해주세요." disabled v-model="paInfo.name" />
                  <button type="button" class="btn btn-sm btn-outline-dark" @click.prevent="showModal('paMemberSelModal')">검색</button>
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">배송그룹명</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="배송그룹명을 입력해주세요." v-model.trim="shippingInfo.name" maxlength="30" />
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">배송타입</label>
              <div class="col">
                <select class="form-select sel_theme_link" @change="typeChange" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "배송타입을 선택해주세요."}'>
                  <option disabled selected>배송타입을 선택해주세요.</option>
                  <option v-for="t in shippingType.items" :key="JSON.stringify(t)" v-text="t" :value="t" :selected="shippingType.selectedItem === t"></option>
                </select>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">지불방법</label>
              <div class="col">
                <select class="form-select sel_theme_link" @change="payTypeChange" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "지불방법을 선택해주세요."}'>
                  <option disabled selected>지불방법을 선택해주세요.</option>
                  <option v-for="t in payType.items" :key="JSON.stringify(t)" v-text="t" :value="t" :selected="payType.selectedItem === t"></option>
                </select>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">계산방법</label>
              <div class="col">
                <select class="form-select sel_theme_link" @change="calcTypeChange" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "계산방법을 선택해주세요."}'>
                  <option disabled selected>계산방법을 선택해주세요.</option>
                  <option v-for="t in calcType.items" :key="JSON.stringify(t)" v-text="t" :value="t" :selected="calcType.selectedItem === t"></option>
                </select>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">반품비설정</label>
              <div class="col">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="반품비를 입력해주세요." v-model.lazy="shippingInfo.change_cost" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" />
                  <div class="input-group-text">
                    <span class="">원</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">교환비설정</label>
              <div class="col">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="교환비를 입력해주세요." v-model.lazy="shippingInfo.return_cost" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" />
                  <div class="input-group-text">
                    <span class="">원</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="card-footer py-2">
            <div class="text-end">
              <button type="button" class="btn btn-sm btn-primary" @click.prevent="modShippingInfo" v-if="shippingId">기본정보저장</button>
            </div>
          </div>
        </div>
        <div class="d-md-none mt-1"></div>
        <div class="card col" v-if="shippingId">
          <div class="card-header py-3">
            <span class="icon icon-xs icon-dark icon-circle" style="width: 0.5rem; height: 0.5rem"></span>
            배송비 정보
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-bordered table-thead-bordered table-align-middle card-table table-nowrap">
                <thead class="thead-light">
                  <tr class="text-center">
                    <th style="width: 15%">배송비 타입</th>
                    <th>배송비 내용</th>
                    <th>수정</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="text-center" v-if="hasCostInfo">
                    <td>{{ convertShippingType }}</td>
                    <td class="text-center">
                      <div class="cost-info-basic row align-items-center border-1 border-bottom mb-2 pb-2">
                        <div class="col-auto">[기본]</div>
                        <div class="col-lg">
                          <div class="row align-items-center" v-for="c in shipping.shipping_costs" :key="c.id">
                            <div class="row align-items-center mb-2 justify-content-between" v-if="c.category === 'basic' && !(c.type === 'fix' || c.type === 'free')">
                              <div class="col-lg-4" v-if="c.section_start >= 0">
                                <div class="input-group">
                                  <input type="number" class="form-control text-end" placeholder="구간시작값" :value="c.section_start" readonly />
                                  <div class="input-group-text px-2">
                                    <span class="" v-if="shipType.startsWith('ea')">개 이상</span>
                                    <span class="" v-else-if="shipType.startsWith('weight')">Kg 이상</span>
                                    <span class="" v-else>원 이상</span>
                                  </div>
                                </div>
                              </div>
                              <span class="col-auto" v-if="c.section_end || c.section_repeat">~</span>
                              <div class="col-lg-4" v-if="c.section_end">
                                <div class="input-group">
                                  <input type="number" class="form-control text-end" placeholder="구간종료값" :value="c.section_end" readonly />
                                  <div class="input-group-text px-2">
                                    <span class="" v-if="shipType.startsWith('ea')">개 미만</span>
                                    <span class="" v-else-if="shipType.startsWith('weight')">Kg 미만</span>
                                    <span class="" v-else>원 미만</span>
                                  </div>
                                </div>
                              </div>
                              <div class="col-lg-4" v-else-if="c.section_repeat">
                                <div class="input-group">
                                  <input type="number" class="form-control text-end" placeholder="구간종료값" :value="c.section_repeat" readonly />
                                  <div class="input-group-text px-2">
                                    <span class="" v-if="shipType.startsWith('ea')">개 당</span>
                                    <span class="" v-else-if="shipType.startsWith('weight')">Kg 당</span>
                                    <span class="" v-else>원 당</span>
                                  </div>
                                </div>
                              </div>
                              <div class="col" v-else></div>
                              <div class="col-lg-3">
                                <div class="input-group">
                                  <input type="text" class="form-control text-end" placeholder="배송비를 입력해주세요." :value="c.cost.toLocaleString()" readonly />
                                  <div class="input-group-text px-2">
                                    <span class="">원</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <div class="row align-items-center" v-else>
                              <div class="col-lg-4 ms-2" v-if="c.category === 'basic'">
                                <div class="input-group">
                                  <input type="text" class="form-control text-end" placeholder="배송비를 입력해주세요." :value="c.cost.toLocaleString()" readonly />
                                  <div class="input-group-text px-2">
                                    <span class="">원</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="cost-info-basic row align-items-center pt-2">
                        <div class="col-auto">[도서산간]</div>
                        <div class="col-lg">
                          <div class="row align-items-center mb-2" v-if="shipping.shipping_costs[shipping.shipping_costs.length - 1].category === 'add'">
                            <div class="col-lg-5 ms-2">
                              <div class="input-group">
                                <input type="text" class="form-control text-end" placeholder="배송비를 입력해주세요." :value="shipping.shipping_costs[shipping.shipping_costs.length - 1].cost.toLocaleString()" readonly />
                                <div class="input-group-text">
                                  <span class="">원</span>
                                </div>
                              </div>
                            </div>
                          </div>
                          <div class="row align-items-center" v-else>
                            <div class="text-center">도서산간 추가 배송비 정보 없음.</div>
                          </div>
                        </div>
                      </div>
                    </td>
                    <td>
                      <button type="button" class="btn btn-sm btn-info" @click.prevent="showModal('CostInfoModal')">수정</button>
                    </td>
                  </tr>
                  <tr class="text-center" v-if="shipping.shipping_costs === null || shipping.shipping_costs?.length === 0">
                    <td colspan="3">배송비 정보가 없습니다. <button type="button" class="btn btn-sm btn-success" @click.prevent="showModal('CostInfoModal')">배송비 정보 입력</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="row align-items-center justify-content-center">
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="addShippingInfo" v-if="!shippingId">기본정보등록</button>
        </div>
      </div>
    </div>
  </div>
  <!-- 컴포넌트 상품 조회 Modal -->
  <Modal :id="'CostInfoModal'" :title="modalTitle" :xlarge="true">
    <template #body>
      <CostInfo ref="costInfoModal" @closeModal="closeModal" :shippingId="shippingId" :calcType="shipping.calc_type" :costInfo="shipping.shipping_costs" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-sm btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="saveCostInfo">저장</button>
    </template>
  </Modal>

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
                      <button type="button" class="btn btn-sm btn-info" @click.prevent="setPAInfo(user)">선택</button>
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
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import { AxiosError } from 'axios';
import type { ShippingCost, ShippingInfo } from 'ShippingInfoModule';
import { useUserStore } from '@/stores/user';
import Modal from '@/components/comm/modal.vue';
import CostInfo from '@/pages/settings/shipping/list/detail/cost/CostInfo.vue';
import { apiResponseCheck, showAlert, showConfirm, getUserClassStr, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import type { Class, User } from 'UserInfoModule';

const router = useRouter();
const shipping = ref({} as ShippingInfo);
const shippingId = ref();
const checkedTypes = ref('PA');
const paInfo = reactive({
  id: 0,
  name: '',
});
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
const setPAInfo = (user: User) => {
  const paCompany = user?.company?.name ? user?.company?.name : '없음';
  paInfo.id = user.id;
  paInfo.name = `${user.name} ( 업체명 : ${paCompany} )`;

  hideModal('paMemberSelModal');
};

const hasCostInfo = computed(() => {
  return shipping.value.shipping_costs?.length > 0;
});
const shipType = computed(() => {
  return shipping.value.shipping_costs[0].type;
});
const convertShippingType = computed(() => {
  if (shipping.value.shipping_costs.length > 0) {
    switch (shipping.value.shipping_costs[0].type) {
      case 'free':
        return '무료';
      case 'fix':
        return '고정';
      case 'cost':
        return `금액${checkRepeat()}`;
      case 'ea':
        return `수량${checkRepeat()}`;
      case 'weight':
        return `무게${checkRepeat()}`;
    }
  }
  return '';
});

const checkRepeat = (): string => {
  let lastIdx = -1;
  lastIdx = shipping.value.shipping_costs.map(el => el.category).lastIndexOf('basic');
  if (lastIdx != -1) {
    if (shipping.value.shipping_costs[lastIdx].section_repeat !== null) {
      //구간 반복
      return '(구간반복)';
    } else {
      return '(구간입력)';
    }
  } else {
    return '';
  }
};

const modalTitle = ref('');
const costInfoModal = ref();

const shippingType = reactive({
  items: ['택배', '퀵서비스', '화물배송', '매장수령'],
  selectedItem: '',
});
const calcType = reactive({
  items: ['묶음', '개별'],
  selectedItem: '',
});
const payType = reactive({
  items: ['선불', '착불'],
  selectedItem: '',
});

const shippingInfo = reactive({
  name: '',
  type: '',
  pay_type: '',
  calc_type: '',
  return_cost: 0,
  change_cost: 0,
});

const typeChange = (event: any) => {
  shippingType.selectedItem = event.target.value;
};

const payTypeChange = (event: any) => {
  payType.selectedItem = event.target.value;
};

const calcTypeChange = (event: any) => {
  calcType.selectedItem = event.target.value;
};

const getShippingInfo = () => {
  apis.shipping.get_shipping_info(shippingId.value).then(res => {
    apiResponseCheck(res, () => {
      shipping.value = res;
      shippingInfo.name = shipping.value.name;
      shippingInfo.type = shipping.value.type;
      shippingInfo.pay_type = shipping.value.pay_type;
      shippingInfo.calc_type = shipping.value.calc_type;
      shippingInfo.return_cost = shipping.value.return_cost;
      shippingInfo.change_cost = shipping.value.change_cost;

      shippingType.selectedItem = shippingInfo.type;
      payType.selectedItem = shippingInfo.pay_type;
      calcType.selectedItem = shippingInfo.calc_type;

      if (shipping.value.shipping_costs === null || shipping.value.shipping_costs?.length === 0) {
        showAlert('배송비 정보가 없습니다.<br/>배송비 정보를 입력해주세요.<br/><span class="text-danger" style="font-size: 0.8rem">* 배송비 정보가 없는 배송그룹은 [상품등록]시에 사용할 수 없습니다.</span>', 'warning', () => {});
        modalTitle.value = '신규 배송비 추가';
      } else {
        modalTitle.value = '배송비 정보 수정';
      }
    });
  });
};

const modShippingInfo = () => {
  const modInfo = {} as any;

  if (shippingInfo.name !== shipping.value.name) {
    modInfo['name'] = shippingInfo.name;
  }
  if (shippingType.selectedItem !== shipping.value.type) {
    modInfo['type'] = shippingType.selectedItem;
  }
  if (payType.selectedItem !== shipping.value.pay_type) {
    modInfo['pay_type'] = payType.selectedItem;
  }
  if (calcType.selectedItem !== shipping.value.calc_type) {
    modInfo['calc_type'] = calcType.selectedItem;
  }
  if (shippingInfo.return_cost !== shipping.value.return_cost) {
    modInfo['return_cost'] = shippingInfo.return_cost;
  }
  if (shippingInfo.change_cost !== shipping.value.change_cost) {
    modInfo['change_cost'] = shippingInfo.change_cost;
  }

  showConfirm('배송그룹 정보를 변경하시겠습니까?', () => {
    apis.shipping.mod_shipping_info(shippingId.value, modInfo).then(res => {
      apiResponseCheck(res, () => {
        showAlert('수정되었습니다.', 'success');
        getShippingInfo();
      });
    });
  });
};

const addShippingInfo = () => {
  if (getUserClassStr.value.includes('CM') && !paInfo.name) {
    showAlert('공급자(PA)를 선택해주세요.', 'warning');
    return;
  }
  if (!shippingInfo.name) {
    showAlert('배송그룹명을 입려해주세요.', 'warning');
    return;
  }
  if (!shippingType.selectedItem) {
    showAlert('배송타입을 선택해주세요.', 'warning');
    return;
  }
  if (!payType.selectedItem) {
    showAlert('지불방법을 선택해주세요.', 'warning');
    return;
  }
  if (!calcType.selectedItem) {
    showAlert('계산방법을 선택해주세요.', 'warning');
    return;
  }
  if (!shippingInfo.change_cost.toString() || shippingInfo.change_cost < 0) {
    showAlert('반품비를 입력해주세요.', 'warning');
    return;
  }

  if (!shippingInfo.return_cost.toString() || shippingInfo.return_cost < 0) {
    showAlert('교환비를 입력해주세요.', 'warning');
    return;
  }

  showConfirm('신규 배송그룹을 생성하시겠습니까?', () => {
    shippingInfo.type = shippingType.selectedItem;
    shippingInfo.pay_type = payType.selectedItem;
    shippingInfo.calc_type = calcType.selectedItem;

    const data = { ...shippingInfo } as any;
    if (getUserClassStr.value.includes('CM')) {
      data.member_id = paInfo.id;
    } else {
      data.member_id = useUserStore().user.id;
    }
    apis.shipping.add_shipping_info(data).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        showAlert('신규 배송그룹이 생성되었습니다.', 'success', () => {
          router.replace({ path: `/setting/shipping/detail`, state: { id: res.data.id } });
        });
      });
    });
  });
};

const saveCostInfo = () => {
  costInfoModal.value.saveClicked();
};

const closeModal = () => {
  hideModal('CostInfoModal');
  getShippingInfo();
};

onMounted(() => {
  const id = history.state.id;

  if (id) {
    shippingId.value = id;
    getShippingInfo();
  }
});
</script>

<style scoped></style>
