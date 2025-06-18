<template>
  <PageNavigator :before_link="['상품요청']" :current="'상품 요청 상세'" />
  <div class="card col-md-6">
    <div class="card-header py-2">
      <div class="form-control-borderless h2 mb-0">상품 요청 상세</div>
    </div>
    <div class="card-body">
      <div class="card">
        <div class="card-header py-3">
          <div class="row align-items-center justify-content-between">
            <div class="col-auto">[상품 요청 내용]</div>
            <div class="col-auto">
              <div class="row" v-if="user_id === 0">
                <label class="col-auto col-form-label">요청 상태 변경</label>
                <div class="col-auto">
                  <!-- Select -->
                  <div class="tom-select-custom">
                    <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                      <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
                    </select>
                  </div>
                  <!-- End Select -->
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card-body">
          <!-- 요청자 -->
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">[요청자]</label>
            <div class="col" v-if="reqInfo.member">
              <input type="text" class="form-control border-0" :value="`${reqInfo.member.name} (${reqInfo.member.email})`" />
            </div>
          </div>
          <!-- 상점(몰) -->
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">[상점명]</label>
            <div class="col" v-if="reqInfo.store">
              <input type="text" class="form-control border-0" :value="`${reqInfo.store.title} (${reqInfo.store.code})`" />
            </div>
          </div>
          <!-- 요청 내용 -->
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">[상품 요청 내용]</label>
            <div class="col" v-if="reqInfo.memo">
              <textarea type="text" class="form-control border-0" :value="reqInfo.memo" style="height: 6.25em; border: none; resize: none" readonly />
            </div>
            <div class="col" v-else>요청 내용 없음.</div>
          </div>
          <!-- 요청 상품 목록 -->
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">[요청 상품 목록]</label>
          </div>
          <div class="table-responsive datatable-custom position-relative">
            <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
              <thead class="thead-light">
                <tr class="text-center">
                  <th>상품코드</th>
                  <th>이미지</th>
                  <th>상품명</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center" v-for="item in reqInfo.products" :key="item.id">
                  <td>{{ item.code }}</td>
                  <td>
                    <div class="avatar" v-if="item.photos.length > 0">
                      <img class="avatar-img" :src="item.photos[0].uri" alt="Image Description" />
                    </div>
                    <div class="avatar" v-if="item.photos.length === 0">
                      <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
                    </div>
                  </td>
                  <td>
                    <span class="d-block h5 mb-0">{{ item.name }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-danger" @click.prevent="deleteReqProd">요청삭제</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import apis from '@/apis';
import { useUserStore } from '@/stores/user';
import { AxiosError } from 'axios';
import type { ProdDetailInfo } from 'ProdReqDetailInfoModule';
import PageNavigator from '@/components/title/PageNavigator.vue';

const router = useRouter();

const mReqId = ref(0);
const user_id = ref(0);
const reqInfo = ref({} as ProdDetailInfo);
const originReqInfo = ref({} as ProdDetailInfo);

const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

const selDetailSearch = reactive({
  items: [
    { name: '요청중', value: 'R' },
    { name: '요청완료', value: 'C' },
    { name: '요청반려', value: 'D' },
  ],
  selectedItem: 'R',
});

const onChangeDetailSearch = () => {
  showConfirm(
    '요청 상태를 변경하시겠습니까?',
    () => {
      apis.product.modProdReq(mReqId.value, { status: selDetailSearch.selectedItem }).then(res => {
        apiResponseCheck(res, () => {
          showLogConsole(res);
          showAlert('요청 상태가 변경되었습니다.', 'success');
          getReqDetail();
        });
      });
    },
    () => {
      selDetailSearch.selectedItem = originReqInfo.value.status;
    },
  );
};

const getReqDetail = () => {
  apis.product.getProdReq(mReqId.value).then(res => {
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg)
        showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error', () => {
          if (window.history.length > 1) {
            router.back();
          } else {
            router.replace('/');
          }
        });
      else
        showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error', () => {
          if (window.history.length > 1) {
            router.back();
          } else {
            router.replace('/');
          }
        });
    } else {
      showLogConsole(res);
      reqInfo.value = res;
      selDetailSearch.selectedItem = reqInfo.value.status;
      originReqInfo.value = JSON.parse(JSON.stringify(res));
    }
  });
};

const deleteReqProd = () => {
  showConfirm('해당 요청을 삭제하시겠습니까?', () => {
    apis.product.deleteProdReq(mReqId.value).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 요청이 삭제되었습니다.', 'success', () => {
          if (window.history.length > 1) {
            router.back();
          } else {
            router.replace('/');
          }
        });
      });
    });
  });
};

onMounted(() => {
  if (history.state.id === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
  }

  mReqId.value = parseInt(history.state.id.toString());

  if (!userClass.value.includes('CM')) {
    user_id.value = useUserStore().user.id as number;
  }

  getReqDetail();
});
</script>

<style scoped></style>
