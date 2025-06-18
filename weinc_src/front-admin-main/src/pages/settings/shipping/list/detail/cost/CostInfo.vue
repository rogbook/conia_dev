<template>
  <div class="card">
    <div class="card-body">
      <div>[기본 배송비]</div>
      <div class="row col mb-2 align-items-center">
        <label class="col-md-2 col-form-label">배송비 타입</label>
        <div class="col-md-4">
          <select class="form-select sel_theme_link" v-model="selCostType.selectedItem" @change="typeChange" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "배송타입을 선택해주세요."}'>
            <option disabled selected>배송비타입을 선택해주세요.</option>
            <option v-for="t in selCostType.items" :key="JSON.stringify(t)" v-text="t.name" :value="t.value" :selected="selCostType.selectedItem === t.value"></option>
          </select>
        </div>
      </div>
      <div class="row col mb-2 align-items-center" v-if="selCostType.selectedItem === 'free'">
        <label class="col-md-2 col-form-label">배송비</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="number" class="form-control text-end" value="0" readonly />
            <div class="input-group-text">
              <span class="">원</span>
            </div>
          </div>
        </div>
      </div>
      <div class="row col mb-2 align-items-center" v-if="selCostType.selectedItem === 'fix'">
        <label class="col-md-2 col-form-label">배송비</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="number" class="form-control text-end" placeholder="고정 배송비를 입력해주세요." v-model="fixCost" />
            <div class="input-group-text">
              <span class="">원</span>
            </div>
          </div>
        </div>
      </div>
      <div class="" v-if="selCostType.selectedItem !== 'free' && selCostType.selectedItem !== 'fix'">
        <div class="row col mb-2 align-items-center">
          <label class="col-md-2 col-form-label">배송비</label>
          <!-- 구간 반복이 아닌경우 START -->
          <div class="col" v-if="!selCostType.selectedItem.includes('repeat')">
            <div class="row align-items-center mb-2" v-for="(s, i) in sectionCostInfo.sections" :key="JSON.stringify(s)">
              <div class="col-md-3">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="구간시작값" v-model="s.start" readonly />
                  <div class="input-group-text">
                    <span class="" v-if="selCostType.selectedItem.startsWith('ea')">개 이상</span>
                    <span class="" v-else-if="selCostType.selectedItem.startsWith('weight')">Kg 이상</span>
                    <span class="" v-else>원 이상</span>
                  </div>
                </div>
              </div>
              <span class="col-auto">~</span>
              <div class="col-md-3">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="구간종료값" v-model.lazy="s.end" @change="checkEndSection(i, s, $event)" />
                  <div class="input-group-text">
                    <span class="" v-if="selCostType.selectedItem.startsWith('ea')">개 미만</span>
                    <span class="" v-else-if="selCostType.selectedItem.startsWith('weight')">Kg 미만</span>
                    <span class="" v-else>원 미만</span>
                  </div>
                </div>
              </div>
              <div class="d-md-none mt-1"></div>
              <div class="col-md-4 ms-md-4">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="배송비를 입력해주세요." v-model.lazy="s.cost" />
                  <div class="input-group-text">
                    <span class="">원</span>
                  </div>
                </div>
              </div>
              <div class="col-auto table-text-center" v-if="i === 0">
                <button type="button" class="btn table-text-center text-primary" @click.prevent="addSectionCost"><i class="bi-plus-circle" style="font-size: 1rem"></i></button>
              </div>
              <div class="col-auto table-text-center" v-else>
                <button type="button" class="btn table-text-center text-danger" @click.prevent="deleteSectionCost(i)"><i class="bi-x-circle" style="font-size: 1rem"></i></button>
              </div>
            </div>
            <div class="row align-items-center">
              <div class="col-md-3">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="구간시작값" v-model="sectionCostInfo.sections[sectionCostInfo.sections.length - 1].end" readonly />
                  <div class="input-group-text">
                    <span class="" v-if="selCostType.selectedItem.startsWith('ea')">개 이상</span>
                    <span class="" v-else-if="selCostType.selectedItem.startsWith('weight')">Kg 이상</span>
                    <span class="" v-else>원 이상</span>
                  </div>
                </div>
              </div>
              <div class="d-md-none mt-1"></div>
              <div class="col-md-4">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="배송비를 입력해주세요." v-model="sectionCostInfo.endSection.cost" />
                  <div class="input-group-text">
                    <span class="">원</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- 구간 반복이 아닌경우 END -->
          <div class="col" v-else>
            <div class="row align-items-center mb-2">
              <div class="col-md-3">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="구간시작값" v-model="sectionCostRepeatInfo.section.start" readonly />
                  <div class="input-group-text">
                    <span class="" v-if="selCostType.selectedItem.startsWith('ea')">개 이상</span>
                    <span class="" v-else-if="selCostType.selectedItem.startsWith('weight')">Kg 이상</span>
                    <span class="" v-else>원 이상</span>
                  </div>
                </div>
              </div>
              <span class="col-auto">~</span>
              <div class="col-md-3">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="구간종료값" v-model="sectionCostRepeatInfo.section.end" @change="checkEnd(sectionCostRepeatInfo.section, $event)" />
                  <div class="input-group-text">
                    <span class="" v-if="selCostType.selectedItem.startsWith('ea')">개 미만</span>
                    <span class="" v-else-if="selCostType.selectedItem.startsWith('weight')">Kg 미만</span>
                    <span class="" v-else>원 미만</span>
                  </div>
                </div>
              </div>
              <div class="d-md-none mt-1"></div>
              <div class="col-md-4 ms-md-4">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="배송비를 입력해주세요." v-model="sectionCostRepeatInfo.section.cost" />
                  <div class="input-group-text">
                    <span class="">원</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="row align-items-center mb-2">
              <div class="col-md-3">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="구간시작값" v-model="sectionCostRepeatInfo.section.end" />
                  <div class="input-group-text">
                    <span class="" v-if="selCostType.selectedItem.startsWith('ea')">개 부터</span>
                    <span class="" v-else-if="selCostType.selectedItem.startsWith('weight')">Kg 부터</span>
                    <span class="" v-else>원 부터</span>
                  </div>
                </div>
              </div>
              <span class="col-auto">~</span>
              <div class="col-md-3">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="반복될 수치를 입력해주세요." v-model="sectionCostRepeatInfo.repeat.repeat" />
                  <div class="input-group-text">
                    <span class="" v-if="selCostType.selectedItem.startsWith('ea')">개 당</span>
                    <span class="" v-else-if="selCostType.selectedItem.startsWith('weight')">Kg 당</span>
                    <span class="" v-else>원 당</span>
                  </div>
                </div>
              </div>
              <div class="d-md-none mt-1"></div>
              <div class="col-md-4 ms-md-4">
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="배송비를 입력해주세요." v-model="sectionCostRepeatInfo.repeat.cost" />
                  <div class="input-group-text">
                    <span class="">원</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row col mb-2 align-items-center">
        <label class="col-md-2 col-form-label text-nowrap">도서산간 추가배송비 사용여부</label>
        <div class="col-auto">
          <div class="form-check form-check-inline">
            <input id="radio_status_y" type="radio" class="form-check-input" name="radio_status" value="Y" v-model="additional_yn" />
            <label class="form-check-label" for="radio_status_y">사용</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-check form-check-inline">
            <input id="radio_status_n" type="radio" class="form-check-input" name="radio_status" value="N" v-model="additional_yn" />
            <label class="form-check-label" for="radio_status_n">사용안함</label>
          </div>
        </div>
      </div>
      <div class="additional-cost" v-if="additional_yn === 'Y'">
        <div class="row col mb-2 align-items-center">
          <label class="col-md-2 col-form-label">도서산간 추가배송비</label>
          <div class="col-md-4">
            <div class="input-group">
              <input type="number" class="form-control text-end" placeholder="도서산간 추가 배송비를 입력해주세요." v-model="additionalCostInfo.cost" />
              <div class="input-group-text">
                <span class="">원</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, PropType, reactive, ref } from 'vue';
import type { ShippingCost, AddShippingInfo } from 'ShippingInfoModule';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm } from '@/utils/common-utils';

const defaultCost = 2500;

const props = defineProps({
  shippingId: {
    type: String,
    required: true,
  },
  calcType: {
    type: String,
    required: true,
  },
  costInfo: {
    type: [] as PropType<ShippingCost[]>,
    required: true,
  },
});

const emit = defineEmits(['closeModal']);

const additional_yn = ref('N');

const selCostType = reactive({
  items: [
    { name: '무료', value: 'free' },
    { name: '고정', value: 'fix' },
    { name: '금액(구간입력)', value: 'cost' },
    { name: '금액(구간반복)', value: 'cost-repeat' },
    { name: '수량(구간입력)', value: 'ea' },
    { name: '수량(구간반복)', value: 'ea-repeat' },
    { name: '무게(구간입력)', value: 'weight' },
    { name: '무게(구간반복)', value: 'weight-repeat' },
  ],
  selectedItem: 'free',
});

const selCostType2 = reactive({
  items: [
    { name: '무료', value: 'free' },
    { name: '고정', value: 'fix' },
    { name: '금액(구간입력)', value: 'cost' },
    { name: '금액(구간반복)', value: 'cost-repeat' },
    { name: '수량(구간입력)', value: 'ea' },
    { name: '수량(구간반복)', value: 'ea-repeat' },
    { name: '무게(구간입력)', value: 'weight' },
    { name: '무게(구간반복)', value: 'weight-repeat' },
  ],
  selectedItem: 'free',
});

const fixCost = ref();

const sectionCostInfo = reactive({
  sections: [{ start: 0, end: 1, cost: defaultCost }] as { start: number; end: number; cost: number }[],
  endSection: { start: 0, cost: defaultCost } as { start: number; cost: number },
});

const sectionCostInfo2 = reactive({
  sections: [{ start: 0, end: 1, cost: defaultCost }] as { start: number; end: number; cost: number }[],
  endSection: {} as { start: number; cost: number },
});

const sectionCostRepeatInfo = reactive({
  section: { start: 0, end: 1, cost: defaultCost } as { start: number; end: number; cost: number },
  repeat: { start: 0, repeat: 1, cost: defaultCost } as { start: number; repeat: number; cost: number },
});

const additionalCostInfo = reactive({
  cost: 0,
});

const deleteCostInfo = async () => {
  const result = await apis.shipping.delete_shipping_cost_info(props.shippingId).then(res => {
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

const saveClicked = () => {
  showConfirm('배송비 정보를 저장하시겠습니까?', () => {
    Promise.resolve(deleteCostInfo()).then(res => {
      if (res) {
        const type = selCostType.selectedItem;
        const costs = [] as AddShippingInfo[];
        switch (type) {
          case 'free':
            costs.push({ type: type, category: 'basic', cost: 0 });
            break;
          case 'fix':
            costs.push({ type: type, category: 'basic', cost: fixCost.value });
            break;
          case 'cost':
          case 'ea':
          case 'weight':
            sectionCostInfo.sections.forEach((value, index) => {
              costs.push({ type: type, category: 'basic', cost: value.cost, section_start: value.start, section_end: value.end });
            });
            costs.push({ type: type, category: 'basic', section_start: sectionCostInfo.sections[sectionCostInfo.sections.length - 1].end, cost: sectionCostInfo.endSection.cost });
            break;
          case 'cost-repeat':
          case 'ea-repeat':
          case 'weight-repeat':
            costs.push({ type: type.split('-')[0], category: 'basic', cost: sectionCostRepeatInfo.section.cost, section_start: sectionCostRepeatInfo.section.start, section_end: sectionCostRepeatInfo.section.end });
            costs.push({ type: type.split('-')[0], category: 'basic', cost: sectionCostRepeatInfo.repeat.cost, section_start: sectionCostRepeatInfo.section.end, section_repeat: sectionCostRepeatInfo.repeat.repeat });
            break;
        }
        if (additional_yn.value === 'Y') {
          costs.push({ type: type.split('-')[0], category: 'add', cost: additionalCostInfo.cost });
        }
        addCostInfo(costs);
      }
    });
  });
};

const addCostInfo = (list: AddShippingInfo[]) => {
  apis.shipping.add_shipping_cost_info(props.shippingId, list).then(res => {
    apiResponseCheck(
      res,
      () => {
        showAlert('배송비 정보가 저장되었습니다.', 'success');
        emit('closeModal');
      },
      (num?: number) => {
        if (num === 403) {
          emit('closeModal');
        }
      },
    );
  });
};

defineExpose({ saveClicked });

const checkEnd = (s: { start: number; end: number; cost: number }, event: any) => {
  if (!s.end) {
    showAlert('구간종료값을 입력해야 합니다.', 'warning');
    s.end = parseInt(s.start.toString()) + 1;
    event.target.focus();
    return;
  }
  const n: number = parseInt(s.end.toString());
  if (n <= parseInt(s.start.toString())) {
    showAlert(`최소 ${s.start} 보다는 큰 값을 입력해야합니다.`, 'warning');
    s.end = parseInt(s.start.toString()) + 1;
    event.target.focus();
  } else {
    s.end = n;
  }
};

const checkEndSection = (i: number, s: { start: number; end: number; cost: number }, event: any) => {
  if (!s.end) {
    showAlert('구간종료값을 입력해야 합니다.', 'warning');
    s.end = parseInt(s.start.toString()) + 1;
    event.target.focus();
    return;
  }
  const n: number = parseInt(s.end.toString());
  if (n <= parseInt(s.start.toString())) {
    showAlert(`최소 ${s.start} 보다는 큰 값을 입력해야합니다.`, 'warning');
    s.end = parseInt(s.start.toString()) + 1;
    event.target.focus();
  } else {
    if (i < sectionCostInfo.sections.length - 1) {
      if (n >= sectionCostInfo.sections[i + 1].end) {
        showAlert(`${sectionCostInfo.sections[i + 1].end} 보다는 작은 값을 입력해야합니다.`, 'warning');
        s.end = sectionCostInfo.sections[i + 1].start;
        event.target.focus();
        return;
      } else {
        sectionCostInfo.sections[i + 1].start = n;
      }
    }
    s.end = n;
  }
};

const addSectionCost = () => {
  const last = sectionCostInfo.sections[sectionCostInfo.sections.length - 1];
  if (last.start === last.end) {
    showAlert('새로운 구간을 입력하시려면 구간종료값을 구간시작값 보다 큰 값을 입력해야 합니다.', 'warning');
    return;
  }
  sectionCostInfo.sections.push({ start: last.end, end: parseInt(last.end.toString()) + 1, cost: defaultCost });
};

const deleteSectionCost = (i: number) => {
  const d = sectionCostInfo.sections.splice(i, 1);
  const dSection = JSON.parse(JSON.stringify(d));
  if (i <= sectionCostInfo.sections.length - 1) {
    sectionCostInfo.sections[i].start = dSection[0].start;
  }
};

const clearCostInfo = () => {
  sectionCostInfo.sections = [{ start: 0, end: 1, cost: defaultCost }];
  sectionCostInfo.endSection = { start: 0, cost: defaultCost } as { start: number; cost: number };

  sectionCostRepeatInfo.section = { start: 0, end: 1, cost: defaultCost };
  sectionCostRepeatInfo.repeat = { start: 0, repeat: 1, cost: defaultCost } as { start: number; repeat: number; cost: number };

  fixCost.value = defaultCost;
  additional_yn.value = 'N';

  selCostType.items = [
    { name: '무료', value: 'free' },
    { name: '고정', value: 'fix' },
    { name: '금액(구간입력)', value: 'cost' },
    { name: '금액(구간반복)', value: 'cost-repeat' },
    { name: '수량(구간입력)', value: 'ea' },
    { name: '수량(구간반복)', value: 'ea-repeat' },
    { name: '무게(구간입력)', value: 'weight' },
    { name: '무게(구간반복)', value: 'weight-repeat' },
  ];

  fixCost.value = defaultCost;
};

const typeChange = () => {
  clearCostInfo();
};

const showCostInfo = () => {
  // 배송비 타입
  const type = props.costInfo[0].type;
  switch (type) {
    case 'free':
    case 'fix':
      selCostType.selectedItem = type;
      if (type === 'fix') {
        fixCost.value = props.costInfo[0].cost;
      }
      break;
    case 'cost':
    case 'ea':
    case 'weight':
      selCostType.selectedItem = `${type}${checkRepeat()}`;
  }

  const list = JSON.parse(JSON.stringify(props.costInfo));
  // 배송비 정보
  if (checkRepeat()) {
    sectionCostRepeatInfo.section = { cost: list[0].cost, start: list[0].section_start, end: list[0].section_end };
    sectionCostRepeatInfo.repeat = { cost: list[1].cost, start: list[1].section_start, repeat: list[1].repeat };
  } else {
    const lastIdx = list[list.length - 1].category === 'add' ? list.length - 2 : list.length - 1;
    sectionCostInfo.sections = [] as { start: number; end: number; cost: number }[];
    list.forEach((value: any, index: number) => {
      if (index > lastIdx) return;
      if (index === lastIdx) {
        sectionCostInfo.endSection.cost = value.cost;
      } else {
        sectionCostInfo.sections.push({ start: value.section_start, end: value.section_end, cost: value.cost });
      }
    });
  }

  // 도서산간 배송비
  if (list[list.length - 1].category === 'add') {
    additional_yn.value = 'Y';
    additionalCostInfo.cost = list[list.length - 1].cost;
  }
};

const checkRepeat = (): string => {
  let lastIdx = -1;
  lastIdx = props.costInfo.map(el => el.category).lastIndexOf('basic');
  if (lastIdx != -1) {
    if (props.costInfo[lastIdx].section_repeat !== null) {
      //구간 반복
      return '-repeat';
    } else {
      return '';
    }
  } else {
    return '';
  }
};

onMounted(() => {
  //@ts-ignore
  document.getElementById('CostInfoModal').addEventListener('show.bs.modal', function (event) {
    if (props.calcType?.includes('무료계산')) {
      selCostType.items.splice(1, selCostType.items.length - 1);
    }

    if (props.costInfo?.length > 0) {
      showCostInfo();
    }
  });

  //@ts-ignore
  document.getElementById('CostInfoModal').addEventListener('hide.bs.modal', function (event) {
    clearCostInfo();
    selCostType.selectedItem = 'free';
  });
});
</script>

<style scoped></style>
