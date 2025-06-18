<template>
  <div class="row">
    <div class="col-md-6 me-3">
      <div class="row align-items-center">
        <div class="card">
          <form class="" @submit.prevent="handleSubmit">
            <div class="card-header py-2">회원정보</div>
            <div class="card-body">
              <div class="row mb-2 align-items-center">
                <label class="col-md-2 col-form-label">회원상태</label>
                <div class="col-md-5">
                  <div class="input-group">
                    <span class="form-control" id="mb_status">{{ mStatus }}</span>
                    <button type="button" class="btn btn-outline-dark" @click.prevent="showModal('statusChangeModal')" v-if="!me">상태 수정</button>
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-md-2 col-form-label">회원타입</label>
                <div class="col-md-5">
                  <div class="input-group">
                    <span class="form-control" id="mb_status">{{ mTypes }}</span>
                    <button type="button" class="btn btn-outline-dark" @click.prevent="showModal('typeChangeModal')" v-if="!me">타입 수정</button>
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-md-2 col-form-label">아이디</label>
                <div class="col-auto">
                  <span class="form-control border-0 ps-0" id="id">{{ props.member.email }}</span>
                </div>
                <div class="col-auto" v-if="getUserClassStr.includes('CM')">
                  <button type="button" class="btn btn-sm btn-outline-danger" @click.prevent="reqTempPassword">임시 비밀번호 발급</button>
                </div>
              </div>
              <div class="row mb-2 align-items-center" v-if="me">
                <label class="col-md-2 col-form-label">비밀번호</label>
                <div class="col-auto">
                  <div class="input-group">
                    <button type="button" class="btn btn-sm btn-outline-secondary" @click.prevent="reqMobileCert('pw')">비밀번호 변경</button>
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-md-2 col-form-label">이름</label>
                <div class="col-md-5">
                  <div class="input-group">
                    <input type="text" class="form-control" name="name" id="name" placeholder="이름을 입력하세요." aria-label="이름을 입력하세요." :value="props.member.name" readonly />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label for="phoneLabel" class="col-md-2 col-form-label form-label">휴대폰번호</label>
                <div class="col-md-5">
                  <input type="text" class="form-control" name="phone" id="phoneLabel" :value="props.member.mobile" readonly @click.prevent="reqMobileCert('mb')" />
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label for="emailLabel" class="col-md-2 col-form-label form-label">가입일시</label>
                <div class="col-md-5">
                  <span class="form-control border-0 ps-0" id="reg_date">{{ dateTimeFormatConverter(props.member.reg_date) }}</span>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label for="emailLabel" class="col-md-2 col-form-label form-label">최종접속</label>
                <div class="col-md-5">
                  <span class="form-control border-0 ps-0" id="id">{{ dateTimeFormatConverter(props.member.lastlogin_date) }}</span>
                </div>
              </div>
              <div class="row mb-2 align-items-center" v-if="!me">
                <label class="col-md-2 col-form-label">상위회원</label>
                <div class="col-md-5">
                  <div class="input-group">
                    <input type="text" class="form-control" id="mb_status" :value="mPMember" readonly />
                    <button type="button" class="btn btn-outline-dark" @click.prevent="showModal('listPmemberModal')" v-if="!me">회원연결수정</button>
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-md-2 col-form-label form-label">마케팅수신동의</label>
                <div class="col ps-0">
                  <div class="row form-control border-0">
                    <div class="col-auto form-check form-check-inline ms-3">
                      <input @change="onClickMarketing" v-model="mAgree.chkEmail" class="form-check-input" type="checkbox" id="m_agree_email" />
                      <label class="form-check-label" for="m_agree_email">이메일</label>
                    </div>
                    <div class="col-auto form-check form-check-inline ms-3">
                      <input @change="onClickMarketing" v-model="mAgree.chkSms" class="form-check-input" type="checkbox" id="m_agree_sms" />
                      <label class="form-check-label" for="m_agree_sms">SMS</label>
                    </div>
                    <div class="col-auto form-check form-check-inline ms-3">
                      <input @change="onClickNotAgree" v-model="mAgree.notAgree" class="form-check-input" type="checkbox" id="m_not_agree" />
                      <label class="form-check-label" for="m_not_agree">미동의</label>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-md-2 col-form-label form-label">SNS 로그인</label>
                <!-- 본인 -->
                <div class="col-md-5" v-if="me">
                  <div class="col">
                    <div class="col form-control border-0 ps-0">
                      <img src="@/assets/images/sns/payco.png" style="width: 30px; height: 30px" />
                      <span>
                        <button type="button" v-if="props.member.sns_payco" class="btn btn-sm btn-outline-info mx-3" @click.prevent="disconnect('payco')">연결해제</button>
                        <button type="button" v-else class="btn btn-sm btn-outline-secondary mx-3" @click.prevent="connectSns('payco')">연결하기</button>
                      </span>
                    </div>
                  </div>
                  <div class="col">
                    <div class="col form-control border-0 ps-0">
                      <img src="@/assets/images/sns/naver.png" style="width: 30px; height: 30px" />
                      <span>
                        <button type="button" v-if="props.member.sns_naver" class="btn btn-sm btn-outline-info mx-3" @click.prevent="disconnect('naver')">연결해제</button>
                        <button type="button" v-else class="btn btn-sm btn-outline-secondary mx-3" @click.prevent="connectSns('naver')">연결하기</button>
                      </span>
                    </div>
                  </div>
                  <div class="col">
                    <div class="col form-control border-0 ps-0">
                      <img src="@/assets/images/sns/kakao.png" style="width: 30px; height: 30px" />
                      <span>
                        <button type="button" v-if="props.member.sns_kakao" class="btn btn-sm btn-outline-info mx-3" @click.prevent="disconnect('kakao')">연결해제</button>
                        <button type="button" v-else class="btn btn-sm btn-outline-secondary mx-3" @click.prevent="connectSns('kakao')">연결하기</button>
                      </span>
                    </div>
                  </div>
                  <div class="col">
                    <div class="col form-control border-0 ps-0">
                      <img src="@/assets/images/sns/google.png" style="width: 30px; height: 30px" />
                      <span>
                        <button type="button" v-if="props.member.sns_google" class="btn btn-sm btn-outline-info mx-3" @click.prevent="disconnect('google')">연결해제</button>
                        <button type="button" v-else class="btn btn-sm btn-outline-secondary mx-3" @click.prevent="connectSns('google')">연결하기</button>
                      </span>
                    </div>
                  </div>
                </div>

                <!-- 관리자 -->
                <div class="col" v-else>
                  <div class="col form-control border-0 ps-0" v-if="!props.member.sns_payco && !props.member.sns_naver && !props.member.sns_kakao && !props.member.sns_google">연결된 계정 없음</div>
                  <div v-else>
                    <div class="col" v-if="props.member.sns_payco">
                      <div class="col form-control border-0 ps-0">
                        <img src="@/assets/images/sns/payco.png" style="width: 30px; height: 30px" />
                        <span class="mx-3">연결됨</span>
                      </div>
                    </div>
                    <div class="col" v-if="props.member.sns_naver">
                      <div class="col form-control border-0 ps-0">
                        <img src="@/assets/images/sns/naver.png" style="width: 30px; height: 30px" />
                        <span class="mx-3">연결됨</span>
                      </div>
                    </div>
                    <div class="col" v-if="props.member.sns_kakao">
                      <div class="col form-control border-0 ps-0">
                        <img src="@/assets/images/sns/kakao.png" style="width: 30px; height: 30px" />
                        <span class="mx-3">연결됨</span>
                      </div>
                    </div>
                    <div class="col" v-if="props.member.sns_google">
                      <div class="col form-control border-0 ps-0">
                        <img src="@/assets/images/sns/google.png" style="width: 30px; height: 30px" />
                        <span class="mx-3">연결됨</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="row mb-2 align-items-center" v-if="!me">
                <label class="col-md-2 col-form-label form-label" for="recommend">추천인 </label>
                <div class="col-md-5">
                  <span class="form-control border-0 ps-0" id="recommend">{{ props.member.recommend ? props.member.recommend : '없음' }}</span>
                </div>
              </div>

              <div class="row mb-2 align-items-center" v-if="getUserClass(props.member.classes).includes('PA')">
                <label class="col-md-2 col-form-label text-nowrap">매장 여부</label>
                <div class="col form-control border-0">
                  <div class="form-check form-check-inline">
                    <input type="radio" id="radio_shop_yn_y" class="form-check-input" name="shop_yn" value="Y" v-model="props.member.shop_yn" />
                    <label class="form-check-label px-1" for="radio_shop_yn_y">사용</label>
                  </div>

                  <div class="form-check form-check-inline">
                    <input type="radio" id="radio_shop_yn_n" class="form-check-input" name="shop_yn" value="N" v-model="props.member.shop_yn" />
                    <label class="form-check-label px-1" for="radio_shop_yn_n">미사용</label>
                  </div>
                </div>
              </div>

              <div class="row mb-2 align-items-center" v-if="getUserClass(props.member.classes).includes('PA') && props.member.shop_yn === 'Y'">
                <label class="col-md-2 col-form-label text-nowrap">직원확인용<br />비밀번호</label>
                <div class="col-md-5">
                  <div class="input-group">
                    <input
                      type="text"
                      class="form-control"
                      name="confirm-pass"
                      id="confirm-pass"
                      maxlength="16"
                      placeholder="직원확인용 비밀번호를 입력해주세요(최대 16자리, 숫자만 입력가능)."
                      aria-label="직원확인용 비밀번호를 입력하세요."
                      v-model="props.member.confirm_pass"
                      oninput="this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');" />
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer py-2">
              <div class="text-center">
                <button type="submit" class="btn btn-sm btn-success end" @click.prevent="modUserInfo">회원 기본정보 저장</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="d-md-none mt-2"></div>

    <div class="col-md-5" v-if="!me">
      <div class="row align-items-center">
        <div class="card mb-4">
          <div class="card-header py-2">회원메모</div>
          <div class="card-body">
            <div class="row mb-2 align-items-center">
              <label class="col-md-2 col-form-label">메모내용</label>
              <div class="col">
                <div class="input-group">
                  <textarea type="text" class="form-control" maxlength="255" name="memo" id="memo" v-model.trim="props.member.memo" />
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
        <div class="card">
          <div class="card-header py-2">변경이력</div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-align-middle card-table table-borderless">
                <thead class="thead-light">
                  <tr class="text-center">
                    <th>변경일</th>
                    <th>등록/수정</th>
                    <th>변경전</th>
                    <th>변경후</th>
                    <th>변경자</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="text-center" v-for="(l, i) in props.member?.log" :key="JSON.stringify(l)">
                    <td>{{ dateTimeFormatConverter(l.reg_date) }}</td>
                    <td>{{ l.action }}</td>
                    <td style="max-width: 8rem">
                      {{ convertLogItem(l.msg, 'before') }}
                    </td>
                    <td style="max-width: 8rem">{{ convertLogItem(l.msg, 'after') }}</td>
                    <td>{{ l.writer }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 비밀번호 변경 Modal -->
  <Modal :id="'pwChangeModal'" :title="'비밀 번호 변경'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">
          <span v-if="me">비밀번호는 영문, 숫자, 특수기호를 포함한 8~20자 이내로 작성해주세요.</span>
          <span v-else>{{ props.member.name }} ({{ props.member.email }}) 회원의 비밀번호를 수정합니다.</span>
        </div>
        <div class="input-group input-group-vertical">
          <input v-model="password" type="password" class="form-control" placeholder="새 비밀번호" aria-label="First name" />
          <input v-model="password_confirmation" type="password" class="form-control mt-1" placeholder="새 비밀번호 확인" aria-label="Last name" />
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="changePwReq">변경</button>
    </template>
  </Modal>

  <!-- 회원상태변경 Modal -->
  <Modal :id="'statusChangeModal'" :title="'회원 상태 변경'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">{{ props.member.name }} ({{ props.member.email }}) 회원의 상태를 수정합니다.</div>
        <div class="row align-items-center mb-4 ms-0 ps-0 me-0 pe-0">
          <div class="col-auto">
            <input type="radio" id="radio_status_y" class="form-check-input" name="radio_status" value="Y" v-model="refStatus" :checked="memberStatus === 'Y'" />
            <label class="form-check-label px-1" for="radio_status_y">정상</label>
          </div>
          <div class="col-auto">
            <input type="radio" id="radio_status_r" class="form-check-input" name="radio_status" value="R" v-model="refStatus" :checked="memberStatus === 'R'" />
            <label class="form-check-label px-1" for="radio_status_r">승인대기중</label>
          </div>
          <div class="col-auto">
            <input type="radio" id="radio_status_p" class="form-check-input" name="radio_status" value="P" v-model="refStatus" :checked="memberStatus === 'P'" />
            <label class="form-check-label px-1" for="radio_status_p">이용정지</label>
          </div>
          <div class="col-auto">
            <input type="radio" id="radio_status_e" class="form-check-input" name="radio_status" value="E" v-model="refStatus" :checked="memberStatus === 'E'" />
            <label class="form-check-label px-1" for="radio_status_e">이메일인증 대기중</label>
          </div>
          <div class="col-auto">
            <input type="radio" id="radio_status_d" class="form-check-input" name="radio_status" value="D" v-model="refStatus" :checked="memberStatus === 'D'" />
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

  <!-- 회원타입변경 Modal -->
  <!-- TODO: 회원타입변경 관련 데이터 반영 해야함. -->
  <Modal :id="'typeChangeModal'" :title="'회원 타입 변경'">
    <template #body>
      <div class="text-start mb-4">{{ props.member.name }} ({{ props.member.email }}) 회원의 타입을 수정합니다.</div>
      <div class="form-check mb-3" v-for="c in props.classList" :key="JSON.stringify(c)">
        <input type="radio" v-bind:id="`radio_type_${c.code}`" v-bind:value="c.code" class="form-check-input" name="radio_type" v-model="refTypes" :checked="mTypes === c?.code" />
        <label class="form-check-label px-1" v-bind:for="`radio_type_${c?.code}`">
          <span class="d-block fw-semibold mb-1">{{ c?.name }}</span>
          <span class="d-block">{{ c.description }}</span>
        </label>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click="changeTypeReq">확인</button>
    </template>
  </Modal>

  <!-- 회원 연결 관리(삭제) 목록 Modal -->
  <!-- TODO: 회원 연결 관리 목록 관련 데이터 작업 해야함 -->
  <Modal :id="'listPmemberModal'" :title="'회원 연결 관리'" :xlarge="false">
    <template #body>
      <div class="text-end mb-2" v-if="props.member?.p_member?.length === 0">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="showModal('pMemberAddModal')">신규연결</button>
      </div>
      <div class="table-responsive">
        <table class="table table-lg table-borderless table-nowrap table-thead-bordered table-align-middle card-table">
          <thead class="thead-light">
            <tr class="text-center">
              <th>연결된 상위 회원</th>
              <th style="width: 10%">연결해제</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(p, i) in props.member?.p_member" :key="p.id">
              <td>{{ p.name }} / {{ p.email }}</td>
              <td><button type="button" class="btn btn-sm btn-danger" @click.prevent="connMemberReq(p.id, 'delete')">해제</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <!-- 회원 연결 관리 추가 Modal -->
  <!-- TODO: 회원연결추가 관련 데이터 작업 해야함. -->
  <Modal :id="'pMemberAddModal'" :title="'회원 연결 관리 (신규연결)'" :xlarge="true">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">{{ props.member.name }} ({{ props.member.email }}) 회원의 연결을 설정합니다.</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <form class="mb-6">
              <div class="row col">
                <label class="col-md-2 col-form-label">회원검색</label>
                <div class="col-md-2">
                  <!-- Select -->
                  <div class="tom-select-custom">
                    <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                      <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
                    </select>
                  </div>
                  <!-- End Select -->
                </div>
                <div class="d-md-none mt-1"></div>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="searchUser" />
                    <button type="button" class="btn btn-outline-dark col-md-2" @click.prevent="searchUser">검색</button>
                  </div>
                </div>
              </div>
            </form>
            <!-- Modal Search Form End -->
            <!-- Member List Table -->
            <div class="table-responsive">
              <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
                <thead class="thead-light">
                  <tr class="text-center">
                    <th>회원타입</th>
                    <th>이름</th>
                    <th>아이디</th>
                    <th>휴대전화</th>
                    <th>선택</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="text-center" v-for="(user, i) in searchUserList.data" :key="user.id">
                    <td>{{ getUserClass(user.classes) }}</td>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.mobile }}</td>
                    <td>
                      <button type="button" class="btn btn-sm btn-info" @click.prevent="connMemberReq(user.id, 'conn')" :class="user.id === props.member.id ? 'disabled' : ''">연결</button>
                    </td>
                  </tr>
                  <tr>
                    <td colspan="5" class="text-center" v-if="searchUserList.data.length === 0">표시할 항목이 없습니다.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- Member List Table End-->
          </div>
          <div class="table-footer-area" v-if="searchUserList.total > 0">
            <div class="row" v-if="cul_total_page > 1">
              <Pagination :currentPage="cul_page_no" :totalPages="cul_total_page" :pageChange="cul_pageChange" />
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import { computed, onMounted, reactive, ref, watch } from 'vue';
import type { PropType } from 'vue';
import type { User, Class } from 'UserInfoModule';
import apis from '@/apis';
import { useRouter } from 'vue-router';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import Pagination from '@/components/comm/Pagination.vue';
import { useAuthStore } from '@/stores/auth';

const props = defineProps({
  member: {
    required: true,
    type: Object as PropType<User>,
  },
  me: {
    required: true,
    type: Boolean,
  },
  classList: {
    required: true,
    type: Array,
  },
});

const originMemberInfo = ref({} as User);

const emit = defineEmits(['updateFromInfo', 'updateMemo', 'changeClass', 'linkMember']);
const router = useRouter();
const nice_cert_call_info = ref({
  token_version_id: '',
  enc_data: '',
  integrity_value: '',
});

const password = ref('');
const password_confirmation = ref('');

const mStatus = computed(() => {
  switch (props.member.status) {
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

const memberStatus = computed(() => {
  return props.member.status;
});

const refStatus = ref('');
const refTypes = ref('');

const mTypes = computed(() => {
  const types = [];
  if (props.member?.classes) {
    for (const c of props.member.classes) {
      types.push(c.class_code);
    }
  }
  return types.length === 0 ? '-' : types.join(',');
});

const mPartner = computed(() => {
  return props.member?.partner === 'Y' ? '승인' : '미승인';
});

const mPMember = computed(() => {
  const pMembers = [];
  if (props.member?.p_member) {
    for (const p of props.member.p_member) {
      pMembers.push(p.name);
    }
  }
  return pMembers.length === 0 ? '-' : pMembers.join(',');
});

const mAgree = reactive({
  chkEmail: false,
  chkSms: false,
  notAgree: true,
  check: true,
});

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

const reqTempPassword = () => {
  showConfirm(`[${props.member?.name} (${props.member?.email})] 회원에게 임시비밀번호를 발급하시겠습니까?`, () => {
    apis.user.temp_password(props.member.id).then(res => {
      apiResponseCheck(res, () => {
        showAlert('임시 비밀번호가 발급되었습니다.');
      });
    });
  });
};

const changeStatusReq = () => {
  showConfirm('회원 상태를 변경하시겠습니까?', () => {
    hideModal('statusChangeModal');
    emit('updateFromInfo', { status: refStatus.value });
  });
};
const changePwReq = () => {
  if (!checkPasswordValidation()) return;
  showConfirm('비밀번호를 변경하시겠습니까?', async () => {
    await apis.user.changePw(nice_cert_call_info.value.token_version_id, props.member.email, password.value).then(res => {
      apiResponseCheck(res, () => {
        if (res.msg == 'success') {
          showAlert('비밀번호를 변경했습니다.', 'success', () => {
            hideModal('pwChangeModal');

            apis.user.logout().then(res => {
              apiResponseCheck(res, () => {
                useAuthStore().logout();
              });
            });
          });
        } else {
          showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
        }
      });
    });
  });
};

const checkPasswordValidation = () => {
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
const validPassword = (password: any) => {
  const re = /^(?=.*[a-zA-Z0-9])(?=.*[a-zA-Z!@#$%^&*])(?=.*[0-9!@#$%^&*]).{10,20}$/;
  return re.test(password);
};

const changeTypeReq = () => {
  // 기존 타입
  showLogConsole('기존 : ' + mTypes.value);
  // 변경
  showLogConsole('변경 : ' + refTypes.value);

  showConfirm('회원 타입을 변경하시겠습니까?', () => {
    emit('changeClass', mTypes.value, refTypes.value);
    hideModal('typeChangeModal');
  });
};

const connMemberReq = (p_id: string | number, method: string) => {
  if (method === 'delete') {
    showConfirm('회원 연결을 해제하시겠습니까?', () => {
      hideModal('listPmemberModal');
      emit('linkMember', p_id, method);
    });
  } else {
    showConfirm('회원 연결을 설정하시겠습니까?', () => {
      hideModal('pMemberAddModal');
      emit('linkMember', p_id, method);
    });
  }
};

const selDetailSearch = reactive({
  items: [
    { name: '이름', value: 'name' },
    { name: '아이디', value: 'user_id' },
    { name: '전화번호', value: 'mobile' },
    { name: '회사명', value: 'company_name' },
    { name: '상점명', value: 'store_title' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 회원의 이름을 입력해주세요.',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'name':
      selDetailSearch.placeholder = '검색할 회원의 이름을 입력해주세요.';
      break;
    case 'user_id':
      selDetailSearch.placeholder = '검색할 회원의 아이디(이메일)을 입력해주세요.';
      break;
    case 'mobile':
      selDetailSearch.placeholder = "검색할 회원의 전화번호를 입력해주세요. ('-' 제외)";
      break;
    case 'company_name':
      selDetailSearch.placeholder = '검색할 회원의 회사명을 입력해주세요.';
      break;
    case 'store_title':
      selDetailSearch.placeholder = '검색할 회원의 상점명을 입력해주세요.';
      break;
  }
};

const searchUserList = ref({
  total: 0,
  data: {} as User[],
});

const getUserClass = (classes: Class[]): string => {
  const types = [];
  if (classes) {
    for (const c of classes) {
      types.push(c.class_code);
    }
  }
  return types.length == 0 ? '-' : types.join(',');
};

const cul_page_no = ref(1);
const cul_offset = computed(() => (cul_page_no.value - 1) * cul_limit.value);
const cul_limit = ref(10);
const cul_total_page = computed(() => Math.ceil(searchUserList.value.total / cul_limit.value));

const cul_pageChange = (page: number) => {
  cul_page_no.value = page;
  searchUser(false);
};

// 상위 회원 연결 검색 목록
const searchUser = (init: boolean = true) => {
  if (init) {
    cul_page_no.value = 1;
  }
  let query = '';
  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    if (query) {
      query = query.concat(`&${detail}&`);
    } else {
      query = query.concat(`${detail}&`);
    }
  }
  apis.user.get_list(query, cul_offset.value, cul_limit.value).then(res => {
    apiResponseCheck(res, () => {
      const idx = (res.datas as User[]).map(item => item.id).indexOf(props.member.id);
      if (idx >= 0) (res.datas as User[]).splice(idx, 1);
      searchUserList.value.total = res.total;
      searchUserList.value.data = res.datas;
    });
  });
};

const setMemo = () => {
  showConfirm('회원 메모를 수정하시겠습니까?', () => {
    emit('updateMemo', { memo: props.member.memo });
  });
};

const convertLogItem = (data: string, when: string): string => {
  let logItem = [];
  const json = JSON.parse(data);
  if (Array.isArray(json.data)) {
    for (const i of json.data) {
      for (const k of Object.keys(i)) {
        switch (when) {
          case 'before':
            logItem.push(i[k].before);
            break;
          case 'after':
            logItem.push(i[k].after);
            break;
        }
      }
    }
  } else {
    if (when !== 'before') {
      logItem.push(json.data);
    }
  }
  return logItem.toString();
};

const modUserInfo = () => {
  const info = {} as any;
  let chkEmail = mAgree.chkEmail === true ? 'Y' : 'N';
  let chkSms = mAgree.chkSms === true ? 'Y' : 'N';

  if (props.member?.partner != originMemberInfo.value.partner) {
    info['partner'] = props.member?.partner;
  }

  if (props.member?.name != originMemberInfo.value.name) {
    info['name'] = props.member?.name;
  }

  if (props.member?.mobile != originMemberInfo.value.mobile) {
    info['mobile'] = props.member?.mobile;
  }

  if (props.member?.shop_yn != originMemberInfo.value.shop_yn) {
    info['shop_yn'] = props.member?.shop_yn;
  }

  if (getUserClass(props.member?.classes).includes('PA')) {
    if (props.member?.confirm_pass != originMemberInfo.value.confirm_pass) {
      info['confirm_pass'] = props.member?.confirm_pass;
    }
  }
  if (chkEmail != originMemberInfo.value.mailling) {
    info['mailling'] = chkEmail;
  }
  if (chkSms != originMemberInfo.value.sms) {
    info['sms'] = chkSms;
  }

  if (Object.keys(info).length === 0) {
    showAlert('변경사항이 없습니다.', 'warning');
  } else {
    showConfirm('화원 기본정보를 저장하시겠습니까?', () => {
      emit('updateFromInfo', info);
    });
  }
};
const handleSubmit = async () => {};

watch(
  () => props.member,
  member => {
    showLogConsole(`watched : ${member}`);
    originMemberInfo.value = JSON.parse(JSON.stringify(member));
    showLogConsole(originMemberInfo.value);

    mAgree.chkEmail = member.mailling === 'Y' ? true : false;
    mAgree.chkSms = member.sms === 'Y' ? true : false;
    mAgree.notAgree = member.mailling === 'N' && member.sms === 'N' ? true : false;
  },
);

const setListener = () => {
  //@ts-ignore
  document.getElementById('statusChangeModal').addEventListener('show.bs.modal', function (event) {
    showLogConsole('statusChangeModal open');
    showLogConsole(mStatus.value);
    refStatus.value = props.member?.status;
  });
};

onMounted(() => {
  // @ts-ignore
  HSBsValidation.init('.js-validate');

  setListener();
});

// 휴대폰 인증 영역
const reqMobileCert = (route: string) => {
  const host = window.location.origin;
  apis.join.phCertReq(host).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      nice_cert_call_info.value.integrity_value = res.integrity_value;
      nice_cert_call_info.value.enc_data = res.enc_data;
      nice_cert_call_info.value.token_version_id = res.token_version_id;
      nice_cert_popup_call(route);
    });
  });
};
const nice_cert_popup_call = (route: string) => {
  showLogConsole('nice_cert_popup_call() called');
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
  if (route === 'mb') window.addEventListener('message', receiveCertValueMb, false);
  else if (route === 'pw') window.addEventListener('message', receiveCertValuePw, false);
  // 본인인증창 팝업으로 띄움
  setTimeout(async () => {
    window.open('', 'cert_form', 'width=500, height=550, top=100, left=100, fullscreen=no, menubar=no, status=no, toolbar=no, titlebar=yes, location=no, scrollbar=no');
    form.submit();
    form.remove();
  });
};

const receiveCertValueMb = (e: any) => {
  window.removeEventListener('message', receiveCertValueMb);
  showLogConsole(e.data);
  if (!e.data.token_version_id || !e.data.enc_data || !e.data.integrity_value) {
    showAlert('본인인증에 실패하였습니다.\n잠시 후 다시 시도해주세요.', 'warning');
  } else {
    apis.join.phCertResult(e.data.token_version_id, e.data.enc_data, e.data.integrity_value).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        props.member.name = res.name;
        props.member.mobile = (res.mobile as string).replace('-', '');
      });
    });
  }
};
const receiveCertValuePw = (e: any) => {
  window.removeEventListener('message', receiveCertValuePw);
  showLogConsole(e.data);
  if (!e.data.token_version_id || !e.data.enc_data || !e.data.integrity_value) {
    showAlert('본인인증에 실패하였습니다.\n잠시 후 다시 시도해주세요.', 'warning');
  } else {
    apis.join.phCertResult(e.data.token_version_id, e.data.enc_data, e.data.integrity_value).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        if (props.me && res.mobile == originMemberInfo.value?.mobile) {
          showModal('pwChangeModal');
        } else {
          showAlert('등록된 회원정보와 인증정보가 서로 다릅니다.<br/>휴대폰번호를 변경하셨다면 먼저 회원정보 저장 후 시도해주세요.', 'warning');
          return;
        }
      });
    });
  }
};

const connectSns = (type: string) => {
  switch (type) {
    case 'payco':
      connectPayco();
      break;
    case 'naver':
      connectNaver();
      break;
    case 'kakao':
      connectKakao();
      break;
    case 'google':
      connectGoogle();
      break;
  }
};

const disconnect = (type: string) => {
  showConfirm('연결을 해제 하시겠습니까?', () => {
    let data = {} as any;
    data[`sns_${type}`] = '';

    const userId = undefined;

    apis.user.mod_user(userId, data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('연결이 해제되었습니다.', 'success', () => {
          router.go(0);
        });
      });
    });
  });
};

const connectKakao = () => {
  const restApiKey = import.meta.env.VITE_KAKAO_RESTAPI_KEY;
  const redirectUri = import.meta.env.VITE_KAKAO_CONNECT_REDIRECT_URI;
  const openUrl = `https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=${restApiKey}&redirect_uri=${redirectUri}`;
  window.addEventListener('message', refreshUserInfo, false);
  window.open(`${openUrl}`, 'oauth-form', 'width=500, height=600');
};

const connectNaver = async () => {
  const restApiKey = import.meta.env.VITE_NAVER_RESTAPI_KEY;
  const redirectUri = import.meta.env.VITE_NAVER_CONNECT_REDIRECT_URI;
  const openUrl = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${restApiKey}&redirect_uri=${redirectUri}`;
  window.addEventListener('message', refreshUserInfo, false);
  window.open(`${openUrl}`, 'oauth-form', 'width=500, height=600');
};

const connectGoogle = async () => {
  const restApiKey = import.meta.env.VITE_GOOGLE_RESTAPI_KEY;
  const redirectUri = import.meta.env.VITE_GOOGLE_CONNECT_REDIRECT_URI;
  const openUrl = `https://accounts.google.com/o/oauth2/v2/auth?response_type=token&client_id=${restApiKey}&redirect_uri=${redirectUri}&scope=email profile&state=${encodeURI('gState')}`;
  window.addEventListener('message', refreshUserInfo, false);
  window.open(`${openUrl}`, 'oauth-form', 'width=500, height=600');
};

const connectPayco = async () => {
  const restApiKey = import.meta.env.VITE_PAYCO_RESTAPI_KEY;
  const redirectUri = import.meta.env.VITE_PAYCO_CONNECT_REDIRECT_URI;
  const openUrl = `https://id.payco.com/oauth2.0/authorize?response_type=code&client_id=${restApiKey}&redirect_uri=${redirectUri}&serviceProviderCode=FRIENDS&userLocale=ko_KR`;
  window.addEventListener('message', refreshUserInfo, false);
  window.open(`${openUrl}`, 'oauth-form', 'width=500, height=600');
};

const refreshUserInfo = async (e: any) => {
  showAlert('정상적으로 연결되었습니다.', 'success', () => {
    router.go(0);
  });
};
</script>

<style scoped></style>
