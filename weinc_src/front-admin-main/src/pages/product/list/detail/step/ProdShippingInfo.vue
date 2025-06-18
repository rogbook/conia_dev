<template>
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">상품 배송 정보</h4>
          <small>상품의 배송 정보를 선택합니다.</small>
        </div>
        <div class="nav-item ms-auto">
          <button type="button" class="btn btn-warning" @click.prevent="saveShippingInfo">저장</button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="row align-items-center mb-3">
        <div class="col-1 ms-1">
          <label>배송그룹 선택</label>
        </div>
        <div class="col-auto">
          <div class="tom-select-custom col-auto">
            <select class="form-select" v-model="selectedShipId" @change="changeShippingInfo" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option value="0" disabled>배송그룹을 선택해주세요</option>
              <option v-for="common in shippingList" :key="common.id" v-text="common.name" :value="common.id"></option>
            </select>
          </div>
        </div>
      </div>
      <div class="shipping-info-area" v-if="selectedShipId !== 0">
        <div class="card-body">
          <div class="row">
            <div class="card col-md-4 me-4">
              <div class="card-header py-3">
                <span class="icon icon-xs icon-dark icon-circle" style="width: 0.5rem; height: 0.5rem"></span>
                기본정보
              </div>
              <div class="card-body">
                <div class="row col mb-2 align-items-center">
                  <label class="col-md-3 col-form-label">배송그룹명</label>
                  <div class="col">
                    <div class="input-group">
                      <input type="text" class="form-control" v-model="shippingInfo.name" readonly />
                    </div>
                  </div>
                </div>
                <div class="row col mb-2 align-items-center">
                  <label class="col-md-3 col-form-label">배송타입</label>
                  <div class="col">
                    <div class="input-group">
                      <input type="text" class="form-control" v-model="shippingInfo.type" readonly />
                    </div>
                  </div>
                </div>
                <div class="row col mb-2 align-items-center">
                  <label class="col-md-3 col-form-label">지불방법</label>
                  <div class="col">
                    <div class="input-group">
                      <input type="text" class="form-control" v-model="shippingInfo.type" readonly />
                    </div>
                  </div>
                </div>
                <div class="row col mb-2 align-items-center">
                  <label class="col-md-3 col-form-label">계산방법</label>
                  <div class="col">
                    <div class="input-group">
                      <input type="text" class="form-control" v-model="shippingInfo.type" readonly />
                    </div>
                  </div>
                </div>
                <div class="row col mb-2 align-items-center">
                  <label class="col-md-3 col-form-label">반품비설정</label>
                  <div class="col">
                    <div class="input-group">
                      <input type="text" class="form-control text-end" placeholder="반품비를 입력해주세요." :value="shippingInfo.change_cost?.toLocaleString()" readonly />
                      <div class="input-group-text">
                        <span class="">원</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row col mb-2 align-items-center">
                  <label class="col-md-3 col-form-label">교환비설정</label>
                  <div class="col">
                    <div class="input-group">
                      <input type="text" class="form-control text-end" placeholder="교환비를 입력해주세요." :value="shippingInfo.return_cost?.toLocaleString()" readonly />
                      <div class="input-group-text">
                        <span class="">원</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="card col" v-if="shippingInfo">
              <div class="card-header py-3">
                <span class="icon icon-xs icon-dark icon-circle" style="width: 0.5rem; height: 0.5rem"></span>
                배송비 정보
              </div>
              <div class="card-body">
                <table class="table table-bordered table-thead-bordered table-align-middle card-table">
                  <thead class="thead-light">
                    <tr class="text-center">
                      <th style="width: 15%">배송비 타입</th>
                      <th>배송비 내용</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="text-center" v-if="hasCostInfo">
                      <td>{{ convertShippingType }}</td>
                      <td class="text-center">
                        <div class="cost-info-basic row align-items-center border-1 border-bottom mb-2 pb-2">
                          <div class="col-auto">[기본]</div>
                          <div class="col">
                            <div class="row align-items-center" v-for="c in shippingInfo.shipping_costs" :key="c.id">
                              <div class="row align-items-center mb-2 justify-content-between" v-if="c.category === 'basic' && !(c.type === 'fix' || c.type === 'free')">
                                <div class="col-md-4" v-if="c.section_start >= 0">
                                  <div class="input-group">
                                    <input type="number" class="form-control text-end" placeholder="구간시작값" :value="c.section_start" readonly />
                                    <div class="input-group-text px-2">
                                      <span class="" v-if="shipType.startsWith('ea')">개 이상</span>
                                      <span class="" v-else-if="shipType.startsWith('weight')">Kg 이상</span>
                                      <span class="" v-else>원 이상</span>
                                    </div>
                                  </div>
                                </div>
                                <span class="col-auto" v-if="c.section_end || c.section_repeat">~</span>
                                <div class="col-md-4" v-if="c.section_end">
                                  <div class="input-group">
                                    <input type="number" class="form-control text-end" placeholder="구간종료값" :value="c.section_end" readonly />
                                    <div class="input-group-text px-2">
                                      <span class="" v-if="shipType.startsWith('ea')">개 미만</span>
                                      <span class="" v-else-if="shipType.startsWith('weight')">Kg 미만</span>
                                      <span class="" v-else>원 미만</span>
                                    </div>
                                  </div>
                                </div>
                                <div class="col-md-4" v-else-if="c.section_repeat">
                                  <div class="input-group">
                                    <input type="number" class="form-control text-end" placeholder="구간종료값" :value="c.section_repeat" readonly />
                                    <div class="input-group-text px-2">
                                      <span class="" v-if="shipType.startsWith('ea')">개 당</span>
                                      <span class="" v-else-if="shipType.startsWith('weight')">Kg 당</span>
                                      <span class="" v-else>원 당</span>
                                    </div>
                                  </div>
                                </div>
                                <div class="col" v-else></div>
                                <div class="col-md-3">
                                  <div class="input-group">
                                    <input type="text" class="form-control text-end" placeholder="배송비를 입력해주세요." :value="c.cost.toLocaleString()" readonly />
                                    <div class="input-group-text px-2">
                                      <span class="">원</span>
                                    </div>
                                  </div>
                                </div>
                              </div>
                              <div class="row align-items-center" v-else>
                                <div class="col-md-4 ms-md-2">
                                  <div class="input-group">
                                    <input type="text" class="form-control text-end" placeholder="배송비를 입력해주세요." :value="c.cost.toLocaleString()" readonly />
                                    <div class="input-group-text px-2">
                                      <span class="">원</span>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="cost-info-basic row align-items-center pt-2">
                          <div class="col-auto">[도서산간]</div>
                          <div class="col">
                            <div class="row align-items-center mb-2" v-if="shippingInfo.shipping_costs[shippingInfo.shipping_costs.length - 1].category === 'add'">
                              <div class="col-md-5 ms-md-2">
                                <div class="input-group">
                                  <input type="number" class="form-control text-end" placeholder="배송비를 입력해주세요." :value="shippingInfo.shipping_costs[shippingInfo.shipping_costs.length - 1].cost" readonly />
                                  <div class="input-group-text">
                                    <span class="">원</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <div class="row align-items-center" v-else>
                              <div class="text-center">도서산간 추가 배송비 정보 없음.</div>
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import apis from '@/apis';
import type { ShippingInfo } from 'ShippingInfoModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
const props = defineProps<{ productId: number; shippingId: number | null; prodMemberId: number }>();
const emits = defineEmits(['saveFinish', 'changedProdInfo']);

const shippingList = ref([] as ShippingInfo[]);
const selectedShipId = ref(0);
const shippingInfo = ref({} as ShippingInfo);

const hasCostInfo = computed(() => {
  return shippingInfo.value.shipping_costs?.length > 0;
});
const shipType = computed(() => {
  return shippingInfo.value.shipping_costs[0].type;
});
const convertShippingType = computed(() => {
  if (shippingInfo.value.shipping_costs.length > 0) {
    switch (shippingInfo.value.shipping_costs[0].type) {
      case 'free':
        return '무료';
      case 'fix':
        return '고정';
      case 'cost':
        return `금액${checkRepeat()}`;
      case 'ea':
        return `수량${checkRepeat()}`;
      case 'weight':
        return `무게${checkRepeat()}`;
    }
  }
  return '';
});

const checkRepeat = (): string => {
  let lastIdx = -1;
  lastIdx = shippingInfo.value.shipping_costs.map(el => el.category).lastIndexOf('basic');
  if (lastIdx != -1) {
    if (shippingInfo.value.shipping_costs[lastIdx].section_repeat !== null) {
      //구간 반복
      return '(구간반복)';
    } else {
      return '(구간입력)';
    }
  } else {
    return '';
  }
};

const saveShippingInfo = () => {
  if (selectedShipId.value === 0) {
    showAlert('배송그룹을 선택해주세요.', 'warning');
    return;
  }

  if (props.shippingId === selectedShipId.value) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  showConfirm('상품 배송 정보를 저장하시겠습니까?', () => {
    apis.product.updateBaseInfo(props.productId, { shipping_info_id: selectedShipId.value }).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 배송 정보가 저장되었습니다.', 'success');
        emits('changedProdInfo');
        emits('saveFinish', 'shipping');
      });
    });
  });
};

const changeShippingInfo = () => {
  shippingList.value.map(item => {
    if (selectedShipId.value === item.id) {
      shippingInfo.value = item;
    }
  });
};

const getShippingList = () => {
  apis.shipping.get_shipping_info_list(`member_id=${props.prodMemberId}`).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      for (const i in res) {
        if (res[i].shipping_costs.length !== 0) {
          shippingList.value.push(res[i]);
        }
      }
      changeShippingInfo();
    });
  });
};
const onStepActive = () => {
  shippingList.value = [];
  if (props.productId) {
    getShippingList();
  }
  if (props.shippingId) {
    selectedShipId.value = props.shippingId;
  }
};

defineExpose({ onStepActive });
</script>

<style scoped></style>
