<template>
  <!-- 기본정보 -->
  <div class="text-end mb-2">
    <button type="button" class="btn btn-primary" @click.prevent="handelSubmit" v-if="!editMode">기본판매정보 등록</button>
    <button type="button" class="btn btn-warning" @click.prevent="handelSubmit" v-else>저장</button>
  </div>
  <div class="card mb-2">
    <div class="card-header">[상품 기본 정보]</div>
    <div class="card-body">
      <div class="row col mb-4">
        <label class="col-md-2 col-form-label">상품유형선택</label>
        <div class="col-auto">
          <!-- Select -->
          <!-- 타입 [DP : 일반 배송, UP-EC : E-쿠폰, UP-OF : 티켓] -->
          <div class="tom-select-custom">
            <select v-model="type.value" class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' disabled>
              <option value="DP">일반 배송</option>
              <option value="UP-EC">E-쿠폰</option>
              <option value="UP-OF">티켓</option>
              <!--              <option value="G">상품그룹</option>-->
            </select>
          </div>
        </div>
      </div>
      <CommFormLine slot-parent="form-control border-0" :title="`외부연동업체`" v-if="type.value === 'UP-EC'">
        <div class="form-check form-check-inline" v-for="(item, i) in api_provider_list">
          <input id="provider1" v-model="api_provider.value" :value="item.value" type="radio" class="form-check-input" name="api_provider" disabled />
          <label class="form-check-label" for="provider1">{{ item.name }}</label>
        </div>
      </CommFormLine>
      <CommFormLine input-for="apiGoodsId" :title="`외부업체 상품 ID`" :width="8" v-if="type.value === 'UP-EC'">
        <input maxlength="100" v-model.trim="api_goods_id.value" id="apiGoodsId" type="text" class="form-control" placeholder="외부업체 상품 ID를 입력해주세요." aria-label="외부업체 상품 ID를 입력해주세요." disabled />
      </CommFormLine>
      <CommFormLine :title="`카테고리`" :width="8">
        <input type="text" class="form-control" :value="cateValues" placeholder="카테고리를 선택해주세요." aria-label="" disabled />
        <div class="d-md-none mt-1"></div>
        <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('modalCategory')">검색</button>
      </CommFormLine>
      <CommFormLine :title="`브랜드`" :width="8">
        <input type="text" class="form-control" :value="brandValues" placeholder="브랜드를 선택해주세요." aria-label="" disabled />
        <div class="d-md-none mt-1"></div>
        <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('modalBrands')">검색</button>
      </CommFormLine>
      <CommFormLine input-for="productName" :title="`상품명`" :width="8">
        <input maxlength="100" @change.prevent="checkNameValid" v-model.trim="name.value" id="productName" type="text" class="form-control" placeholder="상품명을 입력해주세요. (최대 100자)" aria-label="상품명을 입력해주세요." />
      </CommFormLine>
      <CommFormLine input-for="productSubTitle" :title="`부제목`" :width="8">
        <input maxlength="100" v-model.trim="subtitle.value" id="productSubTitle" type="text" class="form-control" placeholder="부제목을 입력해주세요. (최대 100자)" aria-label="부제목을 입력해주세요." />
      </CommFormLine>
      <CommFormLine input-for="code" :title="`상품코드`" :width="8">
        <input maxlength="255" v-model.trim="code.value" id="code" type="text" class="form-control" name="firstName" placeholder="상품 코드를 입력해주세요. (미입력시 자동생성)" aria-label="상품 코드를 입력해주세요. (미입력시 자동생성)" disabled />
      </CommFormLine>
      <CommFormLine input-for="words" :title="`검색어`" :width="8">
        <input v-model.trim="words.value" name="words" id="words" type="text" class="form-control" maxlength="1000" placeholder="검색어는 ,(콤마)로 구분됩니다. 1000자 까지 입력 가능 합니다." aria-label="검색어는 ,(콤마)로 구분됩니다. 1000자 까지 입력 가능 합니다." />
      </CommFormLine>
      <CommFormLine input-for="summary" :title="`간략설명`" :width="8">
        <textarea v-model.trim="summary.value" name="summary" id="summary" type="text" class="form-control" maxlength="255" placeholder="255자 까지 입력 가능합니다." aria-label="255자 까지 입력 가능합니다." />
      </CommFormLine>
    </div>
  </div>
  <!-- 기본정보 END -->
  <!-- 판매정보 -->
  <div class="card mb-2">
    <div class="card-header">[상품 판매 정보]</div>
    <div class="card-body">
      <CommFormLine slot-parent="form-control border-0" :title="`상품 판매 상태`" v-if="getUserClassStr.includes('PA') && status.value === 'N'">
        <div>
          <label class="form-check-label">미승인</label>
        </div>
      </CommFormLine>
      <CommFormLine slot-parent="form-control border-0" :title="`상품 판매 상태`" v-if="getUserClassStr.includes('CM') || status.value !== 'N'">
        <div class="form-check form-check-inline">
          <input value="Y" v-model="status.value" id="use_adult" type="radio" class="form-check-input" name="onsale" />
          <label class="form-check-label" for="use_adult">정상</label>
        </div>
        <div class="form-check form-check-inline">
          <input value="P" v-model="status.value" id="stop_adult" type="radio" class="form-check-input" name="stop" />
          <label class="form-check-label" for="stop_adult">판매중지</label>
        </div>
        <div class="form-check form-check-inline">
          <input value="S" v-model="status.value" id="soldout_adult" type="radio" class="form-check-input" name="soldout" />
          <label class="form-check-label" for="soldout_adult">품절</label>
        </div>
        <div class="form-check form-check-inline" v-if="getUserClassStr.includes('CM')">
          <input value="N" v-model="status.value" id="deny_adult" type="radio" class="form-check-input" name="deny" />
          <label class="form-check-label" for="deny_adult">미승인</label>
        </div>
      </CommFormLine>
      <CommFormLine slot-parent="form-control border-0" :title="`노출여부`">
        <div class="form-check form-check-inline">
          <input value="Y" v-model="view.value" id="use_view" type="radio" class="form-check-input" name="use_view" />
          <label class="form-check-label" for="use_view">노출</label>
        </div>
        <div class="form-check form-check-inline">
          <input value="N" v-model="view.value" id="none_view" type="radio" class="form-check-input" name="none_view" />
          <label class="form-check-label" for="none_view">미노출</label>
        </div>
      </CommFormLine>
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
  <!-- 판매정보 ENd -->
  <!-- 상품 log-->
  <div class="card" v-if="getUserClassStr.includes('CM')">
    <div class="card-header">변경이력</div>
    <div class="card-body">
      <div class="row mb-2 align-items-center justify-content-between">
        <div class="col-auto"></div>
        <div class="col-auto">
          <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
        </div>
      </div>
      <div class="table-responsive">
        <table class="table table-align-middle card-table table-borderless">
          <thead class="thead-light">
            <tr class="text-center">
              <th style="width: 12%">변경일</th>
              <th style="width: 8%">등록/수정</th>
              <th style="width: 20%">항목</th>
              <th style="width: 20%">변경전</th>
              <th style="width: 20%">변경후</th>
              <th style="width: 12%">변경자</th>
              <th style="width: 8%">상세</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in mProdLog.datas" :key="JSON.stringify(item)">
              <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
              <td>{{ item.action }}</td>
              <td>
                <div v-if="item.action === '옵션 등록'">{{ convertLogOptionRegItemCate(item.msg) }}</div>
                <div v-else>{{ convertLogItemCate(item.msg, item.action).replace(/\/\/\//g, ' / ') }}</div>
              </td>
              <td style="max-width: 8rem">
                <div v-if="item.action === '옵션 등록'">-</div>
                <div v-else>
                  {{
                    convertLogItem(item.msg, 'before').length > 20
                      ? convertLogItem(item.msg, 'before')
                          .slice(0, 20)
                          .replace(/\/\/\//g, ' / ') + '...'
                      : convertLogItem(item.msg, 'before').replace(/\/\/\//g, ' / ')
                  }}
                </div>
              </td>
              <td style="max-width: 8rem">
                <div v-if="item.action === '옵션 등록'">
                  {{ convertLogOptionRegItem(item.msg).length > 20 ? convertLogOptionRegItem(item.msg).slice(0, 20) + '...' : convertLogOptionRegItem(item.msg) }}
                </div>
                <div v-else>
                  {{
                    convertLogItem(item.msg, 'after').length > 20
                      ? convertLogItem(item.msg, 'after')
                          .slice(0, 20)
                          .replace(/\/\/\//g, ' / ') + '...'
                      : convertLogItem(item.msg, 'after').replace(/\/\/\//g, ' / ')
                  }}
                </div>
              </td>
              <td>{{ item.writer }}</td>
              <td>
                <span v-if="item.action === '옵션 등록'" class="badge text-bg-primary" style="cursor: pointer" @click.prevent="openOptionRegChangeHistoryModal(convertLogOptionRegItemCate(item.msg), convertLogOptionRegItem(item.msg))">상세보기</span>
                <span v-else class="badge text-bg-primary" style="cursor: pointer" @click.prevent="openChangeHistoryModal(convertLogItemCate(item.msg, item.action), convertLogItem(item.msg, 'before'), convertLogItem(item.msg, 'after'))">상세보기</span>
              </td>
            </tr>
            <tr>
              <td colspan="6" class="text-center" v-if="mProdLog.total === 0">표시할 항목이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="table-footer-area" v-if="mProdLog.total > 0">
        <div class="row" v-if="total_page > 1">
          <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
        </div>
      </div>
    </div>
  </div>
  <!-- 상품 log END-->

  <!-- 카테고리 선택 Modal -->
  <DynamicColumnModal modal-id="modalCategory" modal-name="카테고리" @choice="onChangeCategory" :parent="props.cate" :type="'getCategories'" :selected="selectedCategories" />
  <!-- 브랜드 선택 Modal -->
  <ColumnSelectionModal modal-id="modalBrands" modal-name="브랜드" @choice="onChangeBrand" :parent="props.brands" :type="'getBrands'" :selected="selectedBrand" />
  <ChangeHistoryModal :id="'changeHistoryModal'" :logTitle="logData.title" :logBefore="logData.before" :logAfter="logData.after" />
  <ChangeOptionRegHistoryModal :id="'changeOptionRegHistoryModal'" :logTitle="logData.title" :logAfter="logData.after" />
</template>

<script setup lang="ts">
import CommFormLine from '@/components/comm/CommFormLine.vue';
import { computed, onMounted, reactive, ref, PropType, watch } from 'vue';
import { arrayToStringWithComma } from '@/utils/arrayParser';
import ColumnSelectionModal from '@/components/modals/product/ColumnSelectionModal.vue';
import DynamicColumnModal from '@/components/modals/product/DynamicColumnModal.vue';
import type { IBrand, ICategory } from '@/components/product/type';
import { AxiosError } from 'axios';
import type { Category, Prod, Log } from 'ProductListInfoModule';
import apis from '@/apis';
import { apiResponseCheck, getUserClassStr, showAlert, showConfirm, dateTimeFormatConverter, convertProductLog, showModal, hideModal } from '@/utils/common-utils';
import Pagination from '@/components/comm/Pagination.vue';
import { useUserStore } from '@/stores/user';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import ChangeHistoryModal from '@/components/modals/comm/ChangeHistoryModal.vue';
import ChangeOptionRegHistoryModal from '@/components/modals/comm/ChangeOptionRegHistoryModal.vue';

const emits = defineEmits(['setProductId', 'changedProdInfo']);

const props = defineProps({
  prodId: { type: Number, default: 0 },
  prodInfo: { type: Object as PropType<Prod | null>, default: null },
  editMode: { type: Boolean, default: false },
  type: { type: String, default: '' },
  cate: { type: Array, default: () => [] },
  brands: { type: Array, default: () => [] },
  name: { type: String, default: '' },
  code: { type: String, default: '' },
  words: { type: String, default: '' },
  summary: { type: String, default: '' },
  api_provider: { type: String, default: '' },
  api_goods_id: { type: String, default: '' },
});

const mProdLog = ref({} as Log);
const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mProdLog.value.total / limit.value));

const logData = reactive({
  title: '',
  before: '',
  after: '',
});

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getProdLog();
};

const pageChange = (page: number) => {
  page_no.value = page;
  getProdLog();
  window.scrollTo({ top: 100, left: 0 });
};

const originProdInfo = ref({} as Prod);

const selectedCategories = ref<ICategory[][]>([]);
const selectedBrand = ref<{ id: number; name: string }[]>([]);
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

const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
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
const api_provider = reactive({ value: '', check: true, err_msg: '' });
const api_goods_id = reactive({ value: '', check: true, err_msg: '외부업체 상품 ID를 입력해주세요.' });

// 상품상세
const status = reactive({ value: 'N', check: true, err_msg: '' });
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
        showAlert('사용가능한 상품코드입니다.', 'success');
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
  for (const data of checkList) {
    if (!data.check) {
      showAlert(data.err_msg, 'warning');
      return;
    }
  }
  let data: any = {};

  if (type.value !== originProdInfo.value.type) {
    data['type'] = type.value;
  }
  if (subtitle.value !== originProdInfo.value.subtitle) {
    data['subtitle'] = subtitle.value;
  }
  if (name.value !== originProdInfo.value.name) {
    data['name'] = name.value;
  }
  if (code.value !== originProdInfo.value.code) {
    data['code'] = code.value;
  }
  if (words.value !== originProdInfo.value.keyword) {
    data['keyword'] = words.value;
  }
  if (summary.value !== originProdInfo.value.summary) {
    data['summary'] = summary.value;
  }
  if (inven.value !== originProdInfo.value.inven_use) {
    data['inven_use'] = inven.value;
  }
  if (view_inventory.value !== originProdInfo.value.view_inventory) {
    data['view_inventory'] = view_inventory.value;
  }
  if (view.value !== originProdInfo.value.view_yn) {
    data['view_yn'] = view.value;
  }
  if (tax.value !== originProdInfo.value.tax) {
    data['tax'] = tax.value;
  }
  if (cancel.value !== originProdInfo.value.cancel_yn) {
    data['cancel_yn'] = cancel.value;
  }
  if (resale.value !== originProdInfo.value.resale) {
    data['resale'] = resale.value;
  }
  if (adult.value !== originProdInfo.value.adult) {
    data['adult'] = adult.value;
  }
  if (ipcc.value !== originProdInfo.value.ipcc_yn) {
    data['ipcc_yn'] = ipcc.value;
  }
  if (status.value !== originProdInfo.value.status) {
    data['status'] = status.value;
  }

  const categoryChange = JSON.stringify(selectedCategories.value) !== JSON.stringify(convertCategory(originProdInfo.value.categories));
  const brandChange = JSON.stringify(selectedBrand.value) !== JSON.stringify(originProdInfo.value.brands);

  if (Object.keys(data).length === 0 && !categoryChange && !brandChange) {
    showAlert('변경된 내용이 없습니다.', 'warning');
    return;
  }

  showConfirm('상품 기본판매정보를 수정하시겠습니까?', () => {
    if (Object.keys(data).length > 0) {
      apis.product.updateBaseInfo(props.prodId, data).then(res => {
        apiResponseCheck(res, () => {
          if (categoryChange || brandChange) {
            const unLinkBrand = apis.product.unlinkBrand(props.prodId);
            const unLinkCategory = apis.product.unlinkCategory(props.prodId);
            Promise.all([unLinkBrand, unLinkCategory]).then(() => {
              // 브랜드 insert
              const linkBrand = apis.product.linkBrand({ productId: props.prodId, brandId: selectedBrand.value.map(sb => sb.id) });
              // 카테고리 insert
              const linkCategory = apis.product.linkCategory({ productId: props.prodId, categoryId: categories.selectedCategories.map(sc => sc[sc.length - 1].id) });
              Promise.all([linkBrand, linkCategory]).then(() => {
                showAlert('상품 기본판매정보가 수정되었습니다.', 'success');
                emits('changedProdInfo');
              });
            });
          } else {
            showAlert('상품 기본판매정보가 수정되었습니다.', 'success');
            emits('changedProdInfo');
          }
        });
      });
    } else {
      const unLinkBrand = apis.product.unlinkBrand(props.prodId);
      const unLinkCategory = apis.product.unlinkCategory(props.prodId);
      Promise.all([unLinkBrand, unLinkCategory]).then(() => {
        // 브랜드 insert
        const linkBrand = apis.product.linkBrand({ productId: props.prodId, brandId: selectedBrand.value.map(sb => sb.id) });
        // 카테고리 insert
        const linkCategory = apis.product.linkCategory({ productId: props.prodId, categoryId: categories.selectedCategories.map(sc => sc[sc.length - 1].id) });
        Promise.all([linkBrand, linkCategory]).then(() => {
          showAlert('상품 기본판매정보가 수정되었습니다.', 'success');
          emits('changedProdInfo');
        });
      });
    }
  });
};

const convertCategory = (cate: Category[]): ICategory[][] => {
  const cateList = [] as ICategory[][];
  for (const c of cate) {
    const cateDetail = [] as ICategory[];
    if (c.depth1_id !== null) {
      cateDetail.push({ id: c.depth1_id ? c.depth1_id : c.id, name: c.depth1_name! });
    }
    if (c.depth2_id !== null) {
      cateDetail.push({ id: c.depth2_id ? c.depth2_id : c.id, name: c.depth2_name! });
    }
    if (c.depth3_id !== null) {
      cateDetail.push({ id: c.depth3_id ? c.depth3_id : c.id, name: c.depth3_name! });
    }
    if (c.depth4_id !== null) {
      cateDetail.push({ id: c.depth4_id ? c.depth4_id : c.id, name: c.depth4_name! });
    }
    cateDetail.push({ id: c.id, name: c.name });
    cateList.push(cateDetail);
  }
  return cateList;
};

const setProdInfo = () => {
  const origin = JSON.parse(JSON.stringify(props.prodInfo));
  originProdInfo.value = origin;

  selectedCategories.value = convertCategory(originProdInfo.value.categories);
  selectedBrand.value = JSON.parse(JSON.stringify(originProdInfo.value.brands));
  type.value = originProdInfo.value.type;

  categories.check = true;
  brands.check = true;
  name.value = originProdInfo.value.name;
  name.check = true;
  subtitle.value = originProdInfo.value.subtitle;
  subtitle.check = true;
  code.value = originProdInfo.value.code;
  code.check = true;
  words.value = originProdInfo.value.keyword;
  words.check = true;
  summary.value = originProdInfo.value.summary;
  summary.check = true;
  api_provider.value = originProdInfo.value.api_provider;
  api_provider.check = true;
  api_goods_id.value = originProdInfo.value.api_goods_id;
  api_goods_id.check = true;

  status.value = originProdInfo.value.status;
  adult.value = originProdInfo.value.adult;
  view.value = originProdInfo.value.view_yn;
  ipcc.value = originProdInfo.value.ipcc_yn;
  cancel.value = originProdInfo.value.cancel_yn;
  resale.value = originProdInfo.value.resale;
  tax.value = originProdInfo.value.tax;
  inven.value = originProdInfo.value.inven_use;
  view_inventory.value = originProdInfo.value.view_inventory;
  view_inventory.value = originProdInfo.value.view_inventory;
};

const convertLogItemCate = (data: string, action: string = ''): string => {
  let logItem = [];
  const json = JSON.parse(data);

  if (Array.isArray(json.data)) {
    if (!json.data.length) {
      logItem.push(`-`);
      return logItem.toString();
    }
    for (const i of json.data) {
      for (const k of Object.keys(i)) {
        if (Object.keys(i[k]).length === 0) continue;
        logItem.push(`${convertProductLog(k)}`);
        break;
      }
    }
  } else {
    logItem.push(action);
  }
  return logItem.join('///');
};

const convertLogItem = (data: string, when: string): string => {
  let logItem = [];
  const json = JSON.parse(data);

  if (Array.isArray(json.data)) {
    if (!json.data.length) {
      logItem.push(`-`);
      return logItem.toString();
    }
    for (const i of json.data) {
      for (const k of Object.keys(i)) {
        if (Object.keys(i[k]).length === 0) continue;
        if (!i[k][when]) {
          logItem.push('-');
          break;
        }
        if (k === 'contents') {
          logItem.push(`${k} 변경`);
          break;
        }
        logItem.push(i[k][when]);
      }
    }
  } else {
    if (when === 'after') {
      if (json.data.includes('->')) {
        const splitData = json.data.split('->');
        logItem.push(splitData[1]);
        return logItem[0];
      }
      logItem.push(json.data);
    } else {
      if (json.data.includes('->')) {
        const splitData = json.data.split('->');
        logItem.push(splitData[0]);
        return logItem[0];
      }
      logItem.push('-');
    }
  }
  return logItem.join('///');
};

const convertLogOptionRegItemCate = (data: string): string => {
  let logItem = [];
  const json = JSON.parse(JSON.parse(data).data.replace('옵션 등록 - ', ''));
  for (const k of Object.keys(json)) {
    if (k === 'option_tmp_price') continue;
    if (json[k]) {
      logItem.push(`${convertProductLog(k)}`);
    }
  }
  return logItem.join(' / ');
};

const convertLogOptionRegItem = (data: string) => {
  let logItem = [];
  const json = JSON.parse(JSON.parse(data).data.replace('옵션 등록 - ', ''));

  for (const k of Object.keys(json)) {
    if (k === 'option_tmp_price') continue;
    if (json[k]) {
      logItem.push(json[k]);
    }
  }
  return logItem.join(' / ');
};

const getProdLog = () => {
  apis.product.getProdLog(props.prodId, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      mProdLog.value.datas = res.datas;
      mProdLog.value.total = res.total;
    });
  });
};

watch(
  () => props.prodInfo,
  info => {
    setProdInfo();

    if (userClass.value.includes('CM')) {
      getProdLog();
    }
  },
);
watch(inven, () => {
  if (inven.value === 'N') {
    view_inventory.value = 'N';
  }
});

const onStepActive = () => {
  if (props.prodId !== 0) {
    setProdInfo();
  }
};

const getApiProvider = () => {
  apis.product.get_api_provider_List().then(res => {
    apiResponseCheck(res, () => {
      api_provider_list.value = res;
    });
  });
};

const openChangeHistoryModal = (title: string, before: string, after: string) => {
  logData.title = title;
  logData.before = before;
  logData.after = after;
  showModal('changeHistoryModal');
};
const openOptionRegChangeHistoryModal = (title: string, after: string) => {
  logData.title = title;
  logData.after = after;
  showModal('changeOptionRegHistoryModal');
};

defineExpose({ onStepActive });

onMounted(() => {
  limit.value = useCommonStore().getLimit;
  getApiProvider();
});
</script>

<style scoped></style>
