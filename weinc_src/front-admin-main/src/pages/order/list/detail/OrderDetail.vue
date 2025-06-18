<template>
  <PageNavigator :before_link="['주문관리']" :current="'주문상세'" />
  <div class="card">
    <div class="card-header">
      <div class="row">
        <div class="h3">주문상세현황</div>
        <div class="row align-items-center pe-0">
          <div class="col-auto h4 mt-2" @click.prevent="checkShowForce">주문번호 : {{ mOrderInfo.id }}</div>
          <!-- TODO : 무통장입금 입금대기일 경우에만 노출 -->
          <div class="col" v-if="mOrderInfo.status === 'PW'">
            <button type="button" class="btn btn-sm btn-warning" disabled>입금대기</button>
          </div>
          <div class="col text-end me-0 pe-0" v-if="orderCancelPermission && !['CD', 'AR'].includes(mOrderInfo.status) && !mOrderInfo.pg_cancel_disable">
            <button type="button" class="btn btn-sm btn-warning me-2" v-if="getUserClassStr.includes('CM') && !isAllOpStatusCP" @click.prevent="openAdminRefund">관리자 환불</button>
            <button type="button" class="btn btn-sm btn-danger" v-if="!isAllOpStatusCP" @click.prevent="allProdCancel">주문전체취소</button>
          </div>
          <div class="col text-end me-0 pe-0" v-if="orderCancelPermission && mOrderInfo.status !== 'CD' && mOrderInfo.pg_cancel_disable">
            <span class="text-danger">&#8251; 취소불가 : {{ mOrderInfo.pg_cancel_disable }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="order-info mb-4">
        <div class="h6">주문정보</div>
        <div class="table-responsive">
          <table class="table table-nowrap table-align-middle card-table border">
            <thead class="thead-light">
              <tr>
                <th class="text-center">주문일시</th>
                <th class="text-center">주문번호</th>
                <th class="text-center">주문자</th>
                <th class="text-center">주문자 아이디</th>
                <th class="text-center">주문자 연락처</th>
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
                <td class="text-end p-4" :rowspan="mMyProducts.length" v-if="i === 0">{{ mOrderInfo.discount.toLocaleString() }}원</td>
                <td class="text-end p-4" :rowspan="mMyProducts.length" v-if="i === 0">{{ mOrderInfo.final_amount.toLocaleString() }}원</td>
                <td class="text-center p-4" :rowspan="mMyProducts.length" v-if="i === 0">
                  {{ convertPgType(mOrderInfo.pg_info?.kind) }}<span v-if="mOrderInfo.pg_info?.kind === 'card'"><br />({{ mOrderInfo.pg_info?.card_name }})</span>
                  <span v-else-if="mOrderInfo.pg_info?.pg_info_sub"><br />({{ showPgSubInfo(mOrderInfo.pg_info?.pg_info_sub) }})</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
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
        <div class="row align-items-center">
          <div class="h6 col">주문상품정보</div>
          <div class="h6 col text-end">
            <button type="button" class="btn btn-sm btn-secondary me-2" v-if="!['CD', 'AR'].includes(mOrderInfo.status) && showCancelPart" @click.prevent="toggleCancelPart(false)">취소</button>
            <button type="button" class="btn btn-sm btn-danger me-2" v-if="!['CD', 'AR'].includes(mOrderInfo.status) && showCancelPart" @click.prevent="orderCancelPart">주문개별취소</button>
            <button type="button" class="btn btn-sm btn-warning" v-if="orderCancelPermission && !['CD', 'AR'].includes(mOrderInfo.status) && !mOrderInfo.pg_cancel_disable && !showCancelPart && !isAllOpStatusCP" @click.prevent="toggleCancelPart(true)">주문개별취소 선택</button>
          </div>
        </div>
        <div class="table-responsive-md">
          <table class="table table-nowrap table-align-middle card-table border">
            <thead class="thead-light">
              <tr>
                <th class="text-center">상점</th>
                <th class="text-center">공급자</th>
                <th class="text-center" style="width: 10%">주문상품상태</th>
                <th class="text-center" style="width: 40%">주문상품</th>
                <th class="text-center">상품금액</th>
                <th class="text-center">할인금액</th>
                <th class="text-center">결제금액</th>
                <th class="text-center">수량</th>
                <th class="text-center" v-if="!mMyProducts[0]?.type?.startsWith('UP')">배송비</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(id, i) in Object.keys(mShipGroupProds as object)" :key="JSON.stringify(id)">
                <td class="text-center" :rowspan="mMyProducts.length" v-if="i === 0">{{ (mShipGroupProds[id][0] as Product).store_name }}</td>
                <td class="text-center">{{ (mShipGroupProds[id][0] as Product).seller_title }}</td>
                <td class="text-center p-2">
                  <div class="row align-items-center py-4" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)" style="height: 100px">
                    <div class="col">{{ convertOrderStatus(prod.status) }}</div>
                  </div>
                </td>
                <td class="text-center text-wrap">
                  <div class="row align-items-center" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)" style="height: 100px">
                    <div class="col-1">
                      <input
                        type="checkbox"
                        class="form-check-input"
                        :id="`chkb_prod_id_${id}`"
                        name="cancel_prod_id"
                        :value="prod"
                        v-model="mSelProductList[id]"
                        v-if="showCancelPart && !checkProdCancelLine((prod as Product).status) && (prod as Product).status !== 'CP' && (prod as Product).type !== 'UP-EC' && !(prod as Product).pg_cancel_disable"
                        @change.prevent="onProdCancelCkBox($event)" />
                    </div>
                    <div class="col-auto">
                      <img :src="prod.product_thumbnail" style="width: 70px" />
                    </div>
                    <div class="col text-start">
                      <div class="mb-1">
                        <b :class="{ 'text-decoration-line-through': checkProdCancelLine((prod as Product).status) }">{{ (prod as Product).product_name }}</b>
                      </div>
                      <div class="" :class="{ 'text-decoration-line-through': checkProdCancelLine((prod as Product).status) }">옵션 : {{ (prod as Product).product_option_name ? (prod as Product).product_option_name : '없음' }}</div>
                      <div class="" :class="{ 'text-decoration-line-through': checkProdCancelLine((prod as Product).status) }" v-if="(prod as Product).type.includes('UP-EC') && (prod as Product).ecoupon">
                        ( PIN :
                        <a class="text-decoration-underline" href="" v-if="(prod as Product).ecoupon?.pin_code && getUserClassStr.includes('CM') && (prod as Product).ecoupon?.provider !== 'KT'" @click.prevent="showHistory((prod as Product).ecoupon?.raw_data)">
                          {{ (prod as Product).ecoupon?.pin_code }}
                        </a>
                        <span v-else-if="(prod as Product).ecoupon?.pin_code && (!getUserClassStr.includes('CM') || (prod as Product).ecoupon?.provider === 'KT')">
                          {{ (prod as Product).ecoupon?.pin_code }}
                        </span>
                        <span v-else>-</span>
                        )
                      </div>
                    </div>
                    <!-- 티켓상품 기간연장 -->
                    <div class="col-auto" v-if="getUserClassStr.includes('CM') && (prod as Product).type.startsWith('UP-OF') && !['CD', 'CP', 'AR'].includes((prod as Product).status)">
                      <button type="button" class="btn btn-sm btn-outline-info p-1" @click.prevent="openExtension(prod)">기간연장</button>
                    </div>
                    <div class="col-auto" v-if="getUserClassStr.includes('CM') && (prod as Product).type.startsWith('UP-EC') && ['CP'].includes((prod as Product).status)">
                      <button type="button" class="btn btn-sm btn-outline-primary p-1 me-1" v-if="prod.ecoupon?.provider === 'KT'" @click="resendEcoupon((prod as Product).id)">재발송</button>
                    </div>
                    <!-- E-쿠폰 상품 강제구매확정 -->
                    <div class="col-auto" v-if="getUserClassStr.includes('CM') && (prod as Product).type.startsWith('UP-EC') && !['CD', 'CP', 'AR'].includes((prod as Product).status)">
                      <button type="button" class="btn btn-sm btn-outline-info p-1 me-1" v-if="(prod as Product).ecoupon?.provider !== 'KT'" @click.prevent="openExtension(prod)">기간연장</button>
                      <button type="button" class="btn btn-sm btn-outline-danger p-1" v-if="(prod as Product).ecoupon?.provider !== 'KT'" @click.prevent="orderForceEnd(mOrderInfo.id, (prod as Product).id)">강제구매확정</button>
                    </div>
                  </div>
                </td>
                <td class="text-center p-2">
                  <div class="row align-items-center py-4" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)" style="height: 100px">
                    <div class="col text-end" :class="{ 'text-decoration-line-through': checkProdCancelLine((prod as Product).status) }">{{ (prod as Product).amount.toLocaleString() }}원</div>
                  </div>
                </td>
                <td class="text-center p-2">
                  <div class="row align-items-center py-4" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)" style="height: 100px">
                    <div class="col text-end text-primary" :class="{ 'text-decoration-line-through': checkProdCancelLine((prod as Product).status) }">{{ (prod as Product).discount ? (prod as Product).discount.toLocaleString() : '0' }}원</div>
                  </div>
                </td>
                <td class="text-center p-2">
                  <div class="row align-items-center py-4" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)" style="height: 100px">
                    <div class="col text-end text-danger" :class="{ 'text-decoration-line-through': checkProdCancelLine((prod as Product).status) }">
                      {{ (prod as Product).discount ? ((prod as Product).amount - (prod as Product).discount).toLocaleString() : (prod as Product).amount.toLocaleString() }}원
                    </div>
                  </div>
                </td>
                <td class="text-center p-2">
                  <div class="row align-items-center py-4" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)" style="height: 100px">
                    <div class="col" :class="{ 'text-decoration-line-through': checkProdCancelLine((prod as Product).status) }">{{ (prod as Product).ea }}</div>
                  </div>
                </td>
                <td class="text-end p-2" v-if="!(mShipGroupProds[id][0] as Product).type?.startsWith('UP')">
                  <input
                    type="checkbox"
                    :id="`chkb_ship_id_${id}`"
                    class="me-2"
                    name="cancel_ship_id"
                    :value="(mShipGroupProds[id][0] as Product).order_shipping"
                    v-model="mSelShipList"
                    v-if="showCancelPart && (mShipGroupProds[id][0] as Product).order_shipping?.cost > 0 && (mShipGroupProds[id][0] as Product).order_shipping?.status !== 'CD'" />
                  <span :class="{'text-decoration-line-through' : checkProdCancelLine((mShipGroupProds[id][0] as Product).order_shipping?.status) }">{{ (mShipGroupProds[id][0] as Product).order_shipping?.cost.toLocaleString() }}원</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 배송정보 (배송상품) -->
      <div class="order-release mb-4" v-if="!Object.keys(mShipGroupProds as object).includes('null')">
        <div class="h6">배송정보</div>
        <div class="table-responsive-md">
          <table class="table table-nowrap table-align-middle card-table border">
            <thead class="thead-light">
              <tr>
                <th class="text-center" style="width: 34%">상품</th>
                <th class="text-center">택배사</th>
                <th class="text-center">송장번호</th>
                <th class="text-center">배송비</th>
                <th class="text-center">배송지 주소</th>
                <th class="text-center">배송상태</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="id in Object.keys(mShipGroupProds as object)" :key="JSON.stringify(id)">
                <td class="text-start">
                  <div class="card-body p-0">
                    <div class="row align-items-center mb-2" v-for="prod in mShipGroupProds[id]" :key="JSON.stringify(prod)">
                      <div class="col-auto">
                        <img :src="prod.product_thumbnail" style="width: 70px" />
                      </div>
                      <div class="col text-start text-wrap">
                        <div class="mb-1">
                          <b :class="{'text-decoration-line-through' : checkProdCancelLine((prod as Product).status)}">{{ (prod as Product).product_name }}</b>
                        </div>
                        <div :class="{'text-decoration-line-through' : checkProdCancelLine((prod as Product).status)}">옵션 : {{ (prod as Product).product_option_name ? (prod as Product).product_option_name : '없음' }}</div>
                        <div :class="{'text-decoration-line-through' : checkProdCancelLine((prod as Product).status)}" style="font-size: 0.7rem">상품코드 : {{ (prod as Product).product_code }}</div>
                        <span class="text-danger" v-if="(prod as Product).status === 'CD'">결제취소됨</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="text-center">{{ (mShipGroupProds[id][0] as Product).order_shipping?.provider ? `${(mShipGroupProds[id][0] as Product).order_shipping.provider}` : '미등록' }}</td>
                <td class="text-center">
                  {{ (mShipGroupProds[id][0] as Product).order_shipping?.number ? `${(mShipGroupProds[id][0] as Product).order_shipping.number}` : '미등록' }}
                  <button
                    type="button"
                    class="btn btn-sm btn-info p-1 ms-1"
                    @click.prevent="modOrderShipping(id as number)"
                    v-if="(mShipGroupProds[id][0] as Product).order_shipping?.number && (mShipGroupProds[id][0] as Product).order_shipping?.status === 'DN' && !getUserClassStr.includes('MC')">
                    수정
                  </button>
                </td>
                <td class="text-end">{{ (mShipGroupProds[id][0] as Product).order_shipping?.cost.toLocaleString() }}원</td>
                <td class="text-center">
                  ({{ mOrderInfo.zipcode }}) {{ mOrderInfo.address }}, {{ mOrderInfo.address_detail }}
                  <br />
                  수령인 : {{ mOrderInfo.recipient_name ? mOrderInfo.recipient_name : mOrderInfo.user_name }} ({{ mOrderInfo.recipient_mobile ? mOrderInfo.recipient_mobile : mOrderInfo.user_mobile }}) {{ mOrderInfo.shipping_msg ? ' | ' : '' }}
                  {{ mOrderInfo?.shipping_msg }}
                </td>
                <td class="text-center">
                  <div v-if="(mShipGroupProds[id][0] as Product).order_shipping?.status === 'R'">
                    <div class="prod-wait-area" v-if="checkProductReady(id)">
                      <div class="col">
                        <span>{{ checkDefaultProdStatus(id) }}</span>
                      </div>
                      <div class="col" v-if="!userClass.includes('MC')">
                        <button type="button" class="btn btn-sm btn-info" @click.prevent="setProdDeliveryWait(id as number)" v-if="!getUserClassStr.includes('MC')">상품준비</button>
                      </div>
                    </div>
                    <div class="prod-delivery-area" v-if="checkDeliveryWaitReady(id)">
                      <div class="col">
                        <span>{{ checkDefaultProdStatus(id) }}</span>
                      </div>
                      <div class="col" v-if="!userClass.includes('MC')">
                        <button type="button" class="btn btn-sm btn-warning" @click.prevent="openDeliveryModal(id as number)" v-if="!getUserClassStr.includes('MC')">배송등록</button>
                      </div>
                    </div>
                    <div class="prod-cancel-area" v-if="mOrderInfo.status === 'CD'">
                      <div class="col">
                        <span>{{ convertOrderStatus((mShipGroupProds[id][0] as Product).status) }}</span>
                      </div>
                    </div>
                  </div>
                  <div v-else-if="(mShipGroupProds[id][0] as Product).order_shipping?.status === 'DN'">
                    <div class="col-auto">
                      {{ convertOrderStatus((mShipGroupProds[id][0] as Product).order_shipping?.status) }}
                    </div>
                    <div class="col-auto">
                      <button type="button" class="btn btn-sm btn-success" @click.prevent="openTrackingModal((mShipGroupProds[id][0] as Product).order_shipping)" v-if="!getUserClassStr.includes('MC')">배송추적</button>
                    </div>
                    <div class="col-auto mt-2" v-if="userClass.includes('CM')">
                      <button type="button" class="btn btn-sm btn-danger" @click.prevent="shippingForceEnd(id as number)" v-if="!getUserClassStr.includes('MC')">배송완료 강제변경</button>
                    </div>
                  </div>
                  <div v-else>
                    <div class="col-auto">
                      {{ convertOrderStatus((mShipGroupProds[id][0] as Product).order_shipping?.status) }}
                    </div>
                    <div class="col-auto">
                      <button type="button" class="btn btn-sm btn-success" @click.prevent="openTrackingModal((mShipGroupProds[id][0] as Product).order_shipping)" v-if="!getUserClassStr.includes('MC') && (mShipGroupProds[id][0] as Product).order_shipping?.status !== 'CD'">
                        배송추적
                      </button>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!-- 구매자정보 (미배송상품) -->
      <div class="order-release mb-4" v-else>
        <div class="h6">구매자정보</div>
        <div class="table-responsive-md">
          <table class="table table-nowrap table-align-middle card-table border">
            <thead class="thead-light">
              <tr>
                <th class="text-center">구매자명</th>
                <th class="text-center">구매자 연락처</th>
                <th class="text-center">구매자 이메일</th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-center">
                <td>{{ mOrderInfo.products[0].user_name }}</td>
                <td>{{ mOrderInfo.products[0].user_phone }}</td>
                <td>{{ mOrderInfo.products[0].user_email }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="order-cancel_return mb-4">
        <div class="h6">취소 내역</div>
        <div class="table-responsive-md">
          <table class="table table-nowrap table-align-middle card-table border">
            <thead class="thead-light">
              <tr>
                <th class="text-center">취소일시</th>
                <th class="text-center">취소승인번호</th>
                <th class="text-center">취소유형</th>
                <th class="text-center">취소금액</th>
                <th class="text-center">남은금액</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cancel in mOrderCancelList" :key="cancel">
                <td class="text-center">{{ cancel.reg_date.toString().replace('T', ' ').slice(0, -3) }}</td>
                <td class="text-center">{{ cancel.tno }}</td>
                <td class="text-center">{{ cancel.type === 'ALL' ? '전체취소' : cancel.type === 'PART' ? '부분취소' : '-' }}</td>
                <td class="text-end">{{ cancel.amount.toLocaleString() }}원</td>
                <td class="text-end">{{ cancel.remain ? cancel.remain.toLocaleString() : 0 }}원</td>
              </tr>
              <tr v-if="mOrderCancelList.length === 0">
                <td colspan="5" class="text-center">취소 내역이 없습니다.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <!--    <div class="card-footer"></div>-->
  </div>
  <div class="card mt-4" v-if="!getUserClassStr.includes('MC')">
    <!-- 주문 로그 영역-->
    <!--    <div class="card-body" v-if="getUserClassStr.includes('CM')">-->
    <div class="card-header py-3 h5 text-dark">[변경이력]</div>
    <div class="card-body">
      <div class="row mb-2 align-items-center justify-content-between">
        <div class="col-auto"></div>
        <div class="col-auto">
          <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
        </div>
      </div>
      <div class="table-responsive-md">
        <table class="table table-nowrap table-align-middle card-table table-borderless">
          <thead class="thead-light">
            <tr class="text-center">
              <th style="width: 15%">변경일</th>
              <th style="width: 10%">등록/수정</th>
              <!-- <th>항목</th>
              <th>변경전</th> -->
              <th>변경내용</th>
              <th style="width: 10%">변경자</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in orderLog.datas" :key="JSON.stringify(item)">
              <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
              <td>{{ item.action }}</td>
              <!-- <td>{{ convertLogItemCate(item.msg) }}</td>
              <td style="max-width: 8rem">
                <div v-html="convertLogItem(item.msg, 'before')"></div>
              </td> -->
              <td style="max-width: 8rem">
                <div v-html="convertLogItem(item.msg)"></div>
              </td>
              <td>{{ item.writer }}</td>
            </tr>
            <tr>
              <td colspan="6" class="text-center" v-if="orderLog.total === 0">표시할 항목이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-footer-area" v-if="orderLog.total > 0">
        <div class="row" v-if="total_page > 1">
          <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
        </div>
      </div>
    </div>
  </div>

  <!-- 배송정보(송장번호) 등록 Modal -->
  <Modal :id="'shippingRegModal'" :title="shippingRegInfo.mod ? '배송정보수정' : '배송정보등록'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">배송 기본정보</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <form class="mb-6">
              <div class="row col mb-4 align-items-center">
                <label class="col-md-3 col-form-label text-nowrap">택배사</label>
                <div class="col">
                  <!-- Select -->
                  <div class="tom-select-custom">
                    <select class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' @change="onChangeProvider" v-model="shippingRegInfo.provider.code">
                      <option value="" disabled>택배사선택</option>
                      <option v-for="l in logisticsList" :key="l.id" :value="l.value">{{ l.name }}</option>
                    </select>
                  </div>
                  <!-- End Select -->
                </div>
              </div>
              <div class="row col mb-4 align-items-center">
                <label class="col-md-3 col-form-label text-nowrap">송장번호</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" v-model="shippingRegInfo.code" placeholder="송장번호를 영문과 숫자로만 입력해주세요." oninput="this.value = this.value.replace(/[^a-zA-Z0-9]/gi,'')" />
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
      <button type="button" class="btn btn-primary" @click.prevent="shippingInfoReg" v-if="!getUserClassStr.includes('MC')">{{ shippingRegInfo.mod ? '배송정보 수정' : '배송정보 등록' }}</button>
    </template>
  </Modal>

  <!-- 기간연장 Modal -->
  <Modal :id="'extensionModal'" :title="'상품 사용기한연장'">
    <template #body>
      <div class="row">
        <div class="card">
          <div class="card-body">
            <div class="row mb-4">
              <label for="idLabel" class="col-md-4 col-lg-3 col-form-label">대상 상품정보</label>
              <div class="col-sm col-md col-lg">
                <div class="row align-items-center mb-1">
                  <div class="col-sm-auto col-md-auto col-lg-auto">상품명 : {{ selExtensionInfo.prod.product_name }}</div>
                </div>
                <div class="row align-items-center mb-1">
                  <div class="col-sm-auto col-md-auto col-lg-auto">상품옵션 : {{ selExtensionInfo.prod.product_option_name ? selExtensionInfo.prod.product_option_name : '없음' }}</div>
                </div>
                <div class="row align-items-center mb-1">
                  <div class="col-sm-auto col-md-auto col-lg-auto">상품사용기한 : {{ selExtensionInfo.prod.use_end_date?.slice(0, 10) }} 까지</div>
                </div>
              </div>
            </div>
            <!-- 기간연장 Datepicker -->
            <div class="row">
              <label for="idLabel" class="col-md-4 col-lg-3 col-form-label">연장 날짜선택</label>
              <div class="col-sm col-md col-lg">
                <div class="row align-items-center mb-2">
                  <div class="col-sm-auto col-md-auto col-lg-auto">
                    <!-- Form Group -->
                    <div class="form-group">
                      <div
                        id="endDatepicker"
                        class="js-flatpickr flatpickr-custom input-group"
                        data-hs-flatpickr-options='{
                    "appendTo": "#endDatepicker",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                        <div class="input-group-prepend input-group-text" data-bs-toggle>
                          <i class="bi-calendar-week"></i>
                        </div>
                        <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." v-model="selExtensionInfo.date" @change="eDateChange" />
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row align-items-center mb-2">
                  <div class="col-sm-auto col-md-auto col-lg-auto">
                    <div class="col-sm col-md col-lg">
                      <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setEndPeriod('week')">일주일</button>
                      <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setEndPeriod('month')">1개월</button>
                      <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setEndPeriod('3month')">3개월</button>
                      <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setEndPeriod('6month')">6개월</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="prodEndExtension" v-if="!getUserClassStr.includes('MC')">상품 기간연장</button>
    </template>
  </Modal>

  <!-- 관리자 환불 Modal -->
  <Modal :id="'adminRefundModal'" :title="'관리자 환불'">
    <template #body>
      <div class="row">
        <div class="card">
          <div class="card-body">
            <div class="row mb-2 align-items-center">
              <label class="col-auto col-form-label">
                <span style="font-weight: bold">[{{ mOrderInfo?.id }}]</span> 주문의 총 결제 금액은 <span class="text-danger" style="font-weight: bold">{{ mOrderInfo?.final_amount?.toLocaleString() }}</span> 원 입니다.
              </label>
            </div>
            <div class="row mb-2 align-items-center">
              <label class="col-md-3 col-form-label">환불 처리 금액</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" inputmode="decimal" class="form-control text-end" v-model="adminRefundAmount" @input="checkDigit($event)" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-danger" @click.prevent="executeAdminRefund" v-if="!getUserClassStr.includes('MC')">환불 처리</button>
    </template>
  </Modal>

  <!-- E쿠폰 사용내역  Modal -->
  <Modal :id="'historyModal'" :title="'E쿠폰 사용내역'" :xlarge="true" :centered="true">
    <template #body>
      <div class="card">
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-nowrap table-align-middle card-table">
              <thead class="thead-light">
                <tr class="text-center">
                  <th>쿠폰번호</th>
                  <th>기능구분</th>
                  <th>사용금액</th>
                  <th>잔액</th>
                  <th>처리일시</th>
                  <th>교환매장명</th>
                  <th>교환매장코드</th>
                  <th>거래코드</th>
                  <th>권종</th>
                  <th>고유값</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center" v-for="(item, i) in raw_data" :key="i">
                  <td>{{ JSON.parse(item)?.pin_code ? JSON.parse(item)?.pin_code : '-' }}</td>
                  <td>
                    {{ JSON.parse(item)?.send_status ? (JSON.parse(item).send_status === 'Y' ? '교환' : JSON.parse(item).send_status === 'C' ? '교환취소' : JSON.parse(item)?.send_status) : '-' }}
                  </td>
                  <td>{{ JSON.parse(item)?.use_price ? Number(JSON.parse(item)?.use_price).toLocaleString() + '원' : '-' }}</td>
                  <td>{{ JSON.parse(item)?.balance ? Number(JSON.parse(item)?.balance).toLocaleString() + '원' : '-' }}</td>
                  <td>{{ JSON.parse(item)?.ret_date ? dateConvert(JSON.parse(item)?.ret_date) : '-' }}</td>
                  <td>{{ JSON.parse(item)?.ret_msg ? JSON.parse(item)?.ret_msg : '-' }}</td>
                  <td>{{ JSON.parse(item)?.ret_code ? JSON.parse(item)?.ret_code : '-' }}</td>
                  <td>{{ JSON.parse(item)?.tr_id ? JSON.parse(item)?.tr_id : '-' }}</td>
                  <td>
                    {{ JSON.parse(item)?.goods_type ? (JSON.parse(item).goods_type === '04' ? '금액권' : JSON.parse(item).goods_type === '05' ? '제품권' : JSON.parse(item)?.goods_type) : '-' }}
                  </td>
                  <td>{{ JSON.parse(item)?.seq_idx ? JSON.parse(item)?.seq_idx : '-' }}</td>
                </tr>
                <tr>
                  <td colspan="12" class="text-center" v-if="raw_data.length === 0">사용내역이 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, readonly, ref } from 'vue';
import { apiResponseCheck, convertOrderStatus, dateTimeFormatConverter, showAlert, showConfirm, getUserClassStr, checkPermission, showLogConsole, showModal, hideModal, convertPgType } from '@/utils/common-utils';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import type { OrderDetail, Product, Log, PgCancel, PgInfoSub } from 'OrderDetailInfoModule';
import { useUserStore } from '@/stores/user';
import Modal from '@/components/comm/modal.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import type { ILogisticsList } from '@/components/user/type';
import { useCommonStore } from '@/stores/common';
import Pagination from '@/components/comm/Pagination.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';

const mOrderCancelList = ref([] as PgCancel[]);

// 부분취소 선택상품
const mSelProductList = ref({} as any);
const mSelShipList = ref([]);

const raw_data = ref([] as any);

const logisticsList = readonly<ILogisticsList[]>(useCommonStore().logisticsList);
const orderCancelPermission = computed(() => {
  if (useUserStore().user.admin === 'Y') {
    return true;
  } else {
    if (checkPermission('write:order_cancel')) {
      return true;
    }
  }
  return false;
});

const dateConvert = (date: string) => {
  const dateTimeStr = date;
  const year = dateTimeStr.slice(0, 4);
  const month = dateTimeStr.slice(4, 6);
  const day = dateTimeStr.slice(6, 8);
  const hour = dateTimeStr.slice(8, 10);
  const minute = dateTimeStr.slice(10, 12);
  const second = dateTimeStr.slice(12, 14);

  return `${year}.${month}.${day} ${hour}:${minute}:${second}`;
};

// 기간연장
const selExtensionInfo = reactive({
  date: '',
  prod: {} as Product,
});

// 관리자 환불 금액
const adminRefundAmount = ref(0);

const checkDigit = (e: any) => {
  if (!e.target.value) {
    e.target.value = 0;
    adminRefundAmount.value = 0;
    return;
  }

  if (!araCheck(e.target.value)) {
    e.target.value = (e.target.value as string).slice(0, e.target.value.length - 1);
    adminRefundAmount.value = e.target.value;
  } else {
    if (e.target.value.startsWith('00') || /0\d$/.test(e.target.value)) {
      e.target.value = parseFloat(e.target.value as string);
    }
  }
};

const araCheck = (value: any): boolean => {
  if (value > mOrderInfo.value.final_amount) {
    showAlert('환불 처리 금액은 총 결제금액 보다 클 수 없습니다.', 'warning', () => {
      return false;
    });
  }

  if (value <= 0) {
    showAlert('환불 처리 금액은 0이거나 음수일 수 없습니다.', 'warning', () => {
      return false;
    });
  }

  return true;
};

const checkOpStatus = () => {};

const isAllOpStatusCP = computed(() => {
  const result = !(mOrderInfo.value.products?.filter(item => item.status !== 'CP')?.length > 0);
  return result;
});

const checkProdCancelLine = (status: string = ''): boolean => {
  return ['CD', 'EXC', 'RFC', 'AR'].includes(status);
};

//TODO: 테스트용 추후 삭제
const showForce = reactive({
  show: false,
  count: 0,
});
const checkShowForce = () => {
  showForce.count += 1;
  if (showForce.count > 4) {
    showForce.show = true;
  }
};

const router = useRouter();
const route = useRoute();
const mOrderId = ref(0);
const mOrderInfo = ref({} as OrderDetail);
const mMyProducts = ref([] as Product[]);
const mShipGroupProds = ref({} as any);

const orderLog = ref({} as Log);
const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(orderLog.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getOrderLog();
};

const pageChange = (page: number) => {
  page_no.value = page;
  getOrderLog();
  window.scrollTo({ top: 100, left: 0 });
};

const shippingRegInfo = reactive({
  id: 0,
  mod: false,
  provider: {
    name: '',
    code: '',
  },
  code: '',
});

const showCancelPart = ref(false);
const toggleCancelPart = (flag: boolean) => {
  showCancelPart.value = flag;
  if (!flag) {
    mSelShipList.value = [];
    mSelProductList.value = [];
  }
};

// const checkDeliveryCode = (e: any) => {
//   const reg = /[^a-zA-Z0-9]/gi;
//   if (reg.test(e.target.value)) {
//     showAlert('영문자와 숫자만 입력할 수 있습니다.', 'warning', () => {
//       e.target.focus();
//     });
//   }
// };

const onChangeProvider = () => {
  const selected = logisticsList.filter(item => item.value === shippingRegInfo.provider.code);
  shippingRegInfo.provider.name = selected[0].name;
};
const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

const props = defineProps({
  orderId: {
    type: Number,
    required: true,
  },
});

const resendEcoupon = (order_product_id: number) => {
  showConfirm('재발송 하시겠습니까?', () => {
    apis.ecoupon.resend_ecoupon(order_product_id).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('재발송되었습니다.', 'success');
        },
        undefined,
        true,
      );
    });
  });
};

const getOrderDetail = () => {
  apis.order.get_order_detail(mOrderId.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mOrderInfo.value = res;
      orderCancelList();
      checkProducts();
    });
  });
};

const checkProducts = () => {
  mMyProducts.value = [];
  mShipGroupProds.value = {} as any;
  if (userClass.value.includes('PA')) {
    mOrderInfo.value.products.map(item => {
      if (item.member_id === useUserStore().user.id) {
        mMyProducts.value.push(item);
      }
    });
  } else {
    mMyProducts.value = mOrderInfo.value.products;
  }

  for (const prod of mMyProducts.value) {
    if (Object.keys(mShipGroupProds.value).includes(`${prod.order_shipping_id}`)) {
      mShipGroupProds.value[`${prod.order_shipping_id}`].push(prod);
    } else {
      mShipGroupProds.value[`${prod.order_shipping_id}`] = [prod];
    }
    if (!Object.keys(mSelProductList.value).includes(`${prod.order_shipping_id}`)) {
      mSelProductList.value[`${prod.order_shipping_id}`] = [];
    }
  }
};
const openDeliveryModal = (id: number) => {
  shippingRegInfo.id = id;
  shippingRegInfo.mod = false;

  showModal('shippingRegModal');
};

const checkProductReady = (id: string): boolean => {
  for (const prod of mShipGroupProds.value[id]) {
    if ((prod as Product).status === 'PD' || (prod as Product).status === 'DD') {
      return true;
    }
  }
  return false;
};

const checkDeliveryWaitReady = (id: string): boolean => {
  for (const prod of mShipGroupProds.value[id]) {
    if ((prod as Product).status === 'DW') {
      return true;
    }
  }
  return false;
};

const checkDefaultProdStatus = (id: string): string => {
  let idx = 0;
  for (const i in mShipGroupProds.value[id]) {
    if (mShipGroupProds.value[id][i].status !== 'CD') {
      idx = parseInt(i);
      break;
    }
  }
  return convertOrderStatus((mShipGroupProds.value[id][idx] as Product).status);
};

const setProdDeliveryWait = (id: number) => {
  const order_prod_ids = [] as number[];

  for (const prod of mShipGroupProds.value[id]) {
    if ((prod as Product).status !== 'CD') order_prod_ids.push((prod as Product).id);
  }

  showConfirm('상품준비 상태로 변경하시겠습니까?', () => {
    apis.order.delivery_wait_update_select('DW', order_prod_ids).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품준비중 상태로 변경되었습니다.', 'success', () => {
          getOrderDetail();
          if (!userClass.value.includes('MC')) {
            getOrderLog();
          }
        });
      });
    });
  });
};

const modOrderShipping = (id: number) => {
  shippingRegInfo.id = id;
  shippingRegInfo.mod = true;

  shippingRegInfo.code = mShipGroupProds.value[id][0].order_shipping.number;
  shippingRegInfo.provider.name = mShipGroupProds.value[id][0].order_shipping.provider;
  shippingRegInfo.provider.code = mShipGroupProds.value[id][0].order_shipping.provider_code;
  showModal('shippingRegModal');
};

const shippingInfoReg = () => {
  if (!shippingRegInfo.provider.code) {
    showAlert('택배사를 선택해주세요', 'warning');
    return;
  }

  if (!shippingRegInfo.code) {
    showAlert('송장번호를 입력해주세요.', 'warning');
    return;
  }

  const prodNameList: string[] = [];

  for (const prod of mShipGroupProds.value[shippingRegInfo.id]) {
    prodNameList.push((prod as Product).product_name);
  }
  const msg = shippingRegInfo.mod ? '상품의 배송정보를 수정하시겠습니까?' : '상품의 배송정보를 등록하시겠습니까?';
  showConfirm(`[${prodNameList.join(', ')}] ${msg}`, () => {
    apis.order.order_shipping_reg(shippingRegInfo.id, { delivery_code: shippingRegInfo.code, delivery_provider: shippingRegInfo.provider.name, delivery_provider_code: shippingRegInfo.provider.code }).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert(shippingRegInfo.mod ? '배송정보가 수정되었습니다.' : '배송정보가 등록되었습니다.', 'success', () => {
            hideModal('shippingRegModal');
            getOrderDetail();
            if (!userClass.value.includes('MC')) {
              getOrderLog();
            }
          });
        },
        (num?: number) => {
          if (num === 403) {
            hideModal('shippingRegModal');
          }
        },
      );
    });
  });
};

// 배송상품 강제배송완료 처리
const shippingForceEnd = (id: number) => {
  showConfirm('[주의!!] 배송상품을 강제로 배송완료 하시겠습니까?', () => {
    apis.order.order_shipping_force_end(id).then(res => {
      apiResponseCheck(res, () => {
        showAlert('배송완료 상태로 강제 변경 되었습니다.', 'success', () => {
          getOrderDetail();
          if (!userClass.value.includes('MC')) {
            getOrderLog();
          }
        });
      });
    });
  });
};

// 주문상품 강제 구매확정 처리
const orderForceEnd = (oid: string, opid: number) => {
  showConfirm('<span class="text-danger">[주의!!]</span> 해당 주문상품을 강제로 <span class="text-danger"><strong>구매확정</strong></span> 처리하시겠습니까?', () => {
    apis.order.order_force_end(oid, opid).then(res => {
      apiResponseCheck(res, () => {
        showAlert('강제 구매확정 처리되었습니다.', 'success', () => {
          getOrderDetail();
          if (!userClass.value.includes('MC')) {
            getOrderLog();
          }
        });
      });
    });
  });
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

const setModalListener = () => {
  //@ts-ignore
  document.getElementById('shippingRegModal').addEventListener('show.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('shippingRegModal').addEventListener('hide.bs.modal', function (event) {
    shippingRegInfo.id = 0;
    shippingRegInfo.provider.code = '';
    shippingRegInfo.provider.name = '';
    shippingRegInfo.code = '';
  });
};

const checkStatus = (logItem: string = '') => ['RFN', 'RFC', 'EXN', 'EXC'].some(code => logItem.includes(code));

const convertLogItem = (data: string): string => {
  let logItem = [];
  const json = JSON.parse(data);
  logItem.push(json.data);

  if (logItem.toString().includes('\n')) {
    return logItem[0].split('\n')[1];
  }

  if (checkStatus(logItem.toString())) {
    return logItem[0].split('/')[0].trim() + ' / ' + convertOrderStatus(logItem[0].split('/')[1].trim());
  }

  if (logItem.toString().includes('->')) {
    let convertString = '';
    logItem = logItem[0].split('->');

    for (let i in logItem) {
      logItem[i] = convertOrderStatus(logItem[i].trim(), true);
      convertString += logItem[i];
      if (i == '0') {
        convertString += ' -> ';
      }
    }
    return convertString.toString();
  }
  return logItem.toString();
};

const getOrderLog = () => {
  apis.order.getOrderLog(mOrderId.value.toString(), offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      orderLog.value.datas = res.datas;
      orderLog.value.total = res.total;
    });
  });
};

const allProdCancel = () => {
  if (mOrderInfo.value.products?.filter(item => !['PD', 'DW'].includes(item.status)).length > 0 || mOrderInfo.value.products?.filter(item => ['UP-EC'].includes(item.type)).length > 0) {
    showAlert('<span class="text-danger">취소할 수 없는 주문 상품</span>이 포함되어있어<br />전체취소 기능을 사용할 수 없습니다.', 'error');
  } else {
    showConfirm('해당 주문을 전체 취소하시겠습니까?<br/><span class="text-danger">* 주의를 요하는 작업입니다.</span>', () => {
      apis.order.order_all_cancel(mOrderId.value.toString()).then(res => {
        apiResponseCheck(res, () => {
          showAlert('해당 주문이 전체취소 되었습니다.', 'success', () => {
            getOrderDetail();
            if (!userClass.value.includes('MC')) {
              getOrderLog();
            }
          });
        });
      });
    });
  }
};

const onProdCancelCkBox = (event: any) => {
  const shipping_id = (event.target.id as string).replace('chkb_prod_id_', '');
  if (event.target.checked) {
    if (mShipGroupProds.value[shipping_id].length === mSelProductList.value[shipping_id].length) {
      const o_ship = (mShipGroupProds.value[shipping_id][0] as Product)?.order_shipping;
      if (o_ship?.status !== 'CD' && o_ship?.cost > 0) {
        //@ts-ignore
        mSelShipList.value.push((mShipGroupProds.value[shipping_id][0] as Product)?.order_shipping);
      }
    }
  } else {
    if (mShipGroupProds.value[shipping_id].length !== mSelProductList.value[shipping_id].length) {
      let idx: number = -1;
      for (const i in mSelShipList.value) {
        if ((mSelShipList.value[i] as OrderShipping).id === parseInt(shipping_id)) {
          idx = parseInt(i);
          break;
        }
      }
      if (idx >= 0) {
        mSelShipList.value.splice(idx, 1);
      }
    }
  }
};

const orderCancelPart = () => {
  const order_product_ids = [] as string[];
  const order_shipping_ids = [] as string[];
  let cancel_amount: number = 0;

  for (const id of Object.keys(mSelProductList.value)) {
    for (const item of mSelProductList.value[id]) {
      order_product_ids.push((item as Product).id.toString());
      cancel_amount += (item as Product).discount ? (item as Product).amount - (item as Product).discount : (item as Product).amount;
    }
  }

  mSelShipList.value.map(item => {
    if (!checkProdCancelLine((item as OrderShipping).status)) {
      order_shipping_ids.push((item as OrderShipping).id.toString());
      cancel_amount += (item as OrderShipping).cost;
    }
  });

  if (order_shipping_ids.length === 0 && order_product_ids.length === 0) {
    showAlert('개별 취소할 주문의 상품이나 배송비를 선택해주세요.', 'warning');
    return;
  }

  const data = { cancel_amount: cancel_amount, order_product_ids: order_product_ids, order_shipping_ids: order_shipping_ids };
  showConfirm('주문개별취소를 진행하시겠습니까?', () => {
    apis.order.order_part_cancel(mOrderId.value.toString(), data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('주문 개별취소가 완료되었습니다.', 'success', () => {
          getOrderDetail();
          if (userClass.value.includes('CM')) {
            getOrderLog();
          }
          toggleCancelPart(false);
        });
      });
    });
  });
};

const orderCancelList = () => {
  apis.order.order_cancel_list(mOrderId.value.toString()).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mOrderCancelList.value = res;
    });
  });
};

const showPgSubInfo = (sub: PgInfoSub[]) => {
  const subInfoArr = [] as String[];
  sub.map(item => {
    subInfoArr.push(item.kind);
  });

  return subInfoArr.toString();
};

const openAdminRefund = () => {
  adminRefundAmount.value = 0;
  // @ts-ignore
  window.$('#adminRefundModal').modal('toggle');
};

const showHistory = (data: string) => {
  raw_data.value = data.split('\n').slice(1);
  showModal('historyModal');
};

const executeAdminRefund = () => {
  if (!adminRefundAmount.value || adminRefundAmount.value <= 0) {
    showAlert('환불 처리 금액을 확인해주세요.', 'warning');
    return;
  }

  if (adminRefundAmount.value > mOrderInfo.value.final_amount) {
    showAlert('환불 처리 금액은 총 결제금액보다 클 수 없습니다.', 'warning');
    return;
  }

  showConfirm('해당 주문을 관리자 환불 처리 하시겠습니까?<br/><span class="text-danger">* 주의를 요하는 작업입니다.<br>* 해당 주문의 모든 주문상품이 [관리자환불] 상태로 변경됩니다.</span>', () => {
    apis.order.order_admin_refund(mOrderInfo.value.id, adminRefundAmount.value).then(res => {
      apiResponseCheck(res, () => {
        showAlert('관리자 환불 처리가 완료되었습니다.', 'success', () => {
          //@ts-ignore
          window.$('#adminRefundModal').modal('toggle');
          window.location.reload();
        });
      });
    });
  });
};

const openExtension = (prod: Product) => {
  selExtensionInfo.prod = prod;
  selExtensionInfo.date = '';

  setEndPeriod('');

  //@ts-ignore
  window.$('#extensionModal').modal('toggle');
};

const prodEndExtension = () => {
  const current = selExtensionInfo.prod.use_end_date?.slice(0, 10);
  const extension = selExtensionInfo.date;

  if (current === extension) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  showConfirm(`[${selExtensionInfo.prod.product_name}] 상품의 사용기한을 연장하시겠습니까?`, () => {
    apis.order.prod_use_date_extension(selExtensionInfo.prod.order_id, selExtensionInfo.prod.id, selExtensionInfo.date).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품의 사용기한이 연장되었습니다.', 'success', () => {
          //@ts-ignore
          window.$('#extensionModal').modal('toggle');
          //@ts-ignore
          window.location.reload();
        });
      });
    });
  });
};

// 기간연장 관련
const eDateChange = () => {
  const current = selExtensionInfo.prod.use_end_date?.slice(0, 10);
  const extension = new Date(selExtensionInfo.prod.use_end_date?.slice(0, 10));
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (current === eDate || !current || !eDate) {
    return;
  } else {
    if (current > eDate) {
      showAlert('연장 날짜는 상품 사용기한보다 이전 날짜일 수 없습니다.', 'warning');
      // @ts-ignore
      efp.setDate(new Date(extension), true, 'Y-m-d');
    }
  }
};
const setEndPeriod = (period: string) => {
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});
  const extension = new Date(selExtensionInfo.prod.use_end_date?.slice(0, 10));
  switch (period) {
    case 'week':
      // @ts-ignore
      efp.setDate(new Date(extension.getTime() + 1000 * 60 * 60 * 24 * 7), true, 'Y-m-d');
      break;
    case 'month':
      // @ts-ignore
      efp.setDate(new Date(extension.getTime() + 1000 * 60 * 60 * 24 * 30), true, 'Y-m-d');
      break;
    case '3month':
      // @ts-ignore
      efp.setDate(new Date(extension.getTime() + 1000 * 60 * 60 * 24 * 90), true, 'Y-m-d');
      break;
    case '6month':
      // @ts-ignore
      efp.setDate(new Date(extension.getTime() + 1000 * 60 * 60 * 24 * 180), true, 'Y-m-d');
      break;
    default:
      // @ts-ignore
      efp.setDate(new Date(extension.getTime()), true, 'Y-m-d');
      break;
  }
};

onMounted(() => {
  const orderId = history.state.orderId;
  limit.value = useCommonStore().getLimit;

  if (!orderId) {
    showAlert('비정상적인 접근입니다.', 'error', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
  } else {
    mOrderId.value = orderId;
    getOrderDetail();
    setModalListener();

    if (!userClass.value.includes('MC')) {
      getOrderLog();
    }
  }
});
</script>

<style scoped></style>
