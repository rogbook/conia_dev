<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세'] : ['상점 관리', '상점관리 상세']" :current="'상점 홈화면 관리'" />
  <div class="card">
    <div class="card-header">
      <div class="col-auto">
        <div class="form-control-borderless h2 mb-0">[{{ store.title }}] - 홈 화면 레이아웃 설정</div>
      </div>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <div class="row align-items-center justify-content-between">
                <div class="col-auto">
                  <span>홈 화면 설정 (순서 변경 드래그로 가능)</span>
                </div>
                <div class="col-auto">
                  <button type="button" class="btn btn-sm btn-primary" @click.prevent="saveLayout">저장</button>
                </div>
              </div>
            </div>
            <div class="card-body">
              <!-- List Group -->
              <div class="js-sortable list-group store-layouts" id="store-layouts" data-hs-sortable-options='{"animation": 150,"swapClass": "active"}'>
                <template v-for="(c, i) in mComponentList" :key="JSON.stringify(c)">
                  <component :is="c.comp" :index="i.toString()" :memo="c.memo" @deleteComp="deleteComp" @selectComp="selectComp"> </component>
                </template>
              </div>
              <!-- End List Group -->
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">홈 화면 구성 컴포넌트</div>
            <div class="card-body">
              <!-- 앵커 -->
              <div class="card card-body mb-2">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <button type="button" class="btn btn-white btn-icon border-0" @click.prevent="addComponent('button-grp', { buttons: [] })">
                      <i class="bi bi-plus-square text-primary" style="font-size: 32px"></i>
                    </button>
                  </div>
                  <div class="col">
                    <div class="row ms-4 me-4 g-2">
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">버튼 그룹</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- 슬라이드(L) -->
              <div class="card card-body mb-2">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <button type="button" class="btn btn-white btn-icon border-0" @click.prevent="addComponent('slide-lg', { slides: [] })">
                      <i class="bi bi-plus-square text-primary" style="font-size: 32px"></i>
                    </button>
                  </div>
                  <div class="col slide-lg-img">
                    <div class="row">
                      <div>
                        <div class="square form-control table-text-center py-5 px-1">슬라이드(L)</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- 대형 이미지 -->
              <!--              <div class="card card-body mb-2">-->
              <!--                <div class="row align-items-center">-->
              <!--                  <div class="col-auto">-->
              <!--                    <button type="button" class="btn btn-white btn-icon border-0" @click.prevent="addComponent('lg-img')">-->
              <!--                      <i class="bi bi-plus-square text-primary" style="font-size: 32px"></i>-->
              <!--                    </button>-->
              <!--                  </div>-->
              <!--                  <div class="col lg-img">-->
              <!--                    <div class="square form-control table-text-center py-5">대형 이미지</div>-->
              <!--                  </div>-->
              <!--                </div>-->
              <!--              </div>-->
              <!-- 슬라이드(M) -->
              <div class="card card-body mb-2">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <button type="button" class="btn btn-white btn-icon border-0" @click.prevent="addComponent('slide-md', { slides: [] })">
                      <i class="bi bi-plus-square text-primary" style="font-size: 32px"></i>
                    </button>
                  </div>
                  <div class="col">
                    <div class="row ms-4 me-4 g-2">
                      <div>
                        <div class="square form-control table-text-center py-4 px-1">슬라이드(M)</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- 배너 -->
              <div class="card card-body mb-2">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <button type="button" class="btn btn-white btn-icon border-0" @click.prevent="addComponent('banner', { banners: [] })">
                      <i class="bi bi-plus-square text-primary" style="font-size: 32px"></i>
                    </button>
                  </div>
                  <div class="col">
                    <div class="row ms-4 me-4 g-2">
                      <div>
                        <div class="square form-control table-text-center py-4 px-1">배너</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- 배너 & 아이템2 -->
              <div class="card card-body mb-2">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <button type="button" class="btn btn-white btn-icon border-0" @click.prevent="addComponent('banner-column-2', { banners: [], columns: [] })">
                      <i class="bi bi-plus-square text-primary" style="font-size: 32px"></i>
                    </button>
                  </div>
                  <div class="col">
                    <div class="row ms-4 me-4 g-2 mb-2">
                      <div>
                        <div class="square form-control table-text-center py-4 px-1">배너</div>
                      </div>
                    </div>
                    <div class="row row-cols-md-2 ms-4 me-4 g-2">
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- 배너 & 아이템4 -->
              <div class="card card-body mb-2">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <button type="button" class="btn btn-white btn-icon border-0" @click.prevent="addComponent('banner-column-4', { banners: [], columns: [] })">
                      <i class="bi bi-plus-square text-primary" style="font-size: 32px"></i>
                    </button>
                  </div>
                  <div class="col">
                    <div class="row ms-4 me-4 g-2 mb-2">
                      <div>
                        <div class="square form-control table-text-center py-4 px-1">배너</div>
                      </div>
                    </div>
                    <div class="row row-cols-md-4 ms-4 me-4 g-2">
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- 아이템2 -->
              <div class="card card-body mb-2">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <button type="button" class="btn btn-white btn-icon border-0" @click.prevent="addComponent('column-2', { columns: [] })">
                      <i class="bi bi-plus-square text-primary" style="font-size: 32px"></i>
                    </button>
                  </div>
                  <div class="col">
                    <div class="row row-cols-2 ms-4 me-4 g-2">
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- 아이템4 -->
              <div class="card card-body mb-2">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <button type="button" class="btn btn-white btn-icon border-0" @click.prevent="addComponent('column-4', { columns: [] })">
                      <i class="bi bi-plus-square text-primary" style="font-size: 32px"></i>
                    </button>
                  </div>
                  <div class="col">
                    <div class="row row-cols-md-4 ms-4 me-4 g-2">
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                      <div>
                        <div class="square form-control table-text-center py-3 px-1">아이템</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 컴포넌트 설정 Modal -->
  <Modal :id="'setComponentData'" :title="'컴포넌트 구성 설정'" :xlarge_big="true" :centered="true" :is-editor-in="true">
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
  <Modal :id="'getProductListModal'" :title="'상점 상품 목록'" :xlarge="true" :second="true" :centered="true">
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
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import ButtonGroup from '@/pages/store/list/detail/layout/comp/ButtonGroup.vue';
import SlideLgImg from '@/pages/store/list/detail/layout/comp/SlideLgImg.vue';
import SlideMdImg from '@/pages/store/list/detail/layout/comp/SlideMdImg.vue';
import MdImg from '@/pages/store/list/detail/layout/comp/MdImg.vue';
import MdImgItems2 from '@/pages/store/list/detail/layout/comp/MdImgItems2.vue';
import MdImgItems4 from '@/pages/store/list/detail/layout/comp/MdImgItems4.vue';
import Items2 from '@/pages/store/list/detail/layout/comp/Items2.vue';
import Items4 from '@/pages/store/list/detail/layout/comp/Items4.vue';
import SetComponentInfo from '@/pages/store/list/detail/theme/layout/comp/SetComponentInfo.vue';
import StoreProductList from '@/pages/store/list/detail/theme/StoreProductList.vue';
import apis from '@/apis';
import Modal from '@/components/comm/modal.vue';
import type { Theme } from 'ThemeInfoModule';
import type { Store } from 'StoreListInfoModule';
import { apiResponseCheck, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import StoreShopList from '@/pages/store/list/detail/theme/StoreShopList.vue';

const storeCode = ref();
const store = ref({} as Store);
const themeList = ref([] as Theme[]);
const setCompModalRef = ref();
const getProductList = ref();
const getShopList = ref();

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

const getStore = () => {
  apis.store.get_store(storeCode.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      store.value = res;
      if (store.value.layout) {
        parseLayout(store.value.layout);
      }
    });
  });
};

const getStoreThemeList = () => {
  apis.store.get_store_theme_list(storeCode.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      themeList.value = res;
    });
  });
};

const isThemeInfoChanged = ref(false);
const isCompLengthChange = ref({
  beforeLength: 0,
  currentLength: 0,
  check: false,
});

const mComponentList = ref([] as { comp: any; data: {}; compType: string; top?: string; compId: string; background?: string; memo?: string }[]);

const addComponent = (type: string, data: object, top: string = '', id?: string, background?: string, memo?: string) => {
  let component: { comp: any; data: {}; compType: string; top?: string; compId: string; background?: string; memo?: string };
  switch (type) {
    case 'button-grp':
      component = { comp: ButtonGroup, data: data, compType: 'button-grp', top: top, compId: id ? id : '', background: background ? background : '', memo: memo ? memo : '' };
      mComponentList.value.push(component);
      break;
    case 'slide-lg':
      component = { comp: SlideLgImg, data: data, compType: 'slide-lg', compId: id ? id : '', background: background ? background : '', memo: memo ? memo : '' };
      mComponentList.value.push(component);
      break;
    case 'slide-md':
      component = { comp: SlideMdImg, data: data, compType: 'slide-md', compId: id ? id : '', background: background ? background : '', memo: memo ? memo : '' };
      mComponentList.value.push(component);
      break;
    case 'banner':
      component = { comp: MdImg, data: data, compType: 'banner', compId: id ? id : '', background: background ? background : '', memo: memo ? memo : '' };
      mComponentList.value.push(component);
      break;
    case 'banner-column-2':
      component = { comp: MdImgItems2, data: data, compType: 'banner-column-2', compId: id ? id : '', background: background ? background : '', memo: memo ? memo : '' };
      mComponentList.value.push(component);
      break;
    case 'banner-column-4':
      component = { comp: MdImgItems4, data: data, compType: 'banner-column-4', compId: id ? id : '', background: background ? background : '', memo: memo ? memo : '' };
      mComponentList.value.push(component);
      break;
    case 'column-2':
      component = { comp: Items2, data: data, compType: 'column-2', compId: id ? id : '', background: background ? background : '', memo: memo ? memo : '' };
      mComponentList.value.push(component);
      break;
    case 'column-4':
      component = { comp: Items4, data: data, compType: 'column-4', compId: id ? id : '', background: background ? background : '', memo: memo ? memo : '' };
      mComponentList.value.push(component);
      break;
  }
};

const deleteComp = (id: number) => {
  showConfirm('삭제하시겠습니까?', () => {
    mComponentList.value.splice(id, 1);
  });
};

const selectComp = (id: number) => {
  const cData = JSON.parse(JSON.stringify(mComponentList.value[id].data));

  selCompData.data = cData;
  selCompData.id = id;
  selCompData.compType = mComponentList.value[id].compType;
  selCompData.compId = mComponentList.value[id].compId;
  selCompData.top = mComponentList.value[id]?.top ? mComponentList.value[id].top! : '';
  if (mComponentList.value[id]?.background) {
    selCompData.background = mComponentList.value[id].background!;
  } else {
    selCompData.background = '';
  }
  if (mComponentList.value[id]?.memo) {
    selCompData.memo = mComponentList.value[id].memo!;
  } else {
    selCompData.memo = '';
  }
  showModal('setComponentData');
  setCompModalRef.value.showCompInfo();
};

const saveLayout = () => {
  const layouts = window.document.getElementById('store-layouts')?.children;

  if (layouts != undefined && layouts.length > 0) {
    let layoutJson: any[] = [];
    for (const l of layouts) {
      const c = {} as any;
      c['type'] = l.className;
      //@ts-ignore
      c['id'] = mComponentList.value[l.id].compId;
      //@ts-ignore
      c['background'] = mComponentList.value[l.id].background;
      //@ts-ignore
      c['memo'] = mComponentList.value[l.id].memo;
      if (l.className === 'button-grp') {
        //@ts-ignore
        c['top'] = mComponentList.value[l.id].top;
      }
      //@ts-ignore
      const data = mComponentList.value[l.id].data;
      for (const k of Object.keys(data)) {
        c[k] = data[k];
      }
      layoutJson.push(c);
    }
    showConfirm('레이아웃 구성을 저장하시겠습니까?', () => {
      // emit('modThemeLayout', JSON.stringify(layoutJson));
      apis.store.mod_store(storeCode.value, { layout: JSON.stringify(layoutJson) }).then(res => {
        apiResponseCheck(res, () => {
          showAlert('홈 화면 레이아웃을 저장했습니다.', 'success');
        });
      });
    });
  } else {
    showAlert('구성된 컴포넌트가 없습니다.', 'warning');
  }
};

const parseLayout = async (layoutStr: string) => {
  const layoutObjs = JSON.parse(layoutStr);
  for (const c of layoutObjs) {
    let type = '';
    let id = '';
    let memo = '';
    let background = '';
    let top = '';
    let data = {} as any;
    let productInfo = {} as any;
    for (const k of Object.keys(c)) {
      if (k === 'type') {
        type = c[k];
      } else if (k === 'id') {
        id = c[k];
      } else if (k === 'background') {
        background = c[k];
      } else if (k === 'top') {
        top = c[k];
      } else if (k === 'memo') {
        memo = c[k];
      } else {
        // // 상품 이미지 동적으로 처리
        // if (k === 'columns') {
        //   for (let i in c[k]) {
        //     if (c[k][i].type === 'product') {
        //       productInfo = await getProdInfo(c[k][i].id);
        //       c[k][i].img = productInfo.uri;
        //       c[k][i].name = productInfo.name;
        //     }
        //   }
        // }
        data[k] = c[k];
      }
    }
    addComponent(type, data, top, id, background ? background : '', memo ? memo : '');
  }
};

const getProdInfo = async (id: number) => {
  try {
    const product = await apis.product.getProduct(id);
    let obj = {};
    if (product.photos.length) {
      obj = { uri: product.photos[0].uri, name: product.name };
    } else {
      obj = { uri: '', name: product.name };
    }
    return obj;
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const passToCompInfo = (data: any) => {
  hideModal('setComponentData');

  setComponentInfo(data);
  selCompData.id = -1;
};

const deleteBackImg = (data: any) => {
  mComponentList.value[data.id].background = '';
};

const setComponentInfo = (data: any) => {
  if (mComponentList.value[data.id].data !== data.data) {
    isThemeInfoChanged.value = true;
  }

  mComponentList.value[data.id].data = data.data;
  mComponentList.value[data.id].compId = data.compId;
  if (data.compType === 'button-grp') {
    mComponentList.value[data.id].top = data.top;
  }
  if (data.background) {
    mComponentList.value[data.id].background = data.background;
  }
  if (data.memo) {
    mComponentList.value[data.id].memo = data.memo;
  }
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

onMounted(() => {
  // INITIALIZATION OF SORTABLE
  // @ts-ignore
  HSCore.components.HSSortable.init('.js-sortable');

  const code = history.state.code;
  if (code) {
    storeCode.value = code;
    getStore();
    getStoreThemeList();
  }
});
</script>

<style scoped>
.square {
  background-color: lightgray;
  border-width: 1px;
  border-color: midnightblue;
  vertical-align: middle;
}
</style>
