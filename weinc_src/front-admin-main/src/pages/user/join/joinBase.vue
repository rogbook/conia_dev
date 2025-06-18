<template>
  <form class="js-validate needs-validation col-lg-8" @submit.prevent="handleSubmit" novalidate>
    <!-- Content Step Form -->
    <div id="addUserStepFormContent">
      <!-- Card -->
      <div id="addUserStepProfile" class="card card-lg">
        <!-- Body -->
        <div class="card-body">
          <!-- Form -->
          <div class="row mb-4">
            <label class="col-sm-2 col-form-label form-label text-nowrap" for="email">이메일(아이디) <span class="form-label text-danger">*</span></label>
            <div class="col-sm-4">
              <div class="input-group">
                <input @change="() => onEmailChange(email)" ref="emailRef" v-model.trim="email.value" id="email" aria-label="example@example.com" class="form-control" name="email" placeholder="example@example.com" type="email" required maxlength="45" />
                <button type="button" class="btn btn-outline-secondary" @click="e => checkIdIsValid(e, email)">중복확인</button>
              </div>
              <span class="invalid-feedback"> 올바른 형식의 이메일 주소를 입력해주세요.</span>
            </div>
          </div>
          <!-- End Form -->
          <!-- Form -->
          <div class="row mb-4">
            <label class="col-sm-2 col-form-label form-label text-nowrap" for="password"
              >비밀번호
              <span class="form-label text-danger">*</span>
            </label>
            <div class="col-sm-4">
              <div class="input-group" data-hs-validation-validate-class>
                <input
                  v-model="pwd.password"
                  @keyup="checkPwdIsValid"
                  data-hs-toggle-password-options='{ "target": [".js-toggle-password-target-1", ".js-toggle-password-target-2"], "defaultClass": "bi-eye-slash", "showClass": "bi-eye", "classChangeTarget": ".js-toggle-password-show-icon-1" }'
                  autocomplete="off"
                  id="password"
                  aria-label="영문, 숫자, 특수기호를 포함한 8~20자"
                  class="form-control js-toggle-password"
                  name="password"
                  placeholder="영문, 숫자, 특수기호를 포함한 8~20자"
                  type="password"
                  minlength="8"
                  maxlength="20" />
                <a class="js-toggle-password-target-1 input-group-append input-group-text" href="javascript:;">
                  <i class="js-toggle-password-show-icon-1 bi-eye"></i>
                </a>
              </div>
            </div>

            <label class="col-sm-2 col-form-label form-label text-nowrap" for="chkPassword">비밀번호 확인 <span class="form-label text-danger">*</span></label>

            <div class="col-sm-4">
              <div class="input-group" data-hs-validation-validate-class>
                <input
                  v-model="pwd.chkPassword"
                  @keyup="checkPwdIsValid"
                  data-hs-toggle-password-options='{
                             "target": [".js-toggle-password-target-1", ".js-toggle-password-target-2"],
                             "defaultClass": "bi-eye-slash",
                             "showClass": "bi-eye",
                             "classChangeTarget": ".js-toggle-password-show-icon-2"
                           }'
                  autocomplete="off"
                  id="chkPassword"
                  aria-label="영문, 숫자, 특수기호를 포함한 8~20자"
                  class="form-control js-toggle-password"
                  name="chkPassword"
                  placeholder="영문, 숫자, 특수기호를 포함한 8~20자"
                  type="password"
                  minlength="8"
                  maxlength="20" />
                <a class="js-toggle-password-target-2 input-group-append input-group-text" href="javascript:;">
                  <i class="js-toggle-password-show-icon-2 bi-eye"></i>
                </a>
              </div>
            </div>
            <p class="text-danger" v-text="pwd.check ? '' : pwd.pwdValidate"></p>
          </div>
          <!-- End Form -->
          <!-- Form -->
          <div class="row mb-4">
            <label class="col-sm-2 col-form-label form-label" for="name"
              >이름
              <span class="form-label text-danger">*</span>
            </label>

            <div class="col-sm-4">
              <input @click="onReqCertPh" @change="() => onNameChange(name)" v-model="name.value" id="name" aria-label="Htmlstream" class="form-control" name="name" placeholder="이름을 입력하시려면 휴대폰 인증을 진행해주세요." type="text" readonly />
            </div>
          </div>
          <!-- End Form -->

          <!-- Form -->
          <div class="row mb-4">
            <label class="col-sm-2 col-form-label form-label" for="phoneNumber">휴대폰번호 <span class="form-controll text-danger">*</span> </label>
            <div class="col-sm-4">
              <div class="input-group">
                <input v-model="ph.phoneNumber" @click="onReqCertPh" @change="checkPhValid" id="phoneNumber" class="form-control" name="phoneNumber" type="text" required readonly placeholder="휴대폰 인증하기를 눌러주세요." />
                <button type="button" @click="onReqCertPh" class="btn btn-outline-secondary">휴대폰인증하기</button>
              </div>
            </div>
          </div>
          <!-- End Form -->
          <div class="row mb-4">
            <div class="col-sm-2 col-form-label form-label">마케팅 수신동의</div>
            <div class="col mt-2">
              <div class="form-check form-check-inline">
                <input @change="onClickMarketing" v-model="mAgree.chkEmail" class="form-check-input" type="checkbox" id="m_agree_email" />
                <label class="form-check-label" for="m_agree_email">이메일</label>
              </div>
              <div class="form-check form-check-inline ms-3">
                <input @change="onClickMarketing" v-model="mAgree.chkSms" class="form-check-input" type="checkbox" id="m_agree_sms" />
                <label class="form-check-label" for="m_agree_sms">SMS</label>
              </div>
              <div class="form-check form-check-inline ms-3">
                <input @change="onClickNotAgree" v-model="mAgree.notAgree" class="form-check-input" type="checkbox" id="m_not_agree" />
                <label class="form-check-label" for="m_not_agree">미동의</label>
              </div>
            </div>
          </div>
          <div class="row mb-4">
            <div class="col-sm-2 col-form-label form-label"></div>
            <div class="row col-sm ms-0">
              <div class="form-check form-check-inline">
                <input @change="onClickAllChecked" class="form-check-input" type="checkbox" id="all" v-model="uAgree.all" />
                <label class="form-check-label" for="all">전체 동의합니다.</label>
              </div>
              <div class="form-check form-check-inline ms-3">
                <input @change="onClickUses" class="form-check-input" type="checkbox" id="use" v-model="uAgree.use" />
                <label class="form-check-label" for="use">이용약관 동의(필수)</label>
                <span class="ms-2" style="font-size: 0.75rem; cursor: pointer">자세히보기 ></span>
              </div>
              <div class="form-check form-check-inline ms-3">
                <input @change="onClickUses" class="form-check-input" type="checkbox" id="sales" v-model="uAgree.sales" />
                <label class="form-check-label" for="sales">판매약관 이용동의(필수)</label>
                <span class="ms-2" style="font-size: 0.75rem; cursor: pointer">자세히보기 ></span>
              </div>
              <div class="form-check form-check-inline ms-3">
                <input @change="onClickUses" class="form-check-input" type="checkbox" id="priv" v-model="uAgree.priv" />
                <label class="form-check-label" for="priv">개인정보 수집 이용동의(필수)</label>
                <span class="ms-2" style="font-size: 0.75rem; cursor: pointer">자세히보기 ></span>
              </div>
            </div>
          </div>
          <div class="row">
            <label class="col-sm-2 col-form-label form-label" for="recommend">추천인 </label>
            <div class="col-sm-4">
              <input v-model.trim="recommend.value" id="recommend" aria-label="Htmlstream" class="form-control" name="recommend" placeholder="추천인 이메일(아이디)" type="text" maxlength="45" />
            </div>
          </div>
        </div>
        <!-- End Body -->
        <!-- Footer -->
        <div class="card-footer d-flex justify-content-end align-items-center">
          <button class="btn btn-primary" type="submit">Next <i class="bi-chevron-right"></i></button>
        </div>
        <!-- End Footer -->
      </div>
      <!-- End Card -->
    </div>
    <!-- End Content Step Form -->
    <!-- End Row -->
  </form>
</template>

<script setup lang="ts">
import { AxiosError } from 'axios';
import { IEmail, IName, IPassword, IPhone, IUseAgree } from '@/models/users/join';
import { useRouter } from 'vue-router';
import { nextTick, onMounted, reactive, ref, toRefs } from 'vue';
import machineDetector, { DETECTED_M_TYPE } from '@/utils/machineDetector';
import apis from '@/apis';
import { useAuthStore } from '@/stores/auth';
import { apiResponseCheck, showAlert, showLogConsole } from '@/utils/common-utils';

const emailRef = ref();

const joinPlatform = ref<DETECTED_M_TYPE>(DETECTED_M_TYPE.Pc);
const emits = defineEmits(['nextStep']);
onMounted(() => {
  joinPlatform.value = machineDetector();
  nextTick(() => {
    //@ts-ignore
    emailRef.value.focus();
  });
});

const email: IEmail = reactive({
  value: '',
  check: false,
  err_msg: '이메일을 확인해주세요.',
});

const pwd: IPassword = reactive({
  password: '',
  chkPassword: '',
  pwdValidate: '',
  check: false,
  err_msg: '비밀번호를 확인해주세요.',
});

const name: IName = reactive({
  value: '',
  check: false,
  err_msg: '이름을 확인해주세요.',
});

const ph: IPhone = reactive({
  phoneNumber: '',
  validNumber: '',
  check: false,
  err_msg: '휴대폰번호 인증을 확인해주세요.',
});

const mAgree = reactive({
  chkEmail: false,
  chkSms: false,
  notAgree: true,
  check: true,
});

const uAgree: IUseAgree = reactive({
  all: false,
  use: false,
  sales: false,
  priv: false,
  check: false,
  err_msg: '이용약관을 동의해주세요.',
});

const recommend = reactive({
  value: '',
});

const nice_cert_call_info = ref({
  token_version_id: '',
  enc_data: '',
  integrity_value: '',
});

const validEmail = (email: any) => {
  const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};

const checkIdIsValid = async (e: any, target: IEmail) => {
  e.preventDefault();

  if (!validEmail(email.value)) {
    showAlert('이메일 주소를 다시 확인해 주세요.', 'warning');
    return;
  }

  await apis.join.checkIdIsValid(target.value).then(res => {
    showLogConsole(res);
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      return;
    }
    if (res.exist) {
      showAlert('이미 존재하는 이메일 입니다.', 'error');
      return;
    }
    email.check = true;
    showAlert(`[${target.value}]은 사용할 수 있는 이메일입니다.`, 'success');
  });
};

const checkPwdIsValid = () => {
  const { password, chkPassword, check } = toRefs(pwd);
  const validPwd = /^(?=.*[a-zA-Z0-9])(?=.*[a-zA-Z!@#$%^&*])(?=.*[0-9!@#$%^&*]).{10,20}$/;
  if (!validPwd.test(password.value)) {
    pwd.pwdValidate = '비밀번호는 영문, 숫자, 특수기호를 포함한 8~20자 이내로 작성해주세요.';
    check.value = false;
    return;
  }
  if (password.value !== '' && chkPassword.value !== '') {
    if (password.value !== chkPassword.value) {
      pwd.pwdValidate = '비밀번호가 서로 다릅니다';
      check.value = false;
      return;
    }
  }
  if (password.value === '') {
    pwd.pwdValidate = '';
    check.value = false;
    return;
  }
  if (chkPassword.value === '') {
    pwd.pwdValidate = '';
    check.value = false;
    return;
  }
  check.value = true;
};

const onReqCertPh = (e: FormDataEvent) => {
  e.preventDefault();
  const host = window.location.origin;
  apis.join.phCertReq(host).then(res => {
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      return;
    } else {
      nice_cert_call_info.value.integrity_value = res.integrity_value;
      nice_cert_call_info.value.enc_data = res.enc_data;
      nice_cert_call_info.value.token_version_id = res.token_version_id;
      nice_cert_popup_call();
    }
  });
};

const onCertificatePh = (e: FormDataEvent) => {
  e.preventDefault();
  apis.join.phCertVerify(ph.phoneNumber, ph.validNumber).then(res => {
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      return;
    }
    showAlert('인증이 완료되었습니다.', 'success');
    ph.check = true;
  });
};

const checkPhValid = () => {
  ph.check = ph.phoneNumber !== '' && ph.phoneNumber.length > 9;
};

const onEmailChange = (target: IEmail) => {
  target.check = false;
};

const onNameChange = (target: IName) => {
  target.check = target.value !== '';
};

const onClickMarketing = () => {
  if (mAgree.chkEmail || mAgree.chkSms) {
    mAgree.notAgree = false;
  }
  if (!mAgree.chkEmail && !mAgree.chkSms) {
    mAgree.notAgree = true;
  }
};
const onClickNotAgree = () => {
  if (mAgree.notAgree) {
    mAgree.chkEmail = false;
    mAgree.chkSms = false;
  }
  if (!mAgree.chkEmail && !mAgree.chkSms) mAgree.notAgree = true;
};

const onClickAllChecked = () => {
  uAgree.use = uAgree.all;
  uAgree.sales = uAgree.all;
  uAgree.priv = uAgree.all;
  uAgree.check = uAgree.all;
};

const onClickUses = () => {
  if (uAgree.use && uAgree.sales && uAgree.priv) {
    uAgree.all = true;
    uAgree.check = true;
  } else {
    uAgree.all = false;
    uAgree.check = false;
  }
};

const checkList = reactive([email, pwd, name, ph, uAgree]);

const router = useRouter();
const handleSubmit = () => {
  for (const data of checkList) {
    if (!data.check) {
      showAlert(data.err_msg, 'warning');
      return;
    }
  }
  apis.join
    .onSubmitBaseInfo({
      email: email.value,
      join_platform: joinPlatform.value,
      mailling: mAgree.chkEmail ? 'Y' : 'N',
      sms: mAgree.chkSms ? 'Y' : 'N',
      mobile: ph.phoneNumber,
      name: name.value,
      nickname: name.value,
      password: pwd.password,
      referer: 'https://coniaworld.com',
      referer_domain: 'https://coniaworld.com',
      status: 'R',
      recommend: recommend.value,
    })
    .then(res => {
      if (res instanceof AxiosError) {
        const error = res.response?.data;
        if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        return;
      }
    })
    .then(() => {
      apis.user.login(email.value, pwd.password).then(res => {
        apiResponseCheck(res, () => {
          // 로그인 성공 시 JWT 정보 저장
          const { access_token, refresh_token } = res;
          useAuthStore().updateAuthInfo({ access_token, refresh_token });
          emits('nextStep');
        });
      });
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
        else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        return;
      }
      showLogConsole(res);
      name.value = res.name;
      ph.phoneNumber = res.mobile;

      name.check = true;
      ph.check = true;
    });
  }
};

const nice_cert_popup_call = () => {
  const form = document.createElement('form');
  form.setAttribute('id', 'phone_valid');

  form.action = 'https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb';
  form.name = 'form';
  form.target = 'form';

  const hiM = document.createElement('input');
  hiM.setAttribute('type', 'hidden');
  hiM.setAttribute('name', 'm');
  hiM.setAttribute('id', 'm');
  hiM.setAttribute('value', 'service');
  form.append(hiM);

  const hiToken = document.createElement('input');
  hiToken.setAttribute('type', 'hidden');
  hiToken.setAttribute('name', 'token_version_id');
  hiToken.setAttribute('id', 'token_version_id');
  hiToken.setAttribute('value', nice_cert_call_info.value.token_version_id);
  form.append(hiToken);

  const hiEnc = document.createElement('input');
  hiEnc.setAttribute('type', 'hidden');
  hiEnc.setAttribute('name', 'enc_data');
  hiEnc.setAttribute('id', 'enc_data');
  hiEnc.setAttribute('value', nice_cert_call_info.value.enc_data);
  form.append(hiEnc);

  const hiIntegrity = document.createElement('input');
  hiIntegrity.setAttribute('type', 'hidden');
  hiIntegrity.setAttribute('name', 'integrity_value');
  hiIntegrity.setAttribute('id', 'integrity_value');
  hiIntegrity.setAttribute('value', nice_cert_call_info.value.integrity_value);
  form.append(hiIntegrity);
  // document에 동적 생성한 form 등록
  document.body.appendChild(form);
  // 본인인증 결과값 받을 EventListener 등록
  window.addEventListener('message', receiveCertValue, false);
  // 본인인증창 팝업으로 띄움
  setTimeout(async () => {
    window.open('', 'form', 'width=500, height=550, top=100, left=100, fullscreen=no, menubar=no, status=no, toolbar=no, titlebar=yes, location=no, scrollbar=no');

    form.submit();
    form.remove();
  });
};
</script>

<style scoped></style>
