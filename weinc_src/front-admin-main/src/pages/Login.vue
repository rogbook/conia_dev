<template>
  <div class="mx-auto" style="max-width: 30rem">
    <!-- Card -->
    <div class="card card-lg mb-5 mt-10">
      <!-- Content -->
      <RouterLink class="d-flex justify-content-center mt-5" to="/" tabindex="-1">
        <img alt="Image Description" class="zi-2" src="@/assets/images/coniaworld_logo.png" style="width: 10rem" />
      </RouterLink>
      <div class="card-body">
        <!-- Form -->
        <form class="js-validate needs-validation" novalidate @submit.prevent="handleSubmit">
          <div class="text-center">
            <div class="mb-5">
              <h1 class="display-5">코니아 관리자 로그인</h1>
              <p>
                아직 코니아 회원이 아니신가요?
                <RouterLink class="link" to="/join" no-rel tabindex="-1"> 회원가입</RouterLink>
              </p>
            </div>
          </div>

          <!-- Form -->
          <div class="mb-4">
            <label class="form-label" for="signinSrEmail"> 아이디 (이메일주소) </label>
            <input id="signinSrEmail" v-model="form.id" aria-label="email@address.com" class="form-control form-control-lg" placeholder="email@address.com" required tabindex="1" type="email" />
            <span class="invalid-feedback"> 올바른 형식의 이메일 주소를 입력해주세요. </span>
          </div>
          <!-- End Form -->

          <!-- Form -->
          <div class="mb-4">
            <label class="form-label w-100" for="signupSrPassword" tabindex="-1">
              <span class="d-flex justify-content-between align-items-center">
                <span>비밀번호</span>
                <RouterLink class="form-label-link mb-0" to="user/find" tabindex="-1"> 아이디/비밀번호 찾기 </RouterLink>
              </span>
            </label>

            <div class="input-group input-group-merge" data-hs-validation-validate-class>
              <input
                autocomplete="current-password"
                id="signupSrPassword"
                v-model="form.pw"
                aria-label="비밀번호를 입력해주세요."
                class="js-toggle-password form-control form-control-lg"
                data-hs-toggle-password-options='{"target": "#changePassTarget", "defaultClass": "bi-eye-slash", "showClass": "bi-eye", "classChangeTarget": "#changePassIcon"}'
                minlength="1"
                placeholder="비밀번호를 입력해주세요."
                required
                type="password" />
              <a id="changePassTarget" class="input-group-append input-group-text" href="javascript:" tabindex="-1">
                <i id="changePassIcon" class="bi-eye"></i>
              </a>
            </div>

            <span class="invalid-feedback">비밀번호를 확인해주세요.</span>
          </div>
          <!-- End Form -->

          <!-- Form Check -->
          <!-- TODO: 자동로그인 구현? -->
          <div class="form-check mb-4" v-if="false">
            <input id="termsCheckbox" class="form-check-input" type="checkbox" value="" />
            <label class="form-check-label" for="termsCheckbox"> 자동로그인 </label>
          </div>
          <!-- End Form Check -->

          <div class="d-grid">
            <button class="btn btn-primary btn-lg" type="submit">로그인</button>
          </div>
        </form>
        <!-- End Form -->
        <div class="mt-2">
          <div class="text-center">또는 다른 서비스 계정으로 로그인</div>
          <div class="mt-2 d-flex justify-content-center">
            <img src="@/assets/images/sns/payco.png" style="width: 30px; height: 30px; cursor: pointer" class="mx-1" @click.prevent="connectSns('payco')" />
            <img src="@/assets/images/sns/naver.png" style="width: 30px; height: 30px; cursor: pointer" class="mx-1" @click.prevent="connectSns('naver')" />
            <img src="@/assets/images/sns/kakao.png" style="width: 30px; height: 30px; cursor: pointer" class="mx-1" @click.prevent="connectSns('kakao')" />
            <img src="@/assets/images/sns/google.png" style="width: 30px; height: 30px; cursor: pointer" class="mx-1" @click.prevent="connectSns('google')" />
          </div>
        </div>
      </div>
    </div>
    <!-- End Card -->
  </div>
  <!-- End Content -->
</template>

<script setup lang="ts">
import { AxiosError } from 'axios';
import apis from '@/apis';
import { useAuthStore } from '@/stores/auth';
import { onMounted, ref } from 'vue';
import { apiResponseCheck, showAlert } from '@/utils/common-utils';
import { useCommonStore } from '@/stores/common';
import router from '@/router';
import { useRouter } from 'vue-router';

const form = ref({
  id: '',
  pw: '',
});

const connectSns = (type: string) => {
  switch (type) {
    case 'payco':
      connectPayco();
      break;
    case 'naver':
      connectNaver();
      break;
    case 'kakao':
      connectKakao();
      break;
    case 'google':
      connectGoogle();
      break;
  }
};

const connectKakao = async () => {
  const restApiKey = import.meta.env.VITE_KAKAO_RESTAPI_KEY;
  const redirectUri = import.meta.env.VITE_KAKAO_LOGIN_REDIRECT_URI;
  const openUrl = `https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=${restApiKey}&redirect_uri=${redirectUri}`;
  window.addEventListener('message', snsLogin, false);
  window.open(`${openUrl}`, 'oauth-login-form', 'width=500, height=600');
};

const connectNaver = async () => {
  const restApiKey = import.meta.env.VITE_NAVER_RESTAPI_KEY;
  const redirectUri = import.meta.env.VITE_NAVER_LOGIN_REDIRECT_URI;
  const openUrl = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${restApiKey}&redirect_uri=${redirectUri}`;
  window.addEventListener('message', snsLogin, false);
  window.open(`${openUrl}`, 'oauth-login-form', 'width=500, height=600');
};

const connectGoogle = async () => {
  const restApiKey = import.meta.env.VITE_GOOGLE_RESTAPI_KEY;
  const redirectUri = import.meta.env.VITE_GOOGLE_LOGIN_REDIRECT_URI;
  const openUrl = `https://accounts.google.com/o/oauth2/v2/auth?response_type=token&client_id=${restApiKey}&redirect_uri=${redirectUri}&scope=email profile&state=${encodeURI('gState')};`;
  window.addEventListener('message', snsLogin, false);
  window.open(`${openUrl}`, 'oauth-login-form', 'width=500, height=600');
};

const connectPayco = async () => {
  const restApiKey = import.meta.env.VITE_PAYCO_RESTAPI_KEY;
  const redirectUri = import.meta.env.VITE_PAYCO_LOGIN_REDIRECT_URI;
  const openUrl = `https://id.payco.com/oauth2.0/authorize?response_type=code&client_id=${restApiKey}&redirect_uri=${redirectUri}&serviceProviderCode=FRIENDS&userLocale=ko_KR`;
  window.addEventListener('message', snsLogin, false);
  window.open(`${openUrl}`, 'oauth-login-form', 'width=500, height=600');
};

const snsLogin = async (e: any) => {
  await apis.user.sns_login(e.data.sns_type, e.data.tokenId).then(res => {
    apiResponseCheck(res, () => {
      // 로그인 성공 시 JWT 정보 저장
      const login = useAuthStore().login(res.access_token, res.refresh_token);
      Promise.resolve(login).then(() => {
        const menu = useCommonStore().reqMenus();
        Promise.resolve(menu).then(() => {
          router.push('/dashboard');
        });
      });
    });
  });
};

const handleSubmit = async () => {
  await apis.user.login(form.value.id, form.value.pw).then(res => {
    apiResponseCheck(res, () => {
      // 로그인 성공 시 JWT 정보 저장
      const login = useAuthStore().login(res.access_token, res.refresh_token);
      Promise.resolve(login).then(() => {
        const menu = useCommonStore().reqMenus();
        Promise.resolve(menu).then(() => {
          form.value.id = '';
          form.value.pw = '';
          router.push('/dashboard');
        });
      });

      // 로그인 이후 경로 판별
      // if (referer) {
      //    router.push(`${referer}`);
      // } else {
      //    router.push('/dashboard');
      // }
    });
  });
};

onMounted(() => {
  // @ts-ignore
  new HSTogglePassword('.js-toggle-password');

  // @ts-ignore
  HSBsValidation.init('.js-validate');
});
</script>

<style scoped>
html,
body {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}

.form-signin {
  width: 100%;
  max-width: 460px;
  padding: 15px;
  margin: 30px auto;
}

.form-signin .checkbox {
  font-weight: 400;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type='email'] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type='password'] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.bd-placeholder-img {
  font-size: 1.125rem;
  text-anchor: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
}

@media (min-width: 768px) {
  .bd-placeholder-img-lg {
    font-size: 3.5rem;
  }
}
</style>
