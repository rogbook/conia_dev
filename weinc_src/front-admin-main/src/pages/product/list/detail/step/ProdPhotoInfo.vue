<template>
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">사진정보</h4>
          <small>상품상세에 노출될 사진을 등록할 수 있습니다. (최소 1장, 최대 5장)</small>
        </div>
        <div class="nav-item ms-auto">
          <button type="button" class="btn btn-warning" @click.prevent="onRegistPhoto">저장</button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="current-img">
        <label class="col-form-label mb-2" v-if="currentList.length > 0"><span class="text-danger">* </span>등록된 상품 사진을 삭제하려면 등록된 사진 상단의 'X'버튼을 눌러주세요.</label>
        <!-- 상품 대표 사진 -->
        <div class="card mb-2">
          <div class="card-header py-2">
            <div class="col-auto">
              [상품 대표 사진]
              <span style="font-size: 0.7rem" class="text-danger">(추천 가로 579.5px, 권장 비율 1:1)</span>
            </div>
          </div>
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-auto">
                <div class="py-3 d-flex flex-wrap">
                  <span v-for="(item, index) in currentList" :key="item.id" class="mb-1 position-relative border border-3 me-2 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex" style="width: 5rem; height: 5rem">
                    <button type="button" v-show="item" class="btn btn-close position-absolute top-0 end-0" @click.prevent="() => onDeleteImage(item.id as number)"></button>
                    <img class="d-inline-flex flex-grow-1 w-auto h-100" :src="item.photo.uri" :alt="'사진' + (index + 1)" />
                  </span>
                  <span
                    v-for="(item, index) in previewList"
                    :key="JSON.stringify(item)"
                    class="mb-1 position-relative border border-3 me-2 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex"
                    style="width: 5rem; height: 5rem; border-color: #26a5b5 !important">
                    <button type="button" v-show="item" class="btn btn-close position-absolute top-0 end-0" @click.prevent="() => onDeleteImgList(index)"></button>
                    <img class="d-inline-flex flex-grow-1 w-auto h-100" :src="item" :alt="'사진' + (index + 1)" />
                  </span>
                  <div class="addPhoto" v-if="availableCount > 0">
                    <span v-for="i in availableCount" :key="i" class="mb-1 position-relative border border-3 me-2 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex" style="width: 5rem; height: 5rem; border-color: #26a5b5 !important">
                      <button type="button" @click.prevent="showModal('registProductPhoto')" class="btn btn-sm badge py-2"><i class="bi-plus-circle text-primary" style="font-size: 20px" /></button>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- 상품 옵션별 사진 -->
        <div class="card" v-if="mProdOptionList.length > 0">
          <div class="card-header py-2">
            <div class="col-auto">[상품 옵션별 사진]</div>
          </div>
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-auto">
                <div class="py-3 d-flex flex-wrap">
                  <div class="" v-for="(item, index) in optionCurrentList" :key="item.id">
                    <div class="row align-items-center me-4 mb-2">
                      <div class="col-auto">
                        <span class="position-relative border border-3 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex" style="width: 5rem; height: 5rem">
                          <button type="button" v-show="item" class="btn btn-close position-absolute top-0 end-0" @click.prevent="() => onDeleteImage(item.id as number)"></button>
                          <img class="d-inline-flex flex-grow-1 w-auto h-100" :src="item.photo.uri" :alt="'사진' + (index + 1)" />
                        </span>
                      </div>
                      <div class="col-auto ms-0 ps-0">
                        <div class="text-wrap">[옵션정보] {{ convertOptValue(index) }}</div>
                      </div>
                    </div>
                  </div>
                  <div class="addPhoto" v-if="availableOptCount > 0">
                    <span class="position-relative border border-3 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex" style="width: 5rem; height: 5rem; border-color: #26a5b5 !important">
                      <button type="button" @click.prevent="showModal('registProductOptionPhoto')" class="btn btn-sm badge py-2"><i class="bi-plus-circle text-primary" style="font-size: 20px" /></button>
                    </span>
                  </div>
                </div>
                <div class="col"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <UploadModal @loadImages="loadImages" :current-list="currentList" :image-list="imageList" :preview-list="previewList" />
  <UploadOptionModal @saveOptPhoto="saveOptPhoto" :product-id="props.productId" :current-list="optionCurrentList" :option-list="mProdOptionList" />
</template>

<script setup lang="ts">
import UploadModal from '@/components/product/form/UploadModal.vue';
import { computed, ref, watch } from 'vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import UploadOptionModal from '@/components/product/form/UploadOptionModal.vue';
interface PhotoData {
  id?: number;
  optionInfo?: {
    code: string;
    id: number;
    option_1: string;
    option_2: string;
    option_3: string;
    option_4: string;
    option_5: string;
    option_code_1: string;
    option_code_2: string;
    option_code_3: string;
    option_code_4: string;
    option_code_5: string;
    option_title: string;
  };
  photo: {
    file?: File;
    uri?: string;
  };
}

const imageList = ref([] as PhotoData[]);
const currentList = ref([] as PhotoData[]);
const previewList = ref([] as string[]);

const availableCount = computed(() => {
  return 5 - currentList.value.length - previewList.value.length;
});

const availableOptCount = computed(() => {
  return mProdOptionList.value.length - optionCurrentList.value.length;
});

const mProdOptionList = ref([] as any[]);
const optionCurrentList = ref([] as PhotoData[]);

const props = defineProps<{ productId: number }>();
const emits = defineEmits(['saveFinish', 'changedProdInfo']);
const loadImages = ({ previews, images }: { previews: string[]; images: PhotoData[] }) => {
  imageList.value = images;
  previewList.value = previews;
};

const onRegistPhoto = () => {
  if (currentList.value.length === 0 && imageList.value.length === 0) {
    showAlert('상품 사진을 등록해주세요.', 'warning');
    return;
  }

  if (currentList.value.length > 0 && imageList.value.length === 0) {
    showAlert('상품 사진 정보가 저장되었습니다.', 'success');
    getProdPhotoInfo();
    emits('saveFinish', 'photo');
    return;
  }

  showConfirm('상품 사진 정보를 저장하시겠습니까?', () => {
    const formData = new FormData();
    Array.from(imageList.value).forEach(f => {
      if (f.photo.file instanceof File) formData.append('files', f.photo.file);
    });
    apis.product.regPhotoInfo({ productId: props.productId, formData }).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 사진 정보가 저장되었습니다.', 'success');
        getProdPhotoInfo();
        emits('saveFinish', 'photo');
      });
    });
  });
};

const getProdPhotoInfo = (isSaveOpt: boolean = false) => {
  optionCurrentList.value = [] as PhotoData[];
  if (!isSaveOpt) {
    imageList.value = [] as PhotoData[];
    previewList.value = [] as string[];
    currentList.value = [] as PhotoData[];
  }

  apis.product.getProdPhotoInfo(props.productId).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      for (const p of res) {
        if (p.product_option) {
          // TODO: 옵션 사진
          optionCurrentList.value.push({ id: p.id, photo: { uri: p.uri }, optionInfo: p.product_option });
        } else {
          if (!isSaveOpt) {
            currentList.value.push({ id: p.id, photo: { uri: p.uri } });
          }
        }
      }
    });
  });
};

const getProdOptionList = () => {
  mProdOptionList.value = [] as any[];
  apis.product.getProdOption(props.productId).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mProdOptionList.value = res;
    });
  });
};

const onDeleteImage = (id: number) => {
  if (currentList.value.length === 1) {
    showAlert('최소 한개 이상의 사진은 필수입니다.', 'warning');
    return;
  }

  showConfirm('기존 등록된 해당 상품 사진을 삭제하시겠습니까?', () => {
    apis.product.deletePhotoInfo(props.productId, id).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 사진이 삭제되었습니다.', 'success');
        getProdPhotoInfo();
      });
    });
  });
};

const onDeleteImgList = (index: number) => {
  imageList.value.splice(index, 1);
  previewList.value.splice(index, 1);
};

const convertOptValue = (idx: number) => {
  const value = [] as string[];

  const optionInfo: any = optionCurrentList.value[idx].optionInfo;
  const titleList: string[] = mProdOptionList.value[0].option_title?.split(',');

  for (let i = 0; i < titleList?.length; i++) {
    if (i === 0) {
      value.push(`${titleList[i]}: ${optionInfo.option_1}`);
    } else if (i === 1) {
      value.push(`${titleList[i]}: ${optionInfo.option_2}`);
    } else if (i === 2) {
      value.push(`${titleList[i]}: ${optionInfo.option_3}`);
    } else if (i === 3) {
      value.push(`${titleList[i]}: ${optionInfo.option_4}`);
    } else {
      value.push(`${titleList[i]}: ${optionInfo.option_5}`);
    }
  }
  return value.join(', ');
};

const saveOptPhoto = () => {
  hideModal('registProductOptionPhoto');
  getProdPhotoInfo(true);
};

const onStepActive = () => {
  if (props.productId) {
    imageList.value = [] as PhotoData[];
    currentList.value = [] as PhotoData[];
    previewList.value = [] as string[];
    getProdPhotoInfo();
    getProdOptionList();
  }
};

defineExpose({ onStepActive });
</script>

<style scoped></style>
