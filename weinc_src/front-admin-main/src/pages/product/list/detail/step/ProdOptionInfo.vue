<template>
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">가격 및 옵션정보</h4>
          <small>
            상품의 가격 및 옵션을 설정할 수 있습니다.
            <br />
            옵션을 사용하지 않을 경우 <strong>'사용안함'</strong>을 선택해 기본정보를 저장해야합니다.
          </small>
        </div>
        <div class="nav-item ms-auto">
          <button type="button" class="btn btn-warning" @click.prevent="optionSave">저장</button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <CommFormLine :title="`옵션 사용 여부`" slot-parent="form-control border-0">
        <div class="form-check form-check-inline">
          <input value="Y" v-model="use" id="use" type="radio" class="form-check-input" name="use" />
          <label class="form-check-label" for="use">사용</label>
        </div>
        <button type="button" class="btn btn-sm btn-info" v-if="use === 'Y'" @click.prevent="showModal('OptionCreateModal')">신규생성</button>

        <div class="form-check form-check-inline ms-5">
          <input value="N" v-model="use" id="not_use" type="radio" class="form-check-input" checked name="not_use" />
          <label class="form-check-label" for="not_use">사용안함</label>
        </div>
      </CommFormLine>
      <div v-if="use === 'N'" class="table-responsive">
        <table class="table table-nowrap table-align-middle border card-table table-vertical-border-striped table-bordered mt-3">
          <thead class="table-light">
            <tr class="text-center">
              <th v-if="props.prodType.startsWith('DP')" rowspan="2">무게(kg)</th>
              <th rowspan="2">정상가</th>
              <th rowspan="2">공급가</th>
              <th rowspan="2">판매가</th>
              <th rowspan="2">재고</th>
              <th rowspan="2">안전재고</th>
              <th colspan="2" style="width: 160px">일일재고</th>
            </tr>
            <tr class="text-center">
              <th>누적수량재고사용</th>
              <th>일처리가능수량<br />(1일기준)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td v-if="props.prodType.startsWith('DP')">
                <input @input="checkMaxValue($event)" v-model="data.weight" type="number" class="form-control form-control-sm text-end" @change="checkInputNum('weight', $event, -1)" @focus="checkInputFocus($event)" />
              </td>
              <td>
                <div class="input-group" style="width: 130px">
                  <input
                    v-model.lazy.number="data.origin_price"
                    oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                    type="number"
                    class="form-control form-control-sm text-end"
                    @change="checkInputNum('origin', $event, -1)"
                    @focus="checkInputFocus($event)" />
                  <span class="input-group-text">원</span>
                </div>
              </td>
              <td>
                <div class="input-group" style="width: 130px">
                  <input
                    v-model.lazy.number="data.supply_price"
                    oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                    type="number"
                    class="form-control form-control-sm text-end"
                    @change="checkInputNum('supply', $event, -1)"
                    @focus="checkInputFocus($event)" />
                  <span class="input-group-text">원</span>
                </div>
              </td>
              <td>
                <div class="input-group" style="width: 130px">
                  <input
                    v-model.lazy.number="data.selling_price"
                    oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                    type="number"
                    class="form-control form-control-sm text-end"
                    @change="checkInputNum('selling', $event, -1)"
                    @focus="checkInputFocus($event)" />
                  <span class="input-group-text">원</span>
                </div>
              </td>
              <td>
                <div class="input-group" style="width: 130px">
                  <input
                    v-model.lazy="data.count"
                    oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                    type="number"
                    class="form-control form-control-sm text-end"
                    @change="checkInputNum('count', $event, -1)"
                    @focus="checkInputFocus($event)" />
                </div>
              </td>
              <td>
                <div class="input-group" style="width: 130px">
                  <input
                    v-model.lazy="data.safe_count"
                    oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                    type="number"
                    class="form-control form-control-sm text-end"
                    @change="checkInputNum('safe_count', $event, -1)"
                    @focus="checkInputFocus($event)" />
                </div>
              </td>
              <td>
                <!-- Select -->
                <div class="tom-select-custom" style="width: 120px">
                  <select v-model="data.use_acc_qty" class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                    <option value="Y">사용</option>
                    <option value="N">사용안함</option>
                  </select>
                </div>
              </td>
              <td>
                <div class="input-group" style="width: 120px">
                  <input
                    v-model.lazy="data.day_able_count"
                    oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                    type="number"
                    class="form-control form-control-sm text-end"
                    @change="checkInputNum('day_able_count', $event, -1)"
                    @focus="checkInputFocus($event)" />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-responsive" style="width: 100%; max-height: 400px">
        <table class="table table-sm table-nowrap text-nowrap table-align-middle border card-table table-vertical-border-striped table-bordered" style="overflow: auto" v-bind:class="{ wide: optionTitleList.length > 0 }">
          <thead class="table-light">
            <tr class="text-center">
              <th style="width: 1%" rowspan="2">대표옵션</th>
              <th v-for="title in optionTitleList" :key="JSON.stringify(title)" rowspan="2">{{ title }}(옵션코드/옵션값)</th>
              <th rowspan="2" style="width: 80px">무게(kg)</th>
              <th rowspan="2" style="width: 80px">정상가</th>
              <th rowspan="2" style="width: 80px">공급가</th>
              <th rowspan="2" style="width: 80px">판매가</th>
              <th rowspan="2" style="width: 80px">재고</th>
              <th rowspan="2" style="width: 80px">안전재고</th>
              <th colspan="2">일일재고</th>
              <th rowspan="2" style="width: 80px">옵션노출</th>
            </tr>
            <tr class="text-center">
              <th style="width: 80px">누적수량재고사용</th>
              <th style="width: 80px">일처리가능수량<br />(1일기준)</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-if="optionList.length > 0">
              <td :colspan="optionTitleList.length + 1" class="text-end">값 일괄 적용 >></td>
              <td>
                <div class="col">
                  <div class="input-group">
                    <input type="number" class="form-control text-end" v-model.lazy="allInputValue.weight" oninput="this.value.length > 3 ? this.value = this.value.slice(0,3) : this.value = this.value" />
                    <button type="button" class="btn btn-sm btn-warning p-1" @click.prevent="setAllInputValue('weight')">적용</button>
                  </div>
                </div>
              </td>
              <td>
                <div class="col">
                  <div class="input-group">
                    <input type="number" class="form-control text-end" v-model.number.lazy="allInputValue.origin" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" @change="max100mill($event)" />
                    <span class="input-group-text">원</span>
                    <button type="button" class="btn btn-sm btn-warning p-1" @click.prevent="setAllInputValue('origin')">적용</button>
                  </div>
                </div>
              </td>
              <td>
                <div class="col">
                  <div class="input-group">
                    <input type="number" class="form-control text-end" v-model.number.lazy="allInputValue.supply" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" @change="max100mill($event)" />
                    <span class="input-group-text">원</span>
                    <button type="button" class="btn btn-sm btn-warning p-1" @click.prevent="setAllInputValue('supply')">적용</button>
                  </div>
                </div>
              </td>
              <td>
                <div class="col">
                  <div class="input-group">
                    <input type="number" class="form-control text-end" v-model.number.lazy="allInputValue.selling" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" @change="max100mill($event)" />
                    <span class="input-group-text">원</span>
                    <button type="button" class="btn btn-sm btn-warning p-1" @click.prevent="setAllInputValue('selling')">적용</button>
                  </div>
                </div>
              </td>
              <td>
                <div class="col">
                  <div class="input-group">
                    <input type="number" class="form-control text-end" v-model.lazy="allInputValue.count" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" />
                    <button type="button" class="btn btn-sm btn-warning p-1" @click.prevent="setAllInputValue('count')">적용</button>
                  </div>
                </div>
              </td>
              <td>
                <div class="col">
                  <div class="input-group">
                    <input type="number" class="form-control text-end" v-model.lazy="allInputValue.safe_count" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" />
                    <button type="button" class="btn btn-sm btn-warning p-1" @click.prevent="setAllInputValue('safe_count')">적용</button>
                  </div>
                </div>
              </td>
              <td class="p-1 text-center">
                <div class="row align-items-center">
                  <div class="col-auto ms-1">
                    <!-- Select -->
                    <div class="tom-select-custom">
                      <select class="form-select" v-model="allInputValue.use_acc_qty" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                        <option value="Y">사용</option>
                        <option value="N">사용안함</option>
                      </select>
                    </div>
                  </div>
                  <div class="col-auto m-0 p-0">
                    <button type="button" class="btn btn-sm btn-warning p-1 m-0" @click.prevent="setAllInputValue('use_acc_qty')">적용</button>
                  </div>
                </div>
              </td>
              <td>
                <div class="col">
                  <div class="input-group">
                    <input type="number" class="form-control text-end" v-model.lazy="allInputValue.day_able_count" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" />
                    <button type="button" class="btn btn-sm btn-warning p-1" @click.prevent="setAllInputValue('day_able_count')">적용</button>
                  </div>
                </div>
              </td>
              <td class="p-1 text-center">
                <div class="row align-items-center">
                  <div class="col-auto ms-1">
                    <!-- Select -->
                    <div class="tom-select-custom">
                      <select class="form-select" v-model="allInputValue.view" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                        <option value="Y">노출</option>
                        <option value="N">비노출</option>
                      </select>
                    </div>
                  </div>
                  <div class="col-auto m-0 p-0">
                    <button type="button" class="btn btn-sm btn-warning p-1 m-0" @click.prevent="setAllInputValue('view')">적용</button>
                  </div>
                </div>
              </td>
            </tr>
            <tr v-for="(op, i) in optionList" :key="(op, i)" :id="`op_row_${i}`">
              <td class="text-center">
                <input type="radio" id="radio_defaultOP" class="form-check-input" name="search_type" :value="i" v-model="defaultOpIdx" />
              </td>
              <td v-for="(o, j) in optionTitleList" :key="JSON.stringify(o)">
                <div class="row align-items-center" style="min-width: 300px">
                  <div class="col">
                    <input type="text" class="form-control" placeholder="옵션코드" v-if="j === 0" v-model.lazy="op.option_code_1" @change="changeInput(i, $event)" oninput="this.value = this.value.replace(/[^a-zA-Z0-9]/gi,'')" />
                    <input type="text" class="form-control" placeholder="옵션코드" v-else-if="j === 1" v-model.lazy="op.option_code_2" @change="changeInput(i, $event)" oninput="this.value = this.value.replace(/[^a-zA-Z0-9]/gi,'')" />
                    <input type="text" class="form-control" placeholder="옵션코드" v-else-if="j === 2" v-model.lazy="op.option_code_3" @change="changeInput(i, $event)" oninput="this.value = this.value.replace(/[^a-zA-Z0-9]/gi,'')" />
                    <input type="text" class="form-control" placeholder="옵션코드" v-else-if="j === 3" v-model.lazy="op.option_code_4" @change="changeInput(i, $event)" oninput="this.value = this.value.replace(/[^a-zA-Z0-9]/gi,'')" />
                    <input type="text" class="form-control" placeholder="옵션코드" v-else v-model.lazy="op.option_code_5" @change="changeInput(i, $event)" oninput="this.value = this.value.replace(/[^a-zA-Z0-9]/gi,'')" />
                  </div>
                  <div class="col">
                    <input type="text" class="form-control" placeholder="옵션값" v-if="j === 0" v-model="op.option_1" @change="changeInput(i, $event)" />
                    <input type="text" class="form-control" placeholder="옵션값" v-else-if="j === 1" v-model="op.option_2" @change="changeInput(i, $event)" />
                    <input type="text" class="form-control" placeholder="옵션값" v-else-if="j === 2" v-model="op.option_3" @change="changeInput(i, $event)" />
                    <input type="text" class="form-control" placeholder="옵션값" v-else-if="j === 3" v-model="op.option_4" @change="changeInput(i, $event)" />
                    <input type="text" class="form-control" placeholder="옵션값" v-else v-model="op.option_5" @change="changeInput(i, $event)" />
                  </div>
                </div>
              </td>
              <td>
                <div class="col" style="width: 120px">
                  <input type="number" class="form-control text-end" v-model.number.lazy="op.weight" oninput="this.value.length > 3 ? this.value = this.value.slice(0,3) : this.value = this.value" @change="checkInputNum('weight', $event, i)" @focus="checkInputFocus($event)" />
                </div>
              </td>
              <td>
                <div class="col" style="width: 140px">
                  <div class="input-group">
                    <input
                      type="number"
                      class="form-control text-end"
                      v-model.number.lazy="op.origin_price"
                      oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                      @change="checkInputNum('origin', $event, i)"
                      @focus="checkInputFocus($event)" />
                    <span class="input-group-text">원</span>
                  </div>
                </div>
              </td>
              <td>
                <div class="col" style="width: 140px">
                  <div class="input-group">
                    <input
                      type="number"
                      class="form-control text-end"
                      v-model.number.lazy="op.supply_price"
                      oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                      @change="checkInputNum('supply', $event, i)"
                      @focus="checkInputFocus($event)" />
                    <span class="input-group-text">원</span>
                  </div>
                </div>
              </td>
              <td>
                <div class="col" style="width: 140px">
                  <div class="input-group">
                    <input
                      type="number"
                      class="form-control text-end text-danger"
                      v-model.lazy="op.selling_price"
                      oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                      @change="checkInputNum('selling', $event, i)"
                      @focus="checkInputFocus($event)" />
                    <span class="input-group-text">원</span>
                  </div>
                </div>
              </td>
              <td>
                <div class="col" style="width: 120px">
                  <div class="input-group">
                    <input type="number" class="form-control text-end" v-model.lazy="op.inventory.count" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" @change="checkInputNum('count', $event, i)" @focus="checkInputFocus($event)" />
                  </div>
                </div>
              </td>
              <td>
                <div class="col" style="width: 120px">
                  <div class="input-group">
                    <input
                      type="number"
                      class="form-control text-end"
                      v-model.lazy="op.inventory.safe_count"
                      oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                      @change="checkInputNum('safe_count', $event, i)"
                      @focus="checkInputFocus($event)" />
                  </div>
                </div>
              </td>
              <td>
                <!-- Select -->
                <div class="tom-select-custom" style="width: 120px">
                  <select v-model="op.inventory.use_acc_qty" class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' @change="changeInput(i, $event)">
                    <option value="Y">사용</option>
                    <option value="N">사용안함</option>
                  </select>
                </div>
              </td>
              <td>
                <div class="input-group" style="width: 120px">
                  <input
                    v-model.lazy="op.inventory.day_able_count"
                    oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value"
                    type="number"
                    class="form-control form-control-sm text-end"
                    @change="checkInputNum('day_able_count', $event, i)"
                    @focus="checkInputFocus($event)" />
                </div>
              </td>
              <td>
                <div class="col" style="width: 110px">
                  <!-- Select -->
                  <div class="tom-select-custom">
                    <select class="form-select" v-model="op.view_yn" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' @change="changeInput(i, $event)">
                      <option value="Y">노출</option>
                      <option value="N">비노출</option>
                    </select>
                  </div>
                </div>
              </td>
            </tr>
            <tr v-if="optionList.length === 0">
              <td colspan="8" class="text-center">생성된 옵션이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <OptionUseModal @setProdProp="setProdProp" :has-origin="hasOrigin" />
</template>

<script lang="ts" setup>
import CommFormLine from '@/components/comm/CommFormLine.vue';
import { computed, onMounted, reactive, ref, watch } from 'vue';
import OptionUseModal from '@/components/modals/product/OptionUseModal.vue';
import apis from '@/apis';
import type { IProductOption } from '@/apis/api.product';
import type { Opt, OptionListInfo } from 'ProductListModule';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';

const checkMaxValue = (event: any) => {
  if (event.target.value > 999.99) {
    showAlert('최대 3자리 정수 까지만 입력할 수 있습니다.', 'warning', () => {
      event.target.focus();
      data.weight = 0;
    });
  } else if (event.target.value < 0) {
    showAlert('음수는 입력할 수 없습니다.', 'warning', () => {
      event.target.focus();
      data.weight = 0;
    });
  }
};

const props = defineProps<{ productId: number; prodType: string; status: string | null | undefined }>();
const emits = defineEmits(['saveFinish', 'changedProdInfo']);
const data = reactive<IProductOption>({ id: 0, code: '', view_yn: 'Y', weight: 0, supply_price: 0, origin_price: 0, selling_price: 0, count: 0, safe_count: 0, default_yn: 'Y', day_able_count: 0, use_acc_qty: '', property_detail_ids: [] });

const use = ref('');

const newCreateOption = ref(false);
const existOriginOption = ref(false);

const optionList = ref([] as any[]);
const originOptionList = ref([] as any[]);
const optionTitleList = ref([] as any[]);
const receiveList = ref([] as any[]);

const hasOrigin = computed(() => {
  return originOptionList.value.length > 0;
});

const changedIndex = new Set<number>();

const defaultOpIdx = ref(0);
const originDefaultOpIdx = ref(0);

interface OptPropInfo {
  type: string;
  code: string;
  name: string;
  value: string;
  price: string;
}

const allInputValue = reactive({
  weight: 0,
  origin: 0,
  supply: 0,
  selling: 0,
  count: 0,
  safe_count: 0,
  view: 'Y',
  use_acc_qty: 'N',
  day_able_count: 0,
});

const setAllInputValue = (type: string) => {
  switch (type) {
    case 'weight':
      for (let i = 0; i < optionList.value.length; i++) {
        optionList.value[i].weight = allInputValue.weight;
        changedIndex.add(i);
      }
      break;
    case 'origin':
      for (let i = 0; i < optionList.value.length; i++) {
        optionList.value[i].origin_price = allInputValue.origin;
        changedIndex.add(i);
      }
      break;
    case 'supply':
      for (let i = 0; i < optionList.value.length; i++) {
        optionList.value[i].supply_price = allInputValue.supply;
        changedIndex.add(i);
      }
      break;
    case 'selling':
      for (let i = 0; i < optionList.value.length; i++) {
        optionList.value[i].selling_price = allInputValue.selling;
        changedIndex.add(i);
      }
      break;
    case 'view':
      for (let i = 0; i < optionList.value.length; i++) {
        optionList.value[i].view_yn = allInputValue.view;
        changedIndex.add(i);
      }
      break;
    case 'use_acc_qty':
      for (let i = 0; i < optionList.value.length; i++) {
        optionList.value[i].inventory.use_acc_qty = allInputValue.use_acc_qty;
        changedIndex.add(i);
      }
      break;
    case 'day_able_count':
      for (let i = 0; i < optionList.value.length; i++) {
        optionList.value[i].inventory.day_able_count = allInputValue.day_able_count;
        changedIndex.add(i);
      }
      break;
    case 'count':
      for (let i = 0; i < optionList.value.length; i++) {
        optionList.value[i].inventory.count = allInputValue.count;
        changedIndex.add(i);
      }
      break;
    case 'safe_count':
      for (let i = 0; i < optionList.value.length; i++) {
        optionList.value[i].inventory.safe_count = allInputValue.safe_count;
        changedIndex.add(i);
      }
      break;
  }
};

const setProdProp = (list: Opt[]) => {
  newCreateOption.value = true;

  let tmpOpList: any[];
  let origin: any[];

  optionList.value = [];
  optionTitleList.value = [];
  receiveList.value = [];

  allInputValue.weight = 0;
  allInputValue.origin = 0;
  allInputValue.supply = 0;
  allInputValue.selling = 0;
  allInputValue.count = 0;
  allInputValue.safe_count = 0;
  allInputValue.view = 'Y';

  for (const op of list) {
    const opList = [] as OptPropInfo[];
    const val = op.value.split(',');
    const pri = op.price.split(',');
    const cod = op.code.split(',');
    const count = val.length;
    for (let i = 0; i < count; i++) {
      opList.push({ type: op.type.name, code: cod[i], name: op.name, value: val[i], price: pri[i] });
    }
    receiveList.value.push(opList);
    optionTitleList.value.push(op.name);
  }
  origin = [];
  let tmp: any[] = [];
  for (let i = 0; i < receiveList.value.length; i++) {
    if (i == 0) {
      for (const op of receiveList.value[0]) {
        tmp = [];
        tmp.push(op);
        origin.push(tmp);
      }
    } else {
      tmpOpList = [];
      for (const ori of origin) {
        for (const op of receiveList.value[i]) {
          let tmp = JSON.parse(JSON.stringify(ori));
          tmp.push(op);
          tmpOpList.push(tmp);
        }
      }
      origin = JSON.parse(JSON.stringify(tmpOpList));
      origin = tmpOpList;
    }
  }
  makeOptionList(origin);
};

const makeOptionList = (list: any[]) => {
  const result = [];
  for (const op of list) {
    const data = { code: '', view_yn: 'Y', default_yn: 'N', product_id: props.productId, weight: 0, supply_price: 0, origin_price: 0, selling_price: 0, count: 0, safe_count: 0, inventory: { count: 0, safe_count: 0, use_acc_qty: 'N', day_able_count: 0 } } as OptionListInfo;
    let title = [];
    let prices = [];
    let codes = [];
    for (let i = 0; i < op.length; i++) {
      title.push(op[i].name);
      prices.push(op[i].price);
      codes.push(op[i].code);
      data.selling_price += parseInt(op[i].price);
      switch (i) {
        case 0:
          data.option_1 = op[i].value;
          data.option_code_1 = op[i].code;
          break;
        case 1:
          data.option_2 = op[i].value;
          data.option_code_2 = op[i].code;
          break;
        case 2:
          data.option_3 = op[i].value;
          data.option_code_3 = op[i].code;
          break;
        case 3:
          data.option_4 = op[i].value;
          data.option_code_4 = op[i].code;
          break;
        case 4:
          data.option_5 = op[i].value;
          data.option_code_5 = op[i].code;
          break;
      }
      data.option_title = title.join(',');
      data.option_tmp_price = prices.join(',');
      data.code = codes.join('');
    }
    result.push(JSON.parse(JSON.stringify(data)));
  }
  optionList.value = JSON.parse(JSON.stringify(result));
  optionList.value[0].default_yn = 'Y';
  defaultOpIdx.value = 0;
};

const checkInputFocus = (event: any) => {
  if (event.target.value === '0') {
    event.target.value = '';
  }
  const end = event.target.value.length;
  event.target.type = 'text';
  // event.target.setSelectionRange(0, 0);
  event.target.setSelectionRange(end, end);
  event.target.type = 'number';
};

const max100mill = (event: any) => {
  if (event.target.value > 99999999.99) {
    showAlert('최대 1억 미만 까지 입력할 수 있습니다.', 'warning', () => {
      event.target.focus();
    });
  } else if (event.target.value < 0) {
    showAlert('음수는 입력할 수 없습니다.', 'warning', () => {
      event.target.focus();
    });
  }
};

const checkInputNum = (type: string, event: any, index: number) => {
  const typeStr = type === 'weight' ? '무게를' : type === 'origin' ? '정상가를' : type === 'supply' ? '공급가를' : type === 'selling' ? '판매가를' : type === 'count' ? '재고를' : type === 'safe_count' ? '안전재고를' : '일처리가능수량을';
  if (!event.target.value) {
    showAlert(`${typeStr} 입력해 주세요.`, 'warning', () => {
      event.target.value = 0;
      event.target.focus();
    });
    return;
  } else {
    if (index >= 0) {
      if (checkInputValue(Number(event.target.value), type, index, event)) {
        changedIndex.add(index);
      } else {
        event.target.focus();
      }
    } else {
      if (!checkInputValue(Number(event.target.value), type, index, event)) {
        event.target.focus();
      }
    }
  }
  event.target.value = Number(event.target.value);
};

const checkInputValue = (value: number, type: string, index: number, event: any = null): boolean => {
  let result = true;
  const selling_price = index < 0 ? data.selling_price : optionList.value[index].selling_price;
  const origin_price = index < 0 ? data.origin_price : optionList.value[index].origin_price;
  const supply_price = index < 0 ? data.supply_price : optionList.value[index].supply_price;

  if (value > 99999999) {
    showAlert('1억 이상 입력할 수 없습니다.', 'warning', () => {
      if (event) {
        event.target.focus();
      }
    });
    return false;
  }

  switch (type) {
    case 'origin':
      if (selling_price !== 0 && value < selling_price) {
        showAlert('정상가는 판매가보다 작을 수 없습니다.\n입력하신 정보를 확인해 주세요.', 'warning', () => {
          if (event) {
            event.target.focus();
          }
        });
        result = false;
      }
      break;
    case 'supply':
      if (selling_price !== 0 && value > selling_price) {
        // showAlert('공급가는 판매가보다 클 수 없습니다.\n입력하신 정보를 확인해 주세요.', 'warning', () => {
        //   if (event) {
        //     event.target.focus();
        //   }
        // });
        // result = false;
      }
      break;
    case 'selling':
      if (value < 100) {
        showAlert('판매가는 100원 이상이어야 합니다.', 'warning', () => {
          if (event) {
            event.target.focus();
          }
        });
        result = false;
        break;
      }
      if (origin_price !== 0 && value > origin_price) {
        showAlert('판매가는 정상가보다 클 수 없습니다.\n입력하신 정보를 확인해 주세요.', 'warning', () => {
          if (event) {
            event.target.focus();
          }
        });
        result = false;
      }
      // 23.11.01. 판매가가 공급가보다 적을 수 있다. (마이너스 마진)
      // if (supply_price !== 0 && value < supply_price) {
      //   showAlert('판매가는 공급가보다 작을 수 없습니다.\n입력하신 정보를 확인해 주세요.', 'warning', () => {
      //     if (event) {
      //       event.target.focus();
      //     }
      //   });
      //   result = false;
      // }
      break;
    case 'count':
    case 'safe_count':
    case 'day_able_count':
      if (value < 0) {
        showAlert('0보다 작은 값을 입력할 수 없습니다.', 'warning', () => {
          if (event) {
            event.target.focus();
          }
        });
        result = false;
      }
      break;
  }
  if (result && index >= 0) {
    const row = document.querySelector(`#op_row_${index}`);
    if (row) {
      row.classList.remove('warning_row');
    }
  }

  return result;
};

const changeInput = (index: number, event: any) => {
  changedIndex.add(index);
};

const deleteOriginOption = async () => {
  const ids = [];
  for (const op of originOptionList.value) {
    ids.push(op.id);
  }

  const result = await apis.product.deleteProdOption(props.productId, ids).then(res => {
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      return false;
    } else {
      return true;
    }
  });

  return result;
};

const reqAddProdOption = () => {
  if (use.value !== props.status) {
    apis.product.updateBaseInfo(props.productId, { option_use: use.value }).then(res => {
      apiResponseCheck(res, () => {
        const list: OptionListInfo[] =
          use.value === 'Y'
            ? optionList.value
            : [
                {
                  weight: data.weight,
                  origin_price: data.origin_price,
                  supply_price: data.supply_price,
                  selling_price: data.selling_price,
                  count: data.count,
                  safe_count: data.safe_count,
                  day_able_count: data.day_able_count,
                  use_acc_qty: data.use_acc_qty,
                  view_yn: 'Y',
                  default_yn: 'Y',
                },
              ];
        if (use.value === 'Y') {
          list[0].default_yn = 'N';
          list[defaultOpIdx.value].default_yn = 'Y';
          list.map(item => {
            (item as OptionListInfo).count = (item as OptionListInfo).inventory.count;
            (item as OptionListInfo).safe_count = (item as OptionListInfo).inventory.safe_count;
            (item as OptionListInfo).day_able_count = (item as OptionListInfo).inventory.day_able_count;
            (item as OptionListInfo).use_acc_qty = (item as OptionListInfo).inventory.use_acc_qty;
          });
        }
        apis.product.addProdOption(props.productId, list).then(res => {
          apiResponseCheck(res, () => {
            showAlert('상품 옵션 정보가 등록되었습니다.', 'success');
            getProdOptionList();
            emits('changedProdInfo');
            emits('saveFinish', 'option');
          });
        });
      });
    });
  } else {
    const list: OptionListInfo[] =
      use.value === 'Y'
        ? optionList.value
        : [
            {
              weight: data.weight,
              origin_price: data.origin_price,
              supply_price: data.supply_price,
              selling_price: data.selling_price,
              count: data.count,
              safe_count: data.safe_count,
              view_yn: 'Y',
              default_yn: 'Y',
              day_able_count: data.day_able_count,
              use_acc_qty: data.use_acc_qty,
            },
          ];
    if (use.value === 'Y') {
      list[0].default_yn = 'N';
      list[defaultOpIdx.value].default_yn = 'Y';
      list.map(item => {
        (item as OptionListInfo).count = (item as OptionListInfo).inventory.count;
        (item as OptionListInfo).safe_count = (item as OptionListInfo).inventory.safe_count;
        (item as OptionListInfo).day_able_count = (item as OptionListInfo).inventory.day_able_count;
        (item as OptionListInfo).use_acc_qty = (item as OptionListInfo).inventory.use_acc_qty;
      });
    }
    apis.product.addProdOption(props.productId, list).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 옵션 정보가 등록되었습니다.', 'success');
        getProdOptionList();
        emits('saveFinish', 'option');
      });
    });
  }
};

const clearInfo = () => {
  originOptionList.value = [];
  receiveList.value = [];
  optionTitleList.value = [];
  optionList.value = [];
  data.weight = 0;
  data.selling_price = 0;
  data.origin_price = 0;
  data.supply_price = 0;
  data.count = 0;
  data.safe_count = 0;
  data.use_acc_qty = 'N';
  data.day_able_count = 0;
  newCreateOption.value = false;
  originDefaultOpIdx.value = 0;
  defaultOpIdx.value = 0;
  changedIndex.clear();

  allInputValue.weight = 0;
  allInputValue.origin = 0;
  allInputValue.supply = 0;
  allInputValue.selling = 0;
  allInputValue.count = 0;
  allInputValue.safe_count = 0;
  allInputValue.view = 'Y';
};
const getProdOptionList = () => {
  clearInfo();

  apis.product.getProdOption(props.productId).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      if (res.length > 0) {
        originOptionList.value = res;
        if (use.value === 'Y') {
          optionList.value = JSON.parse(JSON.stringify(res));
          optionTitleList.value = optionList.value[0].option_title.split(',');
          //대표옵션
          for (let i = 0; i < optionList.value.length; i++) {
            if (optionList.value[i].default_yn === 'Y') {
              defaultOpIdx.value = i;
              originDefaultOpIdx.value = i;
              break;
            }
          }
        } else {
          data.weight = res[0].weight;
          data.selling_price = res[0].selling_price;
          data.origin_price = res[0].origin_price;
          data.supply_price = res[0].supply_price;
          data.count = res[0].inventory.count;
          data.safe_count = res[0].inventory.safe_count;
          data.day_able_count = res[0].inventory.day_able_count;
          data.use_acc_qty = res[0].inventory.use_acc_qty;
        }
        newCreateOption.value = false;
        existOriginOption.value = true;
      } else {
        newCreateOption.value = true;
        existOriginOption.value = false;
      }
    });
  });
};

const onStepActive = () => {
  if (props.productId) {
    use.value = JSON.parse(JSON.stringify(props.status));
    getProdOptionList();
  }
};

watch(
  () => props.status,
  status => {
    use.value = JSON.parse(JSON.stringify(status));
  },
);

watch(
  () => use.value,
  flag => {
    if (use.value !== props.status) {
      newCreateOption.value = true;
    } else {
      if (existOriginOption.value) {
        newCreateOption.value = false;
      } else {
        newCreateOption.value = true;
      }
    }
  },
);

defineExpose({ onStepActive });

const optionSave = () => {
  if (use.value === 'Y') {
    if (optionList.value.length === 0) {
      showAlert('옵션 생성 후 저장해주세요.', 'warning');
      return;
    }
  } else {
    if (!Number.isFinite(data.weight) || !Number.isFinite(data.origin_price) || !Number.isFinite(data.supply_price) || !Number.isFinite(data.selling_price)) {
      showAlert('기본 옵션 데이터를 확인해주세요.', 'warning');
      return;
    }
  }

  let valueCheck = true;
  if (use.value === 'Y') {
    for (let i = 0; i < optionList.value.length; i++) {
      const origin = checkInputValue(optionList.value[i].origin_price, 'origin', i);
      const supply = checkInputValue(optionList.value[i].supply_price, 'supply', i);
      const selling = checkInputValue(optionList.value[i].selling_price, 'selling', i);

      if (!origin || !supply || !selling) {
        const row = document.querySelector(`#op_row_${i}`);
        if (row) {
          row.classList.add('warning_row');
        }
        valueCheck = false;
      }
    }
  } else {
    const origin = checkInputValue(data.origin_price, 'origin', -1);
    const supply = checkInputValue(data.supply_price, 'supply', -1);
    const selling = checkInputValue(data.selling_price, 'selling', -1);

    if (!origin || !supply || !selling) {
      valueCheck = false;
    }
  }

  if (valueCheck) {
    showConfirm('저장하시겠습니까?', () => {
      optionListProcess();
    });
  }
};

const optionListProcess = () => {
  // 신규 생성임
  if (newCreateOption.value) {
    // 완전 신규 등록
    if (originOptionList.value.length === 0) {
      reqAddProdOption();
    }
    // 기존 옵션 삭제 후 신규 등록
    else {
      Promise.resolve(deleteOriginOption()).then(res => {
        if (res) {
          reqAddProdOption();
        }
      });
    }
  }
  // 기존 옵션
  else {
    //수정
    if (use.value === 'Y') {
      // 속성 옵션 수정
      if (changedIndex.size === 0 && defaultOpIdx.value === originDefaultOpIdx.value) {
        showAlert('변경사항이 없습니다.', 'warning');
        return;
      } else {
        if (defaultOpIdx.value !== originDefaultOpIdx.value) {
          optionList.value[defaultOpIdx.value].default_yn = 'Y';
          optionList.value[originDefaultOpIdx.value].default_yn = 'N';
          changedIndex.add(defaultOpIdx.value);
          changedIndex.add(originDefaultOpIdx.value);
        }
        const changedList: any[] = [];
        changedIndex.forEach(index => {
          const newCode = [];
          for (let i = 0; i < optionTitleList.value.length; i++) {
            switch (i) {
              case 0:
                newCode.push(optionList.value[index].option_code_1);
                break;
              case 1:
                newCode.push(optionList.value[index].option_code_2);
                break;
              case 2:
                newCode.push(optionList.value[index].option_code_3);
                break;
              case 3:
                newCode.push(optionList.value[index].option_code_4);
                break;
              case 4:
                newCode.push(optionList.value[index].option_code_5);
                break;
            }
          }
          optionList.value[index].code = newCode.join('');
          const tmp = JSON.parse(JSON.stringify(optionList.value[index]));
          tmp['opt_id'] = tmp['id'];
          tmp['count'] = tmp['inventory']['count'];
          tmp['safe_count'] = tmp['inventory']['safe_count'];
          tmp['day_able_count'] = tmp['inventory']['day_able_count'];
          tmp['use_acc_qty'] = tmp['inventory']['use_acc_qty'];
          delete tmp.id;
          delete tmp.inventory;

          changedList.push(tmp);
        });
        apis.product.modProdOption(props.productId, changedList).then(res => {
          apiResponseCheck(res, () => {
            showAlert('상품 옵션이 수정되었습니다.', 'success');
            getProdOptionList();
            emits('saveFinish', 'option');
          });
        });
      }
    } else {
      // 기본 옵션 수정
      if (
        originOptionList.value[0].weight === data.weight &&
        originOptionList.value[0].origin_price === data.origin_price &&
        originOptionList.value[0].supply_price === data.supply_price &&
        originOptionList.value[0].selling_price === data.selling_price &&
        originOptionList.value[0].inventory.count === data.count &&
        originOptionList.value[0].inventory.safe_count === data.safe_count &&
        originOptionList.value[0].inventory.use_acc_qty === data.use_acc_qty &&
        originOptionList.value[0].inventory.day_able_count === data.day_able_count
      ) {
        showAlert('변경사항이 없습니다.', 'warning');
        return;
      } else {
        const changedList: any[] = [];
        changedList.push({
          opt_id: originOptionList.value[0].id,
          weight: data.weight,
          origin_price: data.origin_price,
          supply_price: data.supply_price,
          selling_price: data.selling_price,
          count: data.count,
          safe_count: data.safe_count,
          use_acc_qty: data.use_acc_qty,
          day_able_count: data.day_able_count,
        });
        apis.product.modProdOption(props.productId, changedList).then(res => {
          apiResponseCheck(res, () => {
            showAlert('상품 옵션이 수정되었습니다.', 'success');
            getProdOptionList();
          });
        });
      }
    }
  }
};
</script>

<style scoped>
.wide {
  /*width: 120% !important;*/
}

.warning_row {
  background-color: #ff8c8c !important;
}
</style>
