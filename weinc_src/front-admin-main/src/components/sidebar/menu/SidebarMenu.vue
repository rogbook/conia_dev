<template>
  <!-- 좌측 메뉴 -->
  <div class="navbar-vertical-content">
    <div id="navbarVerticalMenu" class="nav nav-pills nav-vertical card-navbar-nav">
      <!-- 상품/재고 메뉴 -->
      <div class="menu_depth_1" v-if="checkMenu(1, '상품/재고')">
        <span class="dropdown-header mt-4">상품/재고</span>
        <small class="bi-three-dots nav-subtitle-replacer"></small>
        <div id="navbarVerticalProductMenu">
          <div class="nav-item">
            <a class="nav-link dropdown-toggle" href="#navProductMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navProductMenu" aria-expanded="false" aria-controls="navProductMenu">
              <i class="bi-minecart nav-icon"></i>
              <span class="nav-link-title">상품/재고</span>
            </a>
            <div id="navProductMenu" class="nav-collapse collapse" data-bs-parent="#navbarVerticalProductMenu">
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/product/list" v-if="checkMenu(2, '상품조회 및 수정')">상품조회 및 수정 </RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/product/reg" v-if="checkMenu(2, '상품등록')">상품등록</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/product/category" v-if="checkMenu(2, '카테고리설정')">카테고리설정</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/product/brand" v-if="checkMenu(2, '브랜드설정')">브랜드설정</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/product/catalog" v-if="checkMenu(2, '카탈로그설정')">카탈로그설정</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/product/req/list" v-if="checkMenu(2, '상품요청')">상품요청</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/product/qna" v-if="checkMenu(2, '상품문의관리')">상품문의관리</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/product/review" v-if="checkMenu(2, '상품리뷰관리')">상품리뷰관리</RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- 주문/배송 메뉴 -->
      <div class="menu_depth_1" v-if="checkMenu(1, '주문/배송')">
        <span class="dropdown-header mt-4">주문/배송</span>
        <small class="bi-three-dots nav-subtitle-replacer"></small>

        <div id="navbarVerticalOrderMenu">
          <div class="nav-item">
            <a class="nav-link dropdown-toggle" href="#navOrdersMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navOrdersMenu" aria-expanded="false" aria-controls="navOrdersMenu">
              <i class="bi-airplane nav-icon"></i>
              <span class="nav-link-title">주문/배송</span>
            </a>
            <div id="navOrdersMenu" class="nav-collapse collapse" data-bs-parent="#navbarVerticalOrderMenu">
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/order/list" v-if="checkMenu(2, '주문관리')">주문관리</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/order/exre/list" v-if="checkMenu(2, '교환/반품 관리')">교환/반품 관리</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/order/refund" v-if="checkMenu(2, '관리자 환불내역')">관리자 환불내역</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/order/offlist" v-if="checkMenu(2, '오프라인 매출관리') && checkPermission('read:revenue_offline')">오프라인 매출관리</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/order/sales" v-if="checkMenu(2, '매출현황') && checkPermission('read:revenue_month')">매출현황</RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- 상점 메뉴 -->
      <div class="menu_depth_1" v-if="checkMenu(1, '상점')">
        <span class="dropdown-header mt-4">상점</span>
        <small class="bi-three-dots nav-subtitle-replacer"></small>

        <div id="navbarVerticalCommissionMenu">
          <a class="nav-link dropdown-toggle" href="#navCommissionMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navCommissionMenu" aria-expanded="false" aria-controls="navCommissionMenu">
            <i class="bi-shop nav-icon"></i>
            <span class="nav-link-title">상점</span>
          </a>
          <div id="navCommissionMenu" class="nav-collapse collapse" data-bs-parent="#navbarVerticalCommissionMenu">
            <RouterLink @click.prevent="resetSearch" class="nav-link" to="/store/list" v-if="checkMenu(2, '상점 관리') && getUserClassStr.includes('CM')">상점 관리</RouterLink>
            <RouterLink @click.prevent="resetSearch" class="nav-link" :to="useUserStore().user?.store_code ? { path: `/store/detail`, state: { code: useUserStore().user?.store_code } } : `/store/reg`" v-if="!getUserClassStr.includes('CM') && checkMenu(2, '상점 관리')"
              >상점 관리</RouterLink
            >
            <RouterLink @click.prevent="resetSearch" class="nav-link" to="/store/qna" v-if="checkMenu(2, '통합 고객 문의 관리') && getUserClassStr.includes('CM')">통합 고객 문의 관리</RouterLink>
          </div>
        </div>
      </div>

      <!-- 회원 메뉴 -->
      <div class="menu_depth_1" v-if="checkMenu(1, '회원')">
        <span class="dropdown-header mt-4">회원</span>
        <small class="bi-three-dots nav-subtitle-replacer"></small>

        <div id="navbarVerticalUserMenu">
          <div class="nav-item">
            <a class="nav-link dropdown-toggle" href="#navUserMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navUserMenu" aria-expanded="false" aria-controls="navUserMenu">
              <i class="bi-people nav-icon"></i>
              <span class="nav-link-title">회원</span>
            </a>
            <div id="navUserMenu" class="nav-collapse collapse" data-bs-parent="#navbarVerticalUserMenu">
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/user/myinfo" v-if="checkMenu(2, '계정정보') && useUserStore().user?.id > 3">계정정보</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/user/list" v-if="checkMenu(2, '회원조회')">회원조회</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/user/hierarchy" v-if="useUserStore().user.admin === 'Y'">회원계층</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/customer" v-if="checkMenu(2, '고객 회원 관리')">고객 회원 관리</RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- 정산 메뉴 (2차개발예정) -->
      <div class="menu_depth_1" v-if="checkMenu(1, '정산')">
        <span class="dropdown-header mt-4">정산</span>
        <small class="bi-three-dots nav-subtitle-replacer"></small>

        <div id="navbarVerticalCalculateMenu">
          <div class="nav-item">
            <a class="nav-link dropdown-toggle" href="#navCalculateMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navCalculateMenu" aria-expanded="false" aria-controls="navCalculateMenu">
              <i class="bi-calculator nav-icon"></i>
              <span class="nav-link-title">정산</span>
            </a>
            <div id="navCalculateMenu" class="nav-collapse collapse" data-bs-parent="#navbarVerticalCalculateMenu">
              <div class="nav-item" v-if="checkMenu(2, '수수료 관리')">
                <a class="nav-link dropdown-toggle" href="#navProductCommissionMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navProductCommissionMenu" aria-expanded="false" aria-controls="navProductCommissionMenu"> 수수료 관리 </a>
                <div id="navProductCommissionMenu" class="nav-collapse collapse" data-bs-parent="#navProductMenu">
                  <RouterLink
                    @click.prevent="resetSearch"
                    class="nav-link"
                    :to="{ name: 'partnerCommission', state: { memberId: useUserStore().user.id, memberInfo: { name: useUserStore().user.name }, storeCode: useUserStore().user.store_code } }"
                    v-if="checkMenu(3, '수수료 설정') && !getUserClassStr.includes('CM')">
                    수수료 설정
                  </RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/commission/member" v-if="checkMenu(3, '회원 수수료 설정')">회원 수수료 설정</RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" :to="{ name: 'shipMemberPaList', state: { memberId: 1, name: '코니아', email: '' } }" v-if="checkMenu(3, '배송비 수수료 설정') && checkPermission('read:commission_conia')">배송비 수수료 설정</RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/commission/cmc" v-if="checkMenu(3, '코니아 수수료 설정') && checkPermission('read:commission_conia')">코니아 수수료 설정</RouterLink>
                </div>
              </div>
              <div class="nav-item" v-if="checkMenu(2, '정산 관리')">
                <a class="nav-link dropdown-toggle" href="#navProductSettlementMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navProductSettlementMenu" aria-expanded="false" aria-controls="navProductSettlementMenu">정산 관리</a>
                <div id="navProductSettlementMenu" class="nav-collapse collapse" data-bs-parent="#navProductMenu">
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/settlement/member" v-if="getUserClassStr.includes('CM') && checkMenu(3, '정산내역')">정산내역</RouterLink>
                  <RouterLink
                    @click.prevent="resetSearch"
                    class="nav-link"
                    :to="{ name: 'settlementList', state: { memberId: useUserStore().user.id, name: useUserStore().user.name, email: useUserStore().user.email } }"
                    v-if="!getUserClassStr.includes('CM') && checkMenu(3, '정산내역')">
                    정산내역
                  </RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/settlement/excel" v-if="checkMenu(3, '정산내역 엑셀요청관리')">정산내역 엑셀요청관리</RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/settlement/ship" v-if="getUserClassStr.includes('CM') && checkMenu(3, '배송비 정산내역')">배송비 정산내역</RouterLink>
                  <RouterLink
                    @click.prevent="resetSearch"
                    class="nav-link"
                    :to="{ name: 'settlementShipList', state: { memberId: userStore.user.id, name: useUserStore().user.name, email: useUserStore().user.email } }"
                    v-if="!getUserClassStr.includes('CM') && checkMenu(3, '배송비 정산내역')">
                    배송비 정산내역
                  </RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" :to="{ name: 'settlementConia', state: { memberId: 1, name: '코니아', email: '' } }" v-if="getUserClassStr.includes('CM') && checkMenu(3, '코니아 정산내역')">코니아 정산내역</RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" :to="{ name: 'settlementShipConia', state: { memberId: 1, name: '코니아', email: '' } }" v-if="getUserClassStr.includes('CM') && checkMenu(3, '코니아 배송비 정산내역')">코니아 배송비 정산내역</RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" :to="{ name: 'settlementPG', state: { memberId: 1, name: '코니아', email: '' } }" v-if="useUserStore().user.id === 1">PG 정산내역</RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" :to="{ name: 'settlementPgShip', state: { memberId: 1, name: '코니아', email: '' } }" v-if="useUserStore().user.id === 1">PG 배송비 정산내역</RouterLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 마케팅 메뉴 (2차개발예정) -->
      <div class="menu_depth_1" v-if="checkMenu(1, '마케팅')">
        <span class="dropdown-header mt-4">마케팅</span>
        <small class="bi-three-dots nav-subtitle-replacer"></small>

        <div id="navbarVerticalMarketingMenu">
          <div class="nav-item">
            <a class="nav-link dropdown-toggle" href="#navMarketingMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navMarketingMenu" aria-expanded="false" aria-controls="navMarketingMenu">
              <i class="bi-cash-coin nav-icon"></i>
              <span class="nav-link-title">마케팅</span>
            </a>
            <div id="navMarketingMenu" class="nav-collapse collapse" data-bs-parent="#navbarVerticalMarketingMenu">
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/marketing/coupon" v-if="checkMenu(2, '쿠폰관리')">쿠폰관리</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/marketing/acoupon" v-if="checkMenu(2, '자동발급쿠폰관리')">자동발급쿠폰관리</RouterLink>
              <!--              <RouterLink class="nav-link" to="/marketing/message">메시지관리</RouterLink>-->
            </div>
          </div>
        </div>
      </div>

      <!-- 권한 메뉴 -->
      <div class="menu_depth_1" v-if="checkMenu(1, '권한') && checkPermission('read:commission')">
        <span class="dropdown-header mt-4">권한</span>
        <small class="bi-three-dots nav-subtitle-replacer"></small>
        <div id="navbarVerticalPermissionMenu">
          <div class="nav-item">
            <a class="nav-link dropdown-toggle" href="#navPermissionMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navPermissionMenu" aria-expanded="false" aria-controls="navPermissionMenu">
              <i class="bi-key nav-icon"></i>
              <span class="nav-link-title">권한</span>
            </a>
            <div id="navPermissionMenu" class="nav-collapse collapse" data-bs-parent="#navbarVerticalPermissionMenu">
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/permission/type" v-if="checkMenu(2, '타입별 권한설정') && checkPermission('read:commission')">타입별 권한설정</RouterLink>
              <div class="nav-item" v-if="checkMenu(2, '권한설정') && checkPermission('read:commission')">
                <a class="nav-link dropdown-toggle" href="#navPermissionMemberMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navPermissionMemberMenu" aria-expanded="false" aria-controls="navPermissionMemberMenu">권한설정</a>
                <div id="navPermissionMemberMenu" class="nav-collapse collapse" data-bs-parent="#navOrdersMenu">
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/permission/member/list" v-if="checkMenu(3, '개별권한설정') && checkPermission('read:commission')">개별권한설정</RouterLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 운영지원 메뉴 -->
      <div class="menu_depth_1" v-if="checkMenu(1, '운영지원')">
        <span class="dropdown-header mt-4">운영지원</span>
        <small class="bi-three-dots nav-subtitle-replacer"></small>

        <div id="navbarVerticalCommunityMenu">
          <div class="nav-item">
            <a class="nav-link dropdown-toggle" href="#navUserMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navCommunityMenu" aria-expanded="false" aria-controls="navCommunityMenu">
              <i class="bi-people nav-icon"></i>
              <span class="nav-link-title">운영지원</span>
            </a>
            <div id="navCommunityMenu" class="nav-collapse collapse" data-bs-parent="#navbarVerticalCommunityMenu">
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/community/notice" v-if="checkMenu(2, '공지사항')">공지사항</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/community/qna" v-if="checkMenu(2, '1:1문의')">1:1문의</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/community/faq" v-if="checkMenu(2, 'FAQ')">FAQ</RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- 설정 메뉴 -->
      <div class="menu_depth_1" v-if="checkMenu(1, '설정')">
        <span class="dropdown-header mt-4">설정</span>
        <small class="bi-three-dots nav-subtitle-replacer"></small>

        <div id="navbarVerticalSettingMenu">
          <div class="nav-item">
            <a class="nav-link dropdown-toggle" href="#navSettingMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navSettingMenu" aria-expanded="false" aria-controls="navSettingMenu">
              <i class="bi bi-gear nav-icon"></i>
              <span class="nav-link-title">설정</span>
            </a>
            <div id="navSettingMenu" class="nav-collapse collapse" data-bs-parent="#navbarVerticalSettingMenu">
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/setting/product/common" v-if="checkMenu(2, '상품공통정보관리')">상품공통정보관리</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/setting/product/option" v-if="checkMenu(2, '상품옵션관리')">상품옵션관리</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/setting/product/badge" v-if="checkMenu(2, '상품배지관리')">상품배지관리</RouterLink>
              <RouterLink @click.prevent="resetSearch" class="nav-link" to="/setting/shipping" v-if="checkMenu(2, '배송그룹설정')">배송그룹설정</RouterLink>
              <div class="nav-item" v-if="checkMenu(2, '운영지원 관리')">
                <a class="nav-link dropdown-toggle" href="#navSettingCommunityMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navSettingCommunityMenu" aria-expanded="false" aria-controls="navSettingCommunityMenu">운영지원 관리</a>
                <div id="navSettingCommunityMenu" class="nav-collapse collapse" data-bs-parent="#navSettingMenu">
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/setting/community/qna" v-if="checkMenu(3, '1:1문의 관리')">1:1문의 관리</RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/setting/community/notice" v-if="checkMenu(3, '공지사항 관리')">공지사항 관리</RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/setting/community/faq" v-if="checkMenu(3, 'FAQ 관리')">FAQ 관리</RouterLink>
                </div>
              </div>
              <div class="nav-item" v-if="useUserStore().user.id === 1">
                <a class="nav-link dropdown-toggle" href="#navSettingMasterMenu" role="button" data-bs-toggle="collapse" data-bs-target="#navSettingMasterMenu" aria-expanded="false" aria-controls="navSettingMasterMenu">환경설정 관리</a>
                <div id="navSettingMasterMenu" class="nav-collapse collapse" data-bs-parent="#navSettingMenu">
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/setting/sv">SettingValue 관리</RouterLink>
                  <RouterLink @click.prevent="resetSearch" class="nav-link" to="/setting/ov">OptionValue 관리</RouterLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <p class="fs-6 mb-0 text-center pt-4">
    <span class="d-none d-sm-inline-block">Copyright © ConiaLab Corp. <br />All rights reserved.</span>
  </p>
</template>

<script setup lang="ts">
import { apiResponseCheck, checkPermission, getUserClassStr, showLogConsole } from '@/utils/common-utils';
import { useUserStore } from '@/stores/user';
import { onBeforeMount, onMounted, ref } from 'vue';
import apis from '@/apis';
import type { MenuInfo } from 'MenuInfoModule';
import { useRoute, useRouter } from 'vue-router';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';
const userStore = useUserStore();
const menuInfo = ref({} as MenuInfo);

const resetSearch = () => {
  useSearchStore().$reset();
};

const checkMenu = (depth: number, menu_name: string): boolean => {
  if (depth === 1 && menuInfo.value.depth1)
    return menuInfo.value.depth1.some(m => {
      return m.name === menu_name;
    });
  if (depth === 2 && menuInfo.value.depth2)
    return menuInfo.value.depth2.some(m => {
      return m.name === menu_name;
    });
  if (depth === 3 && menuInfo.value.depth3)
    return menuInfo.value.depth3.some(m => {
      return m.name === menu_name;
    });

  return false;
};

onMounted(() => {
  showLogConsole('onMounted() called');
  showLogConsole(useRoute().path);
  menuInfo.value = useCommonStore().getMenus as MenuInfo;

  Promise.resolve(menuInfo.value).then(res => {
    setTimeout(() => {
      //@ts-ignore
      new HSSideNav('.js-navbar-vertical-aside').init();
    }, 300);
  });
});
</script>

<style scoped>
.router-link-active {
  color: #000000 !important;
  background-color: #ededed !important;
}
</style>
