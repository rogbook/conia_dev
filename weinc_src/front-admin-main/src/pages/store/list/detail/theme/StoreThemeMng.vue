<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세'] : ['상점 관리', '상점관리 상세']" :current="'테마 관리'" />
  <div class="card">
    <div class="card-header py-2">
      <div class="form-control-borderless h2 mb-0">테마 관리 - [상점코드 : {{ storeCode }}]</div>
    </div>
    <div class="card-body">
      <div class="row justify-content-between">
        <div class="card col-md-4 col-lg-3 me-4">
          <div class="card-header py-2 pe-0">
            <div class="text-end">
              <button type="button" class="btn btn-sm btn-success" @click.prevent="showModal('addThemeModal')">테마추가</button>
              <!--              <button type="button" class="btn btn-sm btn-danger" @click.prevent="delTheme">삭제</button>-->
            </div>
          </div>
          <div class="card-body">
            <tree-view-store-theme v-for="item in themeList" :key="item.id" :name="item.name" :sort="item.sort" :sub="item.sub" :isRoot="false" :theme="item" @selectTheme="selectTheme" @addThemeModal="addThemeModal"> </tree-view-store-theme>

            <!--            &lt;!&ndash; List Group &ndash;&gt;-->
            <!--            <ul class="list-group-flush ms-0 ps-0">-->
            <!--              <li class="list-group-item py-2" v-for="t1 in themeList" :key="t1.id" v-show="!t1.pid">-->
            <!--                <input class="form-check-input me-2" type="radio" name="sel_theme_id" :value="t1" v-model="selThemeRadio" v-if="false" />-->
            <!--                <span>{{ t1.name }}</span>-->
            <!--                <span style="font-size: 0.5rem"> (표시순번 : {{ t1.sort }})</span>-->
            <!--                <button type="button" class="btn badge bg-info ms-2 me-2" @click.prevent="selectTheme(t1)">설정</button>-->
            <!--                <button type="button" class="btn btn-white btn-sm border-0 p-0" @click.prevent="addThemeModal(t1.id, t1.name)">-->
            <!--                  <i class="bi bi-plus-square text-primary" style="font-size: 14px"></i>-->
            <!--                </button>-->
            <!--                <ul class="list-group-flush mt-2" v-if="t1.sub">-->
            <!--                  <li class="list-group-item py-2" v-for="t2 in t1.sub" :key="t2.id">-->
            <!--                    <input class="form-check-input me-2" type="radio" name="sel_theme_id" :value="t2" v-model="selThemeRadio" v-if="false" />-->
            <!--                    <span>{{ t2.name }}</span>-->
            <!--                    <span style="font-size: 0.5rem"> (표시순번 : {{ t2.sort }})</span>-->
            <!--                    <button type="button" class="btn badge bg-info ms-2" @click.prevent="selectTheme(t2)">설정</button>-->
            <!--                    <ul class="list-group-flush mt-2" v-if="t2.sub">-->
            <!--                      <li class="list-group-item py-2" v-for="t3 in t2.sub" :key="t3.id">-->
            <!--                        <input class="form-check-input me-2" type="radio" name="sel_theme_id" :value="t3" v-model="selThemeRadio" v-if="false" />-->
            <!--                        <span>{{ t3.name }}</span>-->
            <!--                        <button type="button" class="btn badge bg-info ms-2" @click.prevent="selectTheme(t3)">설정</button>-->
            <!--                        <ul class="list-group-flush mt-2" v-if="t3.sub">-->
            <!--                          <li class="list-group-item py-2" v-for="t4 in t3.sub" :key="t4.id">-->
            <!--                            <input class="form-check-input me-1" type="radio" name="sel_theme_id" :value="t4" v-model="selThemeRadio" v-if="false" />-->
            <!--                            <span>{{ t4.name }}</span>-->
            <!--                            <button type="button" class="btn badge bg-info ms-2" @click.prevent="selectTheme(t4)">설정</button>-->
            <!--                          </li>-->
            <!--                        </ul>-->
            <!--                      </li>-->
            <!--                    </ul>-->
            <!--                  </li>-->
            <!--                </ul>-->
            <!--              </li>-->
            <!--            </ul>-->
            <!--            &lt;!&ndash; End List Group &ndash;&gt;-->
          </div>
        </div>
        <div class="d-md-none mt-2"></div>
        <div class="card col" v-if="selTheme.show">
          <div class="card-header">
            <span>선택한 테마 - [{{ selTheme.theme.name }}]</span>
            <span class="ms-2"><MobilePushLink :title="`테마 [ ${selTheme.theme.name} ]`" :storeGroup="storeGroup" :nextValue="`theme/${selTheme.id}`" :isStore="true" /></span>
          </div>
          <div class="card-body">
            <div class="row col mb-2 align-items-center">
              <label class="col-md-2 col-form-label"><span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 테마명</label>
              <div class="col-md-4">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="테마명을 입력해주세요." maxlength="20" v-model.trim="themeInfo.name" />
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-2 col-form-label"><span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 테마내용</label>
              <div class="col-md-4">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="테마 내용을 입력해주세요." maxlength="255" v-model.trim="themeInfo.description" />
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-2 col-form-label"><span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 표시순번 (1~99)</label>
              <div class="col-md-4">
                <!-- Select -->
                <div class="tom-select-custom">
                  <select class="form-select" v-model="themeInfo.sort" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                    <option v-for="i in 99" :key="i" :value="i">{{ i }}</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-2 col-form-label">테마 사용여부</label>
              <div class="col">
                <div class="row form-control border-0">
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_status_y" type="radio" class="form-check-input" name="radio_status" value="Y" v-model="themeInfo.status" />
                    <label class="form-check-label" for="radio_status_y">사용</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_status_n" type="radio" class="form-check-input" name="radio_status" value="N" v-model="themeInfo.status" />
                    <label class="form-check-label" for="radio_status_n">사용안함</label>
                  </div>
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-2 col-form-label">테마 노출여부</label>
              <div class="col">
                <div class="row form-control border-0">
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_visible_y" type="radio" class="form-check-input" name="radio_visible" value="Y" v-model="themeInfo.visible" />
                    <label class="form-check-label" for="radio_visible_y">노출</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_visible_n" type="radio" class="form-check-input" name="radio_visible" value="N" v-model="themeInfo.visible" />
                    <label class="form-check-label" for="radio_visible_n">비노출</label>
                  </div>
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-2 col-form-label">상단메뉴에 노출</label>
              <div class="col">
                <div class="row form-control border-0">
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_top_y" type="radio" class="form-check-input" name="radio_top_visible" value="Y" v-model="themeInfo.top_visible" />
                    <label class="form-check-label" for="radio_top_y">사용</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_top_n" type="radio" class="form-check-input" name="radio_top_visible" value="N" v-model="themeInfo.top_visible" />
                    <label class="form-check-label" for="radio_top_n">사용안함</label>
                  </div>
                </div>
              </div>
            </div>

            <div class="row align-items-center">
              <div class="col-md-2">
                <label class="col-form-label">테마 유형</label>
              </div>
              <div class="col-sm-auto col-md-auto ms-1 py-2">
                <div class="form-check">
                  <input id="radio_layout_y" type="radio" class="form-check-input" name="radio_layout" value="Y" @change="layoutUseChange" v-model="themeInfo.use_layout" />
                  <label class="form-check-label" for="radio_layout_y">레이아웃</label>
                </div>
              </div>
              <div class="col-md-auto">
                <button type="button" class="btn btn-sm btn-success" v-if="themeInfo.use_layout === 'Y' || themeInfo.use_layout === 'L'" @click.prevent="showModal('setThemeLayoutModal')">레이아웃 설정</button>
              </div>
              <div class="col-sm-auto col-md-auto ms-1 py-2">
                <div class="form-check">
                  <input id="radio_layout_n" type="radio" class="form-check-input" name="radio_layout" value="N" @change="layoutUseChange" v-model="themeInfo.use_layout" />
                  <label class="form-check-label" for="radio_layout_n">상품</label>
                </div>
              </div>
              <div class="col-sm-auto col-md-auto">
                <button type="button" class="btn btn-sm btn-success" v-if="themeInfo.use_layout === 'N' || themeInfo.use_layout === 'P'" @click.prevent="showModal('setThemeProductModal')">상품관리</button>
                <button type="button" class="btn btn-sm btn-success ms-2" v-if="themeInfo.use_layout === 'N' || themeInfo.use_layout === 'P'" @click.prevent="showModal('setThemeLayoutModal')">상단 레이아웃</button>
              </div>
              <div class="col-sm-auto col-md-auto ms-1 py-2">
                <div class="form-check">
                  <input id="radio_layout_s" type="radio" class="form-check-input" name="radio_layout" value="S" @change="layoutUseChange" v-model="themeInfo.use_layout" />
                  <label class="form-check-label" for="radio_layout_s">매장</label>
                </div>
              </div>
              <div class="col-sm-auto col-md-auto">
                <button type="button" class="btn btn-sm btn-success" v-if="themeInfo.use_layout === 'S'" @click.prevent="showModal('setThemeShopModal')">매장관리</button>
                <button type="button" class="btn btn-sm btn-success ms-2" v-if="themeInfo.use_layout === 'S'" @click.prevent="showModal('setThemeLayoutModal')">상단 레이아웃</button>
              </div>
            </div>
          </div>
          <div class="card-footer py-2">
            <div class="text-end">
              <button type="button" class="btn btn-sm btn-danger me-2" @click.prevent="delTheme">삭제</button>
              <button type="button" class="btn btn-sm btn-primary" @click.prevent="modThemeInfo">저장</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 테마 상품관리 설정 Modal -->
  <Modal :id="'setThemeProductModal'" :title="'테마 상품 관리'" :xxlarge="true">
    <template #body>
      <StoreProdMng :themeName="selTheme.theme.name" :themeId="selTheme.theme.id" @openCategoryModal="openCategoryModal" @openBrandModal="openBrandModal" @openCategoryAddModal="openCategoryAddModal" @openBrandAddModal="openBrandAddModal" ref="themeProd" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <!-- 테마 매장관리 설정 Modal -->
  <Modal :id="'setThemeShopModal'" :title="'테마 매장 관리'" :xxlarge="true">
    <template #body>
      <StoreShopMng :themeName="selTheme.theme.name" :themeId="selTheme.theme.id" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <!-- 테마 신규 추가 Modal -->
  <Modal :id="'addThemeModal'" :title="'테마 신규 추가'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4" v-if="newTheme.pid_name">
          <b>상위 테마명 : [{{ newTheme.pid_name }}]</b>
        </div>
        <div class="text-start mb-2">신규 테마 기본정보</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <form class="mb-6">
              <div class="row col mb-4 align-items-center">
                <label class="col-md-3 col-form-label text-nowrap">테마명</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" v-model.trim="newTheme.name" maxlength="20" placeholder="테마명을 입력해주세요." />
                  </div>
                </div>
              </div>
              <div class="row col mb-4 align-items-center">
                <label class="col-md-3 col-form-label text-nowrap">테마설명</label>
                <div class="col">
                  <div class="input-group">
                    <textarea type="text" class="form-control" rows="5" v-model.trim="newTheme.description" maxlength="255" placeholder="테마에 대한 설명을 입력해주세요." />
                  </div>
                </div>
              </div>
            </form>
            <!-- Modal Search Form End -->
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="addTheme">테마 생성</button>
    </template>
  </Modal>

  <!-- 컴포넌트 설정 Modal -->
  <Modal :id="'setComponentData'" :title="'컴포넌트 구성 설정'" :xlarge_big="true" :second="true" :centered="true" :is-editor-in="true">
    <template #body>
      <SetComponentInfo @openProdModal="openProdModal" @passToCompInfo="passToCompInfo" @deleteBackImg="deleteBackImg" :storeCode="storeCode" :compData="selCompData" :themeList="themeList" ref="setCompModalRef" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button
        type="button"
        class="btn btn-primary"
        @click.prevent="
          () => {
            setCompModalRef.saveClicked();
          }
        ">
        저장
      </button>
    </template>
  </Modal>

  <!-- 컴포넌트 상품 조회 Modal -->
  <Modal :id="'getProductListModal'" :title="'상점 상품 목록'" :xlarge="true" :third="true" :centered="true">
    <template #body>
      <StoreProductList @passToProduct="passToProduct" @passToProducts="passToProducts" ref="getProductList" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <!-- 컴포넌트 상점 조회 Modal -->
  <Modal :id="'getShopListModal'" :title="'상점 매장 목록'" :xlarge="true" :third="true" :centered="true">
    <template #body>
      <StoreShopList @passToShop="passToShop" ref="getShopList" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <!-- 테마 레이아웃 설정 Modal -->
  <Modal :id="'setThemeLayoutModal'" :title="'테마 레이아웃 설정'" :xxlarge="true">
    <template #body>
      <SetThemeLayout :themeName="selTheme.theme.name" :layout="selectedLayout" @modThemeLayout="modThemeLayout" @receiveFromCompInfo="receiveFromCompInfo" ref="setThemeLayout" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <!-- 카테고리 선택-->
  <Modal :id="'SelCategoryModal'" :title="'카테고리 선택'">
    <template #body>
      <SelectCategoryModal ref="CategoryModal" @closeModal="closeCategoryModal" />
    </template>
  </Modal>

  <!-- 브랜드 선택-->
  <Modal :id="'SelBrandModal'" :title="'브랜드 선택'">
    <template #body>
      <SelectBrandModal @closeModal="closeBrandModal" />
    </template>
  </Modal>

  <!-- 카테고리 선택-->
  <Modal :id="'SelCategoryAddModal'" :title="'카테고리 선택'">
    <template #body>
      <SelectCategoryModal ref="CategoryAddModal" @closeModal="closeCategoryAddModal" />
    </template>
  </Modal>

  <!-- 브랜드 선택-->
  <Modal :id="'SelBrandAddModal'" :title="'브랜드 선택'">
    <template #body>
      <SelectBrandModal @closeModal="closeBrandAddModal" />
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import { AxiosError } from 'axios';
import type { Theme } from 'ThemeInfoModule';
import Modal from '@/components/comm/modal.vue';
import SetThemeLayout from '@/pages/store/list/detail/theme/layout/SetThemeLayout.vue';
import SetComponentInfo from '@/pages/store/list/detail/theme/layout/comp/SetComponentInfo.vue';
import StoreProductList from '@/pages/store/list/detail/theme/StoreProductList.vue';
import StoreProdMng from '@/pages/store/list/detail/theme/product/StoreProdMng.vue';
import StoreShopMng from '@/pages/store/list/detail/theme/shop/StoreShopMng.vue';
import { apiResponseCheck, checkPermission, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import StoreShopList from '@/pages/store/list/detail/theme/StoreShopList.vue';
import MobilePushLink from '@/components/comm/MobilePushLink.vue';
import SelectCategoryModal from '@/components/modals/product/SelectCategoryModal.vue';
import SelectBrandModal from '@/components/modals/product/SelectBrandModal.vue';
import TreeViewStoreTheme from '@/pages/store/list/detail/theme/TreeViewStoreTheme.vue';
const CategoryModal = ref();
const CategoryAddModal = ref();
const themeProd = ref();

const openCategoryModal = () => {
  showModal('SelCategoryModal');
  CategoryModal.value.openModal();
};
const openBrandModal = () => {
  showModal('SelBrandModal');
};
const closeCategoryModal = (cateId: number, cateLabel: string) => {
  themeProd.value.closeCategoryModal(cateId, cateLabel);
  hideModal('SelCategoryModal');
};
const closeBrandModal = (brandId: number, brandName: string) => {
  themeProd.value.closeBrandModal(brandId, brandName);
  hideModal('SelBrandModal');
};

const openCategoryAddModal = () => {
  showModal('SelCategoryAddModal');
  CategoryAddModal.value.openModal();
};
const openBrandAddModal = () => {
  showModal('SelBrandAddModal');
};
const closeCategoryAddModal = (cateId: number, cateLabel: string) => {
  themeProd.value.closeCategoryAddModal(cateId, cateLabel);
  hideModal('SelCategoryAddModal');
};
const closeBrandAddModal = (brandId: number, brandName: string) => {
  themeProd.value.closeBrandAddModal(brandId, brandName);
  hideModal('SelBrandAddModal');
};

const router = useRouter();
const setThemeLayout = ref();
const getProductList = ref();
const getShopList = ref();
const storeCode = ref();
const storeGroup = ref();
const themeList = ref([] as Theme[]);
const isSetLayout = ref(false);
const selThemeRadio = ref({} as Theme);
const selTheme = ref({
  show: false,
  id: -1,
  theme: {} as Theme,
});
const selectedLayout = ref('');
const newTheme = ref({
  name: '',
  description: '',
  pid: 0,
  pid_name: '',
});

const themeInfo = reactive({
  name: '',
  description: '',
  use_layout: '',
  status: '',
  top_visible: '',
  visible: '',
  sort: 99,
});

//레이아웃 설정에서 선택한 컴포넌트의 구성 데이터
const selCompData = reactive({
  data: {} as any,
  id: -1,
  compType: '',
  top: '',
  compId: '',
  background: '',
  memo: '',
});

const setCompModalRef = ref();

const getStoreThemeList = () => {
  apis.store.get_store_theme_list(storeCode.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      themeList.value = res;
    });
  });
};

const addThemeModal = (id: number, name: string) => {
  newTheme.value.pid = id;
  newTheme.value.pid_name = name;
  showModal('addThemeModal');
};

const selectTheme = (theme: Theme) => {
  console.log('StoreThemeMng', 'selectTheme called');
  if (selTheme.value.id === theme.id) {
    selTheme.value.id = -1;
    selTheme.value.show = false;
    isSetLayout.value = false;
    selectedLayout.value = '';
    return;
  }
  selTheme.value.id = theme.id;
  selTheme.value.theme = theme;
  selTheme.value.show = true;
  isSetLayout.value = !!selTheme.value.theme.layout;
  selectedLayout.value = selTheme.value.theme.layout;

  themeInfo.name = selTheme.value.theme.name;
  themeInfo.description = selTheme.value.theme.description;
  themeInfo.status = selTheme.value.theme.status;
  themeInfo.use_layout = selTheme.value.theme.use_layout;
  themeInfo.top_visible = selTheme.value.theme.top_visible;
  themeInfo.visible = selTheme.value.theme.visible;
  themeInfo.sort = selTheme.value.theme.sort;
};

const modThemeInfo = () => {
  if (!themeInfo.name) {
    showAlert('테마명을 입력해주세요.', 'warning');
    return;
  }
  if (!themeInfo.description) {
    showAlert('테마 설명을 입력해주세요.', 'warning');
    return;
  }
  const sort = selTheme.value.theme.sort !== themeInfo.sort;

  showConfirm('테마 정보를 변경하시겠습니까?', () => {
    apis.store.mod_store_theme(storeCode.value, selTheme.value.id, themeInfo).then(res => {
      apiResponseCheck(res, () => {
        showAlert('테마 정보가 변경되었습니다.', 'success');
        selTheme.value.theme.name = themeInfo.name;
        selTheme.value.theme.description = themeInfo.description;
        selTheme.value.theme.status = themeInfo.status;
        selTheme.value.theme.visible = themeInfo.visible;
        selTheme.value.theme.use_layout = themeInfo.use_layout;
        selTheme.value.theme.top_visible = themeInfo.top_visible;
        selTheme.value.theme.sort = themeInfo.sort;
        if (sort) {
          getStoreThemeList();
        }
      });
    });
  });
};

const layoutUseChange = () => {
  apis.store.mod_store_theme(storeCode.value, selTheme.value.id, { use_layout: themeInfo.use_layout }).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      showAlert('테마유형 설정이 변경되었습니다.', 'success');
      selTheme.value.theme.name = themeInfo.name;
      selTheme.value.theme.description = themeInfo.description;
      selTheme.value.theme.status = themeInfo.status;
      selTheme.value.theme.visible = themeInfo.visible;
      selTheme.value.theme.use_layout = themeInfo.use_layout;
      selTheme.value.theme.top_visible = themeInfo.top_visible;
    });
  });
};

const modThemeLayout = (layoutStr: string) => {
  apis.store.mod_store_theme(storeCode.value, selTheme.value.id, { layout: layoutStr }).then(res => {
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      selectedLayout.value = '';
      selectedLayout.value = selTheme.value.theme.layout;
      hideModal('setThemeLayoutModal');
    } else {
      //@ts-ignore
      hideModal('setThemeLayoutModal');
      showAlert('레이아웃이 설정되었습니다.', 'success');
      // 레이아웃 설정 완료 시 true
      selTheme.value.theme.layout = layoutStr;
      selectedLayout.value = selTheme.value.theme.layout;
      isSetLayout.value = true;
    }
  });
};

const addTheme = () => {
  if (!newTheme.value.name) {
    showAlert('테마명을 입력해주세요.', 'warning');
    return;
  }
  if (!newTheme.value.description) {
    showAlert('테마 설명을 입력해주세요.', 'warning');
    return;
  }

  let themeInfo = { name: newTheme.value.name, description: newTheme.value.description, store_code: storeCode.value } as any;
  if (newTheme.value.pid) {
    themeInfo['pid'] = newTheme.value.pid;
  }

  showConfirm('테마를 등록하시겠습니까?', () => {
    apis.store.add_store_theme(storeCode.value, themeInfo).then(res => {
      if (res instanceof AxiosError) {
        const error = res.response?.data;
        if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        return false;
      } else {
        showAlert('테마가 생성되었습니다.', 'success');
        hideModal('addThemeModal');
        newTheme.value.name = '';
        newTheme.value.description = '';
        getStoreThemeList();
      }
    });
  });
};

const delTheme = () => {
  showConfirm(`[${selTheme.value.theme.name}] 테마를 삭제하시겠습니까?<br/><span class='text-danger'>&#8251; 하위 테마가 존재하는 경우 모두 삭제 됩니다.</span>`, () => {
    if (selTheme.value.theme.sub?.length > 0) {
      const result = [];
      for (const i of selTheme.value.theme.sub) {
        const re = apis.store.mod_store_theme(storeCode.value, i.id, { status: 'D' }).then(res => {
          apiResponseCheck(res, () => {
            return true;
          });
        });
        result.push(re);
      }
      const re = apis.store.mod_store_theme(storeCode.value, selTheme.value.id, { status: 'D' }).then(res => {
        apiResponseCheck(res, () => {
          return true;
        });
      });
      result.push(re);
      Promise.all(result).then(() => {
        showAlert('테마가 삭제 되었습니다.', 'success', () => {
          window.location.reload();
        });
      });
    } else {
      apis.store.mod_store_theme(storeCode.value, selTheme.value.id, { status: 'D' }).then(res => {
        apiResponseCheck(res, () => {
          showAlert('테마가 삭제 되었습니다.', 'success', () => {
            window.location.reload();
          });
        });
      });
    }
  });
};

const receiveFromCompInfo = (id: number, data: any, compType: string, top: string, compId: string, background?: string, memo?: string) => {
  selCompData.data = data;
  selCompData.id = id;
  selCompData.compType = compType;
  selCompData.compId = compId;
  selCompData.top = top;

  if (background) {
    selCompData.background = background;
  } else {
    selCompData.background = '';
  }
  if (memo) {
    selCompData.memo = memo;
  } else {
    selCompData.memo = '';
  }

  showModal('setComponentData');
  setCompModalRef.value.showCompInfo();
};

const passToCompInfo = (data: any) => {
  hideModal('setComponentData');

  setThemeLayout.value.setComponentInfo(data);
  selCompData.id = -1;
};

const deleteBackImg = (data: any) => {
  setThemeLayout.value.deleteBackImg(data);
};

const passToProduct = (id: number, name: string, photo: string | undefined) => {
  hideModal('getProductListModal');
  setCompModalRef.value.receiveProduct(id, name, photo);
};

const passToProducts = (products: any[]) => {
  hideModal('getProductListModal');
  setCompModalRef.value.receiveProducts(products);
};

const passToShop = (id: number, name: string, photo: string) => {
  hideModal('getShopListModal');
  setCompModalRef.value.receiveShop(id, name, photo);
};

const openProdModal = (flag: boolean) => {
  getProductList.value.setMod(flag);
  showModal('getProductListModal');
};

const setModalListener = () => {
  //@ts-ignore
  document.getElementById('setThemeLayoutModal').addEventListener('show.bs.modal', function (event) {
    selectedLayout.value = selTheme.value.theme.layout;
  });

  //@ts-ignore
  document.getElementById('setThemeLayoutModal').addEventListener('hide.bs.modal', function (event) {
    selectedLayout.value = '';
  });

  //@ts-ignore
  document.getElementById('addThemeModal').addEventListener('hide.bs.modal', function (event) {
    newTheme.value.pid = 0;
    newTheme.value.pid_name = '';
    newTheme.value.name = '';
    newTheme.value.description = '';
  });
};

onMounted(() => {
  // @ts-ignore
  HSCore.components.HSSortable.init('.js-sortable');

  storeCode.value = history.state.code;
  storeGroup.value = history.state.storeGroup;

  if (storeCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }

  setModalListener();

  getStoreThemeList();
});
</script>

<style scoped></style>
