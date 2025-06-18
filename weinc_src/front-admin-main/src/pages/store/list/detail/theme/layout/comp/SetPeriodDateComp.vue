<template>
  <div class="row mb-2 align-items-center">
    <label for="idLabel" class="col-md-2 col-form-label">노출기간</label>
    <div class="col-auto">
      <div class="row align-items-center mb-2">
        <div class="col-auto">
          <!-- Form Group -->
          <div class="form-group">
            <div id="startDatepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#startDatepicker","dateFormat": "Y-m-d H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
              <div class="input-group-prepend input-group-text" data-bs-toggle>
                <i class="bi-calendar-week"></i>
              </div>
              <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." v-model="startDate" />
            </div>
          </div>
        </div>
        <span class="col-auto align-items-center">~</span>
        <div class="col-auto">
          <!-- Form Group -->
          <div class="form-group">
            <div id="endDatepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#endDatepicker","dateFormat": "Y-m-d H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
              <div class="input-group-prepend input-group-text" data-bs-toggle>
                <i class="bi-calendar-week"></i>
              </div>
              <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." v-model="endDate" />
            </div>
          </div>
        </div>
        <div class="d-lg-none mt-2"></div>
      </div>
      <div class="row align-items-center">
        <div class="col">
          <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
          <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">일주일</button>
          <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('month')">1개월</button>
          <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('3month')">3개월</button>
          <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('6month')">6개월</button>
          <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('all')">상시</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { showAlert } from '@/utils/common-utils';
import { onMounted, ref, watch } from 'vue';

const props = defineProps({
  sId: {
    required: true,
    type: String,
  },
  eId: {
    required: true,
    type: String,
  },
  sDate: {
    type: String,
    default: '',
  },
  eDate: {
    type: String,
    default: '',
  },
});
const sfp = ref();
const efp = ref();
const startDate = ref('');
const endDate = ref('');
const setSearchPeriod = (period: string, time: boolean = false) => {
  const today = new Date();
  switch (period) {
    case 'today':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(today.setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'week':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 7).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'month':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 30).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case '3month':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 90).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case '6month':
      // @ts-ignore
      sfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      efp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 180).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    default:
      startDate.value = '';
      endDate.value = '';
      break;
  }
};

const sDateChange = () => {
  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    // @ts-ignore
    // eslint-disable-next-line vue/no-mutating-props
    props.sDate = sDate;
    return;
  } else {
    if (sDate > eDate) {
      showAlert('노출 시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      sfp.value.setDate(new Date(), true, 'Y-m-d H:i');
    }
  }
};
const eDateChange = () => {
  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    // @ts-ignore
    // eslint-disable-next-line vue/no-mutating-props
    props.eDate = eDate;
    return;
  } else {
    if (sDate > eDate) {
      showAlert('노출 종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      efp.value.setDate(new Date(), true, 'Y-m-d H:i');
    }
  }
};

watch(
  () => props.sDate,
  date => {
    startDate.value = date;
    if (startDate.value) sfp.value.setDate(startDate.value);
  },
);

watch(
  () => props.eDate,
  date => {
    endDate.value = date;
    if (startDate.value) efp.value.setDate(endDate.value);
  },
);

const emits = defineEmits(['returnDate']);

const editFinish = (type: string) => {
  emits('returnDate', startDate.value, endDate.value, type);
};

defineExpose({ editFinish });

onMounted(() => {
  //@ts-ignore
  sfp.value = flatpickr(document.querySelector('#startDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => sDateChange(), static: true });
  //@ts-ignore
  efp.value = flatpickr(document.querySelector('#endDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => eDateChange(), static: true });
  if (props.sDate || props.eDate) {
    startDate.value = props.sDate ? props.sDate : '';
    endDate.value = props.eDate ? props.eDate : '';
    if (startDate.value) sfp.value.setDate(startDate.value);
    if (endDate.value) efp.value.setDate(endDate.value);
  } else {
    setSearchPeriod('all');
  }
});
</script>

<style scoped></style>
