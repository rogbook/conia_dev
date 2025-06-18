<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? [] : ['상점 관리']" :current="storeCode ? '상점관리 상세' : '상점 등록'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center" v-if="storeCode">
        <div class="col-auto mb-1">
          <div class="form-control-borderless h2">상점 관리</div>
          <div class="form-control-borderless h4">
            상점 이름 : [{{ store.title }}]<span class="ms-2 text-danger" style="font-size: 0.7rem">{{ store.dupl_store ? '* 공통몰 이용중' : '' }}</span>
          </div>
          <span v-if="getUserClassStr.includes('CM')"><MobilePushLink :title="`상점 홈 [ ${store.title} ]`" :storeGroup="storeInfo.group" :nextValue="''" :isStore="true" /></span>
          <div class="form-control-borderless h5" v-if="store.dupl_store"></div>
        </div>
        <div class="col-auto">
          <button v-if="!store.dupl_store" type="button" class="btn btn-sm btn-outline-info me-2 mb-1" @click.prevent="router.push({ path: `/store/detail/product`, state: { code: storeCode } })" :disabled="storeInfoDisable">상품 관리</button>
          <button v-if="!store.dupl_store" type="button" class="btn btn-sm btn-outline-info me-2 mb-1" @click.prevent="router.push({ path: `/store/detail/product/memo`, state: { code: storeCode } })" :disabled="storeInfoDisable">상품추가설명 관리</button>
          <button v-if="!store.dupl_store" type="button" class="btn btn-sm btn-outline-info me-2 mb-1" @click.prevent="router.push({ path: `/store/detail/theme`, state: { code: storeCode, storeGroup: storeInfo.group } })" :disabled="storeInfoDisable">테마 관리</button>
          <button v-if="!store.dupl_store" type="button" class="btn btn-sm btn-outline-info me-2 mb-1" @click.prevent="router.push({ path: `/store/detail/layout`, state: { code: storeCode } })" :disabled="storeInfoDisable">홈화면 관리</button>
          <button v-if="!store.dupl_store" type="button" class="btn btn-sm btn-outline-info me-2 mb-1" @click.prevent="router.push({ path: `/store/detail/popup`, state: { code: storeCode } })" :disabled="storeInfoDisable">팝업 관리</button>
          <button
            v-if="!store.dupl_store"
            type="button"
            class="btn btn-sm btn-outline-info me-2 mb-1"
            @click.prevent="router.push({ path: `/store/detail/board`, state: { code: storeCode, groupId: groupId, groupName: groupName, storeGroup: storeInfo.group } })"
            :disabled="storeInfoDisable">
            이벤트 관리
          </button>
          <button type="button" class="btn btn-sm btn-outline-info me-2 mb-1" @click.prevent="router.push({ name: 'storeDetailMember', state: { code: storeCode, able: storeInfo.able_target_use } })" :disabled="storeInfoDisable">이용자 관리</button>
          <button type="button" class="btn btn-sm btn-outline-info me-2 mb-1" @click.prevent="router.push({ path: `/store/detail/qna/list`, state: { code: storeCode } })" :disabled="storeInfoDisable">고객 문의 관리</button>
          <button v-if="!store.dupl_store && useUserStore().user.admin === 'Y'" type="button" class="btn btn-sm btn-outline-info mb-1" @click.prevent="router.push({ path: `/store/detail/exmenu`, state: { code: storeCode } })" :disabled="storeInfoDisable">마이메뉴 관리</button>
        </div>
      </div>
      <div class="row justify-content-between align-items-center" v-else>
        <div class="col-auto">
          <div class="form-control-borderless h2">상점 등록</div>
        </div>
      </div>
    </div>

    <div class="text-end px-5 pt-3">
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="modStoreInfo" v-if="storeCode" :disabled="storeInfoDisable">저장</button>
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="regStoreInfo" v-else>등록</button>
    </div>

    <!-- 
    <div class="card-footer py-2">
      <div class="row align-items-center justify-content-center">
        <div class="col-auto">
          <button class="btn btn-sm btn-primary" @click.prevent="modStoreInfo" v-if="storeCode">저장</button>
          <button class="btn btn-sm btn-primary" @click.prevent="regStoreInfo" v-else>등록</button>
        </div>
      </div>
    </div> -->

    <!-- 기본설정 영역 - [CM:읽기/수정, MC:읽기] -->
    <div class="card-body">
      <div class="card">
        <div class="card-header py-2">
          <span class="icon icon-xs icon-dark icon-circle" style="width: 0.5rem; height: 0.5rem"></span>
          기본정보
        </div>

        <div class="card-body">
          <div class="row col mb-2 align-items-center" v-if="!storeCode">
            <label class="col-lg-1 col-form-label"><span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 상점 운영자(MC)</label>
            <div class="col-lg-4">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="상점 운영자(MC)를 선택해주세요." disabled :value="mcInfo.name" />
                <button v-if="mcInfo.noMc" type="button" class="btn btn-sm btn-outline-dark" @click.prevent="showModal('paMemberSelModal')">검색</button>
              </div>
            </div>
          </div>

          <div class="row col mb-2 align-items-center">
            <label class="col-lg-1 col-form-label"><span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 상점 코드</label>
            <div class="" :class="{ 'col-md-4': storeCode, 'col-md-5': !storeCode }">
              <div class="input-group" v-if="storeCode">
                <input type="text" class="form-control" placeholder="상점 코드를 입력해주세요." disabled :value="store.code" />
              </div>
              <div class="input-group" v-else>
                <span class="input-group-text" style="font-size: 0.7rem">{{ mallHost }}/</span>
                <input type="text" class="form-control input-code" style="min-width: 230px" placeholder="상점 코드를 입력해주세요. (최대 16자)" maxlength="16" v-model="storeInfo.code" @change="codeChanged()" oninput="this.value = this.value.replace(/[^a-zA-Z0-9]/gi,'')" />
                <button type="button" class="btn btn-sm btn-outline-dark" @click.prevent="checkCode">중복체크</button>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-lg-1 col-form-label"><span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 상점 이름</label>
            <div class="col-lg-4">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="상점 이름을 입력해주세요. (최대 20자)" maxlength="20" v-model.trim="storeInfo.title" :disabled="storeInfoDisable" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="store.code">
            <label class="col-lg-1 col-form-label">도메인</label>
            <div class="col-auto">
              <a :href="`${mallHost}/${store.code}`" target="_blank">{{ mallHost }}/{{ store.code }}</a>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="store.code">
            <label class="col-lg-1 col-form-label">외부도메인</label>
            <div class="col-auto">
              <span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span>
              coniaworld.com 외 다른 외부 도메인 사용을 원할 경우 담당자에게 별도 요청 바랍니다.
              <br />
              <span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span>
              외부도메인 사용 시 소셜로그인이 지원되지 않습니다.
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="storeCode">
            <label class="col-lg-1 col-form-label">오픈설정</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_open_y" type="radio" class="form-check-input" name="radio_store_open" value="Y" v-model="storeInfo.status" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_open_y">운영중</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_open_r" type="radio" class="form-check-input" name="radio_store_open" value="R" v-model="storeInfo.status" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_open_r">오픈 준비중</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_open_n" type="radio" class="form-check-input" name="radio_store_open" value="N" v-model="storeInfo.status" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_open_n">미운영</label>
              </div>
            </div>
            <div class="col-auto" v-if="storeInfo?.status === 'SR'">
              <div class="form-check form-check-inline">
                <input id="radio_open_sr" type="radio" class="form-check-input" name="radio_store_open" value="SR" v-model="storeInfo.status" disabled />
                <label class="form-check-label" for="radio_open_sr">설정변경중</label>
              </div>
            </div>
            <div class="col-auto" v-if="storeInfo?.status === 'SP'">
              <div class="form-check form-check-inline">
                <input id="radio_open_sp" type="radio" class="form-check-input" name="radio_store_open" value="SP" v-model="storeInfo.status" disabled />
                <label class="form-check-label" for="radio_open_sp">설정변경중</label>
              </div>
            </div>
          </div>

          <div v-if="storeCode">
            <div class="row col mb-3 align-items-center">
              <label class="col-lg-1 col-form-label">
                PC 로고<br />
                <span style="font-size: 0.7rem" class="text-danger">(추천 가로 142px)</span>
              </label>

              <div class="col-lg-4">
                <div class="input-group" v-if="!storeInfo.logo_pc">
                  <UploadImage
                    class="form-control"
                    @change="
                      () => {
                        uploadImg_p.check = uploadImg_p.value.length > 0;
                      }
                    "
                    @upload="onRegistLogo"
                    :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                    :isDisabled="storeInfoDisable"
                    :compType="'logo-p'"
                    :placeholder="'이미지를 선택해 주세요.'"
                    disabled></UploadImage>
                </div>

                <div v-else>
                  <img class="img-fluid img-thumbnail d-block" :src="storeInfo.logo_pc" alt="pc 로고 이미지" />
                  <div class="mt-3">
                    <button type="button" class="btn btn-outline-info me-2 btn-sm" @click.prevent="storeInfo.logo_pc = ''" :disabled="storeInfoDisable">수정</button>
                  </div>
                </div>
              </div>
            </div>
            <div class="row col mb-3 align-items-center">
              <label class="col-lg-1 col-form-label">
                모바일 로고<br />
                <span style="font-size: 0.7rem" class="text-danger">(추천 가로 120px)</span>
              </label>
              <div class="col-lg-4">
                <div class="input-group" v-if="!storeInfo.logo_mobile">
                  <UploadImage
                    class="form-control"
                    @change="
                      () => {
                        uploadImg_m.check = uploadImg_m.value.length > 0;
                      }
                    "
                    @upload="onRegistLogo"
                    :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                    :isDisabled="storeInfoDisable"
                    :compType="'logo-m'"
                    :placeholder="'이미지를 선택해 주세요.'"
                    disabled />
                </div>

                <div v-else>
                  <img class="img-fluid img-thumbnail d-block" :src="storeInfo.logo_mobile" alt="모바일 로고 이미지" />
                  <div class="mt-3">
                    <button type="button" class="btn btn-outline-info me-2 btn-sm" @click.prevent="storeInfo.logo_mobile = ''" :disabled="storeInfoDisable">수정</button>
                  </div>
                </div>
              </div>
            </div>
            <div class="row col mb-3 align-items-center">
              <label class="col-lg-1 col-form-label">파비콘</label>
              <div class="col-lg-4">
                <div class="input-group" v-if="!storeInfo.favicon">
                  <UploadImage
                    class="form-control"
                    @change="
                      () => {
                        uploadImg_f.check = uploadImg_f.value.length > 0;
                      }
                    "
                    @upload="onRegistLogo"
                    :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                    :isDisabled="storeInfoDisable"
                    :compType="'favicon'"
                    :placeholder="'이미지를 선택해 주세요.'"
                    disabled />
                </div>
                <div v-else>
                  <img class="img-fluid img-thumbnail d-block" :src="storeInfo.favicon" alt="파비콘 로고 이미지" />
                  <div class="mt-3">
                    <button type="button" class="btn btn-outline-info me-2 btn-sm" @click.prevent="storeInfo.favicon = ''" :disabled="storeInfoDisable">수정</button>
                  </div>
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-lg-1 col-form-label">검색어</label>
              <div class="col-lg-4">
                <div class="input-group">
                  <input
                    v-model.trim="storeInfo.keyword"
                    type="text"
                    class="form-control"
                    maxlength="1000"
                    placeholder="검색어는 ,(콤마)로 구분됩니다. 1000자 까지 입력 가능 합니다."
                    aria-label="검색어는 ,(콤마)로 구분됩니다. 1000자 까지 입력 가능 합니다."
                    :disabled="storeInfoDisable" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 기본설정 영역 END -->
    <!-- 운영설정 영역 - [CM:읽기/수정, MC:읽기/수정] -->
    <div class="card-body" v-if="storeCode">
      <div class="card">
        <div class="card-header py-2">
          <span class="icon icon-xs icon-dark icon-circle" style="width: 0.5rem; height: 0.5rem"></span>
          운영설정
        </div>
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-lg-1 col-form-label me-5">상점 공개설정</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_public_y" type="radio" class="form-check-input" name="radio_store_public" value="O" v-model="storeInfo.type" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_public_y">공개몰</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_public_n" type="radio" class="form-check-input" name="radio_store_public" value="C" v-model="storeInfo.type" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_public_n">회원전용</label>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="storeInfo.type === 'C'">
            <label class="col-lg-1 col-form-label text-nowrap me-5">회원검증 사용설정</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_able_target_a" type="radio" class="form-check-input" name="radio_able_target" :value="storeInfo.able_target_use === 'N' ? 'Y' : storeInfo.able_target_use" v-model="storeInfo.able_target_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_able_target_a">사용</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_able_target_n" type="radio" class="form-check-input" name="radio_able_target" value="N" v-model="storeInfo.able_target_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_able_target_n">사용안함</label>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="storeInfo.type === 'C' && storeInfo.able_target_use !== 'N'">
            <label class="col-lg-1 col-form-label text-nowrap me-5">회원검증 방식설정</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_able_target_auto" type="radio" class="form-check-input" name="radio_able_target_type" value="A" v-model="storeInfo.able_target_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_able_target_auto">자동</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_able_target_manual" type="radio" class="form-check-input" name="radio_able_target_type" value="Y" v-model="storeInfo.able_target_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_able_target_manual">수동</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_able_target_fix" type="radio" class="form-check-input" name="radio_able_target_type" value="F" v-model="storeInfo.able_target_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_able_target_fix">고정</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_able_target_email" type="radio" class="form-check-input" name="radio_able_target_type" value="E" v-model="storeInfo.able_target_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_able_target_email">이메일</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_able_target_payco" type="radio" class="form-check-input" name="radio_able_target_type" value="P" v-model="storeInfo.able_target_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_able_target_payco">페이코 기업코드</label>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="storeCode && (storeInfo.able_target_use === 'F' || storeInfo.able_target_use === 'E')">
            <label class="col-lg-1 col-form-label text-nowrap me-5">{{ storeInfo.able_target_use === 'F' ? `회원검증 고정식별값` : '회원검증 이메일 도메인' }}</label>
            <div class="col-auto">
              <div class="input-group">
                <input type="text" class="form-control input-verify" :placeholder="storeInfo.able_target_use === 'F' ? `회원검증 코드를 입력해주세요` : '이메일 도메인을 입력해주세요.'" v-model.trim="storeInfo.verify_code" maxlength="32" :disabled="storeInfoDisable" />
              </div>
            </div>
            <div class="col-auto" v-if="storeInfo.able_target_use === 'E'">
              <span class="text-danger">예시) coniaworld.com</span>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="storeCode && storeInfo.able_target_use === 'P'">
            <label class="col-lg-1 col-form-label text-nowrap me-5">회원검증 기업코드 식별값</label>
            <div class="col-auto">
              <div class="input-group">
                <input type="text" class="form-control input-verify" :placeholder="`회원검증 기업코드를 입력해주세요`" v-model.trim="storeInfo.verify_code" maxlength="32" :disabled="storeInfoDisable" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="storeCode && storeInfo.able_target_use !== 'N' && storeInfo.type === 'C'">
            <label class="col-lg-1 col-form-label text-nowrap me-5">검증대상관리</label>
            <div class="col-auto">
              <button type="button" class="btn btn-sm btn-info" @click.prevent="showModal('ableTargetListModal')" style="min-width: 130px" :disabled="storeInfoDisable">이용가능 회원목록</button>
              <span class="ms-3" style="font-size: 0.8rem"></span>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="storeCode && getUserClassStr.includes('CM')">
            <label class="col-lg-1 col-form-label me-5">공통몰 사용설정</label>
            <div class="col-lg-6 col-xl-5 col-xxl-3">
              <div class="input-group">
                <span class="form-control" v-if="storeInfo.dupl_store" @click.prevent="showModal('searchStoreModal')">복제 대상 상점명 : [{{ storeInfo.dupl_store }}]</span>
                <button type="button" class="btn btn-info btn-sm" v-if="!store.dupl_store" @click.prevent="showModal('searchStoreModal')" style="min-width: 130px" :disabled="storeInfoDisable">
                  <span>복제대상 상점선택</span>
                </button>
                <button type="button" v-if="storeInfo.dupl_store" class="btn btn-danger btn-sm" @click.prevent="delDuplStore" :disabled="storeInfoDisable">공통몰 해제</button>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="getUserClassStr.includes('CM')">
            <label class="col-lg-1 col-form-label me-5">상점 그룹 지정</label>
            <div class="col-lg-3">
              <div class="tom-select-custom">
                <select class="form-select" v-model="storeInfo.group" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' :disabled="storeInfoDisable">
                  <option value="none">그룹 없음</option>
                  <option v-for="opt in storeGroupList" :key="opt.id" v-text="`${opt.name} (${opt.value})`" :value="opt.value"></option>
                </select>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="getUserClassStr.includes('CM')">
            <label class="col-lg-1 col-form-label me-5">상품별 결제수단 옵션 사용여부</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_pg_y" type="radio" class="form-check-input" name="radio_prd_pg_opt_use" value="Y" v-model="storeInfo.prd_pg_opt_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_pg_y">사용</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_pg_n" type="radio" class="form-check-input" name="radio_prd_pg_opt_use" value="N" v-model="storeInfo.prd_pg_opt_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_pg_n">사용안함</label>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="getUserClassStr.includes('CM')">
            <label class="col-lg-1 col-form-label me-5">식권 결제 옵션</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_meal_opt_y" type="radio" class="form-check-input" name="radio_meal_opt_use" value="Y" v-model="storeInfo.meal_opt_use" @change="changeLimitUse" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_meal_opt_y">사용</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_meal_opt_n" type="radio" class="form-check-input" name="radio_meal_opt_use" value="N" v-model="storeInfo.meal_opt_use" @change="changeLimitUse" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_meal_opt_n">사용안함</label>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="storeInfo.meal_opt_use === 'Y'">
            <label class="col-lg-1 col-form-label me-5">식권결제상품 사용시간 제한</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_meal_opt_limit_use_y" type="radio" class="form-check-input" name="radio_meal_opt_limit_use" value="Y" v-model="storeInfo.meal_opt_limit_use" @change="changeLimitUse" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_meal_opt_limit_use_y">사용</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_meal_opt_limit_use_n" type="radio" class="form-check-input" name="radio_meal_opt_limit_use" value="N" v-model="storeInfo.meal_opt_limit_use" @change="changeLimitUse" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_meal_opt_limit_use_n">사용안함</label>
              </div>
            </div>
          </div>

          <div class="row mb-2 align-items-center" v-if="storeInfo.meal_opt_use === 'Y' && storeInfo.meal_opt_limit_use === 'Y'">
            <label for="idLabel" class="col-lg-1 col-form-label me-5">사용시간 제한 설정</label>
            <div class="col">
              <div class="row" v-for="(item, i) in limitTime" :key="i">
                <div class="col-lg-3">
                  <div class="form-group">
                    <div :id="`startTimepicker${i}`" class="js-flatpickr flatpickr-custom input-group" :data-hs-flatpickr-options="{ appendTo: `#startTimepicker${i}`, dateFormat: 'H:i', enableTime: true, time_24hr: true, wrap: true }">
                      <div class="input-group-prepend input-group-text" data-bs-toggle>
                        <i class="bi-calendar-week"></i>
                      </div>
                      <input type="text" class="flatpickr-custom-form-control form-control" :id="`sTimepicker${i}`" @change="onChangeTimePicker('s', i)" placeholder="시간을 선택해주세요." v-model="item.start_time" :disabled="disableStartTime(i) || storeInfoDisable" />
                    </div>
                  </div>
                </div>
                <span class="col-auto align-items-center">~</span>
                <div class="col-lg-3">
                  <div class="form-group">
                    <div :id="`endTimepicker${i}`" class="js-flatpickr flatpickr-custom input-group" :data-hs-flatpickr-options="{ appendTo: `#endTimepicker${i}`, dateFormat: 'H:i', enableTime: true, time_24hr: true, wrap: true }">
                      <div class="input-group-prepend input-group-text" data-bs-toggle>
                        <i class="bi-calendar-week"></i>
                      </div>
                      <input type="text" class="flatpickr-custom-form-control form-control" :id="`eTimepicker${i}`" @change="onChangeTimePicker('e', i)" placeholder="시간을 선택해주세요." v-model="item.end_time" :disabled="disableEndTime(i) || storeInfoDisable" />
                    </div>
                  </div>
                </div>
                <div class="col-auto table-text-center" v-if="i === 0">
                  <button type="button" class="btn table-text-center text-primary" @click.prevent="addSection" :disabled="storeInfoDisable"><i class="bi-plus-circle" style="font-size: 1rem"></i></button>
                </div>
                <div class="col-auto table-text-center" v-else>
                  <button type="button" class="btn table-text-center text-danger" @click.prevent="deleteSection(i)" :disabled="storeInfoDisable"><i class="bi-x-circle" style="font-size: 1rem"></i></button>
                </div>
              </div>
            </div>
          </div>

          <div class="row col mb-2 align-items-center" v-if="storeInfo.meal_opt_use === 'Y'">
            <label class="col-lg-1 col-form-label me-5">식권결제상품 일괄취소</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_meal_opt_cancel_use_y" type="radio" class="form-check-input" name="radio_meal_opt_cancel_use" value="Y" v-model="storeInfo.meal_opt_cancel_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_meal_opt_cancel_use_y">사용</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_meal_opt_cancel_use_n" type="radio" class="form-check-input" name="radio_meal_opt_cancel_use" value="N" v-model="storeInfo.meal_opt_cancel_use" :disabled="storeInfoDisable" />
                <label class="form-check-label" for="radio_meal_opt_cancel_use_n">사용안함</label>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="storeCode && getUserClassStr.includes('CM') && !store.dupl_store">
            <label class="col-lg-1 col-form-label me-5">상점 설정 복사</label>
            <div class="col-lg-6 col-xl-5 col-xxl-3">
              <div class="input-group">
                <button type="button" class="btn btn-danger btn-sm" v-if="!store.dupl_store" @click.prevent="showModal('searchSettingStoreModal')" style="min-width: 130px" :disabled="storeInfoDisable">
                  <span>복사대상 상점선택</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 판매자 정보 설정 영역 -->
    <div class="card-body" v-if="storeCode">
      <div class="card">
        <div class="card-header py-2">
          <span class="icon icon-xs icon-dark icon-circle" style="width: 0.5rem; height: 0.5rem"></span>
          판매자정보
        </div>
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-1 col-form-label"><span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 정보</label>
            <div class="col">
              <div class="input-group">
                <textarea class="form-control" style="height: 15rem" type="text" placeholder="정보를 입력해주세요." v-model.trim="storeInfo.info" :disabled="storeInfoDisable" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 상점 로그 영역-->
    <div class="card-body" v-if="getUserClassStr.includes('CM') && storeCode">
      <div class="card">
        <div class="card-header">변경이력</div>
        <div class="card-body">
          <div class="row mb-2 align-items-center justify-content-between">
            <div class="col-auto"></div>
            <div class="col-auto">
              <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
            </div>
          </div>
          <div class="table-responsive">
            <table class="table table-align-middle card-table table-borderless">
              <thead class="thead-light">
                <tr class="text-center">
                  <th style="width: 12%">변경일</th>
                  <th style="width: 8%">등록/수정</th>
                  <th style="width: 20%">항목</th>
                  <th style="width: 20%">변경전</th>
                  <th style="width: 20%">변경후</th>
                  <th style="width: 12%">변경자</th>
                  <th style="width: 8%">상세</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center" v-for="(item, i) in storeLog.datas" :key="JSON.stringify(item)">
                  <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
                  <td>{{ item.action }}</td>
                  <td>{{ convertLogItemCate(item.msg).replace(/\/\/\//g, ' / ') }}</td>
                  <td style="max-width: 8rem">
                    <div v-if="convertLogItem(item.msg, 'before').startsWith('<img class')" v-html="convertLogItem(item.msg, 'before').replace(/\/\/\//g, ' / ')"></div>
                    <div
                      v-else
                      v-html="
                        convertLogItem(item.msg, 'before').length > 20
                          ? convertLogItem(item.msg, 'before')
                              .slice(0, 20)
                              .replace(/\/\/\//g, ' / ') + '...'
                          : convertLogItem(item.msg, 'before').replace(/\/\/\//g, ' / ')
                      "></div>
                  </td>
                  <td style="max-width: 8rem">
                    <div v-if="convertLogItem(item.msg, 'after').startsWith('<img class')" v-html="convertLogItem(item.msg, 'after').replace(/\/\/\//g, ' / ')"></div>
                    <div
                      v-else
                      v-html="
                        convertLogItem(item.msg, 'after').length > 20
                          ? convertLogItem(item.msg, 'after')
                              .slice(0, 20)
                              .replace(/\/\/\//g, ' / ') + '...'
                          : convertLogItem(item.msg, 'after').replace(/\/\/\//g, ' / ')
                      "></div>
                  </td>
                  <td>{{ item.writer }}</td>
                  <td>
                    <span class="badge text-bg-primary" style="cursor: pointer" @click.prevent="openChangeHistoryModal(convertLogItemCate(item.msg), convertLogItem(item.msg, 'before'), convertLogItem(item.msg, 'after'))">상세보기</span>
                  </td>
                </tr>
                <tr>
                  <td colspan="6" class="text-center" v-if="storeLog.total === 0">표시할 항목이 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="table-footer-area" v-if="storeLog.total > 0">
            <div class="row" v-if="total_page > 1">
              <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- MC 선택 Modal -->
  <Modal :id="'paMemberSelModal'" :title="'상점개시자(MC) 회원 선택'" :xlarge="true">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">상점개시자(MC) 회원을 선택합니다.</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <form class="mb-6">
              <!-- 회원타입 Checkbox -->
              <div class="row col">
                <label for="idLabel" class="col-md-2 col-form-label form-label">회원타입</label>
                <div class="col form-control border-0">
                  <div class="row">
                    <div class="col-auto">
                      <input type="radio" id="radio_type_mc" class="form-check-input" name="search_class_type" value="MC" v-model="checkedTypes" />
                      <label class="form-check-label px-1" for="radio_type_mc">MC</label>
                    </div>
                    <div class="col-auto">
                      <input type="radio" id="radio_type_mc-v" class="form-check-input" name="search_class_type" value="MC-V" v-model="checkedTypes" />
                      <label class="form-check-label px-1" for="radio_type_mc-v">MC-V</label>
                    </div>
                  </div>
                </div>
              </div>
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
                      <button type="button" class="btn btn-sm btn-info" @click.prevent="setMCInfo(user)">선택</button>
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
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <!-- 상점 이용가능 회원목록 Modal -->
  <Modal :id="'ableTargetListModal'" :title="'상점 이용가능 회원목록'" :xlarge="true">
    <template #body>
      <AbleTargetList ref="ableTargetList" @closePopup="hideModal('ableTargetListModal')" @openOneRegPopup="openOneRegPopup" @openModTargetPopup="openModTargetPopup" :store_code="storeCode" :store_title="storeInfo.title" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="hideModal('ableTargetListModal')">닫기</button>
    </template>
  </Modal>

  <Modal :id="'oneRegModal'" :title="modAbleTarget.id ? '상점이용가능자 개별수정' : '상점이용가능자 개별등록'" :second="true" :centered="true">
    <template #body>
      <AbleTargetInfoModal ref="ableTarget" :store_code="storeCode" :able-target="modAbleTarget" @closeAbleTargetPopup="closeAbleTargetPopup" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-sm btn-secondary" @click.prevent="hideModal('oneRegModal')">닫기</button>
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="ableTarget.modAbleTarget" v-if="modAbleTarget.id">수정</button>
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="ableTarget.oneRegAvailable" v-else>등록</button>
    </template>
  </Modal>

  <!-- 상점 검색 Modal -->
  <Modal :id="'searchStoreModal'" :title="'복제 대상 상점 선택'" :xlarge="true" :second="true">
    <template #body>
      <AllStoreListModal ref="storeModal" @selectStore="selectStore" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <!-- 상점 검색 Modal -->
  <Modal :id="'searchSettingStoreModal'" :title="'설정복사 대상 상점 선택'" :xlarge="true" :second="true">
    <template #body>
      <AllStoreListModal ref="storeModal" @selectStore="selectSettingStore" />
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>

  <ChangeHistoryModal :id="'changeHistoryModal'" :logTitle="logData.title" :logBefore="logData.before" :logAfter="logData.after" />
</template>

<script setup lang="ts">
import { onMounted, reactive, computed, ref, watch } from 'vue';
import type { Store, Log } from 'StoreListInfoModule';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import Modal from '@/components/comm/modal.vue';
import { useUserStore } from '@/stores/user';
import { apiResponseCheck, getUserClassStr, showAlert, showConfirm, dateTimeFormatConverter, convertStoreLog, showLogConsole, showModal, hideModal, isAdmin } from '@/utils/common-utils';
import UploadImage from '@/components/comm/uploadImage.vue';
import type { Class, User } from 'UserInfoModule';
import PageNavigator from '@/components/title/PageNavigator.vue';
import AbleTargetList from '@/pages/store/list/detail/available/AbleTargetList.vue';
import AllStoreListModal from '@/pages/store/list/detail/AllStoreListModal.vue';
import AbleTargetInfoModal from '@/pages/store/list/detail/available/AbleTargetInfoModal.vue';
import type { AbleTarget } from 'StoreAbleTargetModule';
import Pagination from '@/components/comm/Pagination.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useAuthStore } from '@/stores/auth';
import MobilePushLink from '@/components/comm/MobilePushLink.vue';
import type { OptionValue } from 'SettingValueModule';
import ChangeHistoryModal from '@/components/modals/comm/ChangeHistoryModal.vue';

const groupId = ref();
const groupName = ref('');

const checkedTypes = ref('MC');

const router = useRouter();
const store = ref({} as Store);
const storeCode = ref();

const ableTargetList = ref();
const ableTarget = ref();
const modAbleTarget = ref({} as AbleTarget);

const storeLog = ref({} as Log);
const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(storeLog.value.total / limit.value));
const mallHost = ref('');
const storeGroupList = ref([] as OptionValue[]);

const logData = reactive({
  title: '',
  before: '',
  after: '',
});

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getStoreLog();
};

const pageChange = (page: number) => {
  page_no.value = page;
  getStoreLog();
  // window.scrollTo({ top: 100, left: 0 });
};

const userName = computed(() => {
  return `${useUserStore().user.name}`;
});
const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});
const selDetailSearch = reactive({
  items: [
    { name: '이름', value: 'name' },
    { name: '아이디', value: 'user_id' },
    { name: '전화번호', value: 'mobile' },
    { name: '회사명', value: 'company_name' },
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
  }
};
const searchUserList = ref({
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

const searchUser = () => {
  let query = `class_code=${checkedTypes.value}&`;
  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    if (query) {
      query = query.concat(`${detail}&`);
    } else {
      query = query.concat(`${detail}&`);
    }
  }
  apis.user.get_list(query, 0, 100).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res.datas);
      searchUserList.value.data = res.datas;
    });
  });
};

const setMCInfo = (user: User) => {
  if (!user.company) {
    showAlert('사업자 정보가 없는 상점 운영자(MC) 회원입니다.\n 사업자 정보를 확인해주세요.', 'warning', () => {
      return;
    });
  } else if (user.store.length > 0) {
    showAlert('이미 상점을 운영중인 회원입니다.\n 다른 회원을 선택해주세요.', 'warning', () => {
      return;
    });
  } else {
    mcInfo.id = user.id;
    mcInfo.name = user.name;

    hideModal('paMemberSelModal');
  }
};

// 공금자(PA) 관련
const mcInfo = reactive({
  id: 0,
  name: '',
  noMc: true,
});

const storeInfo = reactive({
  code: '',
  title: '',
  domain: '',
  status: '',
  type: 'C',
  code_valid: false,
  logo_pc: '',
  logo_mobile: '',
  favicon: '',
  info: '',
  dupl_store: '',
  able_target_use: 'N',
  verify_code: '',
  group: 'none',
  prd_pg_opt_use: '',
  meal_opt_use: '',
  meal_opt_limit_use: '',
  meal_opt_limit_time: '',
  meal_opt_cancel_use: '',
  keyword: '',
});

/** 이벤트게시판 id를 얻기위한 메소드 */
const getStoreBoardGroupList = () => {
  apis.store.get_store_board_group_list(storeCode.value).then(res => {
    apiResponseCheck(res, () => {
      for (let value of res.datas) {
        if (value.name === '이벤트') {
          groupId.value = value.id;
          groupName.value = value.name;
          break;
        }
      }
    });
  });
};

// *** 상점 검색 관련 *** //
const selectStore = (code: string, title: string) => {
  showConfirm(`[${title}] 상점을 복제 대상 상점으로 설정하시겠습니까?`, () => {
    hideModal('searchStoreModal');
    if (store.value.code) {
      apis.store.mod_store(store.value.code, { dupl_store: code }).then(res => {
        apiResponseCheck(res, () => {
          showAlert('공통몰 사용 설정되었습니다.');
          store.value.dupl_store = code;
          storeInfo.dupl_store = code;
        });
      });
    }
  });
};

const selectSettingStore = (code: string, title: string) => {
  showConfirm(`[${title}] 상점의 설정을 복사하시겠습니까?<br /><span class='text-danger'>* 주의를 요하는 작업입니다.</span><br/><span class='text-danger'>(상점의 모든 설정이 대체되며 이 작업은 되돌릴 수 없습니다.)</span>`, () => {
    if (store.value.code) {
      apis.store.store_setting_copy(store.value.code, { target_store_code: code }).then(res => {
        apiResponseCheck(res, () => {
          showAlert('상점 설정 복사가 진행됩니다.<br/>작업 완료까지는 시간이 다소 소요될 수 있습니다.<br /><span class="text-danger">(&#8251; [레이아웃, 팝업, 이벤트내용 등]에 사용된 링크들은 별도 확인 필요)</span>', 'success', () => {
            getStore();
            if (userClass.value.includes('CM')) {
              getStoreLog();
            }
            hideModal('searchSettingStoreModal');
          });
        });
      });
    }
  });
};
// pc로고
const uploadImg_p = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});
// 모바일로고
const uploadImg_m = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});
// 파비콘
const uploadImg_f = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});

const getStore = () => {
  apis.store.get_store(storeCode.value).then(res => {
    apiResponseCheck(res, async () => {
      showLogConsole(res);
      store.value = await res;
      storeInfo.title = store.value.title!;
      storeInfo.domain = store.value.domain!;
      storeInfo.status = store.value.status!;
      storeInfo.type = store.value.type!;
      storeInfo.logo_pc = store.value.logo_pc!;
      storeInfo.logo_mobile = store.value.logo_mobile!;
      storeInfo.favicon = store.value.favicon!;
      storeInfo.info = store.value.info!;
      storeInfo.dupl_store = store.value.dupl_store ? store.value.dupl_store : '';
      storeInfo.able_target_use = store.value.able_target_use!;
      storeInfo.verify_code = store.value.verify_code ? store.value.verify_code : '';
      storeInfo.group = store.value.group ? store.value.group : 'none';
      storeInfo.prd_pg_opt_use = store.value.prd_pg_opt_use ? store.value.prd_pg_opt_use : 'N';
      storeInfo.meal_opt_use = store.value.meal_opt_use ? store.value.meal_opt_use : 'N';
      storeInfo.meal_opt_limit_use = store.value.meal_opt_limit_use ? store.value.meal_opt_limit_use : 'N';
      storeInfo.keyword = store.value.keyword ? store.value.keyword : '';

      //@ts-ignore
      if (JSON.parse(store.value.meal_opt_limit_time).length) {
        //@ts-ignore
        limitTime.value = [...JSON.parse(store.value.meal_opt_limit_time)];
      }

      setTimeout(() => {
        if (storeInfo.meal_opt_use === 'Y' && storeInfo.meal_opt_limit_use === 'Y') {
          initLimitTime();
        }
      }, 200);

      storeInfo.meal_opt_cancel_use = store.value.meal_opt_cancel_use ? store.value.meal_opt_cancel_use : 'N';
    });
  });
};

const codeChanged = () => {
  storeInfo.code_valid = false;
};

const checkCode = () => {
  if (storeInfo.code) {
    if (!/^[a-zA-Z0-9]+$/g.test(storeInfo.code)) {
      showAlert('상점코드는 영문과 숫자만 설정 가능합니다.', 'warning');
      storeInfo.code_valid = false;
      storeInfo.code = '';
      return;
    }

    apis.store.check_store_code(storeInfo.code).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res.exist);
        if (!res.exist) {
          showAlert('등록 가능한 코드 입니다.', 'success');
          storeInfo.code_valid = true;
        } else {
          showAlert('중복된 코드 입니다. 다시 입력해주세요.', 'error');
          storeInfo.code_valid = false;
        }
      });
    });
  } else {
    showAlert('상점 코드를 입력해주세요.', 'warning');
  }
};

const regStoreInfo = () => {
  let addValue: Store = {};
  if (mcInfo.noMc && !mcInfo.name) {
    showAlert('상점게시자(MC)를 선택해주세요.', 'warning');
    return;
  }
  if (!storeInfo.code) {
    showAlert('상점 코드를 입력해주세요.', 'warning');
    return;
  }
  if (!storeInfo.code_valid) {
    showAlert('상점 코드 중복체크를 진행해주세요.', 'warning');
    return;
  }
  if (!storeInfo.title) {
    showAlert('상점 이름을 입력해주세요.', 'warning');
    return;
  }
  if (storeInfo.able_target_use === 'F' && !storeInfo.verify_code) {
    showAlert('회원검증 고정코드를 입력해주세요.', 'warning');
    return;
  }
  if (storeInfo.able_target_use === 'E' && !storeInfo.verify_code) {
    showAlert('회원검증 이메일 도메일을 입력해주세요.', 'warning');
    return;
  }

  addValue = {
    code: storeInfo.code,
    title: storeInfo.title,
    domain: storeInfo.domain,
    type: storeInfo.type,
    member_id: mcInfo.id,
    able_target_use: storeInfo.able_target_use,
  };

  showConfirm('상점을 등록하시겠습니까?', () => {
    apis.store.reg_store(addValue).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        if (getUserClassStr.value.includes('CM')) {
          showAlert('상점이 등록되었습니다.', 'success', () => {
            if (window.history.length > 1) {
              router.back();
            } else {
              router.replace('/');
            }
          });
        } else {
          showAlert('상점이 등록되었습니다.<br/>다시 로그인 후 이용해주세요.', 'success', () => {
            useAuthStore().logout();
          });
        }
      });
    });
  });
};

const modStoreInfo = () => {
  let changeValue: Store = {};
  if (storeInfo.title !== store.value.title) {
    changeValue.title = storeInfo.title;
  }
  if (storeInfo.domain !== store.value.domain) {
    changeValue.domain = storeInfo.domain;
  }
  if (storeInfo.status !== store.value.status) {
    changeValue.status = storeInfo.status;
  }
  if (storeInfo.type !== store.value.type) {
    changeValue.type = storeInfo.type;
  }
  if (storeInfo.type !== store.value.type) {
    changeValue.type = storeInfo.type;
  }
  if (storeInfo.logo_pc !== store.value.logo_pc) {
    changeValue.logo_pc = storeInfo.logo_pc;
  }
  if (storeInfo.logo_mobile !== store.value.logo_mobile) {
    changeValue.logo_mobile = storeInfo.logo_mobile;
  }
  if (storeInfo.favicon !== store.value.favicon) {
    changeValue.favicon = storeInfo.favicon;
  }
  if (storeInfo.info !== store.value.info) {
    changeValue.info = storeInfo.info;
  }
  if (storeInfo.able_target_use !== store.value.able_target_use) {
    changeValue.able_target_use = storeInfo.able_target_use;
  }
  if (storeInfo.verify_code !== store.value.verify_code) {
    changeValue.verify_code = storeInfo.verify_code;
  }
  if (storeInfo.prd_pg_opt_use !== store.value.prd_pg_opt_use) {
    changeValue.prd_pg_opt_use = storeInfo.prd_pg_opt_use;
  }
  if (storeInfo.meal_opt_use !== store.value.meal_opt_use) {
    changeValue.meal_opt_use = storeInfo.meal_opt_use;
  }
  if (storeInfo.meal_opt_limit_use !== store.value.meal_opt_limit_use) {
    changeValue.meal_opt_limit_use = storeInfo.meal_opt_limit_use;
  }
  if (JSON.stringify(limitTime.value) !== store.value.meal_opt_limit_time) {
    changeValue.meal_opt_limit_time = JSON.stringify(limitTime.value);
  }
  if (storeInfo.meal_opt_cancel_use !== store.value.meal_opt_cancel_use) {
    changeValue.meal_opt_cancel_use = storeInfo.meal_opt_cancel_use;
  }
  if (storeInfo.keyword !== store.value.keyword) {
    changeValue.keyword = storeInfo.keyword;
  }

  //TODO: 상점 그룹 지정
  if (storeInfo.group != store.value.group) {
    if (storeInfo.group === 'none') {
      if (store.value.group != null) {
        changeValue.group = '_null_';
      }
    } else {
      changeValue.group = storeInfo.group;
    }
  }

  if (!Object.keys(changeValue).length) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }
  if (storeInfo.able_target_use === 'F' && !storeInfo.verify_code) {
    showAlert('회원검증 고정코드를 입력해주세요.', 'warning');
    return;
  }

  if (storeInfo.meal_opt_use === 'Y' && storeInfo.meal_opt_limit_use === 'Y') {
    if (limitTime.value.length > 1 && limitTime.value[1].start_time > limitTime.value[1].end_time) {
      showAlert('사용시간 제한 설정 값이 올바르지 않습니다.', 'warning');
      return;
    }
    if (limitTime.value[0].start_time !== '00:00') {
      showAlert('최초 시간은 00:00분으로 시작해야 합니다.', 'warning');
      return;
    }
    if (limitTime.value.length === 1 && limitTime.value[0].end_time !== '23:50') {
      showAlert('마지막 시간은 23:50분으로 끝나야 합니다.', 'warning');
      return;
    }
    if (limitTime.value.length === 2 && limitTime.value[1].end_time !== '23:50') {
      showAlert('마지막 시간은 23:50분으로 끝나야 합니다.', 'warning');
      return;
    }
    if (limitTime.value.length === 3 && limitTime.value[2].end_time !== '23:50') {
      showAlert('마지막 시간은 23:50분으로 끝나야 합니다.', 'warning');
      return;
    }
    for (let i in limitTime.value) {
      if (limitTime.value[i].start_time === '' || limitTime.value[i].end_time === '') {
        showAlert('사용시간 제한 설정 값을 입력해 주세요.', 'warning');
        return;
      }
      if (limitTime.value[i].start_time === limitTime.value[i].end_time) {
        showAlert('사용시간 제한 설정 값이 올바르지 않습니다.', 'warning');
        return;
      }
    }
  }
  // if (storeInfo.dupl_store !== store.value.dupl_store) {
  //   changeValue.dupl_store = storeInfo.dupl_store;
  //   if (!changeValue.dupl_store) {
  //     changeValue.dupl_store = '_null_';
  //   }
  // }
  showConfirm(`[${store.value.title}] 상점 정보를 변경하시겠습니까?`, () => {
    if (store.value.code) {
      apis.store.mod_store(store.value.code, changeValue).then(res => {
        apiResponseCheck(res, () => {
          showAlert('상점 정보가 변경되었습니다.', 'success');
          store.value.title = storeInfo.title;
          store.value.domain = storeInfo.domain;
          store.value.status = storeInfo.status;
          store.value.type = storeInfo.type;
          store.value.logo_pc = storeInfo.logo_pc;
          store.value.logo_mobile = storeInfo.logo_mobile;
          store.value.favicon = storeInfo.favicon;
          store.value.info = storeInfo.info;
          store.value.able_target_use = storeInfo.able_target_use;
          store.value.dupl_store = storeInfo.dupl_store;
          store.value.verify_code = storeInfo.verify_code;
          store.value.group = storeInfo.group ? storeInfo.group : 'none';
          store.value.prd_pg_opt_use = storeInfo.prd_pg_opt_use;
          store.value.meal_opt_use = storeInfo.meal_opt_use;
          store.value.meal_opt_limit_use = storeInfo.meal_opt_limit_use;
          store.value.meal_opt_limit_time = JSON.stringify(limitTime.value);
          store.value.meal_opt_cancel_use = storeInfo.meal_opt_cancel_use;
          store.value.keyword = storeInfo.keyword;
        });
      });
    } else {
      showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
    }
  });
};

const delDuplStore = () => {
  showConfirm('공통몰 사용해제를 진행하시겠습니까?', () => {
    if (store.value.code) {
      apis.store.mod_store(store.value.code, { dupl_store: '_null_' }).then(res => {
        apiResponseCheck(res, () => {
          showAlert('공통몰 사용이 해제되었습니다.');
          store.value.dupl_store = '';
          storeInfo.dupl_store = '';
        });
      });
    }
  });
};

const onRegistLogo = (files: File, target: string) => {
  apis.store.uploadLogo(storeCode.value, target, files).then(res => {
    apiResponseCheck(res, () => {
      switch (target) {
        case 'logo-p':
          storeInfo.logo_pc = res.uri;
          uploadImg_p.value = files.name;
          uploadImg_p.fileData = files;
          break;
        case 'logo-m':
          storeInfo.logo_mobile = res.uri;
          uploadImg_m.value = files.name;
          uploadImg_m.fileData = files;
          break;
        case 'favicon':
          storeInfo.favicon = res.uri;
          uploadImg_f.value = files.name;
          uploadImg_f.fileData = files;
          break;
      }
    });
  });
};
const openOneRegPopup = () => {
  modAbleTarget.value = {} as AbleTarget;
  showModal('oneRegModal');
};

const closeAbleTargetPopup = () => {
  hideModal('oneRegModal');

  ableTargetList.value.refreshList();
};

const openModTargetPopup = (t: AbleTarget) => {
  modAbleTarget.value = t;

  setTimeout(() => {
    showModal('oneRegModal');
  }, 200);
};

const checkCompany = () => {
  if (useUserStore().user.company_id === 0) {
    showAlert('사업자 정보가 없는 경우 상점을 등록할 수 없습니다.\n사업자 정보를 확인해주세요.', 'warning', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
  }
};

const convertLogItemCate = (data: string): string => {
  let logItem = [];
  const json = JSON.parse(data);

  if (Array.isArray(json.data)) {
    if (!json.data.length) {
      logItem.push(`-`);
      return logItem.toString();
    }
    for (const i of json.data) {
      for (const k of Object.keys(i)) {
        logItem.push(`${convertStoreLog(k)}`);
        break;
      }
    }
  } else {
    logItem.push('-');
  }
  return logItem.join('///');
};

const convertLogItem = (data: string, when: string): string => {
  let logItem = [];
  const json = JSON.parse(data);
  if (Array.isArray(json.data)) {
    if (!json.data.length) {
      logItem.push(`-`);
      return logItem.toString();
    }
    for (const i of json.data) {
      for (const k of Object.keys(i)) {
        if (!i[k][when]) {
          logItem.push('-');
          break;
        }
        if (k === 'layout' || k === 'contents') {
          logItem.push(`${k} 변경`);
          break;
        }
        if (k === 'logo_pc' || k === 'logo_mobile' || k === 'favicon' || k === 'image' || k === 'img') {
          logItem.push(`<img class='img-fluid img-thumbnail mb-2' style='height:60px' src='${i[k][when]}' />`);
          break;
        }
        logItem.push(i[k][when]);
      }
    }
  } else {
    if (when === 'after') {
      logItem.push(json.data);
    } else {
      logItem.push('-');
    }
  }

  // if (logItem.toString().startsWith('<img class')) {
  //   return logItem.toString().replace(/\,/g, '<br/>');
  // }
  return logItem.join('///');
};

const getStoreLog = () => {
  apis.store.getStoreLog(storeCode.value, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      storeLog.value.datas = res.datas;
      storeLog.value.total = res.total;
    });
  });
};

const getStoreGroupList = () => {
  apis.common.getOptionValue('store_group').then(res => {
    apiResponseCheck(res, () => {
      storeGroupList.value = res;
    });
  });
};

const stp0 = ref();
const etp0 = ref();
const stp1 = ref();
const etp1 = ref();
const stp2 = ref();
const etp2 = ref();

interface TimeRange {
  start_time: string;
  end_time: string;
}
const limitTime = ref<TimeRange[]>([]);

const changeLimitUse = (event: any) => {
  setTimeout(() => {
    if (storeInfo.meal_opt_use === 'Y' && storeInfo.meal_opt_limit_use === 'Y') {
      initLimitTime();
    }
  }, 200);
};

const addSection = () => {
  if (limitTime.value.length >= 3) return;
  limitTime.value.push({
    start_time: '',
    end_time: '',
  });

  switch (limitTime.value.length) {
    case 1:
      limitTime.value[0].start_time = '00:00';
      limitTime.value[0].end_time = '23:50';
      break;
    case 2:
      limitTime.value[0].end_time = '';
      limitTime.value[1].end_time = '23:50';
      break;
    case 3:
      limitTime.value[1].end_time = '';
      limitTime.value[2].end_time = '23:50';
      break;
  }

  setTimeout(() => {
    if (limitTime.value.length === 2) {
      //@ts-ignore
      stp1.value = flatpickr(document.querySelector('#sTimepicker1'), { noCalendar: true, enableTime: true, time_24hr: true });
      //@ts-ignore
      etp1.value = flatpickr(document.querySelector('#eTimepicker1'), { noCalendar: true, enableTime: true, time_24hr: true });
    } else if (limitTime.value.length === 3) {
      //@ts-ignore
      stp2.value = flatpickr(document.querySelector('#sTimepicker2'), { noCalendar: true, enableTime: true, time_24hr: true });
      //@ts-ignore
      etp2.value = flatpickr(document.querySelector('#eTimepicker2'), { noCalendar: true, enableTime: true, time_24hr: true });
    }
  }, 200);
};

const deleteSection = (i: number) => {
  if (limitTime.value.length === 3 && i === 1) {
    return;
  }
  limitTime.value.splice(i, 1);
  limitTime.value[limitTime.value.length - 1].end_time = '23:50';
};

const disableStartTime = (i: number) => {
  if (i === 0) {
    return true;
  } else {
    return false;
  }
};
const disableEndTime = (i: number) => {
  if (limitTime.value.length === i + 1) {
    return true;
  } else {
    return false;
  }
};

const onChangeEtp0 = () => {
  //@ts-ignore
  // stp1.value.setDate(window.$('#eTimepicker0').val() as string, true, 'H:i');

  //@ts-ignore
  limitTime.value[1].start_time = window.$('#eTimepicker0').val() as string;
};
const onChangeStp1 = () => {
  //@ts-ignore
  etp0.value.setDate(window.$('#sTimepicker1').val() as string, true, 'H:i');

  //@ts-ignore
  // limitTime.value[0].end_time = window.$('#sTimepicker1').val() as string;
};
const onChangeEtp1 = () => {
  //@ts-ignore
  // stp2.value.setDate(window.$('#eTimepicker1').val() as string, true, 'H:i');

  //@ts-ignore
  limitTime.value[2].start_time = window.$('#eTimepicker1').val() as string;
};
const onChangeStp2 = () => {
  //@ts-ignore
  etp1.value.setDate(window.$('#sTimepicker2').val() as string, true, 'H:i');

  //@ts-ignore
  // limitTime.value[1].end_time = window.$('#sTimepicker2').val() as string;
};

const onChangeTimePicker = (type: string, i: number) => {
  if (type === 's') {
    if (i === 1) {
      onChangeStp1();
    } else if (i === 2) {
      onChangeStp2();
    }
  } else if (type === 'e') {
    if (i === 0) {
      onChangeEtp0();
    } else if (i === 1) {
      onChangeEtp1();
    }
  }
};

const initLimitTime = () => {
  if (limitTime.value.length === 0) {
    addSection();
    setTimeout(() => {
      //@ts-ignore
      stp0.value = flatpickr(document.querySelector('#sTimepicker0'), { noCalendar: true, enableTime: true, time_24hr: true });
      //@ts-ignore
      etp0.value = flatpickr(document.querySelector('#eTimepicker0'), { noCalendar: true, enableTime: true, time_24hr: true });
    }, 200);
    return;
  }

  //@ts-ignore
  stp0.value = flatpickr(document.querySelector('#sTimepicker0'), { noCalendar: true, enableTime: true, time_24hr: true });
  //@ts-ignore
  etp0.value = flatpickr(document.querySelector('#eTimepicker0'), { noCalendar: true, enableTime: true, time_24hr: true });

  if (limitTime.value.length === 2) {
    //@ts-ignore
    stp1.value = flatpickr(document.querySelector('#sTimepicker1'), { noCalendar: true, enableTime: true, time_24hr: true });
    //@ts-ignore
    etp1.value = flatpickr(document.querySelector('#eTimepicker1'), { noCalendar: true, enableTime: true, time_24hr: true });
    return;
  }
  if (limitTime.value.length === 3) {
    //@ts-ignore
    stp1.value = flatpickr(document.querySelector('#sTimepicker1'), { noCalendar: true, enableTime: true, time_24hr: true });
    //@ts-ignore
    etp1.value = flatpickr(document.querySelector('#eTimepicker1'), { noCalendar: true, enableTime: true, time_24hr: true });
    //@ts-ignore
    stp2.value = flatpickr(document.querySelector('#sTimepicker2'), { noCalendar: true, enableTime: true, time_24hr: true });
    //@ts-ignore
    etp2.value = flatpickr(document.querySelector('#eTimepicker2'), { noCalendar: true, enableTime: true, time_24hr: true });
    return;
  }
};

const openChangeHistoryModal = (title: string, before: string, after: string) => {
  logData.title = title;
  logData.before = before;
  logData.after = after;
  showModal('changeHistoryModal');
};

const storeInfoDisable = computed(() => {
  return ['SR', 'SP'].includes(storeInfo?.status);
});

onMounted(() => {
  mallHost.value = import.meta.env.VITE_MALL_HOST;
  const code = history.state.code;
  limit.value = useCommonStore().getLimit;
  getStoreGroupList();
  if (code) {
    storeCode.value = code;
    getStore();
    getStoreBoardGroupList();
    if (userClass.value.includes('CM')) {
      getStoreLog();
    }
  }
  if (userClass.value.includes('MC')) {
    //@ts-ignore
    mcInfo.id = parseInt(useUserStore().user.id.toString());
    mcInfo.name = userName.value;
    mcInfo.noMc = false;

    checkCompany();
  }
});
</script>

<style scoped>
input.input-verify::placeholder {
  font-size: 0.7rem;
}
</style>
