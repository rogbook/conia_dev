<template>
  <PageNavigator :before_link="['교환/반품 관리']" :current="'교환/반품 상세'" />
  <div class="card">
    <div class="card-header">
      <div class="row">
        <div class="h3">교환/반품 상세현황</div>
        <div class="row align-items-center">
          <div class="col-auto h4 mt-2">주문번호 : {{ mOrderInfo.id }}</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="order-cancel_return mb-5">
        <div class="h5 mb-3">교환/반품 내역</div>
        <div class="table-responsive">
          <table class="table table-nowrap table-align-middle card-table border" v-if="mOrderExRe.parent && mOrderExRe.product">
            <thead class="thead-light text-center">
              <tr>
                <th>교환/반품</th>
                <th>상품</th>
                <th>반품사유</th>
                <th v-if="mOrderExRe.parent.type === 'refund'">처리금액</th>
                <th>처리수량</th>
                <th>처리상태</th>
                <th>접수일</th>
                <th>완료일</th>
                <th v-if="!getUserClassStr.includes('MC')">처리</th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-center">
                <td>{{ mOrderExRe.parent.type === 'exchange' ? '교환' : mOrderExRe.parent.type === 'return' ? '반품' : '-' }}</td>
                <td class="text-center text-wrap">
                  <div class="card-body p-0">
                    <div class="row align-items-center p-0">
                      <div class="col-auto">
                        <img :src="mOrderExRe.product.product_thumbnail" style="width: 70px" />
                      </div>
                      <div class="col text-start">
                        <div class="mb-1">
                          <b>{{ mOrderExRe.product.product_name }}</b>
                        </div>
                        <div class="" v-if="mOrderExRe.product.product_option_name">옵션 : {{ mOrderExRe.product.product_option_name }}</div>
                      </div>
                    </div>
                  </div>
                </td>
                <td>{{ mOrderExRe.parent.contents }}</td>
                <td v-if="mOrderExRe.parent.type === 'refund'">{{ mOrderExRe.parent.refund_amount }} 원</td>
                <td>{{ mOrderExRe.product.ea }}</td>
                <td>{{ convertOrderStatus(mOrderExRe.product.status) }}</td>
                <td>{{ dateTimeFormatConverter(mOrderExRe.reg_date) }}</td>
                <td>{{ mOrderExRe.end_date ? dateTimeFormatConverter(mOrderExRe.end_date) : '-' }}</td>
                <td v-if="!getUserClassStr.includes('MC')">
                  <div v-if="['RFR', 'EXR'].includes(mOrderExRe.product.status)">
                    <button type="button" class="btn btn-sm btn-warning" @click.prevent="orderReChange(mOrderExRe.product.status)">요청승인</button>
                  </div>
                  <div v-if="mOrderExRe.product.status === 'RFN' || mOrderExRe.product.status === 'CD'">
                    <button type="button" class="btn btn-sm btn-warning me-2" @click.prevent="orderCancel" v-if="mOrderExRe.product.status === 'RFN'">결제취소</button>
                    <button type="button" class="btn btn-sm btn-danger" @click.prevent="orderReChange(mOrderExRe.product.status)">반품진행 완료처리</button>
                  </div>
                  <div v-if="mOrderExRe.product.status === 'EXN'">
                    <button type="button" class="btn btn-sm btn-warning me-2" @click.prevent="openProductModal">교환주문생성</button>
                    <button type="button" class="btn btn-sm btn-danger" @click.prevent="orderReChange(mOrderExRe.product.status)">교환진행 완료처리</button>
                  </div>
                </td>
              </tr>
              <tr v-if="!mOrderExRe">
                <td colspan="7" class="text-center">취소/반품 내역이 없습니다.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="order-info mb-4">
        <div class="h6">주문정보</div>
      </div>
      <div class="table-responsive">
        <table class="table table-nowrap table-align-middle card-table border">
          <thead class="thead-light">
            <tr>
              <th class="text-center">주문일시</th>
              <th class="text-center">주문번호</th>
              <th class="text-center">주문자</th>
              <th class="text-center">주문자 아이디</th>
              <th class="text-center">주문자 연락처</th>
              <th class="text-center">주문상태</th>
              <th class="text-center">할인금액</th>
              <th class="text-center">총 결제금액</th>
              <th class="text-center">결제수단</th>
            </tr>
          </thead>
          <tbody>
            <tr class="" v-for="(id, i) in Object.keys(mShipGroupProds as object)" :key="JSON.stringify(id)">
              <td class="text-center p-4" :rowspan="mMyProducts.length" v-if="i === 0">{{ dateTimeFormatConverter(mOrderInfo.reg_date) }}</td>
              <td class="text-center p-4" :rowspan="mMyProducts.length" v-if="i === 0">{{ mOrderInfo.id }}</td>
              <td class="text-center p-4" :rowspan="mMyProducts.length" v-if="i === 0">{{ mOrderInfo.user_name }}</td>
              <td class="text-center p-4" :rowspan="mMyProducts.length" v-if="i === 0">{{ mOrderInfo.user_email }}</td>
              <td class="text-center p-4" :rowspan="mMyProducts.length" v-if="i === 0">{{ mOrderInfo.user_mobile }}</td>
              <td class="text-center p-4" :rowspan="mMyProducts.length" v-if="i === 0">{{ convertOrderStatus(mOrderInfo.status) }}</td>
              <td class="text-end p-4" :rowspan="mMyProducts.length" v-if="i === 0">{{ mOrderInfo.discount.toLocaleString() }}원</td>
              <td class="text-end p-4" :rowspan="mMyProducts.length" v-if="i === 0">{{ mOrderInfo.final_amount.toLocaleString() }}원</td>
              <td class="text-center p-4" :rowspan="mMyProducts.length" v-if="i === 0">
                {{ mOrderInfo.pg_info?.kind === 'card' ? '신용카드' : mOrderInfo.pg_info?.kind }}<span v-if="mOrderInfo.pg_info?.kind === 'card'"><br />({{ mOrderInfo.pg_info?.card_name }})</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- TODO: 결제 확인 단계에서 하단 항목 표시되야함 -->
      <div class="row align-items-center mt-2 ps-2 pe-2 pt-1 pb-1 mb-4" v-if="mOrderInfo.status === 'PW'">
        <div class="col-auto">
          <div class="text-danger">&#8251; 입금대기 상태인 이 주문은 입금이 확인 되어야 상품을 준비/배송할 수 있습니다.</div>
          <!--          <div class="text-black">-->
          <!--            결제확인 상태인 이 주문 <span style="color: red">1</span>개(종)는 <span style="color: red">1</span>개를 보내야 <button class="btn btn-sm btn-dark p-1">출고처리</button> 하며, <span style="color: red">0</span>개는 발송 준비중이며,-->
          <!--            <span style="color: yellow">0</span>개는 발송되었습니다.-->
          <!--          </div>-->
        </div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-warning py-1">입금확인</button>
        </div>
      </div>
      <div class="order-prod-info mb-4">
        <div class="h6">주문상품정보</div>
        <div class="table-responsive">
          <table class="table table-nowrap table-align-middle card-table border">
            <thead class="thead-light">
              <tr>
                <th class="text-center">상점</th>
                <th class="text-center">공급자</th>
                <th class="text-center">주문상품상태</th>
                <th class="text-center">주문상품</th>
                <th class="text-center">상품금액</th>
                <th class="text-center">수량</th>
                <th class="text-center" v-if="!mMyProducts[0]?.type.startsWith('UP')">배송비</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(id, i) in Object.keys(mShipGroupProds as object)" :key="JSON.stringify(id)">
                <td class="text-center p-2" :rowspan="mMyProducts.length" v-if="i === 0">{{ (mShipGroupProds[id][0] as Product).store_name }}</td>
                <td class="text-center p-2">{{ (mShipGroupProds[id][0] as Product).seller_title }}</td>
                <td class="text-center p-2">{{ convertOrderStatus((mShipGroupProds[id][0] as Product).status) }}</td>
                <td class="text-center text-wrap">
                  <div class="card-body p-0">
                    <div class="row align-items-center mb-2" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)">
                      <div class="col-auto">
                        <img :src="prod.product_thumbnail" style="width: 70px" />
                      </div>
                      <div class="col text-start">
                        <div class="mb-1">
                          <b>{{ (prod as Product).product_name }}</b>
                        </div>
                        <div class="">옵션 : {{ (prod as Product).product_option_name ? (prod as Product).product_option_name : '없음' }}</div>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="text-center p-2">
                  <div class="row align-items-center py-4" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)">
                    <div class="col">{{ (prod as Product).amount.toLocaleString() }}원</div>
                  </div>
                </td>
                <td class="text-center p-2">
                  <div class="row align-items-center py-4" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)">
                    <div class="col">{{ (prod as Product).ea }}</div>
                  </div>
                </td>
                <td class="text-end p-2" v-if="!(mShipGroupProds[id][0] as Product).type.startsWith('UP')">{{ (mShipGroupProds[id][0] as Product).order_shipping?.cost.toLocaleString() }}원</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="order-release mb-4">
        <div class="h6">배송정보</div>
        <div class="table-responsive">
          <table class="table table-nowrap table-align-middle card-table border">
            <thead class="thead-light">
              <tr>
                <th class="text-center">상품</th>
                <th class="text-center">택배사</th>
                <th class="text-center">송장번호</th>
                <th class="text-center">배송비</th>
                <th class="text-center">배송지 주소</th>
                <th class="text-center">배송상태</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(id) in Object.keys(mShipGroupProds as object)" :key="JSON.stringify(id)">
                <td class="text-start">
                  <div class="card-body p-0">
                    <div class="row align-items-center mb-2" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)">
                      <div class="col-auto">
                        <img :src="prod.product_thumbnail" style="width: 70px" />
                      </div>
                      <div class="col text-start">
                        <div class="mb-1">
                          <b>{{ (prod as Product).product_name }}</b>
                        </div>
                        <div class="">옵션 : {{ (prod as Product).product_option_name ? (prod as Product).product_option_name : '없음' }}</div>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="text-center">{{ (mShipGroupProds[id][0] as Product).order_shipping.provider ? `${(mShipGroupProds[id][0] as Product).order_shipping.provider}` : '미등록' }}</td>
                <td class="text-center">{{ (mShipGroupProds[id][0] as Product).order_shipping.number ? `${(mShipGroupProds[id][0] as Product).order_shipping.number}` : '미등록' }}</td>
                <td class="text-center">{{ (mShipGroupProds[id][0] as Product).order_shipping.cost.toLocaleString() }}</td>
                <td class="text-center">({{ mOrderInfo.zipcode }}) {{ mOrderInfo.address }}, {{ mOrderInfo.address_detail }}<br />{{ mOrderInfo.user_mobile }} {{ mOrderInfo.shipping_msg ? ' | ' : '' }} {{ mOrderInfo?.shipping_msg }}</td>
                <td class="text-center">
                  <div class="col-auto">
                    {{ convertOrderStatus((mShipGroupProds[id][0] as Product).order_shipping.status) }}
                  </div>
                  <div class="col-auto">
                    <button type="button" class="btn btn-sm btn-success" @click.prevent="openTrackingModal(id as number)" v-if="!getUserClassStr.includes('MC')">배송추적</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <!--    <div class="card-footer"></div>-->
  </div>

  <!-- 교환 상품 선택 Modal -->
  <Modal :id="'exchangeProdModal'" :title="'교환 상품 선택'">
    <template #body>
      <div class="card" v-if="mOrderExRe.product">
        <div class="card-header">교환상품 옵션 정보</div>
        <div class="card-body">
          <div class="label h4 mb-2">상품명 : {{ mOrderExRe.product.product_name }}</div>
          <div class="row align-items-center">
            <div class="col-auto">
              <img :src="mOrderExRe.product.product_thumbnail" style="max-height: 10rem" />
            </div>
            <div class="col">
              <div class="">
                <div class="" v-if="mProdOptionTitleList.length > 0">
                  <div class="label mb-2">상품 옵션 선택:</div>
                  <div class="mb-2" v-for="(title, i) in mProdOptionTitleList" :key="JSON.stringify(title)">
                    <!-- Select -->
                    <div class="tom-select-custom">
                      <select class="form-select" v-model="selectOption[i]" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                        <option value="" disabled>{{ title }}</option>
                        <option value="" v-if="i > 0 && !selectOption[i - 1]">상위 옵션을 선택해주세요.</option>
                        <option v-for="detail in options[i]" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.code" v-show="options[i].length > 0 && i === 0"></option>
                        <option v-for="detail in options[i]" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.code" v-show="options[i].length > 0 && i > 0 && selectOption[i - 1]"></option>
                      </select>
                    </div>
                  </div>
                </div>
                <div class="label mb-2">수량 입력:</div>
                <input class="form-control mb-2" type="number" v-model="exchangeCount" @input="checkCountInput($event)" />
                <div class="label" v-if="findSelectOption !== null">{{ getOptionPrice }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-sm btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="makeExchangeOrder">교환주문생성</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onBeforeMount, onMounted, reactive, ref } from 'vue';
import { apiResponseCheck, convertOrderStatus, dateTimeFormatConverter, showAlert, showConfirm, getUserClassStr, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import type { OrderDetail, Product } from 'OrderDetailInfoModule';
import { useUserStore } from '@/stores/user';
import Modal from '@/components/comm/modal.vue';
import type { ExReListInfo } from 'ExReInfoModule';
import PageNavigator from '@/components/title/PageNavigator.vue';
import { useCommonStore } from '@/stores/common';

const router = useRouter();
const route = useRoute();

const mOrderOriginId = ref(0);
const mOrderExReId = ref(0);
const mOrderExRe = ref({} as ExReListInfo);
const mOrderExReOrigin = ref({} as ExReListInfo);

const mOrderInfo = ref({} as OrderDetail);

const mMyProducts = ref([] as Product[]);
const mShipGroupProds = ref({} as any);

const mProdOptionList = ref([] as any[]);
const mProdOptionTitleList = ref([] as string[]);
const options = ref([] as any[][]);
const selectOption = ref([] as string[]);
const exchangeCount = ref(1);

const trackingInfo = reactive({
  order_shipping_id: 0,
  code: '',
  provider: '',
  status: '',
  contents: [],
});

const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

const props = defineProps({
  orderId: {
    type: Number,
    required: true,
  },
});

const getOrderOriginDetail = () => {
  apis.order.get_order_detail(mOrderOriginId.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mOrderInfo.value = res;
      checkProducts();
    });
  });
};

const checkProducts = () => {
  mMyProducts.value = [];
  mShipGroupProds.value = {} as any;
  if (userClass.value.includes('CM')) {
    mMyProducts.value = mOrderInfo.value.products;
  } else if (userClass.value.includes('PA')) {
    mOrderInfo.value.products.map(item => {
      if (item.member_id === useUserStore().user.id) {
        mMyProducts.value.push(item);
      }
    });
  }

  for (const prod of mMyProducts.value) {
    if (Object.keys(mShipGroupProds.value).includes(`${prod.order_shipping_id}`)) {
      mShipGroupProds.value[`${prod.order_shipping_id}`].push(prod);
    } else {
      mShipGroupProds.value[`${prod.order_shipping_id}`] = [prod];
    }
  }
};

const orderReChange = (currentStatus: string) => {
  let status = '';
  switch (currentStatus) {
    case 'RFR':
      status = 'RFN';
      break;
    case 'EXR':
      status = 'EXN';
      break;
    case 'RFN':
    case 'CD':
      status = 'RFC';
      break;
    case 'EXN':
      status = 'EXC';
      break;
  }
  showConfirm(`처리 상태를 [${convertOrderStatus(status)}] 상태로 변경하시겠습니까?`, () => {
    apis.order.mod_exre_status(mOrderExRe.value.parent.id, { order_product_ids: [mOrderExRe.value.product.id], status: status }).then(res => {
      apiResponseCheck(res, () => {
        showAlert('처리 상태가 변경되었습니다.', 'success', () => {
          mOrderExReOrigin.value.product.status = status;
          mOrderExRe.value.product.status = status;
          history.state.order_re = JSON.stringify(mOrderExRe.value);
        });
      });
    });
  });
};

const orderCancel = () => {
  showConfirm(`해당 반품요청 상품에 대하여 결제를 취소 하시겠습니까?`, () => {
    apis.order
      .order_cancel_exre(mOrderExRe.value.parent.order_id, { cancel_amount: mOrderExRe.value.product.amount + mOrderExRe.value.product.order_shipping.cost, order_product_ids: [mOrderExRe.value.product.id], order_shipping_ids: [mOrderExRe.value.product.order_shipping_id] })
      .then(res => {
        apiResponseCheck(res, () => {
          showAlert(`결제 취소가 완료되었습니다.\n반품진행완료를 통해 완료처리 해주세요.`, 'success', () => {
            mOrderExReOrigin.value.product.status = 'CD';
            mOrderExRe.value.product.status = 'CD';
            history.state.order_re = JSON.stringify(mOrderExRe.value);
          });
        });
      });
  });
};

const openProductModal = () => {
  getProdInfo();
  showModal('exchangeProdModal');
};

const getProdInfo = () => {
  mProdOptionList.value = [];
  mProdOptionTitleList.value = [];
  options.value = [];
  selectOption.value = [];
  exchangeCount.value = mOrderExRe.value.product.ea;
  apis.product.getProdOption(mOrderExRe.value.product.product_id).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mProdOptionList.value = JSON.parse(JSON.stringify(res));
      if (mProdOptionList.value.length > 1) {
        mProdOptionTitleList.value = mProdOptionList.value[0].option_title.split(',');
        mProdOptionTitleList.value.map(item => {
          selectOption.value.push('');
          options.value.push([]);
        });
        mProdOptionList.value.map(item => {
          if (
            item.option_1 &&
            !options.value[0].some(op => {
              return op.name === item.option_1;
            })
          )
            options.value[0].push({ name: item.option_1, code: item.option_code_1 });
          if (
            item.option_2 &&
            !options.value[1].some(op => {
              return op.name === item.option_2;
            })
          )
            options.value[1].push({ name: item.option_2, code: item.option_code_2 });
          if (
            item.option_3 &&
            !options.value[2].some(op => {
              return op.name === item.option_3;
            })
          )
            options.value[2].push({ name: item.option_3, code: item.option_code_3 });
          if (
            item.option_4 &&
            !options.value[3].some(op => {
              return op.name === item.option_4;
            })
          )
            options.value[3].push({ name: item.option_4, code: item.option_code_4 });
          if (
            item.option_5 &&
            !options.value[4].some(op => {
              return op.name === item.option_5;
            })
          )
            options.value[4].push({ name: item.option_5, code: item.option_code_5 });
        });
      }
    });
  });
};

const makeExchangeOrder = () => {
  let selected = true;
  selectOption.value.map(item => {
    if (!item) {
      selected = false;
    }
  });
  if (!selected) {
    showAlert('상품 옵션을 모두 선택 하였는지 확인해주세요.', 'warning');
    return;
  }

  if (exchangeCount.value === 0) {
    showAlert('상품 수량을 입력해주세요.', 'warning');
    return;
  }
  const option = mProdOptionList.value.length > 1 ? findSelectOption() : mProdOptionList.value[0];

  showConfirm(`해당 내용으로 교환 주문을 생성하시겠습니까?`, () => {
    apis.order.order_exchange(mOrderExRe.value.product.id, option.id, option.selling_price * exchangeCount.value, exchangeCount.value).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('교환 주문이 생성되었습니다.\n주문 관리에서 해당 교환 주문 정보를 확인해주세요.');
          hideModal('exchangeProdModal');
        },
        (num?: number) => {
          if (num === 403) {
            hideModal('exchangeProdModal');
          }
        },
      );
    });
  });
};

const findSelectOption = (): any => {
  for (const op of mProdOptionList.value) {
    if (op.code === selectOption.value.join(',').replace(',', '').trim()) {
      return op;
    }
  }
  return null;
};

const getOptionPrice = computed(() => {
  const op = findSelectOption();
  return op ? `상품 가격 : ${(op.selling_price * exchangeCount.value).toLocaleString()} (${op.selling_price.toLocaleString()} x ${exchangeCount.value})원` : '';
});

const checkCountInput = (e: any) => {
  if (!e.target.value) {
    e.target.value = 0;
    exchangeCount.value = 0;
    return;
  }

  if (e.target.value.startsWith('00') || /0\d$/.test(e.target.value)) {
    e.target.value = parseInt(e.target.value as string);
  }
};

interface OrderShipping {
  id: 0;
  provider: string;
  provider_code: string;
  number: string;
  status: string;
  cost: number;
  shipping_type: string;
  pay_type: string;
  order_id: string;
  member_id: number;
  shipping_info_id: number;
}

const openTrackingModal = (order_shipping: OrderShipping | null) => {
  if (!order_shipping) {
    showAlert('배송정보에 오류가 있습니다.\n관리자에게 문의해주세요.', 'error');
    return;
  }

  const form = document.createElement('form');
  form.action = 'https://info.sweettracker.co.kr/tracking/3';
  form.name = 'form';
  form.target = 'form';

  const tKey = document.createElement('input');
  tKey.setAttribute('type', 'hidden');
  tKey.setAttribute('name', 't_key');
  tKey.setAttribute('id', 't_key');
  tKey.setAttribute('value', (useCommonStore().logisticsKey as any).value);
  form.append(tKey);

  const tCode = document.createElement('input');
  tCode.setAttribute('type', 'hidden');
  tCode.setAttribute('name', 't_code');
  tCode.setAttribute('id', 't_code');
  tCode.setAttribute('value', order_shipping.provider_code);
  form.append(tCode);

  const tInvoice = document.createElement('input');
  tInvoice.setAttribute('type', 'hidden');
  tInvoice.setAttribute('name', 't_invoice');
  tInvoice.setAttribute('id', 't_invoice');
  tInvoice.setAttribute('value', order_shipping.number);
  form.append(tInvoice);

  // document에 동적 생성한 form 등록
  document.body.appendChild(form);
  // 본인인증창 팝업으로 띄움
  setTimeout(async () => {
    window.open('', 'form', 'width=500, height=550, top=100, left=100, fullscreen=no, menubar=no, status=no, toolbar=no, titlebar=yes, location=no, scrollbar=no');

    form.submit();
    form.remove();
  });
};

onMounted(() => {
  const orderOriginId = history.state.orderOriginId;
  const order_re = history.state.order_re;

  if (!order_re) {
    showAlert('비정상적인 접근입니다.', 'error', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
  } else {
    mOrderExRe.value = JSON.parse(order_re);
    mOrderExReOrigin.value = JSON.parse(order_re);
    mOrderExReId.value = order_re.id;
    mOrderOriginId.value = orderOriginId;
    showLogConsole(mOrderExRe.value);
    // getOrderExReDetail();
    getOrderOriginDetail();
  }
});
</script>

<style scoped></style>
