<template>
  <PageNavigator :before_link="me ? [] : ['회원조회']" :current="me ? '계정정보' : '회원상세'" />
  <ul class="nav nav-tabs mb-4" role="tablist">
    <li class="nav-item">
      <a class="nav-link active" id="nav-userInfoTab" href="#navTabUser" data-bs-toggle="pill" data-bs-target="#navTabUser" role="tab" aria-controls="navTabUser" aria-selected="true">기본정보</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" id="nav-companyInfoTab" href="#navTabCompany" data-bs-toggle="pill" data-bs-target="#navTabCompany" role="tab" aria-controls="navTabCompany" aria-selected="false">사업자정보</a>
    </li>
    <li class="nav-item" v-if="getUserClass(userInfo.classes).includes('PA') && userInfo.shop_yn === 'Y'">
      <a class="nav-link" id="nav-shopInfoTab" href="#navTabShop" data-bs-toggle="pill" data-bs-target="#navTabShop" role="tab" aria-controls="navTabShop" aria-selected="false" @click.prevent="getShopInfo.getShopInfo()">매장정보</a>
    </li>
  </ul>

  <div class="tab-content" id="navTabUserInfo">
    <div class="tab-pane fade show active" id="navTabUser" role="tabpanel" aria-labelledby="nav-userInfoTab">
      <UserInfo :member="userInfo" :me="me" :classList="classList" @updateFromInfo="updateUserInfo" @updateMemo="updateMemo" @changeClass="changeClass" @linkMember="linkMember" />
    </div>
    <div class="tab-pane fade" id="navTabCompany" role="tabpanel" aria-labelledby="nav-companyInfoTab">
      <CompanyInfo :company="companyInfo" @updateCompanyInfo="updateCompanyInfo" @getUserInfo="getUserInfo" v-if="companyInfo.id" />
      <div v-else>
        <CompanyInfoReg
          :member="userInfo"
          v-if="isShow"
          @getUserInfo="
            () => {
              router.go(0);
            }
          " />
        <div class="card-body" v-else>
          <button type="button" class="btn btn-sm btn-info" @click="showCompanyInfoReg">사업자정보 등록</button>
        </div>
      </div>
    </div>
    <div class="tab-pane fade" id="navTabShop" role="tabpanel" aria-labelledby="nav-shopInfoTab">
      <ShopInfo v-if="userInfo.id && userInfo.shop_yn === 'Y'" :memberId="userInfo.id" ref="getShopInfo" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import UserInfo from '@/components/user/detail/UserInfo.vue';
import CompanyInfo from '@/components/user/detail/CompanyInfo.vue';
import CompanyInfoReg from '@/components/user/detail/CompanyInfoReg.vue';
import ShopInfo from '@/components/user/detail/ShopInfo.vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import type { Company } from 'CompanyInfoModule';
import { useRoute } from 'vue-router';
import type { User, Class } from 'UserInfoModule';
import { apiResponseCheck, showAlert, showLogConsole } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import router from '@/router';

const userInfo = ref({} as User);
const companyInfo = ref({} as Company);
const classList = ref([]);
const memberId = ref();
const companyId = ref();
const me = ref(false);
const isShow = ref(false);
const getShopInfo = ref();

const getUserInfo = async (id: string | undefined) => {
  id = memberId.value;
  if (id === undefined) {
    await apis.user.me().then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        userInfo.value = res;
        companyId.value = userInfo.value.company?.id ? userInfo.value.company!.id : undefined;
        if (companyId.value === undefined) return;
        getCompanyInfo(undefined);
      });
    });
  } else {
    await apis.user.get_user(id, 'member').then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        userInfo.value = res;
        companyId.value = userInfo.value.company?.id ? userInfo.value.company!.id : undefined;
        if (companyId.value === undefined) return;
        getCompanyInfo(companyId.value);
      });
    });
  }
};

const getCompanyInfo = (id: number | string | undefined) => {
  if (id === undefined) {
    // 개인 회사 정보
    apis.company.me().then(res => {
      if (res instanceof AxiosError) {
        const error = res.response?.data;
        if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        return false;
      } else {
        showLogConsole(res);
        companyInfo.value = res;
      }
    });
  } else {
    // 회원 회사 정보
    apis.company.get_company(id).then(res => {
      if (res instanceof AxiosError) {
        const error = res.response?.data;
        if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        return false;
      } else {
        showLogConsole(res);
        companyInfo.value = res;
      }
    });
  }
};

const getClassList = () => {
  apis.user.get_class().then(res => {
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      return false;
    } else {
      showLogConsole(res);
      classList.value = res;
      return true;
    }
  });
};

const getUserClass = (classes: Class[]): string => {
  const types = [];
  if (classes) {
    for (const c of classes) {
      types.push(c.class_code);
    }
  }
  return types.length == 0 ? '-' : types.join(',');
};

const updateUserInfo = (info: object): any => {
  const userClass = getUserClass(userInfo.value.classes);
  if (!companyInfo.value.id && Object.keys(info).includes('status') && !userClass.includes('CM')) {
    showAlert('사업자정보가 없는 회원의 상태를 변경할 수 없습니다.\n사업자 정보를 확인해주세요.', 'warning');
  } else {
    apis.user.mod_user(memberId.value, info).then(res => {
      if (res instanceof AxiosError) {
        const error = res.response?.data;
        if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        return false;
      } else {
        showAlert(Object.keys(info).includes('status') ? '회원 상태가 변경되었습니다.' : '회원 정보가 저장되었습니다.', 'success');
        getUserInfo(memberId.value);
        return true;
      }
    });
  }
};

const updateMemo = (info: object) => {
  apis.user.mod_user(memberId.value, info).then(res => {
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      return false;
    } else {
      showAlert('회원 메모 내용이 수정되었습니다.', 'success');
      getUserInfo(memberId.value);
      return true;
    }
  });
};

const changeClass = (befor_class: string, after_class: string) => {
  if (befor_class === '-') {
    apis.user.link_class(memberId.value, after_class).then(res => {
      if (res instanceof AxiosError) {
        const error = res.response?.data;
        if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        return false;
      } else {
        showAlert('회원 타입이 변경되었습니다.', 'success');
        getUserInfo(memberId.value);
        return true;
      }
    });
  } else {
    apis.user.unlink_class(memberId.value, befor_class).then(res => {
      if (res instanceof AxiosError) {
        const error = res.response?.data;
        if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        return false;
      } else {
        apis.user.link_class(memberId.value, after_class).then(res => {
          apiResponseCheck(res, () => {
            showAlert('회원 타입이 변경되었습니다.', 'success');
            getUserInfo(memberId.value);
            return true;
          });
        });
      }
    });
  }
};

const linkMember = (p_id: number, method: string) => {
  // 회원 연결 해제
  if (method === 'delete') {
    apis.user.unlink_member(memberId.value, p_id).then(res => {
      if (res instanceof AxiosError) {
        const error = res.response?.data;
        if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        return false;
      } else {
        showAlert('회원 연결이 해제되었습니다.', 'success');
        getUserInfo(memberId.value);
        return true;
      }
    });
  }
  // 회원 연결 설정
  else {
    apis.user.link_member(memberId.value, p_id).then(res => {
      if (res instanceof AxiosError) {
        const error = res.response?.data;
        if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        return false;
      } else {
        showAlert('회원 연결이 설정되었습니다.', 'success');
        getUserInfo(memberId.value);
        return true;
      }
    });
  }
};

const updateCompanyInfo = () => {
  apis.company.mod_company(companyInfo.value.id, companyInfo.value).then(res => {
    showLogConsole(res);
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      return false;
    } else {
      showAlert('사업자 정보가 변경되었습니다.', 'success');
      getCompanyInfo(companyId.value);
    }
  });
};

const showCompanyInfoReg = () => {
  isShow.value = !isShow.value;
};

onMounted(() => {
  memberId.value = history.state.id;
  me.value = memberId.value === undefined;
  getUserInfo(memberId.value);
  if (!me.value) {
    getClassList();
  }
});
</script>

<style scoped></style>
