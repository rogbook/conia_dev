<template>
  <div class="mx-auto" style="max-width: 30rem">
    <!-- Card -->
    <div class="card card-lg mb-5">
      <div class="card-body">
        <div class="text-center">
          <div class="mb-5">
            <h1 class="display-5">비밀번호 변경</h1>
            <p>비밀번호를 찾고자하는 아이디를 입력해주세요.</p>
          </div>
        </div>

        <div class="mb-4">
          <label class="form-label">아이디 (이메일 주소)</label>
          <input v-model="userEmail" type="email" class="form-control form-control-lg" name="email" tabindex="1" placeholder="email@address.com" aria-label="email@address.com" />
        </div>

        <div class="d-grid gap-2">
          <button v-if="authBtn" @click="checkMember" type="button" class="btn btn-primary btn-lg">본인인증</button>

          <div v-if="formOpen">
            <!-- Input Group -->
            <label class="form-label">비밀번호 변경</label>
            <div class="input-group input-group-vertical">
              <input v-model="password" type="password" class="form-control" placeholder="새 비밀번호" aria-label="First name" />
              <input v-model="password_confirmation" type="password" class="form-control mt-1" placeholder="새 비밀번호 확인" aria-label="Last name" />
            </div>
            <!-- End Input Group -->
          </div>

          <button v-if="formOpen" @click="changePassword()" type="button" class="btn btn-primary btn-lg">변경</button>

          <div class="text-center">
            <a class="btn btn-link">
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
import { useRouter } from 'vue-router';
const router = useRouter();

const userEmail = ref('');
const authBtn = ref(true);
const formOpen = ref(false);
const password = ref('');
const password_confirmation = ref('');

const nice_cert_call_info = ref({
  token_version_id: '',
  enc_data: '',
  integrity_value: '',
});

const checkEmailValidation = () => {
  if (!userEmail.value) {
    showAlert('아이디를 입력해 주세요.', 'warning');
    return;
  }
  if (!validEmail(userEmail.value)) {
    showAlert('이메일 주소를 다시 확인해 주세요.', 'warning');
    return;
  }

  return true;
};

const checkPasswordValidation = () => {
  if (!formOpen.value) {
    return;
  }
  if (!password.value || !password_confirmation.value) {
    showAlert('비밀번호를 입력해 주세요', 'warning');
    return;
  }
  if (password.value !== password_confirmation.value) {
    showAlert('비밀번호가 서로 다릅니다.', 'warning');
    return;
  }
  if (!validPassword(password.value)) {
    showAlert('비밀번호는 영문, 숫자, 특수기호를 포함한 8~20자 이내로 작성해주세요.', 'warning');
    return;
  }

  return true;
};

const changePassword = async () => {
  if (!checkPasswordValidation()) return;

  await apis.user.changePw(nice_cert_call_info.value.token_version_id, userEmail.value, password.value).then(res => {
    apiResponseCheck(res, () => {
      if (res.msg == 'success') {
        showAlert('비밀번호를 변경했습니다.');
        router.push('/login');
      } else {
        showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      }
    });
  });
};

const reqMobileCert = async () => {
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
        authBtn.value = false;
        formOpen.value = true;
      } else {
        showAlert('등록된 회원정보가 없습니다.', 'warning');
      }
    });
  }
};

const checkMember = async () => {
  if (!checkEmailValidation()) return;

  await apis.join.checkIdIsValid(userEmail.value).then(res => {
    apiResponseCheck(res, () => {
      if (!res.exist) {
        showAlert('존재하지 않는 아이디 입니다.', 'warning');
      } else {
        reqMobileCert();
      }
    });
  });
};

const validEmail = (email: any) => {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};

const validPassword = (password: any) => {
  const re = /^(?=.*[a-zA-Z0-9])(?=.*[a-zA-Z!@#$%^&*])(?=.*[0-9!@#$%^&*]).{10,20}$/;
  return re.test(password);
};
</script>
