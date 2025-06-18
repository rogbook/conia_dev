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
const restApiKey = ref('');

onMounted(() => {
  code.value = useRoute().query.code;
  restApiKey.value = import.meta.env.VITE_PAYCO_RESTAPI_KEY;
  getUserInfo();
  issueAccessToken();
});

const getUserInfo = async () => {
  await apis.user.me().then(res => {
    apiResponseCheck(res, () => {
      userInfo.value = res;
    });
  });
};

const issueAccessToken = async () => {
  const clientSecret = import.meta.env.VITE_PAYCO_CLIENT_SECRET_KEY;
  const headers = {
    'Content-type': `application/x-www-form-urlencoded;charset=utf-8`,
  };
  const params = {
    grant_type: 'authorization_code',
    client_id: restApiKey.value,
    client_secret: clientSecret,
    code: code.value,
  };

  try {
    const res = await axios.post('/payco-issue-token', params, { headers: headers });
    if (res.status === 200) {
      getTokenInfo(res.data.access_token);
    }
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const getTokenInfo = async (accessToken: string) => {
  const headers = {
    client_id: restApiKey.value,
    access_token: accessToken,
  };

  try {
    const res = await axios.post('/payco-get-token', {}, { headers: headers });

    if (res.status === 200 && res.data.header.isSuccessful) {
      modUserInfo(res.data.data.member.idNo);
    }
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const modUserInfo = (tokenId: string) => {
  let data = {} as any;
  data['sns_payco'] = tokenId;

  const userId = undefined;

  apis.user.mod_user(userId, data).then(res => {
    apiResponseCheck(res, () => {
      window.opener.postMessage({});
      window.close();
    });
  });
};
</script>
