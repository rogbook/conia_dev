<template>
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">상품 매장 정보</h4>
          <small>상품의 매장 정보를 선택합니다.</small>
        </div>
        <div class="nav-item ms-auto">
          <button type="button" class="btn btn-warning" @click.prevent="saveStoreInfo">저장</button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <CommFormLine :title="'전화번호'" :width="8">
        <input type="text" class="form-control" placeholder="전화번호를 입력해주세요." v-model="prodInfo.tel" />
      </CommFormLine>

      <CommFormLine :title="'주소'" :width="8">
        <div class="input-group">
          <input disabled v-model="prodInfo.address" id="addressLabel" class="form-control" name="addr" placeholder="매장 주소를 입력해주세요." type="text" readonly required />
          <button type="button" @click.prevent="onSearchAddress($event)" class="btn btn-outline-secondary">찾기</button>
        </div>
      </CommFormLine>
      <CommFormLine :title="'상세주소'" :width="8">
        <div class="input-group">
          <input v-model="prodInfo.address_detail" id="addressDetailLabel" class="form-control" name="addrdetail" placeholder="상세 주소를 입력해주세요." type="text" />
        </div>
      </CommFormLine>
      <CommFormLine :title="'지도'" :width="8">
        <div id="map" style="width: 100%; height: 350px"></div>
      </CommFormLine>
    </div>
  </div>
</template>

<script setup lang="ts">
import { loadScript, unloadScript } from '@/utils/standaloneImport';
import { ref, onMounted, onUnmounted, reactive } from 'vue';
import apis from '@/apis';
import CommFormLine from '@/components/comm/CommFormLine.vue';
import { apiResponseCheck, showAlert, showConfirm } from '@/utils/common-utils';
import type { Prod } from 'ProductListInfoModule';
const installList = reactive(['//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js', `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_JS_KEY}&autoload=false`]);
const props = defineProps<{ productId: number; productInfo: Prod | null }>();
const emits = defineEmits(['saveFinish', 'changedProdInfo']);

const prodInfo = ref({} as Prod);

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

const onStepActive = () => {
  if (props.productId && props.productInfo) {
    prodInfo.value = JSON.parse(JSON.stringify(props.productInfo));
  }
  if (prodInfo.value.address) {
    getCoordinate(prodInfo.value.address);
  }
};
defineExpose({ onStepActive });

const saveStoreInfo = () => {
  if (!prodInfo.value.tel) {
    showAlert('전화번호를 입력해주세요.', 'warning');
    return;
  }
  if (!prodInfo.value.address) {
    showAlert('주소를 입력해주세요.', 'warning');
    return;
  }

  let params: object = {
    tel: prodInfo.value.tel,
    address: prodInfo.value.address,
    lat: prodInfo.value.lat,
    lng: prodInfo.value.lng,
    address_detail: prodInfo.value.address_detail,
  };

  showConfirm('상품 매장 정보를 저장하시겠습니까?', () => {
    apis.product.updateBaseInfo(props.productId, params).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 매장 정보가 저장되었습니다.', 'success');
        emits('changedProdInfo');
        emits('saveFinish', 'store');
      });
    });
  });
};

const onSearchAddress = (e: any) => {
  e.preventDefault();
  //@ts-ignore
  new daum.Postcode({
    oncomplete: (data: any) => {
      const { roadAddress } = data;
      prodInfo.value.address = roadAddress;
      getCoordinate(roadAddress);
    },
  }).open();
};

const getCoordinate = async (roadAddress: string) => {
  const res = await apis.map.getCoordinate(roadAddress);
  prodInfo.value.lat = res.y;
  prodInfo.value.lng = res.x;
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
</script>
