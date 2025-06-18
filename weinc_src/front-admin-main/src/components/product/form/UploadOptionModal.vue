<template>
  <Modal :xlarge="false" id="registProductOptionPhoto" title="신규 상품 옵션별 사진 등록">
    <template #header></template>
    <template #body>
      <div class="mb-5">
        <div class="py-3 d-flex flex-wrap row align-items-center">
          <div class="col-auto">
            <span class="position-relative border border-3 me-2 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex" style="width: 5rem; height: 5rem">
              <template v-if="previews">
                <img class="d-inline-flex flex-grow-1 w-auto h-100" :src="previews" />
              </template>
            </span>
          </div>
          <div class="col">
            <UploadImage class="form-control d-none" @upload="onUploadFile" :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-secondary' }" :placeholder="'상품 이미지를 등록해주세요.'" />
          </div>
        </div>
        <div class="">
          <div class="">
            <div class="label mb-2">상품 옵션 선택:</div>
            <div class="tom-select-custom">
              <select class="form-select" v-model="selectOption" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                <option value="" disabled>상품 옵션을 선택해주세요.</option>
                <option v-for="opt in options" :key="opt.id" v-text="opt.value" :value="opt.id"></option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-secondary me-2" @click="regOptionPhoto">추가</button>
      <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">취소</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import UploadImage from '@/components/comm/uploadImage.vue';
import { ref, PropType, watch, onMounted, computed } from 'vue';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import apis from '@/apis';
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

const props = defineProps({
  productId: {
    type: Number,
    required: true,
  },
  currentList: {
    type: Array as PropType<PhotoData[]>,
    required: true,
    default: [] as PhotoData[],
  },
  optionList: {
    type: Array as PropType<any[]>,
    required: true,
    default: [] as any[],
  },
});

const images = ref<PhotoData>({} as PhotoData);
const previews = ref<string>('');

const currentOptPhotoList = ref<PhotoData[]>([] as PhotoData[]);
const mProdOptionList = ref([] as any[]);
const mProdOptionTitleList = ref([] as string[]);
const options = ref([] as { id: number; value: string }[]);
const selectOption = ref<string | number>('');

const emits = defineEmits(['saveOptPhoto']);

const onUploadFile = (img: File) => {
  Promise.resolve(addPhotoList(img)).then(res => {
    showLogConsole(res);
    if (!res) {
      // showAlert(`현재 신규 등록 가능한 이미지는 ${availableCount.value}개 입니다.\n다른 이미지를 추가로 등록하시려면 기존 선택된 이미지를 지우고 등록해주세요.`, 'warning');
    }
  });
};

const addPhotoList = async (img: File) => {
  const buffer = await img.arrayBuffer();
  images.value = { photo: { file: img } };
  previews.value = URL.createObjectURL(new Blob([buffer]));
  return true;
};

const regOptionPhoto = () => {
  if (!selectOption.value) {
    showAlert('상품 옵션을 선택해주세요.', 'warning');
    return;
  }
  showConfirm('상품 옵션 사진을 등록하시겠습니까?', () => {
    const formData = new FormData();
    if (images.value.photo.file instanceof File) formData.append('files', images.value.photo.file);
    apis.product.regPhotoInfo({ productId: props.productId, formData, query: `?product_option_id=${selectOption.value}` }).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 옵션 사진 정보가 저장되었습니다.', 'success', () => {
          emits('saveOptPhoto');
        });
      });
    });
  });
};

const checkAvailableOpt = () => {
  let photoIdx: any[] = [];
  currentOptPhotoList.value.map(item => {
    photoIdx.push(item.optionInfo!.id);
  });

  const availableArr = mProdOptionList.value.filter(item => !photoIdx.includes(item.id));

  mProdOptionList.value = availableArr;
};

const convertOption = () => {
  checkAvailableOpt();

  mProdOptionTitleList.value = mProdOptionList.value[0].option_title.split(',');
  selectOption.value = '';
  options.value = [];

  for (const opt of mProdOptionList.value) {
    let op = { id: 0, value: '' };
    const value = [];
    for (let i = 0; i < mProdOptionTitleList.value.length; i++) {
      if (i === 0) {
        value.push(`${mProdOptionTitleList.value[i]}: ${opt.option_1}`);
      } else if (i === 1) {
        value.push(`${mProdOptionTitleList.value[i]}: ${opt.option_2}`);
      } else if (i === 2) {
        value.push(`${mProdOptionTitleList.value[i]}: ${opt.option_3}`);
      } else if (i === 3) {
        value.push(`${mProdOptionTitleList.value[i]}: ${opt.option_4}`);
      } else {
        value.push(`${mProdOptionTitleList.value[i]}: ${opt.option_5}`);
      }
    }
    op.id = opt.id;
    op.value = value.join(', ');
    options.value.push(op);
  }
};

onMounted(() => {
  //@ts-ignore
  document.getElementById('registProductOptionPhoto').addEventListener('show.bs.modal', function (event) {
    showLogConsole('registProductOptionPhoto.show.listener');
    currentOptPhotoList.value = props.currentList;
    mProdOptionList.value = JSON.parse(JSON.stringify(props.optionList));
    convertOption();
    images.value = {} as PhotoData;
    previews.value = '';
  });

  //@ts-ignore
  document.getElementById('registProductOptionPhoto').addEventListener('hide.bs.modal', function (event) {
    showLogConsole('registProductOptionPhoto.hide.listener');
  });
});
</script>

<style scoped></style>
