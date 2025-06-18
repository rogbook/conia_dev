<template>
  <Modal :xlarge="true" id="registProductPhoto" title="신규 상품 대표 사진 등록">
    <template #header></template>
    <template #body>
      <div class="mb-5">
        <UploadImage class="form-control d-none" @upload="onUploadFile" :btn="{ btnName: '파일 선택', btnClass: 'btn btn-secondary' }" :placeholder="'상품 이미지를 등록해주세요.'" />

        <div class="py-3 d-flex flex-wrap">
          <span v-for="(item, index) in previews" :key="JSON.stringify(item)" class="position-relative border border-3 me-2 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex" style="width: 5rem; height: 5rem">
            <template v-if="item">
              <img class="d-inline-flex flex-grow-1 w-auto h-100" :src="item" :alt="'사진' + index + 1" />
              <button type="button" v-show="item" class="btn btn-close position-absolute top-0 end-0" @click.prevent="() => onDeleteImage(index)"></button>
            </template>
            <div v-else>사진{{ index + 1 }}</div>
            <!--            https://picsum.photos/200-->
          </span>
        </div>
      </div>
      <ul>
        <li>총 {{ availableCount }} 개의 이미지를 선택 및 등록 가능합니다.</li>
        <li>첫번째 등록된 이미지가 대표 이미지 및 자동 리사이징 됩니다.</li>
        <li>첨부 가능한 용량 및 개수는 아래와 같습니다.</li>
        <li>한 개 파일 : 최대 6MB</li>
        <li>총 합 : 최대 20MB</li>
      </ul>
      <button
        type="button"
        class="btn btn-secondary me-2"
        @click="
          () => {
            emits('loadImages', { images, previews });
          }
        "
        data-bs-dismiss="modal">
        추가
      </button>
      <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">취소</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import UploadImage from '@/components/comm/uploadImage.vue';
import { ref, PropType, watch, onMounted, computed } from 'vue';
import { showAlert, showLogConsole } from '@/utils/common-utils';
interface PhotoData {
  id?: number;
  photo: {
    file?: File;
    uri?: string;
  };
}

const props = defineProps({
  currentList: {
    type: Array as PropType<PhotoData[]>,
    required: true,
    default: [] as PhotoData[],
  },
  imageList: {
    type: Array as PropType<PhotoData[]>,
    required: true,
    default: [] as PhotoData[],
  },
  previewList: {
    type: Array as PropType<string[]>,
    required: true,
    default: [] as string[],
  },
});

const images = ref<PhotoData[]>([] as PhotoData[]);
const previews = ref<string[]>([]);

const availableCount = computed(() => {
  return 5 - props.currentList.length;
});

const emits = defineEmits(['loadImages']);
const onDeleteImage = (index: number) => {
  images.value.splice(index, 1);
  previews.value.splice(index, 1);
};

const onUploadFile = (img: File) => {
  Promise.resolve(addPhotoList(img)).then(res => {
    if (!res) {
      showAlert(`현재 신규 등록 가능한 이미지는 ${availableCount.value}개 입니다.\n다른 이미지를 추가로 등록하시려면 기존 선택된 이미지를 지우고 등록해주세요.`, 'warning');
    }
  });
};

const addPhotoList = async (img: File) => {
  if (images.value.length === availableCount.value) {
    return false;
  } else {
    const buffer = await img.arrayBuffer();
    images.value.push({ photo: { file: img } });
    previews.value.push(URL.createObjectURL(new Blob([buffer])));
    return true;
  }
};

onMounted(() => {
  //@ts-ignore
  document.getElementById('registProductPhoto').addEventListener('show.bs.modal', function (event) {
    showLogConsole('registProductPhoto.show.listener');
    images.value = props.imageList;
    previews.value = props.previewList;
  });

  //@ts-ignore
  document.getElementById('registProductPhoto').addEventListener('hide.bs.modal', function (event) {
    showLogConsole('registProductPhoto.hide.listener');
  });
});
</script>

<style scoped></style>
