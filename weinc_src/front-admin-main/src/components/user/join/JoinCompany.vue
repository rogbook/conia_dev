<template>
  <!-- Form -->
  <div class="row mb-xl-6">
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="c_name">상호명 <span class="form-label text-danger">*</span></label>
    <div class="col-xl-4">
      <input
        id="c_name"
        aria-label="c_name"
        class="form-control"
        name="c_name"
        placeholder="상호명을 입력해주세요."
        type="text"
        v-model.trim="corpName.value"
        maxlength="20"
        @keyup.prevent="
          () => {
            corpName.check = corpName.value !== '';
          }
        " />
    </div>
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="locationLabel">대표자명 </label>
    <div class="col-xl-4">
      <input
        id="ceo_name"
        aria-label="ceo_name"
        class="form-control"
        name="ceo_name"
        placeholder="대표자 성명을 입력해주세요."
        type="text"
        v-model.trim="ceoName.value"
        maxlength="20"
        @keyup.prevent="
          () => {
            ceoName.check = ceoName.value !== '';
          }
        " />
    </div>
  </div>
  <!-- End Form -->

  <!-- Form -->
  <div class="row mb-xl-6">
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="locationLabel">사업자 등록번호</label>
    <div class="col-xl-4">
      <input
        id="com_reg_num"
        aria-label="com_reg_num"
        class="form-control"
        name="com_reg_num"
        placeholder="사업자 등록번호를 입력해주세요 (숫자만 입력)"
        type="text"
        v-model="corpRegNumber.value"
        oninput="this.value = this.value.replace(/[^0-9]/g,'')"
        maxlength="30"
        @keyup.prevent="
          () => {
            corpRegNumber.check = corpRegNumber.value !== '';
          }
        " />
    </div>
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="locationLabel">사업자 등록증 </label>
    <div class="col-xl-4">
      <div class="input-group">
        <UploadImage
          class="form-control"
          @change="
            () => {
              photoComReg.check = photoComReg.value.length > 0;
            }
          "
          @upload="onRegistComRegPhoto"
          :btn="{ btnName: '파일 선택', btnClass: 'btn btn-outline-secondary' }"
          type="text"
          :placeholder="photoComReg.value || '사업자등록증을 등록해 주세요.'"
          disabled />
      </div>
    </div>
  </div>
  <!-- End Form -->
  <!-- Form -->
  <div class="row mb-xl-6">
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="locationLabel" v-if="props.joinType === 'B'">법인등록번호 </label>
    <div class="col-xl-4" v-if="props.joinType === 'B'">
      <input
        id="corp_number"
        aria-label="corp_number"
        class="form-control"
        name="corp_number"
        placeholder="법인등록번호를 입력해주세요. (숫자만 입력)"
        type="text"
        v-model="corpNumber.value"
        oninput="this.value = this.value.replace(/[^0-9]/g,'')"
        maxlength="30"
        @keyup.prevent="
          () => {
            if (props.joinType === 'B') {
              corpNumber.check = corpNumber.value !== '';
            }
          }
        " />
    </div>
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="locationLabel">계산서 이메일 </label>
    <div class="col-xl-4">
      <input
        id="receipt"
        aria-label="receipt"
        class="form-control"
        name="receipt"
        placeholder="계산서를 받을 이메일을 입력해주세요."
        type="text"
        oninput="this.value = this.value.replace(/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/g, '')"
        v-model.trim="taxEmail.value"
        maxlength="45"
        @keyup.prevent="
          () => {
            taxEmail.check = taxEmail.value !== '';
          }
        " />
    </div>
  </div>
  <!-- End Form -->

  <!-- Form -->
  <div class="row mb-xl-6">
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="locationLabel">은행명 </label>
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
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="locationLabel">예금주 </label>
    <div class="col-xl-4">
      <input
        id="bank_user"
        aria-label="bank_user"
        class="form-control"
        name="bank_user"
        placeholder="예금주를 입력해주세요."
        type="text"
        v-model.trim="bankUser.value"
        maxlength="20"
        @keyup.prevent="
          () => {
            bankUser.check = bankUser.value !== '';
          }
        " />
    </div>
  </div>
  <!-- End Form -->

  <!-- Form -->
  <div class="row mb-xl-6">
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="locationLabel">계좌번호 </label>
    <div class="col-xl-4">
      <input
        id="account_num"
        aria-label="account_num"
        class="form-control"
        name="account_num"
        placeholder="계좌번호를 입력해주세요. (숫자만 입력)"
        oninput="this.value = this.value.replace(/[^0-9]/g,'')"
        maxlength="30"
        type="text"
        v-model="account.value"
        @keyup.prevent="
          () => {
            account.check = account.value !== '';
          }
        " />
    </div>
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="locationLabel">통장사본 </label>
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
          :placeholder="photoBank.value || '통장사본을 등록해 주세요.'"
          disabled />
      </div>
    </div>
  </div>
  <!-- End Form -->

  <div class="row mb-2">
    <label class="col-xl-2 col-form-label form-label text-nowrap" for="addr">주소 </label>
    <div class="col-xl-4 mb-2">
      <div class="input-group">
        <input disabled v-model="addr.zonecode" id="addressLabel" class="form-control" name="addr" placeholder="우편번호" type="text" readonly required />
        <button type="button" @click.prevent="onSearchAddress" class="btn btn-outline-secondary">우편번호 찾기</button>
      </div>
    </div>
  </div>
  <div class="row mb-xl-6">
    <div class="col-xl-2"></div>
    <div class="col-xl-10">
      <div class="input-group mb-xl-2 mb-2">
        <input disabled v-model="addr.baseAddress" id="address" class="form-control" name="department" placeholder="주소는 우편번호를 찾으면 자동으로 입력됩니다." type="text" readonly required />
      </div>
      <div class="input-group">
        <input @keyup="checkAddrValid" v-model.trim="addr.detailAddress" id="addrDetails" class="form-control" name="department" placeholder="상세 주소를 입력해 주세요." type="text" required maxlength="128" />
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
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue';
import type { IAddress, IDaumPostcodeApi } from '@/models/users/join';
import apis from '@/apis';
import type { IBankList, TJoinType } from '@/components/user/type';
import type { IDynamicKeyValue } from '@/components/types';
import UploadImage from '@/components/comm/uploadImage.vue';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import { useAuthStore } from '@/stores/auth';
import type { IAdditionalInfo } from '@/apis/api.join';

const props = defineProps<{ joinType: TJoinType; bankList: IBankList[]; user: IDynamicKeyValue; isAfterReg: Boolean }>();

// 상호명
const corpName = reactive({
  value: '',
  check: false,
  err_msg: '상호명을 입력해주세요.',
});

// 대표자명
const ceoName = reactive({
  value: '',
  check: false,
  err_msg: '대표자명을 입력해주세요.',
});

// 사업자등록번호
const corpRegNumber = reactive({
  value: '',
  check: false,
  err_msg: '사업자 등록 번호를 입력해 주세요.',
});

// 사업자등록증
const photoComReg = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '사업자등록증을 업로드해주세요.',
});

// 법인등록번호
const corpNumber = reactive({
  value: '',
  check: false,
  err_msg: '법인번호를 입력해 주세요.',
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
  err_msg: '계산서메일을 입력해 주세요.',
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

const onRegistBankPhoto = (files: File) => {
  photoBank.value = files.name; // 추후에 로직 추가예정
  photoBank.fileData = files;
  photoBank.check = true;
};

const onRegistComRegPhoto = (files: File) => {
  photoComReg.value = files.name; // 추후에 로직 추가예정
  photoComReg.fileData = files;
  photoComReg.check = true;
};

// 주소
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

const companyCheckList = reactive([corpName, ceoName, corpRegNumber, photoComReg, corpNumber, taxEmail, bank, bankUser, account, photoBank, addr]);

const emits = defineEmits(['nextStep']);

watch(
  () => props.joinType,
  type => {},
);

const onSubmitInfo = () => {
  if (props.joinType !== 'B') {
    corpNumber.check = true;
    corpNumber.value = '';
  }

  if (!corpName.check) {
    showAlert(corpName.err_msg, 'warning');
    return;
  }

  // for (const data of companyCheckList) {
  //   if (!data.check) {
  //     showAlert(data.err_msg, 'warning');
  //     return;
  //   }
  // }

  showConfirm('사업자정보를 등록하시겠습니까?', () => {
    const addCompanyData = {
      member_id: props.user.id,
      corp_type: props.joinType,
      tax_email: taxEmail.value,
      bank: bank.value,
      bank_user: bankUser.value,
      account: account.value,
      address: addr.baseAddress,
      address_detail: addr.detailAddress,
      zipcode: addr.zonecode,
      photo_bank: photoBank.fileData,
      photo_reg: photoComReg.fileData,
      name: corpName.value,
      ceo: ceoName.value,
      reg_no: corpRegNumber.value,
    } as IAdditionalInfo;

    if (props.joinType === 'B') {
      addCompanyData.corp_number = corpNumber.value;
    }

    showLogConsole(addCompanyData);

    apis.join.onSubmitAdditionalInfo(addCompanyData).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(`회원가입 신청 완료 : ${res}`);
        emits('nextStep');
      });
    });
  });
};
</script>

<style scoped></style>
