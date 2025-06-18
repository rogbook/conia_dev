<template>
  <PageNavigator :before_link="['주문관리']" :current="'매출현황'" />
  <div class="card col-md-9">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">매출현황</div>
    </div>
    <div class="card-body ps-8">
      <div class="row mb-2 align-items-center justify-content-between">
        <div class="col-auto">
          <button type="button" class="btn btn-outline-secondary" @click="goToToday">이번달</button>
        </div>
        <div class="col-auto">
          <h3 class="mb-0 text-center">
            <button class="btn btn-md btn-outline-secondary me-2" @click="prevMonth"><i class="bi bi-chevron-left"></i></button>
            {{ selYear }}년 {{ selMonth }}월
            <button class="btn btn-outline-secondary ms-2" @click="nextMonth"><i class="bi bi-chevron-right"></i></button>
          </h3>
        </div>
        <div class="col-auto">
          <select class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' v-model="viewMode" @change="changeViewMode">
            <option value="calendar">캘린더 모드</option>
            <option value="table">리스트 모드</option>
          </select>
        </div>
      </div>

      <FullCalendar class="fullcalendar-custom" ref="calendarRef" :options="calendarOptions" v-if="viewMode === 'calendar'" />

      <div class="row" v-else>
        <div class="col">
          <div class="table-responsive datatable-custom position-relative mt-4">
            <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table table-striped">
              <thead class="thead-light">
                <tr class="text-center">
                  <th style="width: 20%">날짜</th>
                  <th style="width: 25%">온라인 매출</th>
                  <th style="width: 25%">오프라인 매출</th>
                  <th style="width: 25%">합계</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center" v-for="(item, i) in revenueMonthTable">
                  <td>{{ item.date }}</td>
                  <td>
                    <RouterLink v-if="item.onlineSales" :to="{ path: '/order/list', state: { orderDate: item.date } }">
                      {{ item.onlineSales.toLocaleString() + '원' }}
                    </RouterLink>
                    <a v-else> - </a>
                  </td>
                  <td>
                    <RouterLink v-if="item.offlineSales" :to="{ path: '/order/offlist', state: { orderDate: item.date } }">
                      {{ item.offlineSales.toLocaleString() + '원' }}
                    </RouterLink>
                    <a v-else> - </a>
                  </td>
                  <td>{{ item.sum ? item.sum.toLocaleString() + '원' : '-' }}</td>
                </tr>
                <tr>
                  <td colspan="3" class="text-center" v-if="revenueMonthTable.length === 0">표시할 항목이 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { onMounted, reactive, ref, watch } from 'vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import { useSearchStore } from '@/stores/search';
import apis from '@/apis';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';

const router = useRouter();
const calendarRef = ref();
const viewMode = ref('calendar');
const nowDate = ref(new Date());
const selYear = ref(nowDate.value.getFullYear());
const selMonth = ref(nowDate.value.getMonth() + 1);
const revenueMonthCalendar = reactive({
  online: [],
  offline: [],
  sum: [],
});
const revenueMonthTable = ref([
  {
    date: '',
    onlineSales: '',
    offlineSales: '',
    sum: '',
  },
]);

const calendarOptions = reactive({
  plugins: [dayGridPlugin],
  events: [],
  headerToolbar: {
    left: '',
    center: '',
    right: '',
  },
  height: '1020px',
  fixedWeekCount: false,
  eventOrder: 'displayOrder',
  eventColor: 'transparent',
  titleFormat: (info: any) => {
    const year = info.date.year;
    const month = info.date.month + 1;

    return year + '년 ' + month + '월';
  },
  dayCellDidMount: (info: any) => {
    const date = info.date;
    const dayOfWeek = date.getDay();
    const cell = info.el;

    // 일요일 배경
    if (dayOfWeek === 0) {
      cell.style.backgroundColor = 'rgba(255, 128, 128, 0.06)';
    }
    // 토요일 배경
    else if (dayOfWeek === 6) {
      cell.style.backgroundColor = 'rgba(0, 0, 255, 0.03)';
    }
  },
  eventContent: (info: any) => {
    return { html: info.event.title };
  },
  eventClick: (info: any) => {
    if (info.event.extendedProps.description === 'online') {
      router.push({ path: '/order/list', state: { orderDate: info.event.extendedProps.date } });
    } else if (info.event.extendedProps.description === 'offline') {
      router.push({ path: '/order/offlist', state: { orderDate: info.event.extendedProps.date } });
    }
  },
});

watch(revenueMonthCalendar, newValue => {
  const events = [...newValue.online, ...newValue.offline, ...newValue.sum];
  calendarOptions.events = events;
});

const prevMonth = () => {
  if (selMonth.value === 1) {
    selMonth.value = 12;
    selYear.value--;
  } else {
    selMonth.value--;
  }
  if (viewMode.value === 'calendar') calendarRef.value.getApi().prev();
  getRevenueMonth();
};

const nextMonth = () => {
  if (selMonth.value === 12) {
    selMonth.value = 1;
    selYear.value++;
  } else {
    selMonth.value++;
  }
  if (viewMode.value === 'calendar') calendarRef.value.getApi().next();
  getRevenueMonth();
};

const goToToday = () => {
  if (viewMode.value === 'calendar') calendarRef.value.getApi().today();
  selYear.value = nowDate.value.getFullYear();
  selMonth.value = nowDate.value.getMonth() + 1;
  getRevenueMonth();
};

const changeViewMode = (event: any) => {
  if (event.target.value === 'calendar') {
    const setDate = `${selYear.value}-${String(selMonth.value).length === 1 ? '0' + selMonth.value : selMonth.value}-01`;
    calendarRef.value.getApi().gotoDate(setDate);
  }
  getRevenueMonth();
};

const getRevenueMonth = async () => {
  try {
    let res = await apis.revenue.get_revenue_month(selYear.value, selMonth.value);

    if (viewMode.value === 'calendar') {
      revenueMonthCalendar.online = res.online.map((item: { date: string; total_sales: number }) => ({
        date: item.date,
        title: `<span class="badge text-bg-primary">온라인</span><br><span class="text-dark">${item.total_sales.toLocaleString()}원</span>`,
        extendedProps: {
          description: 'online',
          date: item.date,
        },
        color: 'rgba(55, 125, 255, 0.1);',
      }));

      revenueMonthCalendar.offline = res.offline.map((item: { date: string; total_sales: number }) => ({
        date: item.date,
        title: `<span class="badge text-bg-success">오프라인</span><br><span class="text-dark">${item.total_sales.toLocaleString()}원</span>`,
        extendedProps: {
          description: 'offline',
          date: item.date,
        },
        color: 'rgba(55, 125, 255, 0.1);',
      }));

      const sumByDate: { [date: string]: number } = {};
      for (const item of [...res.offline, ...res.online]) {
        sumByDate[item.date] = (sumByDate[item.date] || 0) + item.total_sales;
      }
      //@ts-ignore
      revenueMonthCalendar.sum = Object.keys(sumByDate).map(date => ({
        date,
        title: `<div class="text-danger text-end">총 : ${sumByDate[date].toLocaleString()}원</div>`,
        extendedProps: {
          description: 'sum',
        },
        color: '',
      }));

      return;
    }

    if (viewMode.value === 'table') {
      const allDates = getAllDatesOfMonth(selYear.value, selMonth.value);

      revenueMonthTable.value = Array.from(allDates).map(date => {
        const onlineItem = res.online.find((item: { date: string }) => item.date === date);
        const offlineItem = res.offline.find((item: { date: string }) => item.date === date);
        const returnObj = {
          date: date,
          onlineSales: onlineItem ? onlineItem.total_sales : 0,
          offlineSales: offlineItem ? offlineItem.total_sales : 0,
          sum: (offlineItem ? offlineItem.total_sales : 0) + (onlineItem ? onlineItem.total_sales : 0),
        };
        return returnObj;
      });
    }
  } catch (error) {
    console.error(error);
  }
};

const getAllDatesOfMonth = (year: number, month: number): string[] => {
  const numDays = new Date(year, month, 0).getDate();
  const datesOfMonth = [];

  for (let i = 1; i <= numDays; i++) {
    const monthString = month < 10 ? '0' + month : month.toString();
    const dayString = i < 10 ? '0' + i : i.toString();
    const dateString = `${year}-${monthString}-${dayString}`;
    datesOfMonth.push(dateString);
  }
  return datesOfMonth;
};

onMounted(() => {
  getRevenueMonth();
  useSearchStore().$reset();
});
</script>

<style scoped></style>
