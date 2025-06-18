<template>
  <div></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { showLogConsole } from '@/utils/common-utils';

const router = useRouter();
const code = ref();

onMounted(() => {
  code.value = useRoute().query.code;
  issueAccessToken();
});

const issueAccessToken = async () => {
  const restApiKey = import.meta.env.VITE_KAKAO_RESTAPI_KEY;
  const clientSecret = import.meta.env.VITE_KAKAO_CLIENT_SECRET_KEY;
  const redirectUri = import.meta.env.VITE_OAUTH_REDIRECT_URI;
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
      showLogConsole(res.data.id);
      userLogin(res.data.id);
    }
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const userLogin = async (tokenId: string) => {
  window.opener.postMessage({
    tokenId: tokenId,
    sns_type: 'kakao',
  });
  window.close();
};
</script>
