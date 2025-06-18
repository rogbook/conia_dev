<template>
  <div class="row mb-6" v-if="false">
    <div class="col-2">
      <!-- Card -->
      <a class="card card-hover-shadow h-100" href="#">
        <div class="card-body">
          <h6 class="card-subtitle">총 회원수</h6>

          <div class="row align-items-center gx-2 mb-1">
            <div class="col-6">
              <h2 class="card-title text-inherit">{{ mDashboardInfo.member_all_cnt }}</h2>
            </div>
            <!-- End Col -->

            <div class="col-6">
              <!-- Chart -->
              <div class="chartjs-custom" v-if="false" style="height: 3rem">
                <canvas
                  class="js-chart"
                  data-hs-chartjs-options='{
                              "type": "line",
                              "data": {
                                 "labels": ["1 May","2 May","3 May","4 May","5 May","6 May","7 May","8 May","9 May","10 May","11 May","12 May","13 May","14 May","15 May","16 May","17 May","18 May","19 May","20 May","21 May","22 May","23 May","24 May","25 May","26 May","27 May","28 May","29 May","30 May","31 May"],
                                 "datasets": [{
                                  "data": [21,20,24,20,18,17,15,17,18,30,31,30,30,35,25,35,35,40,60,90,90,90,85,70,75,70,30,30,30,50,72],
                                  "backgroundColor": ["rgba(55, 125, 255, 0)", "rgba(255, 255, 255, 0)"],
                                  "borderColor": "#377dff",
                                  "borderWidth": 2,
                                  "pointRadius": 0,
                                  "pointHoverRadius": 0
                                }]
                              },
                              "options": {
                                 "scales": {
                                   "y": {
                                     "display": false
                                   },
                                   "x": {
                                     "display": false
                                   }
                                 },
                                "hover": {
                                  "mode": "nearest",
                                  "intersect": false
                                },
                                "plugins": {
                                  "tooltip": {
                                    "postfix": "k",
                                    "hasIndicator": true,
                                    "intersect": false
                                  }
                                }
                              }
                            }'>
                </canvas>
              </div>
              <!-- End Chart -->
            </div>
            <!-- End Col -->
          </div>
          <!-- End Row -->

          <span class="badge bg-soft-success text-success"> <i class="bi-graph-up"></i> 100% </span>
          <span class="text-body fs-6 ms-1">from {{ mDashboardInfo.member_all_cnt }}</span>
        </div>
      </a>
      <!-- End Card -->
    </div>
    <div class="col-2">
      <!-- Card -->
      <a class="card card-hover-shadow h-100" href="#">
        <div class="card-body">
          <h6 class="card-subtitle">오늘 가입한 회원</h6>

          <div class="row align-items-center gx-2 mb-1">
            <div class="col-6">
              <h2 class="card-title text-inherit">{{ mDashboardInfo.member_today_cnt }}</h2>
            </div>
            <!-- End Col -->

            <div class="col-6">
              <!-- Chart -->
              <div class="chartjs-custom" v-if="false" style="height: 3rem">
                <canvas
                  class="js-chart"
                  data-hs-chartjs-options='{
                              "type": "line",
                              "data": {
                                 "labels": ["1 May","2 May","3 May","4 May","5 May","6 May","7 May","8 May","9 May","10 May","11 May","12 May","13 May","14 May","15 May","16 May","17 May","18 May","19 May","20 May","21 May","22 May","23 May","24 May","25 May","26 May","27 May","28 May","29 May","30 May","31 May"],
                                 "datasets": [{
                                  "data": [21,20,24,20,18,17,15,17,18,30,31,30,30,35,25,35,35,40,60,90,90,90,85,70,75,70,30,30,30,50,72],
                                  "backgroundColor": ["rgba(55, 125, 255, 0)", "rgba(255, 255, 255, 0)"],
                                  "borderColor": "#377dff",
                                  "borderWidth": 2,
                                  "pointRadius": 0,
                                  "pointHoverRadius": 0
                                }]
                              },
                              "options": {
                                 "scales": {
                                   "y": {
                                     "display": false
                                   },
                                   "x": {
                                     "display": false
                                   }
                                 },
                                "hover": {
                                  "mode": "nearest",
                                  "intersect": false
                                },
                                "plugins": {
                                  "tooltip": {
                                    "postfix": "k",
                                    "hasIndicator": true,
                                    "intersect": false
                                  }
                                }
                              }
                            }'>
                </canvas>
              </div>
              <!-- End Chart -->
            </div>
            <!-- End Col -->
          </div>
          <!-- End Row -->

          <span class="badge bg-soft-success text-success"> <i class="bi-graph-up"></i> {{ todayMemberPercent }}% </span>
          <span class="text-body fs-6 ms-1">from {{ mDashboardInfo.member_today_cnt }}</span>
        </div>
      </a>
      <!-- End Card -->
    </div>
    <div class="col-2">
      <!-- Card -->
      <a class="card card-hover-shadow h-100" href="#">
        <div class="card-body">
          <h6 class="card-subtitle">총 주문 건수</h6>

          <div class="row align-items-center gx-2 mb-1">
            <div class="col-6">
              <h2 class="card-title text-inherit">{{ mDashboardInfo.order_all_cnt }}</h2>
            </div>
            <!-- End Col -->

            <div class="col-6">
              <!-- Chart -->
              <div class="chartjs-custom" v-if="false" style="height: 3rem">
                <canvas
                  class="js-chart"
                  data-hs-chartjs-options='{
                              "type": "line",
                              "data": {
                                 "labels": ["1 May","2 May","3 May","4 May","5 May","6 May","7 May","8 May","9 May","10 May","11 May","12 May","13 May","14 May","15 May","16 May","17 May","18 May","19 May","20 May","21 May","22 May","23 May","24 May","25 May","26 May","27 May","28 May","29 May","30 May","31 May"],
                                 "datasets": [{
                                  "data": [21,20,24,20,18,17,15,17,18,30,31,30,30,35,25,35,35,40,60,90,90,90,85,70,75,70,30,30,30,50,72],
                                  "backgroundColor": ["rgba(55, 125, 255, 0)", "rgba(255, 255, 255, 0)"],
                                  "borderColor": "#377dff",
                                  "borderWidth": 2,
                                  "pointRadius": 0,
                                  "pointHoverRadius": 0
                                }]
                              },
                              "options": {
                                 "scales": {
                                   "y": {
                                     "display": false
                                   },
                                   "x": {
                                     "display": false
                                   }
                                 },
                                "hover": {
                                  "mode": "nearest",
                                  "intersect": false
                                },
                                "plugins": {
                                  "tooltip": {
                                    "postfix": "k",
                                    "hasIndicator": true,
                                    "intersect": false
                                  }
                                }
                              }
                            }'>
                </canvas>
              </div>
              <!-- End Chart -->
            </div>
            <!-- End Col -->
          </div>
          <!-- End Row -->

          <span class="badge bg-soft-success text-success"> <i class="bi-graph-up"></i> 100% </span>
          <span class="text-body fs-6 ms-1">from {{ mDashboardInfo.order_today_cnt }}</span>
        </div>
      </a>
      <!-- End Card -->
    </div>
    <div class="col-2">
      <!-- Card -->
      <a class="card card-hover-shadow h-100" href="#">
        <div class="card-body">
          <h6 class="card-subtitle">오늘 주문 건수</h6>

          <div class="row align-items-center gx-2 mb-1">
            <div class="col-6">
              <h2 class="card-title text-inherit">{{ mDashboardInfo.order_today_cnt }}</h2>
            </div>
            <!-- End Col -->

            <div class="col-6">
              <!-- Chart -->
              <div class="chartjs-custom" v-if="false" style="height: 3rem">
                <canvas
                  class="js-chart"
                  data-hs-chartjs-options='{
                              "type": "line",
                              "data": {
                                 "labels": ["1 May","2 May","3 May","4 May","5 May","6 May","7 May","8 May","9 May","10 May","11 May","12 May","13 May","14 May","15 May","16 May","17 May","18 May","19 May","20 May","21 May","22 May","23 May","24 May","25 May","26 May","27 May","28 May","29 May","30 May","31 May"],
                                 "datasets": [{
                                  "data": [21,20,24,20,18,17,15,17,18,30,31,30,30,35,25,35,35,40,60,90,90,90,85,70,75,70,30,30,30,50,72],
                                  "backgroundColor": ["rgba(55, 125, 255, 0)", "rgba(255, 255, 255, 0)"],
                                  "borderColor": "#377dff",
                                  "borderWidth": 2,
                                  "pointRadius": 0,
                                  "pointHoverRadius": 0
                                }]
                              },
                              "options": {
                                 "scales": {
                                   "y": {
                                     "display": false
                                   },
                                   "x": {
                                     "display": false
                                   }
                                 },
                                "hover": {
                                  "mode": "nearest",
                                  "intersect": false
                                },
                                "plugins": {
                                  "tooltip": {
                                    "postfix": "k",
                                    "hasIndicator": true,
                                    "intersect": false
                                  }
                                }
                              }
                            }'>
                </canvas>
              </div>
              <!-- End Chart -->
            </div>
            <!-- End Col -->
          </div>
          <!-- End Row -->

          <span class="badge bg-soft-success text-success"> <i class="bi-graph-up"></i> {{ todayOrderPercent }}% </span>
          <span class="text-body fs-6 ms-1">from {{ mDashboardInfo.order_today_cnt }}</span>
        </div>
      </a>
      <!-- End Card -->
    </div>
  </div>
  <!-- <div class="row text-center">
    <div class="col-lg-3 col-sm-6 mb-5 mb-lg-0">
      <div
        class="js-counter h1 mb-1"
        data-hs-counter-options='{
           "isCommaSeparated": true
         }'>
        {{ mDashboardInfo.member_all_cnt }}
      </div>
      <span>총 회원 수</span>
    </div>

    <div class="col-lg-3 col-sm-6 mb-5 mb-lg-0">
      <div
        class="js-counter h1 mb-1"
        data-hs-counter-options='{
           "isCommaSeparated": true
         }'>
        {{ mDashboardInfo.member_today_cnt }}
      </div>
      <span>오늘 가입 회원 수</span>
    </div>

    <div class="col-lg-3 col-sm-6 mb-5 mb-lg-0">
      <div
        class="js-counter h1 mb-1"
        data-hs-counter-options='{
           "isCommaSeparated": true
         }'>
        {{ mDashboardInfo.order_all_cnt }}
      </div>
      <span>총 주문 건수</span>
    </div>

    <div class="col-lg-3 col-sm-6 mb-5 mb-lg-0">
      <div
        class="js-counter h1 mb-1"
        data-hs-counter-options='{
           "isCommaSeparated": true
         }'
        v-text="mDashboardInfo.order_today_cnt"></div>
      <span>오늘 주문 건수</span>
    </div>
  </div> -->

  <div class="row">
    <!-- 공지사항 -->
    <div class="col-lg-6 mb-3">
      <!-- Card -->
      <div class="card">
        <!-- Header -->
        <div class="card-header card-header-content-between py-1">
          <h4 class="card-header-title">공지사항</h4>
          <a class="btn btn-ghost-secondary btn-sm" @click.prevent="router.push({ path: `/community/notice` })">전체보기</a>
        </div>
        <!-- End Header -->

        <!-- Body -->
        <div class="card-body">
          <div class="table-responsive datatable-custom position-relative">
            <table class="table table-lg table-thead-bordered table-nowrap table-align-middle card-table">
              <thead class="thead-light">
                <tr class="text-center">
                  <th>제목</th>
                  <th>대상</th>
                  <th>표시대상 상점</th>
                  <th>등록일</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center" v-for="(item, i) in noticeList.datas" :key="item.id" @click.prevent="router.push({ path: `/community/notice/detail`, state: { id: item.id } })">
                  <td>
                    <a class="text-decoration-underline" href="" @click.prevent="router.push({ path: `/community/notice/detail`, state: { id: item.id } })" style="color: #0b1328 !important; text-decoration-color: #0b1328 !important">{{ item.title }}</a>
                  </td>
                  <td>{{ convertPartner(item.target) }}</td>
                  <td>{{ !item.store_code ? '없음' : item.store?.title }}</td>
                  <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
                </tr>
                <tr v-if="noticeList.total === 0">
                  <td colspan="4" class="text-center">표시할 항목이 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <!-- End Body -->
      </div>
      <!-- End Card -->
    </div>
    <!-- End 공지사항 -->
    <!-- FAQ -->
    <div class="col-lg-6 mb-3">
      <!-- Card -->
      <div class="card">
        <!-- Header -->
        <div class="card-header card-header-content-between py-1">
          <h4 class="card-header-title">FAQ</h4>
          <a class="btn btn-ghost-secondary btn-sm" @click.prevent="router.push({ path: `/community/faq` })">전체보기</a>
        </div>
        <!-- End Header -->

        <!-- Body -->
        <div class="card-body">
          <!-- Nav -->
          <div class="category-area">
            <ul class="nav nav-segment nav-pills mb-4" role="tablist">
              <li class="nav-item" v-for="(cate, i) in Object.keys(faqCateList)" :key="JSON.stringify(cate)">
                <a class="nav-link" :id="`nav-${convertID(cate)}-tab`" :href="`#nav-${convertID(cate)}`" data-bs-toggle="pill" :data-bs-target="`#nav-${convertID(cate)}`" role="tab" :aria-controls="`#nav-${convertID(cate)}`" aria-selected="true" :class="{ active: i === 0 }">{{
                  cate
                }}</a>
              </li>
            </ul>
          </div>
          <!-- End Nav -->

          <!-- Tab Content -->
          <div class="tab-content" v-for="(cate, i) in Object.keys(faqCateList)" :key="JSON.stringify(cate)">
            <div class="tab-pane fade show" :id="`nav-${convertID(cate)}`" role="tabpanel" :aria-labelledby="`nav-${convertID(cate)}-tab`" :class="{ active: i === 0 }">
              <div class="accordion" :id="`faqList-${convertID(cate)}-${i}`">
                <div class="accordion-item" v-for="(faq, i) in faqCateList[cate]" :key="JSON.stringify(faq)">
                  <div class="accordion-header" :id="`${faq.id}`">
                    <a class="accordion-button" role="button" data-bs-toggle="collapse" :data-bs-target="`#faq_content_${convertID(cate)}_${i}`" aria-expanded="true" :aria-controls="`#faq_content_${convertID(cate)}_${i}`"> Q. {{ faq.title }} </a>
                  </div>
                  <div :id="`faq_content_${convertID(cate)}_${i}`" class="accordion-collapse collapse" :aria-labelledby="`${faq.id}`" :data-bs-parent="`#faqList-${convertID(cate)}-${i}`">
                    <div class="accordion-body">
                      A.
                      <div v-html="faq.contents"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- End Body -->
      </div>
      <!-- End Card -->
    </div>
    <!-- End FAQ -->
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { computed, onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import { apiResponseCheck, dateTimeFormatConverter, showLogConsole, getUserClassStr, convertPartner } from '@/utils/common-utils';
import type { NoticeInfoList } from 'BoardInfoModule';
import type { FaqInfo } from 'BoardInfoModule';
import { useSearchStore } from '@/stores/search';
const router = useRouter();

const noticeList = ref({} as NoticeInfoList);
const getNoticeList = (target: string = '') => {
  let query = '';
  query = query.concat(`target=${target}&`);

  if (target === 'partner') {
    query = query.concat(`sub_target=${getUserClassStr.value}&`);
  }

  apis.community.get_notice_list(query, 0, 5).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      noticeList.value.datas = res.datas;
      noticeList.value.total = res.total;
    });
  });
};

const faqList = ref([] as FaqInfo[]);
const faqCateList = ref({} as any);
const getFaqList = (target: string = '') => {
  let query = '';
  query = query.concat(`target=${target}&`);
  apis.community.get_faq_list(query).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      faqList.value = res;
      makeFaqCateList();
    });
  });
};

const convertID = (id: string) => {
  return id.replace('/', '-');
};

const makeFaqCateList = () => {
  if (faqList.value.length > 0) {
    for (const faq of faqList.value) {
      if (Object.keys(faqCateList.value).includes(faq.category)) {
        if (faqCateList.value[faq.category].length < 5) {
          faqCateList.value[faq.category].push(faq);
        }
      } else {
        faqCateList.value[faq.category] = [faq];
      }
    }
  }
};

const linkRef = ref();
const mDashboardInfo = reactive({
  member_all_cnt: 0,
  member_today_cnt: 0,
  order_all_cnt: 0,
  order_today_cnt: 0,
});

const todayMemberPercent = computed(() => {
  return (mDashboardInfo.member_today_cnt / mDashboardInfo.member_all_cnt) * 100;
});

const todayOrderPercent = computed(() => {
  return (mDashboardInfo.order_today_cnt / mDashboardInfo.order_all_cnt) * 100;
});

const getDashboardData = () => {
  apis.dashboard.get_dashboard_data().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mDashboardInfo.member_all_cnt = res.member_all_cnt;
      mDashboardInfo.order_all_cnt = res.order_all_cnt;
      mDashboardInfo.member_today_cnt = res.member_today_cnt;
      mDashboardInfo.order_today_cnt = res.order_today_cnt;
    });
  });
};

onMounted(() => {
  useSearchStore().$reset();
  getDashboardData();
  if (getUserClassStr.value.includes('CM')) {
    getNoticeList('admin');
    getFaqList('admin');
  } else {
    getNoticeList('partner');
    getFaqList('partner');
  }
});
</script>

<style scoped></style>
