<template>
  <div class="row">
    <div class="col">
      <div class="card">
        <div class="card-header py-2">사업자정보</div>
        <div class="card-body">
          <div class="row mb-2">
            <div class="row">
              <label class="col-md-1 col-form-label">사업자명 <span class="text-danger">*</span></label>
              <div class="col-md-4">
                <input type="text" class="form-control" placeholder="사업자명을 입력해주세요." v-model.trim="props.company.name" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
          </div>
          <div class="row mb-2" v-if="props.company.corp_type !== 'P'">
            <div class="row">
              <label class="col-md-1 col-form-label">사업자등록번호</label>
              <div class="col-md-3">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="사업자 등록번호를 입력해주세요 (숫자만 입력)" maxlength="30" oninput="this.value = this.value.replace(/[^0-9]/g,'')" v-model.trim="props.company.reg_no" :readonly="!checkUserClassesCM" />
                </div>
              </div>
              <div class="d-md-none mt-1"></div>
              <div class="col-auto" style="max-height: inherit">
                <img :src="props.company?.photo_reg" class="rounded mx-auto d-block" alt="" style="height: 40px" v-if="props.company.photo_reg" @click.prevent="openImgModal(props.company?.photo_reg)" />
                <i class="bi bi-image" style="font-size: 30px" v-else></i>
              </div>
              <div class="col-md-3 ps-0" v-if="checkUserClassesCM">
                <div class="input-group">
                  <UploadImage
                    class="form-control"
                    @change="
                      () => {
                        photoComReg.check = photoComReg.value.length > 0;
                      }
                    "
                    @upload="onRegistComRegPhoto"
                    :btn="{ btnName: '사업자등록증 등록/변경', btnClass: 'btn btn-outline-secondary' }"
                    type="text"
                    :placeholder="photoComReg.value || '사업자등록증을 등록해 주세요.'"
                    :hidden="props.company?.photo_reg"
                    disabled />
                </div>
              </div>
            </div>
          </div>
          <div class="row mb-2">
            <div class="row">
              <label class="col-md-1 col-form-label" v-if="props.company.corp_type === 'B'">법인등록번호 </label>
              <div class="col-md-3" v-if="props.company.corp_type === 'B'">
                <div class="input-group">
                  <input
                    v-if="props.company.corp_type === 'B'"
                    type="text"
                    class="form-control"
                    laceholder="법인등록번호를 입력해주세요. (숫자만 입력)"
                    oninput="this.value = this.value.replace(/[^0-9]/g,'')"
                    maxlength="30"
                    v-model.trim="props.company.corp_number"
                    :readonly="!checkUserClassesCM" />
                </div>
              </div>
              <label class="col-md-1 col-form-label">계산서 이메일 </label>
              <div class="col-md-3">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="계산서 이메일을 입력해주세요." v-model.trim="props.company.tax_email" maxlength="45" oninput="this.value = this.value.replace(/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/g, '')" :readonly="!checkUserClassesCM" />
                </div>
              </div>
            </div>
          </div>
          <div class="row mb-2">
            <div class="row">
              <label class="col-md-1 col-form-label">계좌번호 </label>
              <div class="col-md-2">
                <!-- Select -->
                <div class="tom-select-custom">
                  <select class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' v-model="props.company.bank" :disabled="!checkUserClassesCM">
                    <option value="" disabled>은행선택</option>
                    <option v-for="b in bankList" :key="b.id" :value="b.name">{{ b.name }}</option>
                  </select>
                </div>
                <!-- End Select -->
              </div>
              <div class="d-md-none mt-1"></div>
              <div class="col-md-3">
                <input type="text" class="form-control" placeholder="계좌번호를 입력해주세요. (숫자만 입력)" oninput="this.value = this.value.replace(/[^0-9]/g,'')" maxlength="20" v-model.trim="props.company.account" :readonly="!checkUserClassesCM" />
              </div>
              <div class="d-md-none mt-1"></div>
              <div class="col-auto" style="max-height: inherit">
                <img :src="props.company?.photo_bank" class="rounded mx-auto d-block" alt="" style="height: 40px" v-if="props.company.photo_bank" @click.prevent="openImgModal(props.company?.photo_bank)" />
                <i class="bi bi-image" style="font-size: 30px" v-else></i>
              </div>
              <div class="col-auto ps-0 me-2">
                <div class="input-group" v-if="checkUserClassesCM">
                  <UploadImage
                    class="form-control"
                    @change="
                      () => {
                        photoBank.check = photoBank.value.length > 0;
                      }
                    "
                    @upload="onRegistBankPhoto"
                    :btn="{ btnName: '통장사본 등록/변경', btnClass: 'btn btn-outline-secondary' }"
                    :placeholder="photoBank.value || '통장사본을 등록해 주세요.'"
                    :hidden="props.company?.photo_bank"
                    disabled />
                </div>
              </div>
              <div class="col row ms-2 border-start">
                <label class="col-auto col-form-label">예금주 </label>
                <div class="col-md">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="예금주명을 입력해주세요." v-model.trim="props.company.bank_user" maxlength="20" :readonly="!checkUserClassesCM" />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- 주소 정보 -->
          <div class="row mb-2">
            <div class="row">
              <label class="col-md-1 col-form-label" for="addr">주소</label>
              <div class="col-md-3 mb-2">
                <div class="input-group">
                  <input disabled v-model="props.company.zipcode" id="addressLabel" class="form-control" name="addr" placeholder="우편번호" type="text" readonly required />
                  <button type="button" @click.prevent="onSearchAddress" class="btn btn-outline-secondary" v-if="checkUserClassesCM">우편번호 찾기</button>
                </div>
              </div>
            </div>
            <div class="row mb-2">
              <div class="row">
                <label class="col-md-1 col-form-label d-none d-md-block" for="address"></label>
                <div class="col-md-5">
                  <input disabled v-model="props.company.address" id="address" class="form-control" name="department" placeholder="주소는 우편번호를 찾으면 자동으로 입력됩니다." type="text" readonly required />
                </div>
              </div>
            </div>
            <div class="row mb-2">
              <div class="row">
                <label class="col-md-1 col-form-label d-none d-md-block" for="addrDetails"></label>
                <div class="col-md-5">
                  <input @keyup="checkAddrValid" v-model.trim="props.company.address_detail" maxlength="128" id="addrDetails" class="form-control" name="department" placeholder="상세 주소를 입력해 주세요." type="text" required :readonly="!checkUserClassesCM" />
                </div>
              </div>
            </div>
          </div>
          <!-- 사업자 직원 정보 -->
          <div class="row mb-2">
            <div class="row col">
              <label class="col-md-2 col-form-label pe-0">대표자</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="대표자명을 입력해주세요." v-model.trim="props.company.ceo" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
            <div class="row col">
              <label class="col-md-2 col-form-label border-start pe-0">대표자 전화</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="대표자 전화번호를 입력해주세요. (숫자만 입력)" oninput="this.value = this.value.replace(/[^0-9]/g,'')" v-model.trim="props.company.phone" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
          </div>
          <div class="row mb-2">
            <div class="row col">
              <label class="col-md-2 col-form-label pe-0">대표자 휴대전화</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="대표자 휴대전화번호를 입력해주세요. (숫자만 입력)" oninput="this.value = this.value.replace(/[^0-9]/g,'')" v-model.trim="props.company.mobile" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
            <div class="row col"></div>
          </div>
          <div class="row mb-2">
            <div class="row col">
              <label class="col-md-2 col-form-label pe-0">영업담당</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="영업담당자 이름을 입력해주세요." v-model.trim="props.company.manager_name" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
            <div class="row col">
              <label class="col-md-2 col-form-label border-start pe-0">영업담당 전화</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="영업담당자 전화번호를 입력해주세요. (숫자만 입력)" oninput="this.value = this.value.replace(/[^0-9]/g,'')" v-model.trim="props.company.manager_phone" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
          </div>
          <div class="row mb-2">
            <div class="row col">
              <label class="col-md-2 col-form-label pe-0">영업담당 휴대전화</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="영업담당자 휴대전화번호를 입력해주세요. (숫자만 입력)" oninput="this.value = this.value.replace(/[^0-9]/g,'')" v-model.trim="props.company.manager_mobile" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
            <div class="row col">
              <label class="col-md-2 col-form-label border-start pe-0">영업담당 이메일</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="영업담당자 이메일주소를 입력해주세요." oninput="this.value = this.value.replace(/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/g, '')" v-model.trim="props.company.manager_email" maxlength="45" :readonly="!checkUserClassesCM" />
              </div>
            </div>
          </div>
          <div class="row mb-2">
            <div class="row col">
              <label class="col-md-2 col-form-label pe-0">정산담당</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="정산담당자 이름을 입력해주세요." v-model.trim="props.company.settlement_name" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
            <div class="row col">
              <label class="col-md-2 col-form-label border-start pe-0">정산담당 전화</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="정산담당자 전화번호를 입력해주세요. (숫자만 입력)" oninput="this.value = this.value.replace(/[^0-9]/g,'')" v-model.trim="props.company.settlement_phone" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
          </div>
          <div class="row mb-2">
            <div class="row col">
              <label class="col-md-2 col-form-label pe-0">정산담당 휴대전화</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="정산담당자 휴대전화번호를 입력해주세요. (숫자만 입력)" oninput="this.value = this.value.replace(/[^0-9]/g,'')" v-model.trim="props.company.settlement_mobile" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
            <div class="row col">
              <label class="col-md-2 col-form-label border-start pe-0">정산담당 이메일</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="정산담장자 이메일 주소를 입력해주세요." oninput="this.value = this.value.replace(/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/g, '')" v-model.trim="props.company.settlement_email" maxlength="45" :readonly="!checkUserClassesCM" />
              </div>
            </div>
          </div>
          <div class="row mb-2">
            <div class="row col">
              <label class="col-md-2 col-form-label pe-0">CS담당</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="CS담당자 이름을 입력해주세요." v-model.trim="props.company.cs_name" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
            <div class="row col">
              <label class="col-md-2 col-form-label border-start pe-0">CS담당 전화</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="CS담당자 전화번호를 입력해주세요. (숫자만 입력)" oninput="this.value = this.value.replace(/[^0-9]/g,'')" v-model.trim="props.company.cs_phone" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
          </div>
          <div class="row mb-2">
            <div class="row col">
              <label class="col-md-2 col-form-label pe-0">CS담당 휴대전화</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="CS담당자 휴대전화번호를 입력해주세요. (숫자만 입력)" oninput="this.value = this.value.replace(/[^0-9]/g,'')" v-model.trim="props.company.cs_mobile" maxlength="20" :readonly="!checkUserClassesCM" />
              </div>
            </div>
            <div class="row col">
              <label class="col-md-2 col-form-label border-start pe-0">CS담당 이메일</label>
              <div class="col">
                <input type="text" class="form-control" placeholder="CS담당자 이메일 주소를 입력해주세요." oninput="this.value = this.value.replace(/[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/g, '')" v-model.trim="props.company.cs_email" maxlength="45" :readonly="!checkUserClassesCM" />
              </div>
            </div>
          </div>
          <!-- 사업자 직원 정보 END -->
          <!-- TODO: 제휴회원 약관동의 항목은 CM이 접근했을때만 보여준다. -->
          <div class="row mb-2" v-if="true">
            <div class="row">
              <label class="col-md-1 col-form-label pe-0">제휴회원 약관동의</label>
              <div class="col-md-4">
                <div class="input-group">
                  <span class="form-control border-0" id="id">동의 (23-01-27 10:47:20)</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer py-2" v-if="getUserClassStr.includes('CM')">
          <div class="text-center">
            <button type="button" class="btn btn-sm btn-success end" @click.prevent="updateCompanyInfo">사업자정보 저장</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <OpenImgModal :id="'openImgModal'" :openImgUrl="openImgUrl" />
</template>

<script setup lang="ts">
import type { IAddress, IDaumPostcodeApi } from '@/models/users/join';
import { ref, onMounted, onUnmounted, PropType, reactive, readonly } from 'vue';
import { loadScript, unloadScript } from '@/utils/standaloneImport';
import type { Company } from 'CompanyInfoModule';
import { apiResponseCheck, getUserClassStr, showAlert, showConfirm, showModal, hideModal } from '@/utils/common-utils';
import UploadImage from '@/components/comm/uploadImage.vue';
import apis from '@/apis';
import type { Class } from 'UserInfoModule';
import OpenImgModal from '@/components/modals/img/OpenImgModal.vue';
import type { IBankList } from '@/components/user/type';
import { useCommonStore } from '@/stores/common';
const installList = reactive(['//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js']);

const bankList = readonly<IBankList[]>(useCommonStore().bankList);

const openImgUrl = ref('');
const props = defineProps({
  company: {
    required: true,
    type: Object as PropType<Company>,
  },
});

const originCompany = ref();
const emit = defineEmits(['updateCompanyInfo', 'getUserInfo']);
const checkUserClassesCM = ref();

const addr: IAddress = reactive({
  zonecode: '',
  baseAddress: '',
  detailAddress: '',
  check: false,
  err_msg: '주소를 입력해 주세요.',
});

// 통장사본
const photoBank = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '통장사본을 업로드해주세요.',
});

// 사업자등록증
const photoComReg = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '사업자등록증을 업로드해주세요.',
});

const onRegistBankPhoto = (files: File) => {
  photoBank.value = files.name; // 추후에 로직 추가예정
  photoBank.fileData = files;
  photoBank.check = true;
  modCompanyPhoto(files, 'bank');
};

const onRegistComRegPhoto = (files: File) => {
  photoComReg.value = files.name; // 추후에 로직 추가예정
  photoComReg.fileData = files;
  photoComReg.check = true;
  modCompanyPhoto(files, 'reg');
};

const modCompanyPhoto = (file: File, type: string) => {
  const kind = type === 'bank' ? '통장사본' : '사업자등록증';
  showConfirm(
    `${kind}을 변경하시겠습니까?`,
    () => {
      let data: any = {};
      if (type === 'bank') {
        data['photo_bank'] = file;
      } else {
        data['photo_reg'] = file;
      }
      apis.company.mod_company_photo(props.company!.id, data).then(res => {
        apiResponseCheck(res, () => {
          showAlert(`${kind}가 변경되었습니다.`);
          emit('getUserInfo');
        });
      });
    },
    () => {
      photoBank.value = '';
      photoBank.fileData = undefined;
      photoBank.check = false;
      photoComReg.value = '';
      photoComReg.fileData = undefined;
      photoComReg.check = false;
    },
  );
};
const checkPersonalValidation = () => {
  if (!props.company.name) {
    showAlert('사업자명을 입력해주세요.', 'warning');
    return;
  }
  // if (!/^[0-9]{13}$/.test(props.company.corp_number)) {
  //   showAlert('주민등록번호가 올바르지 않습니다.', 'warning');
  //   return;
  // }
  // if (!props.company.tax_email) {
  //   showAlert('계산서 이메일을 입력해주세요.', 'warning');
  //   return;
  // }
  // if (!props.company.bank) {
  //   showAlert('은행을 선택해주세요.', 'warning');
  //   return;
  // }
  // if (!props.company.account) {
  //   showAlert('계좌번호를 입력해주세요.', 'warning');
  //   return;
  // }
  // if (!props.company.photo_bank) {
  //   showAlert('통장사본을 등록해주세요.', 'warning');
  //   return;
  // }
  // if (!props.company.bank_user) {
  //   showAlert('예금주를 입력해주세요.', 'warning');
  //   return;
  // }
  return true;
};

const checkCompanyValidation = () => {
  if (!props.company.name) {
    showAlert('사업자명을 입력해주세요.', 'warning');
    return;
  }
  // if (!props.company.reg_no) {
  //   showAlert('사업자 등록번호를 입력해주세요.', 'warning');
  //   return;
  // }
  // if (props.company.corp_type === 'B') {
  //   if (!props.company.corp_number) {
  //     showAlert('법인등록 번호가 올바르지 않습니다.', 'warning');
  //     return;
  //   }
  // } else {
  //   // if (!/^[0-9]{13}$/.test(props.company.corp_number)) {
  //   //   showAlert('주민등록번호가 올바르지 않습니다.', 'warning');
  //   //   return;
  //   // }
  // }
  // if (!props.company.tax_email) {
  //   showAlert('계산서 이메일을 입력해주세요.', 'warning');
  //   return;
  // }
  // if (!props.company.bank) {
  //   showAlert('은행을 선택해주세요.', 'warning');
  //   return;
  // }
  // if (!props.company.account) {
  //   showAlert('계좌번호를 입력해주세요.', 'warning');
  //   return;
  // }
  // if (!props.company.photo_bank) {
  //   showAlert('통장사본을 등록해주세요.', 'warning');
  //   return;
  // }
  // if (!props.company.bank_user) {
  //   showAlert('예금주를 입력해주세요.', 'warning');
  //   return;
  // }
  return true;
};

const checkIsChange = () => {
  if (props.company.name !== originCompany.value.name) return true;
  if (props.company.tax_email !== originCompany.value.tax_email) return true;
  if (props.company.bank !== originCompany.value.bank) return true;
  if (props.company.account !== originCompany.value.account) return true;
  if (props.company.bank_user !== originCompany.value.bank_user) return true;
  if (props.company.address !== originCompany.value.address) return true;
  if (props.company.address_detail !== originCompany.value.address_detail) return true;
  if (props.company.ceo !== originCompany.value.ceo) return true;
  if (props.company.phone !== originCompany.value.phone) return true;
  if (props.company.mobile !== originCompany.value.mobile) return true;
  if (props.company.manager_name !== originCompany.value.manager_name) return true;
  if (props.company.manager_phone !== originCompany.value.manager_phone) return true;
  if (props.company.manager_mobile !== originCompany.value.manager_mobile) return true;
  if (props.company.manager_email !== originCompany.value.manager_email) return true;
  if (props.company.settlement_name !== originCompany.value.settlement_name) return true;
  if (props.company.settlement_phone !== originCompany.value.settlement_phone) return true;
  if (props.company.settlement_mobile !== originCompany.value.settlement_mobile) return true;
  if (props.company.settlement_email !== originCompany.value.settlement_email) return true;
  if (props.company.cs_name !== originCompany.value.cs_name) return true;
  if (props.company.cs_phone !== originCompany.value.cs_phone) return true;
  if (props.company.cs_mobile !== originCompany.value.cs_mobile) return true;
  if (props.company.cs_email !== originCompany.value.cs_email) return true;
  if (props.company?.corp_type !== 'P') {
    if (props.company?.reg_no !== originCompany.value.reg_no) return true;
  }

  showAlert('변경된 내용이 없습니다.', 'warning');
  return false;
};

const updateCompanyInfo = () => {
  if (props.company.corp_type === 'P') {
    if (!checkPersonalValidation()) return;
  } else {
    if (!checkCompanyValidation()) return;
  }
  if (!checkIsChange()) return;

  showConfirm('사업자 정보를 변경하시겠습니까?', () => {
    emit('updateCompanyInfo');
  });
};

const checkAddrValid = () => {
  addr.check = addr.zonecode.length > 0 && addr.baseAddress.length > 0 && addr.detailAddress.length > 0;
};

const onSearchAddress = (e: FormDataEvent) => {
  e.preventDefault();
  //@ts-ignore
  new daum.Postcode({
    oncomplete: function (data: IDaumPostcodeApi) {
      const { jibunAddress, roadAddress, zonecode, userSelectedType } = data;
      props.company.address = userSelectedType === 'J' ? jibunAddress : roadAddress;
      props.company.zipcode = zonecode;
    },
  }).open();
};

const getUserClass = (classes: Class[]): string => {
  const types = [];
  if (classes) {
    for (const c of classes) {
      types.push(c.class_code);
    }
  }
  return types.length == 0 ? '-' : types.join(',');
};

const openImgModal = (src: string) => {
  openImgUrl.value = src;
  showModal('openImgModal');
};

onMounted(() => {
  installList.map(path => {
    loadScript(path);
  });

  if (getUserClassStr.value.includes('CM')) {
    checkUserClassesCM.value = true;
  } else {
    checkUserClassesCM.value = false;
  }
  originCompany.value = { ...props.company };
});

onUnmounted(() => {
  installList.map(path => {
    unloadScript(path);
  });
});
</script>

<style scoped></style>
