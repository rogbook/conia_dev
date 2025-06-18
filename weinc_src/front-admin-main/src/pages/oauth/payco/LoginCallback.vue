<template>
  <div></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { showLogConsole } from '@/utils/common-utils';

const code = ref();
const restApiKey = ref('');

onMounted(() => {
  code.value = useRoute().query.code;
  restApiKey.value = import.meta.env.VITE_PAYCO_RESTAPI_KEY;
  issueAccessToken();
});

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

const getTokenInfo = async (access_token: string) => {
  const headers = {
    client_id: restApiKey.value,
    access_token: access_token,
  };

  try {
    const res = await axios.post('/payco-get-token', {}, { headers: headers });
    if (res.status === 200 && res.data.header.isSuccessful) {
      userLogin(res.data.data.member.idNo);
    }
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const userLogin = async (tokenId: string) => {
  window.opener.postMessage({
    tokenId: tokenId,
    sns_type: 'payco',
  });
  window.close();
};
</script>
