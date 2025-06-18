<template>
  <div class="row">
    <div class="col-lg-7">
      <div class="card">
        <div class="card-header py-2">
          매장정보
          <span v-if="getUserClassStr.includes('CM')" class="ms-2"><MobilePushLink :title="`매장 [ ${shopInfo.name} ]`" :nextValue="`shop/${shopInfo.id}`" /></span>
        </div>
        <div class="card-body">
          <div class="row mb-2">
            <label class="col-md-2 col-form-label">상호명 <span class="text-danger">*</span></label>
            <div class="col">
              <input type="text" class="form-control" placeholder="상호명을 입력해주세요." v-model="shopInfo.name" maxlength="30" />
            </div>
          </div>
          <div class="row mb-2">
            <label class="col-md-2 col-form-label">부제목</label>
            <div class="col">
              <input type="text" class="form-control" placeholder="부제목을 입력해주세요. (최대 100자)" maxlength="100" v-model="shopInfo.subtitle" />
            </div>
          </div>
          <div class="row mb-2">
            <label class="col-md-2 col-form-label">주소 <span class="text-danger">*</span></label>
            <div class="col">
              <div class="input-group">
                <input disabled v-model="shopInfo.address" id="addressLabel" class="form-control" name="addr" placeholder="매장 주소를 입력해주세요." type="text" readonly required />
                <button type="button" class="btn btn-outline-secondary" @click.prevent="onSearchAddress($event)">찾기</button>
              </div>
              <input v-model="shopInfo.address_detail" maxlength="128" id="addressDetailLabel" class="form-control mt-1" name="addrdetail" placeholder="상세 주소를 입력해주세요." type="text" />
            </div>
          </div>
          <div class="row mb-2">
            <label class="col-md-2 col-form-label">전화번호 <span class="text-danger">*</span></label>
            <div class="col">
              <input type="text" class="form-control" placeholder="전화번호를 입력해주세요." v-model="shopInfo.tel" maxlength="20" />
            </div>
          </div>
          <div class="row mb-2">
            <label class="col-md-2 col-form-label">영업시간 </label>
            <div class="col">
              <textarea type="text" class="form-control" maxlength="255" placeholder="영업시간을 입력해주세요." v-model="shopInfo.work_time" />
            </div>
          </div>
          <div class="row mb-2">
            <label class="col-md-2 col-form-label">휴무일 </label>
            <div class="col">
              <textarea type="text" class="form-control" maxlength="255" placeholder="휴무일을 입력해주세요." v-model="shopInfo.holiday" />
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label"
              >매장사진 <br />
              <span style="font-size: 0.7rem" class="text-danger"
                >(추천 가로 485px, <br />
                고정 비율 1:1)</span
              >
            </label>
            <div class="col">
              <div class="input-group" v-if="!shopInfo.image">
                <UploadImage
                  class="form-control"
                  @change="
                    () => {
                      uploadImg.check = uploadImg.value.length > 0;
                    }
                  "
                  @upload="onRegistComRegPhoto"
                  :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                  :placeholder="'이미지를 선택해 주세요.'"
                  disabled />
              </div>
              <div v-else>
                <img class="img-fluid img-thumbnail d-block" :src="shopInfo.image" alt="쿠폰 이미지" />
                <div class="mt-3">
                  <button type="button" class="btn btn-outline-info me-2 btn-sm" @click="shopInfo.image = ''">수정</button>
                </div>
              </div>
            </div>
          </div>
          <div class="row mb-2">
            <label class="col-md-2 col-form-label">매장정보 <span class="text-danger">*</span></label>
            <div class="col">
              <textarea type="text" class="form-control" style="height: 20rem" maxlength="500" placeholder="매장정보를 입력해주세요." v-model="shopInfo.description" />
            </div>
          </div>
          <div class="row mb-2">
            <div class="col-md-2 col-form-label">매장배지</div>
            <div class="col">
              <div class="py-1 d-flex flex-wrap" v-if="shopInfo.id">
                <span v-for="item in currentBadgeList" :key="item.id" class="mb-1 position-relative border border-1 me-2 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex" style="width: 5rem; height: 5rem">
                  <button type="button" v-show="item" class="btn btn-close position-absolute top-0 end-0" @click.prevent="() => onDeleteBadge(item.id)"></button>
                  <div>
                    <span class="badge" :style="{ 'background-color': `${item.color} !important` }">{{ item.name }}</span>
                  </div>
                </span>
                <div class="addPhoto" v-if="availableCount > 0">
                  <span v-for="i in availableCount" :key="i" class="mb-1 position-relative border border-1 me-2 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex" style="width: 5rem; height: 5rem; border-color: #26a5b5 !important">
                    <button type="button" @click.prevent="showModal('addBadgeModal')" class="btn btn-sm badge py-2"><i class="bi-plus-circle text-primary" style="font-size: 20px" /></button>
                  </span>
                </div>
              </div>
              <div class="form-control border-0 ps-0 text-danger" style="font-size: 0.8rem" v-else>※ 매장 배지는 매장 정보가 등록된 후 추가할 수 있습니다.</div>
            </div>
          </div>
          <div class="row mb-2">
            <label class="col-md-2 col-form-label">지도 </label>
            <div class="col">
              <div id="map" style="width: 100%; height: 350px"></div>
            </div>
          </div>
          <div class="col-auto text-end">
            <button class="btn btn-primary" type="submit" v-if="isData" @click.prevent="modShop">수정</button>
            <button class="btn btn-primary" type="submit" v-else @click.prevent="regShop">등록</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Modal :id="'addBadgeModal'" :title="'배지 선택'">
    <template #body>
      <BadgeList @addBadgeList="addBadgeList" :currentList="currentBadgeList" :previewList="[]" />
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, onUnmounted, computed } from 'vue';
import { loadScript, unloadScript } from '@/utils/standaloneImport';
import type { Shop } from 'ShopInfoModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, getUserClassStr, showModal, hideModal } from '@/utils/common-utils';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useUserStore } from '@/stores/user';
import { useAuthStore } from '@/stores/auth';
import UploadImage from '@/components/comm/uploadImage.vue';
import MobilePushLink from '@/components/comm/MobilePushLink.vue';
import Modal from '@/components/comm/modal.vue';
import BadgeList from '@/pages/product/list/detail/step/badge/BadgeList.vue';
const installList = reactive(['//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js', `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_JS_KEY}&autoload=false`]);

const props = defineProps<{
  memberId: number;
}>();

const shopInfo = ref({} as Shop);
const originShopInfo = ref({} as Shop);
const isData = ref(false);

// 이미지
const uploadImg = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});

onMounted(() => {
  installList.map(path => {
    loadScript(path);
  });
});

onUnmounted(() => {
  installList.map(path => {
    unloadScript(path);
  });
});

const onRegistComRegPhoto = (files: File) => {
  apis.common.upload_photo(files, 'shop/').then(res => {
    apiResponseCheck(res, () => {
      shopInfo.value.image = res.uri;
      uploadImg.value = files.name;
      uploadImg.fileData = files;
    });
  });
};

const onSearchAddress = (e: any) => {
  e.preventDefault();
  //@ts-ignore
  new daum.Postcode({
    oncomplete: (data: any) => {
      const { roadAddress } = data;
      shopInfo.value.address = roadAddress;
      getCoordinate(roadAddress);
    },
  }).open();
};

const getCoordinate = async (roadAddress: string) => {
  const res = await apis.map.getCoordinate(roadAddress);
  shopInfo.value.lat = res.y;
  shopInfo.value.lng = res.x;
  loadMap(res.x, res.y);
};

const loadMap = (x: string, y: string) => {
  //@ts-ignore
  kakao.maps.load(() => {
    const mapContainer = document.getElementById('map'); // 지도를 표시할 div
    const mapOption = {
      //@ts-ignore
      center: new kakao.maps.LatLng(y, x), // 지도의 중심좌표
      level: 3, // 지도의 확대 레벨
    };

    //@ts-ignore
    let map = new kakao.maps.Map(mapContainer, mapOption);

    //@ts-ignore
    const markerPosition = new kakao.maps.LatLng(y, x);
    //@ts-ignore
    const marker = new kakao.maps.Marker({
      position: markerPosition,
    });
    marker.setMap(map);
  });
};

const getShopInfo = () => {
  apis.company.get_shop(props.memberId).then(res => {
    if (res instanceof AxiosError) {
      isData.value = false;
    } else {
      isData.value = true;
      shopInfo.value = res;
      originShopInfo.value = { ...shopInfo.value };
      currentBadgeList.value = res.badges;
      if (shopInfo.value.address) {
        getCoordinate(shopInfo.value.address);
      }
    }
  });
};

const checkValidation = () => {
  if (!shopInfo.value.name) {
    showAlert('상호명을 입력해주세요.', 'warning');
    return;
  }
  if (!shopInfo.value.address) {
    showAlert('주소를 입력해주세요.', 'warning');
    return;
  }
  if (!shopInfo.value.tel) {
    showAlert('전화번호를 입력해주세요.', 'warning');
    return;
  }
  if (!shopInfo.value.description) {
    showAlert('매장정보를 입력해주세요.', 'warning');
    return;
  }
  return true;
};

const regShop = () => {
  if (!checkValidation()) return;
  showLogConsole(shopInfo.value);

  showConfirm('매장정보를 등록하시겠습니까?', () => {
    apis.company.reg_shop(props.memberId, shopInfo.value).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        showAlert('매장정보가 등록되었습니다.', 'success');
      });
    });
  });
};

const modShop = () => {
  if (!checkValidation()) return;
  if (!checkIsChange()) return;

  showConfirm('매장정보를 수정하시겠습니까?', () => {
    apis.company.mod_shop(props.memberId, shopInfo.value).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        showAlert('매장정보가 수정되었습니다.', 'success');
      });
    });
  });
};

const checkIsChange = () => {
  if (shopInfo.value.name !== originShopInfo.value.name) return true;
  if (shopInfo.value.subtitle !== originShopInfo.value.subtitle) return true;
  if (shopInfo.value.address !== originShopInfo.value.address) return true;
  if (shopInfo.value.address_detail !== originShopInfo.value.address_detail) return true;
  if (shopInfo.value.work_time !== originShopInfo.value.work_time) return true;
  if (shopInfo.value.holiday !== originShopInfo.value.holiday) return true;
  if (shopInfo.value.image !== originShopInfo.value.image) return true;
  if (shopInfo.value.tel !== originShopInfo.value.tel) return true;
  if (shopInfo.value.description !== originShopInfo.value.description) return true;
  showAlert('변경된 내용이 없습니다.', 'warning');
  return false;
};

// 배지 관련 코드
const currentBadgeList = ref();

const availableCount = computed(() => {
  if (!currentBadgeList.value) {
    return 0;
  }
  return 3 - currentBadgeList.value.length;
});

const addBadgeList = (badges: any[]) => {
  let duplicateIdx: number[] = [];
  for (let i = 0; i < badges.length; i++) {
    duplicateIdx.push(badges[i].id);
  }
  hideModal('addBadgeModal');
  onSaveBadge(duplicateIdx);
};

const onSaveBadge = (badgesId: number[]) => {
  showConfirm('매장 배지 정보를 저장하시겠습니까?', async () => {
    apis.company.link_shop_badge(shopInfo.value.id, badgesId).then(res => {
      apiResponseCheck(res, () => {
        showAlert('매장 배지가 등록되었습니다.', 'success');
        getShopInfo();
      });
    });
  });
};

const onDeleteBadge = (id: number) => {
  showConfirm('기존 등록된 해당 매장 배지를 삭제하시겠습니까?', () => {
    apis.company.unlink_shop_badge(shopInfo.value.id, [id]).then(res => {
      apiResponseCheck(res, () => {
        showAlert('매장 배지가 삭제되었습니다.', 'success');
        getShopInfo();
      });
    });
  });
};

defineExpose({ getShopInfo });
</script>

<style scoped></style>
