<template>
  <PageNavigator :before_link="['고객 회원 관리']" :current="'고객회원 상세'" />
  <ul class="nav nav-tabs mb-4" role="tablist">
    <li class="nav-item">
      <a class="nav-link active" id="nav-userInfoTab" href="#navTabUser" data-bs-toggle="pill" data-bs-target="#navTabUser" role="tab" aria-controls="navTabUser" aria-selected="true">기본정보</a>
    </li>
  </ul>

  <div class="tab-content" id="navTabUserInfo">
    <div class="tab-pane fade show active" id="navTabUser" role="tabpanel" aria-labelledby="nav-userInfoTab">
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header py-2">고객 회원 정보</div>
            <div class="card-body">
              <div class="row col mb-2">
                <label class="col-md-2 col-form-label">회원상태</label>
                <div class="col-md-5">
                  <div class="input-group">
                    <span class="form-control" id="mb_status">{{ mStatus }}</span>
                    <button type="button" class="btn btn-outline-dark" @click.prevent="showModal('statusChangeModal')" v-if="isAdmin">상태 수정</button>
                  </div>
                </div>
              </div>
              <div class="row col mb-2">
                <label for="idLabel" class="col-md-2 col-form-label form-label">아이디</label>
                <div class="col-auto ps-0">
                  <span class="form-control border-0" id="id">{{ mCustomerInfo.email }}</span>
                </div>
                <div class="col-auto" v-if="getUserClassStr.includes('CM')">
                  <button type="button" class="btn btn-sm btn-outline-danger" @click.prevent="reqTempPassword">임시 비밀번호 발급</button>
                </div>
              </div>
              <div class="row mb-2">
                <label class="col-md-2 col-form-label">이름</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" name="name" id="name" placeholder="이름을 입력하세요." aria-label="이름을 입력하세요." :value="mCustomerInfo.name" readonly />
                  </div>
                </div>
              </div>
              <div class="row mb-2">
                <label for="phoneLabel" class="col-md-2 col-form-label form-label">휴대폰번호</label>
                <!-- TODO: 전화번호 표현 마스크 처리 -->
                <div class="col">
                  <input type="text" class="js-input-mask form-control" name="phone" id="phoneLabel" placeholder="xxx-xxxx-xxxx" aria-label="xxx-xxxx-xxxx" :value="mCustomerInfo.mobile" readonly @click.prevent="reqMobileCert" data-hs-mask-options='{ "mask": "000-0000-0000" }' />
                </div>
              </div>
              <div class="row mb-2">
                <label for="emailLabel" class="col-md-2 col-form-label form-label">가입일시</label>
                <div class="col ps-0">
                  <span class="form-control border-0" id="reg_date">{{ dateTimeFormatConverter(mCustomerInfo.reg_date) }}</span>
                </div>
              </div>
              <div class="row mb-2">
                <label for="emailLabel" class="col-md-2 col-form-label form-label">최종접속</label>
                <div class="col ps-0">
                  <span class="form-control border-0" id="id">{{ dateTimeFormatConverter(mCustomerInfo.lastlogin_date) }}</span>
                </div>
              </div>
              <div class="row mb-2">
                <label class="col-xl-2 col-form-label form-label text-nowrap" for="addr">주소</label>
                <div class="col-xl-4 mb-2">
                  <div class="input-group">
                    <input disabled v-model="mCustomerInfo.zipcode" id="addressLabel" class="form-control" name="addr" placeholder="우편번호" type="text" readonly required />
                    <button type="button" @click.prevent="onSearchAddress" class="btn btn-outline-secondary" v-if="isAdmin">우편번호 찾기</button>
                  </div>
                </div>
              </div>
              <div class="row mb-2">
                <div class="col-xl-2"></div>
                <div class="col-xl-10">
                  <div class="input-group mb-xl-2 mb-2">
                    <input disabled v-model="mCustomerInfo.address" id="address" class="form-control" name="department" placeholder="주소는 우편번호를 찾으면 자동으로 입력됩니다." type="text" readonly required />
                  </div>
                  <div class="input-group">
                    <input v-model.trim="mCustomerInfo.address_detail" maxlength="128" id="addrDetails" class="form-control" name="department" placeholder="상세 주소를 입력해 주세요." type="text" required :readonly="!isAdmin" />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-xl-2 col-form-label form-label text-nowrap">마케팅 동의여부</label>
                <div class="col-auto">
                  <div class="col-auto">
                    <span>SMS{{ mCustomerInfo.sms === 'Y' ? '(동의)' : '(미동의)' }} / EMAIL{{ mCustomerInfo.mailling === 'Y' ? '(동의)' : '(미동의)' }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer py-2" v-if="isAdmin">
              <div class="text-center">
                <button type="submit" class="btn btn-sm btn-success end" @click.prevent="modUserInfo">고객 회원 기본정보 저장</button>
              </div>
            </div>
          </div>
        </div>
        <!-- TODO : 메모 필요시 복원 -->
        <div class="col" v-if="false">
          <div class="card">
            <div class="card-header py-2">고객 회원 메모</div>
            <div class="card-body">
              <div class="row mb-2">
                <label class="col-md-2 col-form-label">메모내용</label>
                <div class="col">
                  <div class="input-group">
                    <textarea type="text" class="form-control" maxlength="255" name="memo" id="memo" v-model="mCustomerInfo.memo" />
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer py-2">
              <div class="text-end">
                <button type="button" class="btn btn-sm btn-success" @click.prevent="setMemo">메모 저장</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 회원상태변경 Modal -->
  <Modal :id="'statusChangeModal'" :title="'회원 상태 변경'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">{{ mCustomerInfo.name }} ({{ mCustomerInfo.email }}) 회원의 상태를 수정합니다.</div>
        <div class="row align-items-center mb-4 ms-0 ps-0 me-0 pe-0">
          <div class="col-auto">
            <input type="radio" id="radio_status_y" class="form-check-input" name="radio_status" value="Y" v-model="refStatus" :checked="mCustomerInfo.status === 'Y'" />
            <label class="form-check-label px-1" for="radio_status_y">정상</label>
          </div>
          <div class="col-auto">
            <input type="radio" id="radio_status_r" class="form-check-input" name="radio_status" value="R" v-model="refStatus" :checked="mCustomerInfo.status === 'R'" />
            <label class="form-check-label px-1" for="radio_status_r">승인대기중</label>
          </div>
          <div class="col-auto">
            <input type="radio" id="radio_status_p" class="form-check-input" name="radio_status" value="P" v-model="refStatus" :checked="mCustomerInfo.status === 'P'" />
            <label class="form-check-label px-1" for="radio_status_p">이용정지</label>
          </div>
          <div class="col-auto">
            <input type="radio" id="radio_status_e" class="form-check-input" name="radio_status" value="E" v-model="refStatus" :checked="mCustomerInfo.status === 'E'" />
            <label class="form-check-label px-1" for="radio_status_e">이메일인증 대기중</label>
          </div>
          <div class="col-auto">
            <input type="radio" id="radio_status_d" class="form-check-input" name="radio_status" value="D" v-model="refStatus" :checked="mCustomerInfo.status === 'D'" />
            <label class="form-check-label px-1" for="radio_status_d">탈퇴</label>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="changeStatusReq">확인</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue';
import apis from '@/apis';
import { useRoute, useRouter } from 'vue-router';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import type { Customer } from 'CustomerInfoModule';
import Modal from '@/components/comm/modal.vue';
import type { IDaumPostcodeApi } from '@/models/users/join';
import { loadScript, unloadScript } from '@/utils/standaloneImport';
import PageNavigator from '@/components/title/PageNavigator.vue';

const installList = reactive(['//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js']);

const customerId = ref('');
const mCustomerInfo = ref({} as Customer);
const mOriginCustomerInfo = ref({} as Customer);
const router = useRouter();
const isAdmin = ref(false);

const nice_cert_call_info = ref({
  token_version_id: '',
  enc_data: '',
  integrity_value: '',
});

const refStatus = ref('');
const mStatus = computed(() => {
  switch (mCustomerInfo.value.status) {
    case 'Y':
      return '정상';
    case 'R':
      return '승인대기중';
    case 'D':
      return '탈퇴';
    case 'P':
      return '이용정지';
    case 'E':
      return '이메일인증대기중';
    default:
      return '-';
  }
});

const onSearchAddress = (e: FormDataEvent) => {
  e.preventDefault();
  //@ts-ignore
  new daum.Postcode({
    oncomplete: function (data: IDaumPostcodeApi) {
      // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분입니다.
      // 예제를 참고하여 다양한 활용법을 확인해 보세요.
      const { jibunAddress, roadAddress, zonecode, userSelectedType } = data;
      mCustomerInfo.value.address = userSelectedType === 'J' ? jibunAddress : roadAddress;
      mCustomerInfo.value.zipcode = zonecode;
    },
  }).open();
};

const changeStatusReq = () => {
  if (refStatus.value !== mCustomerInfo.value.status) {
    showConfirm('회원 상태를 변경하시겠습니까?', () => {
      hideModal('statusChangeModal');
      updateUserInfo({ status: refStatus.value });
    });
  } else {
    showAlert('변경사항이 없습니다.', 'warning', () => {
      hideModal('statusChangeModal');
    });
  }
};

const modUserInfo = () => {
  let info: any = {};

  if (mCustomerInfo.value.name !== mOriginCustomerInfo.value.name) {
    info['name'] = mCustomerInfo.value.name;
    info['mobile'] = mCustomerInfo.value.mobile;
  }

  if (mCustomerInfo.value.address !== mOriginCustomerInfo.value.address) {
    info['zipcode'] = mCustomerInfo.value.zipcode;
    info['address'] = mCustomerInfo.value.address;
  }

  if (mCustomerInfo.value.address_detail !== mOriginCustomerInfo.value.address_detail) {
    info['address_detail'] = mCustomerInfo.value.address_detail;
  }

  if (Object.keys(info).length === 0) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  showConfirm('고객 화원 기본정보를 저장하시겠습니까?', () => {
    updateUserInfo(info);
  });
};

const setMemo = () => {
  if (mCustomerInfo.value.memo === mOriginCustomerInfo.value.memo) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  showConfirm('회원 메모를 수정하시겠습니까?', () => {
    updateUserInfo({ memo: mCustomerInfo.value.memo });
  });
};

const updateUserInfo = (info: object) => {
  apis.customer.mod_customer(customerId.value, info).then(res => {
    apiResponseCheck(res, () => {
      showAlert(Object.keys(info).includes('status') ? '고객 회원 상태가 변경되었습니다.' : Object.keys(info).includes('memo') ? '고객 회원 메모가 저장되었습니다.' : '고객 회원 정보가 저장되었습니다.', 'success');
      getCustomerInfo();
    });
  });
};

const reqTempPassword = () => {
  showConfirm(`[${mCustomerInfo.value.name} (${mCustomerInfo.value.email})] 회원에게 임시비밀번호를 발급하시겠습니까?`, () => {
    apis.customer.temp_password(customerId.value).then(res => {
      apiResponseCheck(res, () => {
        showAlert('임시 비밀번호가 발급되었습니다.');
      });
    });
  });
};

const getCustomerInfo = () => {
  apis.customer.get_customer(customerId.value, 'customer').then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mCustomerInfo.value = res;
      refStatus.value = mCustomerInfo.value.status;
      mOriginCustomerInfo.value = JSON.parse(JSON.stringify(res));
    });
  });
};

// 휴대폰 인증 영역
const reqMobileCert = () => {
  if (isAdmin.value) {
    const host = window.location.origin;
    apis.join.phCertReq(host).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        nice_cert_call_info.value.integrity_value = res.integrity_value;
        nice_cert_call_info.value.enc_data = res.enc_data;
        nice_cert_call_info.value.token_version_id = res.token_version_id;
        nice_cert_popup_call();
      });
    });
  }
};
const receiveCertValue = (e: any) => {
  window.removeEventListener('message', receiveCertValue);
  if (!e.data.token_version_id || !e.data.enc_data || !e.data.integrity_value) {
    showAlert('본인인증에 실패하였습니다.\n잠시 후 다시 시도해주세요.', 'warning');
  } else {
    apis.join.phCertResult(e.data.token_version_id, e.data.enc_data, e.data.integrity_value).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        mCustomerInfo.value.name = res.name;
        mCustomerInfo.value.mobile = res.mobile;
      });
    });
  }
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

onMounted(() => {
  const customer_id = history.state.id;
  if (customer_id) {
    customerId.value = customer_id as string;
    getCustomerInfo();
  } else {
    showAlert('잘못된 접근입니다.', 'warning', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
  }

  if (getUserClassStr.value.includes('CM')) {
    isAdmin.value = true;
  }

  installList.map(path => {
    loadScript(path);
  });
});

onUnmounted(() => {
  installList.map(path => {
    unloadScript(path);
  });
});
</script>

<style scoped></style>
