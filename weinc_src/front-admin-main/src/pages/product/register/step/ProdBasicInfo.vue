<template>
  <div class="text-end mb-2">
    <button type="button" class="btn btn-primary" @click.prevent="handelSubmit" v-if="!editMode">기본판매정보 등록</button>
  </div>
  <div class="card mb-2">
    <div class="card-header">[상품 기본 정보]</div>
    <div class="card-body">
      <div class="row col mb-4">
        <label class="col-sm-2 col-form-label">상품유형선택</label>
        <div class="col-sm-auto">
          <!-- Select -->
          <!-- 타입 [DP : 일반 배송, UP-EC : E-쿠폰, UP-OF : 티켓, G : 상품그룹] -->
          <div class="tom-select-custom">
            <select v-model="type.value" class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' @change="changeType">
              <option value="DP">일반 배송</option>
              <option value="UP-EC">E-쿠폰</option>
              <option value="UP-OF">티켓</option>
              <!--              <option value="G">상품그룹</option>-->
            </select>
          </div>
        </div>
      </div>
      <CommFormLine :title="`공급자(PA)`" :width="8">
        <input type="text" class="form-control" v-model="paInfo.name" placeholder="공급자(PA)를 선택해주세요." aria-label="" disabled />
        <div class="d-lg-none mt-1"></div>
        <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('paMemberSelModal')" v-if="paInfo.noPa">검색</button>
      </CommFormLine>

      <CommFormLine slot-parent="form-control border-0" :title="`외부연동업체`" v-if="type.value === 'UP-EC'">
        <div class="form-check form-check-inline" v-for="(item, i) in api_provider_list">
          <input :id="`provider${item.id}`" v-model="api_provider.value" :value="item.value" type="radio" class="form-check-input" name="api_provider" />
          <label class="form-check-label" :for="`provider${item.id}`">{{ item.name }}</label>
        </div>
      </CommFormLine>
      <CommFormLine input-for="apiGoodsId" :title="`외부업체 상품 ID`" :width="8" v-if="type.value === 'UP-EC'">
        <input maxlength="100" v-model.trim="api_goods_id.value" id="apiGoodsId" type="text" class="form-control" placeholder="외부업체 상품 ID를 입력해주세요." aria-label="외부업체 상품 ID를 입력해주세요." />
      </CommFormLine>
      <CommFormLine :title="`카테고리`" :width="8">
        <input type="text" class="form-control" :value="cateValues" placeholder="카테고리를 선택해주세요." aria-label="" disabled />
        <div class="d-lg-none mt-1"></div>
        <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('modalCategory')">검색</button>
      </CommFormLine>
      <CommFormLine :title="`브랜드`" :width="8">
        <input type="text" class="form-control" :value="brandValues" placeholder="브랜드를 선택해주세요." aria-label="" disabled />
        <div class="d-lg-none mt-1"></div>
        <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('modalBrands')">검색</button>
      </CommFormLine>
      <CommFormLine input-for="productName" :title="`상품명`" :width="8">
        <input maxlength="100" @change.prevent="checkNameValid" v-model.trim="name.value" id="productName" type="text" class="form-control" placeholder="상품명을 입력해주세요. (최대 100자)" aria-label="상품명을 입력해주세요." />
      </CommFormLine>
      <CommFormLine input-for="productSubTitle" :title="`부제목`" :width="8">
        <input maxlength="100" v-model.trim="subtitle.value" id="productSubTitle" type="text" class="form-control" placeholder="부제목을 입력해주세요. (최대 100자)" aria-label="부제목을 입력해주세요." />
      </CommFormLine>
      <CommFormLine input-for="code" :title="`상품코드`" :width="8">
        <input
          maxlength="255"
          v-model.trim="code.value"
          @change.prevent="
            () => {
              code.check = false;
            }
          "
          id="code"
          type="text"
          class="form-control"
          name="firstName"
          placeholder="상품 코드를 입력해주세요. (미입력시 자동생성)"
          aria-label="상품 코드를 입력해주세요. (미입력시 자동생성)"
          :disabled="code.check" />
        <div class="d-lg-none mt-1"></div>
        <button
          type="button"
          v-if="code.check"
          @click.prevent="
            () => {
              code.check = false;
            }
          "
          class="btn btn-outline-secondary">
          직접생성
        </button>
        <button type="button" v-else @click.prevent="onCheckProductCode" class="btn btn-outline-secondary">중복체크</button>
      </CommFormLine>
      <CommFormLine input-for="words" :title="`검색어`" :width="8">
        <input v-model.trim="words.value" name="words" id="words" type="text" class="form-control" maxlength="1000" placeholder="검색어는 ,(콤마)로 구분됩니다. 1000자 까지 입력 가능 합니다." aria-label="검색어는 ,(콤마)로 구분됩니다. 1000자 까지 입력 가능 합니다." />
      </CommFormLine>
      <CommFormLine input-for="summary" :title="`간략설명`" :width="8">
        <textarea v-model.trim="summary.value" name="summary" id="summary" type="text" class="form-control" maxlength="255" placeholder="255자 까지 입력 가능합니다." aria-label="255자 까지 입력 가능합니다." />
      </CommFormLine>
    </div>
  </div>
  <div class="card mb-2">
    <div class="card-header">[상품 판매 정보]</div>
    <div class="card-body">
      <CommFormLine slot-parent="form-control border-0" :title="`재고에 따른 판매`">
        <div class="form-check form-check-inline">
          <input value="N" v-model="inven.value" id="inf_inven" type="radio" class="form-check-input" name="inf_inven" />
          <label class="form-check-label" for="inf_inven">무제한</label>
        </div>
        <div class="form-check form-check-inline">
          <input value="Y" v-model="inven.value" id="lim_inven" type="radio" class="form-check-input" name="lim_inven" />
          <label class="form-check-label" for="lim_inven">재고 적용</label>
        </div>
      </CommFormLine>
      <CommFormLine slot-parent="form-control border-0" :title="`재고 노출여부`" v-if="inven.value === 'Y'">
        <div class="form-check form-check-inline">
          <input value="Y" v-model="view_inventory.value" id="use_view_inventory" type="radio" class="form-check-input" name="use_view_inventory" />
          <label class="form-check-label" for="use_view_inventory">노출</label>
        </div>
        <div class="form-check form-check-inline">
          <input value="N" v-model="view_inventory.value" id="none_view_inventory" type="radio" class="form-check-input" name="none_view_inventory" />
          <label class="form-check-label" for="none_view_inventory">미노출</label>
        </div>
      </CommFormLine>
      <CommFormLine slot-parent="form-control border-0" :title="`과세여부`">
        <div class="form-check form-check-inline">
          <input value="Y" v-model="tax.value" id="ues_tax" type="radio" class="form-check-input" name="ues_tax" />
          <label class="form-check-label" for="ues_tax">과세</label>
        </div>
        <div class="form-check form-check-inline">
          <input value="N" v-model="tax.value" id="none_tax" type="radio" class="form-check-input" name="none_tax" />
          <label class="form-check-label" for="none_tax">비과세</label>
        </div>
      </CommFormLine>
      <CommFormLine slot-parent="form-control border-0" :title="`청약철회`">
        <div class="form-check form-check-inline">
          <input value="Y" v-model="cancel.value" id="use_cancel" type="radio" class="form-check-input" name="use_cancel" />
          <label class="form-check-label" for="use_cancel">가능</label>
        </div>
        <div class="form-check form-check-inline">
          <input value="N" v-model="cancel.value" id="none_cancel" type="radio" class="form-check-input" name="none_cancel" />
          <label class="form-check-label" for="none_cancel">불가(취소/교환/반품 불가)</label>
        </div>
      </CommFormLine>
      <CommFormLine slot-parent="form-control border-0" :title="`사입여부`" v-if="getUserClassStr.includes('CM')">
        <div class="form-check form-check-inline">
          <input value="Y" v-model="resale.value" id="use_resale" type="radio" class="form-check-input" name="use_resale" />
          <label class="form-check-label" for="use_resale">예</label>
        </div>
        <div class="form-check form-check-inline">
          <input value="N" v-model="resale.value" id="none_resale" type="radio" class="form-check-input" name="none_resale" />
          <label class="form-check-label" for="none_resale">아니오</label>
        </div>
      </CommFormLine>
      <CommFormLine slot-parent="form-control border-0" :title="`성인인증`" v-if="false">
        <div class="form-check form-check-inline">
          <input value="Y" v-model="adult.value" id="use_adult" type="radio" class="form-check-input" name="use_adult" />
          <label class="form-check-label" for="use_adult">사용</label>
        </div>
        <div class="form-check form-check-inline">
          <input value="N" v-model="adult.value" id="none_adult" type="radio" class="form-check-input" name="none_adult" />
          <label class="form-check-label" for="none_adult">사용안함</label>
        </div>
      </CommFormLine>
      <CommFormLine slot-parent="form-control border-0" :title="`개인통관부호`" v-if="false">
        <div class="form-check form-check-inline">
          <input value="Y" id="use_ipcc" v-model="ipcc.value" type="radio" class="form-check-input" name="use_ipcc" />
          <label class="form-check-label" for="use_ipcc">수집</label>
        </div>
        <div class="form-check form-check-inline">
          <input value="N" id="none_ipcc" v-model="ipcc.value" type="radio" class="form-check-input" name="none_ipcc" />
          <label class="form-check-label" for="none_ipcc">수집 안함</label>
        </div>
      </CommFormLine>
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
                <div class="col">
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
                      <button type="button" class="btn btn-sm btn-info" @click.prevent="setPaInfo(user)" :disabled="user.status !== 'Y'">{{ user.status === 'Y' ? '선택' : '선택불가' }}</button>
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
  <!-- 카테고리 선택 Modal -->
  <DynamicColumnModal modal-id="modalCategory" modal-name="카테고리" @choice="onChangeCategory" :parent="props.cate" :type="'getCategories'" :selected="selectedCategories" />
  <!-- 브랜드 선택 Modal -->
  <ColumnSelectionModal modal-id="modalBrands" modal-name="브랜드" @choice="onChangeBrand" :parent="props.brands" :type="'getBrands'" :selected="selectedBrand" />
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import CommFormLine from '@/components/comm/CommFormLine.vue';
import { computed, onMounted, reactive, ref, watch, PropType } from 'vue';
import ColumnSelectionModal from '@/components/modals/product/ColumnSelectionModal.vue';
import { arrayToStringWithComma } from '@/utils/arrayParser';
import DynamicColumnModal from '@/components/modals/product/DynamicColumnModal.vue';
import type { IBrand, ICategory } from '@/components/product/type';
import apis from '@/apis';
import { useUserStore } from '@/stores/user';
import { AxiosError } from 'axios';
import type { Class, User } from 'UserInfoModule';
import type { Prod } from 'ProductListInfoModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal, getUserClassStr } from '@/utils/common-utils';
import { useRouter } from 'vue-router';

const router = useRouter();
const emits = defineEmits(['setProductId', 'changeType']);
const user = useUserStore().user;
const props = defineProps({
  prodId: { type: Number, default: 0 },
  prodInfo: { type: Object as PropType<Prod | null>, default: null },
  editMode: { type: Boolean, default: false },
  prodType: { type: String, default: '' },
  cate: { type: Array, default: () => [] },
  brands: { type: Array, default: () => [] },
  name: { type: String, default: '' },
  code: { type: String, default: '' },
  words: { type: String, default: '' },
  summary: { type: String, default: '' },
  api_provider: { type: String, default: '' },
  api_goods_id: { type: String, default: '' },
});
const checkedTypes = ref('PA');
const changeType = (event: any) => {
  emits('changeType', event.target.value);
  type.value = event.target.value;
};

const selectedCategories = ref<ICategory[][]>([]);
const selectedBrand = ref<IBrand[]>([]);
const api_provider_list = ref([
  {
    id: '',
    name: '',
    sort: '',
    value: '',
  },
]);

const cateValues = computed(() => {
  const arr = [];
  for (const sc of selectedCategories.value) {
    const tmp = [];
    for (const c of sc) {
      tmp.push(c.name);
    }
    arr.push(tmp.join(' > '));
  }
  // return arr.join(', ');
  return arr.length > 1 ? `${arr[0]} 외 ${arr.length - 1}건` : arr;
});

const type = reactive({ value: 'DP', check: true, err_msg: '' });
const brandValues = computed(() => arrayToStringWithComma(selectedBrand.value, 'name'));
const categories = reactive({ value: cateValues, check: false, selectedCategories, err_msg: '카테고리를 선택해 주세요.' });
const brands = reactive({ value: brandValues, check: false, selectedBrand, err_msg: '브랜드를 선택해 주세요.' });
const name = reactive({ value: '', check: false, err_msg: '상품명을 입력해주세요.' });
const subtitle = reactive({ value: '', check: true, err_msg: '부제목을 입력해주세요.' });
const code = reactive({ value: '', check: true, err_msg: '상품코드를 중복체크 해주세요.' });
const words = reactive({ value: '', check: true, err_msg: '1000자 까지 입력이 가능합니다.' });
const summary = reactive({ value: '', check: true, err_msg: '255자 까지 입력이 가능합니다.' });
const api_provider = reactive({ value: 'M12', check: true, err_msg: '' });
const api_goods_id = reactive({ value: '', check: true, err_msg: '' });

// 성인인증
const adult = reactive({ value: 'N', check: true, err_msg: '' });
// 노출여부
const view = reactive({ value: 'N', check: true, err_msg: '' });
// 개인통관부호
const ipcc = reactive({ value: 'N', check: true, err_msg: '' });
// 청약철회
const cancel = reactive({ value: 'Y', check: true, err_msg: '' });
// 사입여부
const resale = reactive({ value: 'N', check: true, err_msg: '' });
// 과세여부
const tax = reactive({ value: 'Y', check: true, err_msg: '' });
// 재고사용여부
const inven = reactive({ value: 'N', check: true, err_msg: '' });
// 재고노출여부
const view_inventory = reactive({ value: 'N', check: true, err_msg: '' });

const onChangeCategory = (selectedIds: ICategory[][]) => {
  categories.check = selectedIds.length != 0;
  selectedCategories.value = selectedIds;
};
const onChangeBrand = (selectedIds: IBrand[]) => {
  brands.check = selectedIds.length != 0;
  selectedBrand.value = selectedIds;
};

const onCheckProductCode = async () => {
  if (code.value) {
    await apis.product.checkProductCode(code.value).then(({ exist }: { exist: boolean }) => {
      if (exist) {
        code.check = false;
        showAlert('상품코드가 이미 존재합니다.', 'error');
      } else {
        code.check = true;
        showAlert('사용할 수 있는 상품코드입니다.', 'success');
      }
    });
  } else {
    code.check = true;
  }
};

const checkNameValid = () => {
  name.check = name.value !== '';
};

const checkList = reactive([type, categories, brands, name, subtitle, code, words, summary, adult, view, ipcc, cancel, resale, tax, inven, view_inventory]);

const handelSubmit = () => {
  if (paInfo.id === 0) {
    showAlert('공급자(PA)를 선택해주세요', 'warning');
    return;
  }
  if (type.value === 'UP-EC') {
    if (!api_provider.value) {
      showAlert('외부연동업체를 선택해주세요.', 'warning');
      return;
    }
    if (!api_goods_id.value) {
      showAlert('외부업체 상품 ID를 입력해주세요.', 'warning');
      return;
    }
  }
  for (const data of checkList) {
    if (!data.check) {
      showAlert(data.err_msg, 'warning');
      return;
    }
  }

  showConfirm(`<span class="text-danger">기본판매정보 등록 후 상품유형은 변경할수 없습니다.</span> \n 상품 기본판매정보를 등록하시겠습니까?`, () => {
    apis.product
      .makeProduct({
        type: type.value,
        name: name.value,
        subtitle: subtitle.value,
        adult: adult.value,
        cancel_yn: cancel.value,
        resale: resale.value,
        ipcc_yn: ipcc.value,
        view_yn: view.value,
        tax: tax.value,
        inven_use: inven.value,
        view_inventory: view_inventory.value,
        code: code.value,
        keyword: words.value,
        summary: summary.value,
        api_provider: api_provider.value,
        api_goods_id: api_goods_id.value,
        member_id: paInfo.id,
      })
      .then(data => {
        if (data instanceof AxiosError) {
          console.error(data);
          showAlert('상품 등록중 문제가 발생했습니다.\n 관리자에게 문의하세요.', 'error');
          return;
        }
        // 브랜드 insert
        // 카테고리 insert
        const linkBrand = apis.product.linkBrand({ productId: data.id, brandId: selectedBrand.value.map(sb => sb.id) });
        const linkCategory = apis.product.linkCategory({ productId: data.id, categoryId: categories.selectedCategories.map(sc => sc[sc.length - 1].id) });
        Promise.all([linkBrand, linkCategory]).then(() => {
          showAlert('상품 기본판매정보가 등록되었습니다.', 'success');
          emits('setProductId', data.id);
        });
      });
  });
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

const userName = computed(() => {
  return `${useUserStore().user.name}`;
});
const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

watch(inven, () => {
  if (inven.value === 'N') {
    view_inventory.value = 'N';
  }
});

const checkCompany = () => {
  if (useUserStore().user.company_id === 0) {
    showAlert('사업자 정보가 없는 경우 상품을 등록할 수 없습니다.\n사업자 정보를 확인해주세요.', 'warning', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
  }
};

const getApiProvider = () => {
  apis.product.get_api_provider_List().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      api_provider_list.value = res;
    });
  });
};

onMounted(() => {
  if (userClass.value.includes('PA')) {
    //@ts-ignore
    paInfo.id = parseInt(user.id.toString());
    paInfo.name = userName.value;
    paInfo.noPa = false;

    checkCompany();
  }
  getApiProvider();
});
</script>

<style scoped></style>
