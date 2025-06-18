<template>
  <!-- Form -->
  <div class="row mb-xl-6 mb-3">
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="regNum">주민등록번호<span class="form-label text-danger">*</span></label>
    <div class="col-xl-4">
      <input
        v-model="corpNumber.value"
        @keyup.prevent="
          () => {
            corpNumber.check = /^[0-9]{13}$/.test(corpNumber.value);
          }
        "
        oninput="this.value = this.value.replace(/[^0-9]/g,'')"
        id="regNum"
        aria-label="주민번호를 입력해 주세요. (숫자만 입력)"
        class="form-control"
        name="regNum"
        placeholder="주민번호를 입력해 주세요. (숫자만 입력)"
        maxlength="13"
        type="text" />
    </div>

    <label class="col-xl-2 col-form-label form-label text-nowrap" for="taxEmail">계산서 이메일 <span class="form-label text-danger">*</span></label>
    <div class="col-xl-4">
      <input
        v-model.trim="taxEmail.value"
        @keyup.prevent="
          () => {
            taxEmail.check = taxEmail.value.length >= 8;
          }
        "
        oninput="this.value = this.value.replace(/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/g, '')"
        id="taxEmail"
        aria-label="example@example.com"
        class="form-control"
        name="taxEmail"
        placeholder="example@example.com"
        maxlength="45"
        type="text"
        required />
    </div>
  </div>
  <!-- End Form -->
  <!-- Form -->
  <div class="row mb-xl-6 mb-3">
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="bank">은행명 <span class="form-label text-danger">*</span></label>
    <div class="col-xl-4">
      <select
        id="bank"
        v-model="bank.value"
        @change.prevent="
          () => {
            bank.check = bank.value !== '';
          }
        "
        class="form-select form-select-sm"
        aria-label=".form-select-sm example">
        <option selected value="">은행명을 선택해 주세요.</option>
        <option v-for="b in bankList" :key="b.id" :value="b.name">{{ b.name }}</option>
      </select>
    </div>

    <label class="col-xl-2 col-form-label form-label text-nowrap" for="bank-user">예금주 <span class="form-label text-danger">*</span></label>
    <div class="col-xl-4">
      <input
        v-model.trim="bankUser.value"
        @keyup="
          () => {
            bankUser.check = bankUser.value.length > 0;
          }
        "
        maxlength="20"
        id="bank-user"
        aria-label="bank-user"
        class="form-control"
        name="bank-user"
        placeholder="예금주를 입력해 주세요."
        type="text" />
    </div>
  </div>
  <!-- End Form -->
  <!-- Form -->
  <div class="row mb-xl-6 mb-3">
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="account">계좌번호 <span class="form-label text-danger">*</span></label>
    <div class="col-xl-4">
      <input
        v-model.lazy="account.value"
        @keyup="
          () => {
            account.check = /^[0-9]{1,20}$/.test(account.value);
          }
        "
        oninput="this.value = this.value.replace(/[^0-9]/g,'')"
        maxlength="20"
        id="account"
        aria-label="account"
        class="form-control"
        name="account"
        placeholder="계좌번호를 입력해 주세요. (숫자만 입력)"
        type="text" />
    </div>

    <label class="col-xl-2 col-form-label form-label text-nowrap" for="reg">통장사본 <span class="form-label text-danger">*</span></label>
    <div class="col-xl-4">
      <div class="input-group">
        <UploadImage
          class="form-control"
          @change="
            () => {
              photoBank.check = photoBank.value.length > 0;
            }
          "
          @upload="onRegistBankPhoto"
          :btn="{ btnName: '파일 선택', btnClass: 'btn btn-outline-secondary' }"
          :placeholder="photoBank.value || '통장사본을 등록해 주세요.'" />
      </div>
    </div>
  </div>

  <div class="row mb-xl-2 mb-1">
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="addr"
      >주소
      <span class="form-controll text-danger">*</span>
    </label>
    <div class="col-xl-4 mb-2">
      <div class="input-group">
        <input disabled v-model="addr.zonecode" id="addressLabel" class="form-control" name="addr" placeholder="우편번호" type="text" readonly required />
        <button type="button" @click.prevent="onSearchAddress" class="btn btn-outline-secondary">우편번호 찾기</button>
      </div>
    </div>
    <!--    <div class="col-xl-2"></div>-->
  </div>
  <div class="row mb-xl-6 mb-4">
    <div class="col-xl-2"></div>
    <div class="col-xl-10">
      <div class="input-group mb-xl-2 mb-2">
        <input disabled v-model="addr.baseAddress" id="address" class="form-control" name="department" placeholder="주소는 우편번호를 찾으면 자동으로 입력됩니다." type="text" readonly required />
      </div>
      <div class="input-group">
        <input @keyup="checkAddrValid" v-model.trim="addr.detailAddress" maxlength="128" id="addrDetails" class="form-control" name="department" placeholder="상세 주소를 입력해 주세요." type="text" required />
      </div>
    </div>
  </div>
  <div class="col-auto text-end">
    <RouterLink v-if="useAuthStore().isLoggedIn && !isAfterReg" to="/user/wait"><button type="button" class="btn text-primary">건너뛰기</button></RouterLink>
    <span class="mx-1"></span>
    <button @click.prevent="onSubmitInfo" class="btn btn-primary" type="submit">
      <span>{{ isAfterReg ? '등록' : '다음' }}</span> <i class="bi-chevron-right"></i>
    </button>
  </div>
  <!-- End Form -->
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import type { IAddress, IDaumPostcodeApi } from '@/models/users/join';
import type { IBankList, IPersonalJoin, TJoinType } from '@/components/user/type';
import type { IDynamicKeyValue } from '@/components/types';
import UploadImage from '@/components/comm/uploadImage.vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useUserStore } from '@/stores/user';
import { apiResponseCheck, showAlert, showLogConsole } from '@/utils/common-utils';
import { useAuthStore } from '@/stores/auth';

const props = defineProps<{ joinType: TJoinType; bankList: IBankList[]; user: IDynamicKeyValue; isAfterReg: Boolean }>();

const corpNumber = reactive({
  value: '',
  check: false,
  err_msg: '주민번호를 입력해 주세요.',
});

const onCheckCorpNumber = () => {
  if (corpNumber.value.length !== 13) {
    corpNumber.check = false;
  }
  /^[0-9]{,13}$/.test(corpNumber.value);
};

// 계산서 이메일
const taxEmail = reactive({
  value: '',
  check: false,
  err_msg: '계산서 이메일을 입력해 주세요.',
});

// 은행
const bank = reactive({
  value: '',
  check: false,
  err_msg: '사용하시는 은행을 선택해 주세요.',
});

// 예금주
const bankUser = reactive({
  value: '',
  check: false,
  err_msg: '예금주를 입력해 주세요.',
});

// 계좌번호
const account = reactive({
  value: '',
  check: false,
  err_msg: '계좌번호를 입력해 주세요.',
});

// 통장사본
const photoBank = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '통장사본을 업로드해주세요.',
});

const onlyNumber = () => {
  corpNumber.value = corpNumber.value.replace(/[^0-9]/g, '');
};

const onRegistBankPhoto = (files: File) => {
  photoBank.value = files.name; // 추후에 로직 추가예정
  photoBank.fileData = files;
  photoBank.check = true;
};

const addr: IAddress = reactive({
  zonecode: '',
  baseAddress: '',
  detailAddress: '',
  check: false,
  err_msg: '주소를 입력해 주세요.',
});

const checkAddrValid = () => {
  addr.check = addr.zonecode.length > 0 && addr.baseAddress.length > 0 && addr.detailAddress.length > 0;
};

const onSearchAddress = (e: FormDataEvent) => {
  e.preventDefault();
  //@ts-ignore
  new daum.Postcode({
    oncomplete: function (data: IDaumPostcodeApi) {
      // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분입니다.
      // 예제를 참고하여 다양한 활용법을 확인해 보세요.
      const { jibunAddress, roadAddress, zonecode, userSelectedType } = data;
      addr.baseAddress = userSelectedType === 'J' ? jibunAddress : roadAddress;
      addr.zonecode = zonecode;
    },
  }).open();
};

const personalCheckList = reactive([corpNumber, taxEmail, bank, bankUser, account, photoBank, addr]);

const emits = defineEmits(['nextStep']);

const onSubmitInfo = (data: IPersonalJoin) => {
  const name = useUserStore().user.name;
  const currentCheckList = props.joinType === 'P' ? personalCheckList : [];
  for (const data of currentCheckList) {
    if (!data.check) {
      showAlert(data.err_msg, 'warning');
      return;
    }
  }
  apis.join
    .onSubmitAdditionalInfo({
      member_id: props.user.id,
      corp_type: props.joinType,
      corp_number: corpNumber.value,
      tax_email: taxEmail.value,
      bank: bank.value,
      bank_user: bankUser.value,
      account: account.value,
      address: addr.baseAddress,
      address_detail: addr.detailAddress,
      zipcode: addr.zonecode,
      photo_bank: photoBank.fileData,
      name: `${name}`,
    })
    .then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(`회원가입 신청 완료 : ${res}`);
        emits('nextStep');
      });
    });
};
</script>

<style scoped></style>
