<template>
  <div></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import apis from '@/apis';
import type { User } from 'UserInfoModule';
const userInfo = ref({} as User);
import { apiResponseCheck, showLogConsole } from '@/utils/common-utils';

const code = ref();

onMounted(() => {
  code.value = useRoute().query.code;
  getUserInfo();
  issueAccessToken();
});

const getUserInfo = async () => {
  await apis.user.me().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      userInfo.value = res;
    });
  });
};

const issueAccessToken = async () => {
  const restApiKey = import.meta.env.VITE_KAKAO_RESTAPI_KEY;
  const clientSecret = import.meta.env.VITE_KAKAO_CLIENT_SECRET_KEY;
  const redirectUri = import.meta.env.VITE_KAKAO_CONNECT_REDIRECT_URI;
  const headers = {
    'Content-type': `application/x-www-form-urlencoded;charset=utf-8`,
  };
  const params = {
    grant_type: 'authorization_code',
    client_id: restApiKey,
    client_secret: clientSecret,
    redirectUri: redirectUri,
    code: code.value,
  };

  try {
    const res = await axios.post('https://kauth.kakao.com/oauth/token', params, { headers: headers });
    if (res.status === 200) {
      getTokenInfo(res.data.access_token);
    }
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const getTokenInfo = async (access_token: string) => {
  const headers = {
    Authorization: `Bearer ${access_token}`,
  };

  try {
    const res = await axios.get('https://kapi.kakao.com/v1/user/access_token_info', { headers: headers });
    if (res.status === 200) {
      modUserInfo(res.data.id);
    }
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const modUserInfo = (tokenId: string) => {
  let data = {} as any;
  data['sns_kakao'] = tokenId;

  const userId = undefined;

  apis.user.mod_user(userId, data).then(res => {
    apiResponseCheck(res, () => {
      window.opener.postMessage({});
      window.close();
    });
  });
};
</script>
