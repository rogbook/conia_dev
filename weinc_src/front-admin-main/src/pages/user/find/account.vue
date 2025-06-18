<template>
  <div class="mx-auto" style="max-width: 30rem">
    <!-- Card -->
    <div class="card card-lg mb-5">
      <div class="card-body text-center">
        <div class="text-center">
          <div class="mb-5">
            <h1 class="display-5">아이디(이메일) 찾기</h1>
            <p v-if="authBtn">휴대폰 본인 인증을 완료 해주세요.</p>
          </div>
        </div>

        <div class="d-grid gap-2">
          <button v-if="authBtn" @click="reqMobileCert" type="button" class="btn btn-primary btn-lg">본인인증</button>

          <div v-if="formOpen">
            <p class="mb-1">입력하신 정보와 일치하는 아이디입니다.</p>
            <h4>{{ findedId }}</h4>
          </div>

          <div class="text-center">
            <a class="btn btn-link" href="@@autopath/authentication-login-basic.html">
              <RouterLink to="/login"><i class="bi-chevron-left"></i> Back to Sign in</RouterLink>
            </a>
          </div>
        </div>
      </div>
    </div>
    <!-- End Card -->
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, dateTimeFormatConverter, showAlert, showLogConsole } from '@/utils/common-utils';
const nice_cert_call_info = ref({
  token_version_id: '',
  enc_data: '',
  integrity_value: '',
});

const authBtn = ref(true);
const formOpen = ref(false);
const findedId = ref('');

const reqMobileCert = () => {
  const host = window.location.origin;
  apis.join.phCertReq(host).then(res => {
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      return;
    } else {
      showLogConsole(res);
      nice_cert_call_info.value.integrity_value = res.integrity_value;
      nice_cert_call_info.value.enc_data = res.enc_data;
      nice_cert_call_info.value.token_version_id = res.token_version_id;

      nice_cert_popup_call();
    }
  });
};

const nice_cert_popup_call = () => {
  const form = document.createElement('form');
  form.action = 'https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb';
  form.name = 'cert_form';
  form.id = 'cert_form';
  form.target = 'cert_form';

  const hiM = document.createElement('input');
  hiM.setAttribute('type', 'hidden');
  hiM.setAttribute('name', 'm');
  hiM.setAttribute('id', 'm');
  hiM.setAttribute('value', 'service');
  form.appendChild(hiM);

  const hiToken = document.createElement('input');
  hiToken.setAttribute('type', 'hidden');
  hiToken.setAttribute('name', 'token_version_id');
  hiToken.setAttribute('id', 'token_version_id');
  hiToken.setAttribute('value', nice_cert_call_info.value.token_version_id);
  form.appendChild(hiToken);

  const hiEnc = document.createElement('input');
  hiEnc.setAttribute('type', 'hidden');
  hiEnc.setAttribute('name', 'enc_data');
  hiEnc.setAttribute('id', 'enc_data');
  hiEnc.setAttribute('value', nice_cert_call_info.value.enc_data);
  form.appendChild(hiEnc);

  const hiIntegrity = document.createElement('input');
  hiIntegrity.setAttribute('type', 'hidden');
  hiIntegrity.setAttribute('name', 'integrity_value');
  hiIntegrity.setAttribute('id', 'integrity_value');
  hiIntegrity.setAttribute('value', nice_cert_call_info.value.integrity_value);
  form.appendChild(hiIntegrity);
  // document에 동적 생성한 form 등록
  document.body.appendChild(form);
  // 본인인증 결과값 받을 EventListener 등록
  window.addEventListener('message', receiveCertValue, false);

  // 본인인증창 팝업으로 띄움
  setTimeout(async () => {
    window.open('', 'cert_form', 'width=500, height=550, top=100, left=100, fullscreen=no, menubar=no, status=no, toolbar=no, titlebar=yes, location=no, scrollbar=no');
    form.submit();
    form.remove();
  });
};

const receiveCertValue = (e: any) => {
  window.removeEventListener('message', receiveCertValue);
  if (!e.data.token_version_id || !e.data.enc_data || !e.data.integrity_value) {
    showAlert('본인인증에 실패하였습니다.\n잠시 후 다시 시도해주세요.', 'warning');
  } else {
    apis.join.phCertResult(e.data.token_version_id, e.data.enc_data, e.data.integrity_value).then(res => {
      if (res instanceof AxiosError) {
        const error = res.response?.data;
        if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요..', 'error');
        return;
      }
      showLogConsole(res);
      if (res) {
        getFindId();
      } else {
        showAlert('등록된 회원정보가 없습니다.', 'warning');
      }
    });
  }
};

const getFindId = async () => {
  await apis.user.findId(nice_cert_call_info.value.token_version_id).then(res => {
    apiResponseCheck(res, () => {
      authBtn.value = false;
      formOpen.value = true;
      findedId.value = res;
      showLogConsole(res);
    });
  });
};
</script>
