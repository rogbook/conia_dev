<template>
  <div class="row justify-content-center">
    <div class="col-lg mb-1" :class="{ 'col-lg-8': !(showAddInfo.id || showAddInfo.memo || showAddInfo.background || showAddInfo.slide || showAddInfo.column || showAddInfo.banner || showAddInfo.button || showAddInfo.link) }">
      <div class="card">
        <div class="card-header">
          <div class="row col align-items-center py-0 justify-content-between">
            <label class="col-auto col-form-label py-0">컴포넌트 구성정보 - [{{ convertType }}] </label>
            <div class="col-auto">
              <button type="button" class="btn btn-sm btn-info" v-if="!showAddInfo.memo" @click.prevent="showAddInfoArea('memo', true)">메모입력</button>
            </div>
            <div class="col-auto" v-if="props.compData.compType === 'button-grp'">
              <input id="chkb-top" class="form-check-input chkb-ex me-2 text-danger" type="checkbox" name="chkb_exclude" value="Y" v-model="currentCompInfo.top" />
              <label class="text-danger" for="chkb-top">상단고정</label>
            </div>
            <div class="col-lg row align-items-center justify-content-end text-end">
              <label class="col-auto col-form-label py-0" v-if="props.compData?.compId">컴포넌트 아이디 - [{{ props.compData?.compId }}] </label>
              <button type="button" class="btn btn-sm btn-info col-auto ms-2" v-if="!showAddInfo.id" @click.prevent="showAddInfoArea('id', true)">{{ props.compData?.compId ? '변경' : '컴포넌트 아이디 지정' }}</button>
              <button type="button" class="btn btn-sm btn-info col-auto ms-2" v-if="!showAddInfo.background" @click.prevent="showAddInfoArea('background', true)">
                {{ props.compData?.background ? '배경 이미지 변경' : '배경 이미지 지정' }}
              </button>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="card back-card mb-2" v-if="props.compData?.background">
            <div class="card-header py-2">
              <div class="row align-items-center justify-content-between">
                <div class="columns col-auto">[배경이미지]</div>
              </div>
            </div>
            <div class="card-body">
              <div class="row align-items-center justify-content-between">
                <div class="col-auto">
                  <img :src="props.compData?.background" style="max-height: 2rem" />
                </div>
                <div class="col-auto">
                  <button type="button" class="btn btn-sm" @click.prevent="deleteBackgroundImg()">
                    <i class="bi-x-lg text-danger"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="button-info p-0 m-0" v-show="props.compData.compType.includes('button')">
            <div class="card button-card">
              <div class="card-header py-2">
                <div class="row align-items-center justify-content-between">
                  <div class="buttons col-auto">[버튼그룹 정보] <span style="font-size: 0.7rem">(드래그로 순서변경 가능)</span></div>
                  <div class="col-auto">
                    <button type="button" class="btn btn-sm btn-info" @click.prevent="showAddInfoArea('button', true)" v-if="!showAddInfo.button">버튼 추가</button>
                  </div>
                </div>
              </div>
              <div class="card-body button-card-body">
                <draggable v-model="props.compData.data.buttons" item-key="s">
                  <template #item="{ element: a, index: i }">
                    <div class="buttons form-control py-1 mb-1">
                      <div class="row align-items-center justify-content-between">
                        <div class="col row align-items-center">
                          <div class="ps-3 mb-2">
                            <div class="col-auto" v-if="a.type === 'anchor'">
                              <div class="ab-img" v-if="a.view_type === 'img'">[앵커] 이미지 : <img :src="a.view_src" style="max-height: 2rem" /> (타겟 : {{ a.target }})</div>
                              <div class="ab-text" v-else>[앵커] 표시명 : {{ a.name }} (타겟 : {{ a.target }})</div>
                            </div>
                            <div class="col-auto" v-else>
                              <div class="lb-img" v-if="a.view_type === 'img'">
                                <div>[링크] 이미지 : <img :src="a.view_src" style="max-height: 2rem" /></div>
                                <div v-if="a.full_link">
                                  외부링크 : <a :href="a.full_link" target="_blank">{{ a.full_link }}</a>
                                </div>
                                <div v-else-if="a.link">
                                  테마링크 : <a :href="`${mallHost}/${props.storeCode}${a.link}`" target="_blank">{{ a.link }}</a>
                                </div>
                              </div>
                              <div class="lb-text" v-else>
                                <div v-if="a.name">표시명 : {{ a.name }}</div>
                                <div v-if="a.full_link">
                                  외부링크 : <a :href="a.full_link" target="_blank">{{ a.full_link }}</a>
                                </div>
                                <div v-else-if="a.link">
                                  테마링크 : <a :href="`${mallHost}/${props.storeCode}${a.link}`" target="_blank">{{ a.link }}</a>
                                </div>
                              </div>
                            </div>
                          </div>
                          <div class="ps-3" v-if="a.visible === 'N' || a.start_date || a.end_date">
                            <div class="col-auto" style="font-size: 0.75rem">
                              <span v-if="a.visible === 'N'">[노출여부] : {{ a.visible === 'N' ? '비노출' : '노출' }}</span> <span v-if="a.visible === 'N' && (a.start_date || a.end_date)">/</span>
                              <span v-if="a.start_date || a.end">[노출기간] : {{ !a.start_date && !a.end_date ? '상시' : `${a.start_date} ~ ${a.end_date}` }}</span>
                            </div>
                          </div>
                        </div>
                        <div class="col-auto py-2">
                          <button type="button" class="btn badge bg-info me-2" @click.prevent="modSelButton(a, i)">수정</button>
                          <button type="button" class="btn badge bg-danger me-2" @click.prevent="deleteInfo('button', i)">삭제</button>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>
                <div class="button" v-if="currentCompInfo.buttons.length === 0">없음</div>
              </div>
            </div>
          </div>
          <div class="slide-info p-0 m-0" v-show="props.compData.compType.includes('slide')">
            <div class="card slide-card">
              <div class="card-header py-2">
                <div class="row align-items-center justify-content-between">
                  <div class="slides col-auto">[슬라이드 정보] <span style="font-size: 0.7rem">(드래그로 순서변경 가능)</span></div>
                  <div class="col-auto">
                    <button type="button" class="btn btn-sm btn-info" @click.prevent="showAddInfoArea('slide', true)" v-if="!showAddInfo.slide">슬라이드 추가</button>
                  </div>
                </div>
              </div>
              <div class="card-body slide-card-body">
                <draggable v-model="props.compData.data.slides" item-key="s">
                  <template #item="{ element: s, index: i }">
                    <div class="slides form-control py-1 mb-1">
                      <div class="row align-items-center justify-content-between">
                        <div class="col-auto ps-3">
                          <div class="row col align-items-center">
                            <div class="col-auto" v-if="s.img">이미지(PC) : <img :src="s.img" style="max-height: 2rem" /></div>
                            <div class="col-auto" v-if="s.img_m">이미지(모바일) : <img :src="s.img_m" style="max-height: 2rem" /></div>
                            <div class="col-auto" v-if="s.full_link">
                              외부링크 : <a :href="s.full_link" target="_blank">{{ s.full_link }}</a>
                            </div>
                            <div class="col-auto" v-else-if="s.link">
                              테마링크 : <a :href="`${mallHost}/${props.storeCode}${s.link}`" target="_blank">{{ s.link }}</a>
                            </div>
                          </div>
                          <div class="col row align-items-center mt-2" v-if="s.visible === 'N' || s.start_date || s.end_date">
                            <div class="col-auto" style="font-size: 0.75rem">
                              <span v-if="s.visible === 'N'">[노출여부] : {{ s.visible === 'N' ? '비노출' : '노출' }}</span> <span v-if="s.visible === 'N' && (s.start_date || s.end_date)">/</span>
                              <span v-if="s.start_date || s.end">[노출기간] : {{ !s.start_date && !s.end_date ? '상시' : `${s.start_date} ~ ${s.end_date}` }}</span>
                            </div>
                          </div>
                        </div>
                        <div class="col-auto">
                          <button type="button" class="btn badge bg-info me-2" @click.prevent="modSelSlide(s, i)">수정</button>
                          <button type="button" class="btn badge bg-danger me-2" @click.prevent="deleteInfo('slide', i)">삭제</button>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>
                <div class="slide" v-if="currentCompInfo.slides.length === 0">없음</div>
              </div>
            </div>
          </div>
          <div class="banner-info p-0 m-0 mb-4" v-show="props.compData.compType.includes('banner')">
            <div class="card banner-card">
              <div class="card-header py-2">
                <div class="row align-items-center justify-content-between">
                  <div class="banners col-auto">[배너 정보] <span style="font-size: 0.7rem">(드래그로 순서변경 가능)</span></div>
                  <div class="col-auto">
                    <button type="button" class="btn btn-sm btn-info" @click.prevent="showAddInfoArea('banner', true)" v-if="!showAddInfo.banner">배너 추가</button>
                  </div>
                </div>
              </div>
              <div class="card-body banner-card-body">
                <draggable v-model="props.compData.data.banners" item-key="b">
                  <template #item="{ element: b, index: i }">
                    <div class="banners form-control mb-1 py-1">
                      <div class="row col align-items-center justify-content-between">
                        <div class="col-auto">
                          <div class="row col align-items-center" v-if="b.type === 'img'">
                            <div class="col-auto" v-if="b.img">이미지(PC) : <img :src="b.img" style="max-height: 2rem" /></div>
                            <div class="col-auto" v-if="b.img_m">이미지(모바일) : <img :src="b.img_m" style="max-height: 2rem" /></div>
                            <div class="col-auto" v-if="b.full_link">
                              외부링크 : <a :href="b.full_link" target="_blank">{{ b.full_link }}</a>
                            </div>
                            <div class="col-auto" v-else-if="b.link">
                              테마링크 : <a :href="`${mallHost}/${props.storeCode}${b.link}`" target="_blank">{{ b.link }}</a>
                            </div>
                          </div>
                          <div class="" v-else-if="b.type?.startsWith('video')">
                            <div class="col-auto">
                              영상링크 : <a :href="b.v_link" target="_blank" style="font-size: 0.7rem">{{ b.v_link }}</a>
                            </div>
                          </div>
                          <div class="" v-else>
                            <div class="col-auto">
                              텍스트 :
                              <div v-html="b.text"></div>
                            </div>
                          </div>
                          <div class="col row align-items-center mt-2" v-if="b.visible === 'N' || b.start_date || b.end_date">
                            <div class="col-auto" style="font-size: 0.75rem">
                              <span v-if="b.visible === 'N'">[노출여부] : {{ b.visible === 'N' ? '비노출' : '노출' }}</span> <span v-if="b.visible === 'N' && (b.start_date || b.end_date)">/</span>
                              <span v-if="b.start_date || b.end">[노출기간] : {{ !b.start_date && !b.end_date ? '상시' : `${b.start_date} ~ ${b.end_date}` }}</span>
                            </div>
                          </div>
                        </div>
                        <div class="col-auto">
                          <button type="button" class="btn badge bg-info me-2" @click.prevent="modSelBanner(b, i)">수정</button>
                          <button type="button" class="btn badge bg-danger me-2" @click.prevent="deleteInfo('banner', i)">삭제</button>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>
                <div class="banner" v-if="currentCompInfo.banners.length === 0">없음</div>
              </div>
            </div>
          </div>
          <div class="column-info p-0 m-0" v-show="props.compData.compType.includes('column')">
            <div class="card column-card">
              <div class="card-header py-2">
                <div class="row align-items-center justify-content-between">
                  <div class="columns col-auto">[아이템 정보] <span style="font-size: 0.7rem">(드래그로 순서변경 가능)</span></div>
                  <div class="col-auto">
                    <button type="button" class="btn btn-sm btn-info" @click.prevent="showAddInfoArea('column', true)" v-if="!showAddInfo.column">아이템추가</button>
                  </div>
                </div>
              </div>
              <div class="card-body column-card-body">
                <draggable v-model="props.compData.data.columns" item-key="b">
                  <template #item="{ element: c, index: i }">
                    <div class="columns form-control mb-1 py-1">
                      <div class="row align-items-center justify-content-between">
                        <div class="col-auto">
                          <div class="" v-if="c.type === 'normal'">
                            <div class="row align-items-center">
                              <img :src="c.img" style="max-height: 2rem" />
                              <div class="col-auto" v-if="c.full_link">
                                외부링크 : <a :href="c.full_link" target="_blank">{{ c.full_link }}</a>
                              </div>
                              <div class="col-auto" v-else-if="c.link">
                                테마링크 : <a :href="`${mallHost}/${props.storeCode}${c.link}`" target="_blank">{{ c.link }}</a>
                              </div>
                            </div>
                          </div>
                          <div class="" v-else-if="c.type === 'product'">
                            <div class="row align-items-center">
                              <div class="col-auto" v-if="c.img">
                                <img :src="c.img" style="max-height: 2rem" />
                              </div>
                              <div class="col-auto" v-else>
                                <img src="@/assets/images/layers.png" style="max-height: 2rem" />
                              </div>
                              <div class="col-auto">상품명 : {{ c.name }}</div>
                              <div class="col-auto" v-if="c.thumbnail">썸네일 :</div>
                              <div class="col-auto" v-if="c.thumbnail">
                                <img :src="c.thumbnail" style="max-height: 2rem" />
                              </div>
                              <div class="col-auto">표시방식 : {{ c.view_type === 'list' ? '리스트형' : '기본형' }}</div>
                            </div>
                          </div>
                          <div class="" v-else-if="c.type?.startsWith('video')">
                            <div class="col-auto">
                              영상링크 : <a :href="c.v_link" target="_blank" style="font-size: 0.7rem">{{ c.v_link }}</a>
                            </div>
                          </div>
                          <div class="" v-else-if="c.type === 'shop'">
                            <div class="row align-items-center">
                              <div class="col-auto" v-if="c.img">
                                <img :src="c.img" style="max-height: 2rem" />
                              </div>
                              <div class="col-auto" v-else>
                                <img src="@/assets/images/layers.png" style="max-height: 2rem" />
                              </div>
                              <div class="col-auto">매장명 : {{ c.name }}</div>
                            </div>
                          </div>
                          <div class="" v-else>
                            <div class="col-auto">
                              텍스트 :
                              <div v-html="c.text"></div>
                            </div>
                          </div>
                          <div class="col row align-items-center mt-2" v-if="c.visible === 'N' || c.start_date || c.end_date">
                            <div class="col-auto" style="font-size: 0.75rem">
                              <span v-if="c.visible === 'N'">[노출여부] : {{ c.visible === 'N' ? '비노출' : '노출' }}</span> <span v-if="c.visible === 'N' && (c.start_date || c.end_date)">/</span>
                              <span v-if="c.start_date || c.end">[노출기간] : {{ !c.start_date && !c.end_date ? '상시' : `${c.start_date} ~ ${c.end_date}` }}</span>
                            </div>
                          </div>
                        </div>
                        <div class="col-auto">
                          <button type="button" class="btn badge bg-info me-2" @click.prevent="modSelColumn(c, i)">수정</button>
                          <button type="button" class="btn badge bg-danger me-2" @click.prevent="deleteInfo('column', i)">삭제</button>
                        </div>
                      </div>
                    </div>
                  </template>
                </draggable>
                <div class="column" v-if="currentCompInfo.columns.length === 0">없음</div>
              </div>
              <div class="card-footer">
                <div class="linkinfo">
                  <div class="linkinfo title">[텍스트 링크 정보] <span style="font-size: 0.7rem">(아이템 목록 하단 버튼)</span></div>
                  <div class="row align-items-center justify-content-between">
                    <div class="col-auto">
                      <div class="linkinfo info" v-if="currentCompInfo.link !== null">
                        <div>표시명 : {{ currentCompInfo.link.title }}</div>
                        <div v-if="currentCompInfo.link.full_link">
                          외부링크 : <a :href="currentCompInfo.link.full_link" target="_blank">{{ currentCompInfo.link.full_link }}</a>
                        </div>
                        <div v-else-if="currentCompInfo.link.link">
                          테마링크 : <a :href="`${mallHost}/${props.storeCode}${currentCompInfo.link.link}`" target="_blank">{{ currentCompInfo.link.link }}</a>
                        </div>
                      </div>
                      <div class="linkinfo info" v-else>없음</div>
                    </div>
                    <div class="col-auto" v-if="currentCompInfo.link !== null">
                      <button type="button" class="btn badge bg-info me-2" @click.prevent="modColumnLink">수정</button>
                      <button type="button" class="btn badge bg-danger me-2" @click.prevent="deleteColumnLink">삭제</button>
                    </div>
                    <div class="col-auto" v-else>
                      <button type="button" class="btn btn-sm btn-info" @click.prevent="showAddInfoArea('link', true)" v-if="!showAddInfo.link">텍스트 링크 설정</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer"></div>
      </div>
    </div>
    <div class="col-lg" v-if="showAddInfo.id || showAddInfo.memo || showAddInfo.background || showAddInfo.button || showAddInfo.slide || showAddInfo.banner || showAddInfo.column || showAddInfo.link">
      <div class="card">
        <div class="card-header py-2">
          <div class="row align-items-center justify-content-between">
            <div class="col-auto">{{ showAddInfo.id ? '컴포넌트 아이디 지정' : isMod ? '컴포넌트 정보 수정' : '컴포넌트 정보 추가' }}</div>
            <div class="col-auto">
              <button type="button" class="btn btn-sm btn-secondary" @click.prevent="showAddInfoArea('', false)">닫기</button>
            </div>
          </div>
        </div>
        <div class="card-body" v-if="showAddInfo.id">
          <div class="row mb-2 align-items-center">
            <label class="col-lg-3 col-form-label">컴포넌트 아이디</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="컴포넌트 아이디를 입력해주세요." v-model.lazy="currentCompInfo.id" @input="handleInput($event)" oninput="this.value = this.value.replace(/[^a-zA-Z0-9]/gi,'')" />
              </div>
            </div>
          </div>
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-info" @click.prevent="checkCompId">확인</button>
          </div>
        </div>
        <div class="card-body" v-if="showAddInfo.memo">
          <div class="row mb-2 align-items-center">
            <label class="col-lg-3 col-form-label">컴포넌트 메모</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="컴포넌트 메모를 입력해주세요. 최대 20자" maxlength="20" v-model.lazy="currentCompInfo.memo" />
              </div>
            </div>
          </div>
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-info" @click.prevent="checkCompMemo">확인</button>
          </div>
        </div>
        <div class="card-body" v-else-if="showAddInfo.background">
          <div class="row mb-2 align-items-center">
            <label class="col-lg-2 col-form-label">배경 이미지</label>
            <div class="col">
              <div class="input-group">
                <UploadImage
                  class="form-control"
                  @change="
                    () => {
                      uploadImgBack.check = uploadImgBack.value.length > 0;
                    }
                  "
                  @upload="onRegistComRegPhoto"
                  :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                  :compType="'back'"
                  :placeholder="uploadImgBack.value || '이미지를 선택해 주세요.'"
                  disabled />
              </div>
            </div>
          </div>
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-info" @click.prevent="checkBackImg">확인</button>
          </div>
        </div>
        <div class="card-body" v-else>
          <div class="button-grp-info-info p-0 m-0" v-if="props.compData.compType.includes('button') && showAddInfo.button">
            <div class="buttons mb-3">{{ isMod ? '[버튼 수정]' : '[버튼 추가]' }}</div>
            <div class="row align-items-center border-0 mb-2">
              <label class="col-lg-2 col-form-label">유형</label>
              <div class="col">
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_button_anchor" type="radio" class="form-check-input" name="radio_buttonType_a" value="anchor" v-model="newButtonType" @change="buttonTypeChange" />
                  <label class="form-check-label" for="radio_button_anchor">앵커</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_button_link" type="radio" class="form-check-input" name="radio_buttonType_l" value="link" v-model="newButtonType" @change="buttonTypeChange" />
                  <label class="form-check-label" for="radio_button_link">링크</label>
                </div>
              </div>
            </div>
            <div class="row align-items-center border-0 mb-2">
              <label class="col-lg-2 col-form-label">버튼 표시유형</label>
              <div class="col">
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_button_v_txt" type="radio" class="form-check-input" name="radio_buttonVType_t" value="" v-model="newCompInfo.button.view_type" />
                  <label class="form-check-label" for="radio_button_v_txt">텍스트</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_button_v_img" type="radio" class="form-check-input" name="radio_buttonVType_i" value="img" v-model="newCompInfo.button.view_type" />
                  <label class="form-check-label" for="radio_button_v_img">이미지</label>
                </div>
              </div>
            </div>
            <div class="button-anchor p-0 m-0" v-if="newButtonType === 'anchor'">
              <div class="v_type_img" v-if="newCompInfo.button.view_type === 'img'">
                <div class="row mb-2 align-items-center">
                  <label class="col-lg-2 col-form-label">앵커 표시 이미지 <br /><span style="font-size: 0.7rem" class="text-danger">(가로 길이는 64px로 자동 변환됨)</span></label>
                  <div class="col">
                    <div class="input-group">
                      <UploadImage
                        class="form-control"
                        @change="
                          () => {
                            uploadImgB.check = uploadImgB.value.length > 0;
                          }
                        "
                        @upload="onRegistComRegPhotoB"
                        :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                        :compType="'back'"
                        :placeholder="uploadImgB.value || '이미지를 선택해 주세요.'"
                        disabled />
                    </div>
                  </div>
                </div>
              </div>
              <div class="v_type_text" v-else>
                <div class="row mb-2 align-items-center">
                  <label class="col-lg-2 col-form-label">앵커 표시명</label>
                  <div class="col">
                    <div class="input-group">
                      <input type="text" class="form-control" placeholder="앵커 버튼 표시명을 입력해주세요." v-model.trim="newCompInfo.button.name" maxlength="6" />
                    </div>
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label">앵커타겟</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="앵커가 이동할 타겟의 아이디를 입력해주세요." v-model="newCompInfo.button.target" maxlength="20" oninput="this.value = this.value.replace(/[^a-zA-Z0-9]/gi,'')" />
                  </div>
                </div>
              </div>
            </div>
            <div class="button-link p0 m-0" v-else>
              <div class="v_type_img" v-if="newCompInfo.button.view_type === 'img'">
                <div class="row mb-2 align-items-center">
                  <label class="col-lg-2 col-form-label">링크 표시 이미지<br /><span style="font-size: 0.7rem" class="text-danger">(가로 길이는 64px로 자동 변환됨)</span></label>
                  <div class="col">
                    <div class="input-group">
                      <UploadImage
                        class="form-control"
                        @change="
                          () => {
                            uploadImgB.check = uploadImgB.value.length > 0;
                          }
                        "
                        @upload="onRegistComRegPhotoB"
                        :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                        :compType="'back'"
                        :placeholder="uploadImgB.value || '이미지를 선택해 주세요.'"
                        disabled />
                    </div>
                  </div>
                </div>
              </div>
              <div class="v_type_text" v-else>
                <div class="row mb-2 align-items-center">
                  <label class="col-lg-2 col-form-label">링크 표시명</label>
                  <div class="col">
                    <div class="input-group">
                      <input type="text" class="form-control" placeholder="링크 버튼 표시명을 입력해주세요." v-model.trim="newCompInfo.button.name" maxlength="6" />
                    </div>
                  </div>
                </div>
              </div>
              <div class="row align-items-center border-0 mb-2">
                <label class="col-lg-2 col-form-label">링크 유형</label>
                <div class="col">
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_button_l_f" type="radio" class="form-check-input" name="radio_buttonLType_f" value="full" v-model="newCompInfo.button.link_type" />
                    <label class="form-check-label" for="radio_button_l_f">외부링크</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_button_l_theme" type="radio" class="form-check-input" name="radio_buttonLType_t" value="theme" v-model="newCompInfo.button.link_type" />
                    <label class="form-check-label" for="radio_button_l_theme">테마링크</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_button_l_n" type="radio" class="form-check-input" name="radio_buttonLType_n" value="" v-model="newCompInfo.button.link_type" />
                    <label class="form-check-label" for="radio_button_l_n">사용안함</label>
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center" v-if="newCompInfo.button.link_type === 'full'">
                <label class="col-lg-2 col-form-label">외부링크</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="페이지 이동시 사용할 외부링크를 입력해주세요. (URL 전체)" v-model.trim="newCompInfo.button.full_link" />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center" v-else-if="newCompInfo.button.link_type === 'theme'">
                <label class="col-lg-2 col-form-label">링크(테마)</label>
                <div class="col">
                  <select class="form-select sel_theme_link" v-model="selLinkTheme1" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "링크(테마)를 선택해주세요."}'>
                    <option value="0" disabled selected>링크(테마)를 선택해주세요.</option>
                    <option v-for="t in linkThemeList" :key="t.id" v-text="t.pid ? `&nbsp;&nbsp;└&nbsp;${t.name}` : t.name" :value="t.id"></option>
                  </select>
                </div>
              </div>
            </div>
            <div class="row mb-2 align-items-center">
              <label class="col-lg-2 col-form-label">노출여부</label>
              <div class="col">
                <div class="row align-items-center form-control border-0">
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_button_visible_y" type="radio" class="form-check-input" name="radio_button_visible" value="Y" v-model="newCompInfo.button.visible" />
                    <label class="form-check-label" for="radio_button_visible_y">노출</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_button_visible_n" type="radio" class="form-check-input" name="radio_button_visible" value="N" v-model="newCompInfo.button.visible" />
                    <label class="form-check-label" for="radio_button_visible_n">비노출</label>
                  </div>
                </div>
              </div>
            </div>
            <SetPeriodDateComp :s-date="newCompInfo.button.start_date" :e-date="newCompInfo.button.end_date" @return-date="returnDate" ref="buttonDateRef" />
            <div class="text-end">
              <button type="button" class="btn btn-sm btn-info" @click.prevent="addNewButton" v-if="!isMod">버튼 추가</button>
              <button type="button" class="btn btn-sm btn-info" @click.prevent="modButtonData" v-else>버튼 수정</button>
            </div>
          </div>
          <div class="slide-info p-0 m-0" v-if="props.compData.compType.includes('slide') && showAddInfo.slide">
            <div class="slides mb-3">{{ isMod ? '[슬라이드 수정]' : '[슬라이드 추가]' }}</div>
            <div class="row mb-2 align-items-center">
              <label class="col-lg-2 col-form-label"
                >이미지(PC)<br />
                <span v-if="props.compData.compType.includes('lg')" style="font-size: 0.7rem" class="text-danger">(추천 가로 1920px)</span>
                <span v-if="props.compData.compType.includes('md')" style="font-size: 0.7rem" class="text-danger">(추천 가로 1230px)</span>
              </label>
              <div class="col">
                <div class="input-group">
                  <UploadImage
                    class="form-control"
                    @change="
                      () => {
                        uploadImg.check = uploadImg.value.length > 0;
                      }
                    "
                    @upload="onRegistComRegPhoto"
                    :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                    :compType="'slide'"
                    :placeholder="uploadImg.value || '이미지를 선택해 주세요.'"
                    disabled />
                </div>
              </div>
            </div>
            <div class="row mb-2 align-items-center">
              <label class="col-lg-2 col-form-label"
                >이미지(모바일)<br />
                <span v-if="props.compData.compType.includes('lg')" style="font-size: 0.7rem" class="text-danger">(추천 가로 991px)</span>
                <span v-if="props.compData.compType.includes('md')" style="font-size: 0.7rem" class="text-danger">(추천 가로 991px)</span>
              </label>
              <div class="col">
                <div class="input-group">
                  <UploadImage
                    class="form-control"
                    @change="
                      () => {
                        uploadImgM.check = uploadImgM.value.length > 0;
                      }
                    "
                    @upload="onRegistComRegPhotoM"
                    :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                    :compType="'slide'"
                    :placeholder="uploadImgM.value || '이미지를 선택해 주세요.'"
                    disabled />
                </div>
              </div>
            </div>
            <div class="row align-items-center border-0 mb-2">
              <label class="col-lg-2 col-form-label">링크 유형</label>
              <div class="col">
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_slide_l_f" type="radio" class="form-check-input" name="radio_slideLType_f" value="full" v-model="newCompInfo.slide.link_type" />
                  <label class="form-check-label" for="radio_slide_l_f">외부링크</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_slide_l_theme" type="radio" class="form-check-input" name="radio_slideLType_t" value="theme" v-model="newCompInfo.slide.link_type" />
                  <label class="form-check-label" for="radio_slide_l_theme">테마링크</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_slide_l_n" type="radio" class="form-check-input" name="radio_slideLType_n" value="" v-model="newCompInfo.slide.link_type" />
                  <label class="form-check-label" for="radio_slide_l_n">사용안함</label>
                </div>
              </div>
            </div>
            <div class="row mb-2 align-items-center" v-if="newCompInfo.slide.link_type === 'full'">
              <label class="col-lg-2 col-form-label">외부링크</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="페이지 이동시 사용할 외부링크를 입력해주세요. (URL 전체)" v-model.trim="newCompInfo.slide.full_link" />
                </div>
              </div>
            </div>
            <div class="row mb-2 align-items-center" v-else-if="newCompInfo.slide.link_type === 'theme'">
              <label class="col-lg-2 col-form-label">링크(테마)</label>
              <div class="col">
                <select class="form-select sel_theme_link" v-model="selLinkTheme1" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "링크(테마)를 선택해주세요."}'>
                  <option value="0" disabled selected>링크(테마)를 선택해주세요.</option>
                  <option v-for="t in linkThemeList" :key="t.id" v-text="t.pid ? `&nbsp;&nbsp;└&nbsp;${t.name}` : t.name" :value="t.id"></option>
                </select>
              </div>
            </div>
            <div class="row mb-2 align-items-center">
              <label class="col-lg-2 col-form-label">노출여부</label>
              <div class="col">
                <div class="row align-items-center form-control border-0">
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_slide_visible_y" type="radio" class="form-check-input" name="radio_slide_visible" value="Y" v-model="newCompInfo.slide.visible" />
                    <label class="form-check-label" for="radio_slide_visible_y">노출</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_slide_visible_n" type="radio" class="form-check-input" name="radio_slide_visible" value="N" v-model="newCompInfo.slide.visible" />
                    <label class="form-check-label" for="radio_slide_visible_n">비노출</label>
                  </div>
                </div>
              </div>
            </div>
            <SetPeriodDateComp :s-date="newCompInfo.slide.start_date" :e-date="newCompInfo.slide.end_date" @return-date="returnDate" ref="slideDateRef" />
            <div class="text-end">
              <button type="button" class="btn btn-sm btn-info" @click.prevent="addNewSlide" v-if="!isMod">슬라이드 추가</button>
              <button type="button" class="btn btn-sm btn-info" @click.prevent="modSlideData" v-else>슬라이드 수정</button>
            </div>
          </div>
          <div class="banner-info p-0 m-0" v-if="props.compData.compType.includes('banner') && showAddInfo.banner">
            <div class="banners mb-3">{{ isMod ? '[배너 수정]' : '[배너 추가]' }}</div>
            <div class="col mb-2 align-items-center">
              <label class="col-lg-2 col-form-label">유형</label>
              <div class="row form-control border-0">
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_img" type="radio" class="form-check-input" name="radio_columnType_b" value="img" v-model="newBannerType" @change="bannerTypeChange" />
                  <label class="form-check-label" for="radio_column_img">이미지</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_video" type="radio" class="form-check-input" name="radio_columnType_b" value="video" v-model="newBannerType" @change="bannerTypeChange" />
                  <label class="form-check-label" for="radio_column_video">영상(YOUTUBE)</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_videov" type="radio" class="form-check-input" name="radio_columnType_b" value="video-vimeo" v-model="newBannerType" @change="bannerTypeChange" />
                  <label class="form-check-label" for="radio_column_videov">영상(VIMEO)</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_text" type="radio" class="form-check-input" name="radio_columnType_b" value="text" v-model="newBannerType" @change="bannerTypeChange" />
                  <label class="form-check-label" for="radio_column_text">텍스트</label>
                </div>
              </div>
            </div>
            <div class="normal_banner" v-if="newBannerType === 'img'">
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label"
                  >이미지(PC)<br />
                  <span style="font-size: 0.7rem" class="text-danger">(추천 가로 1230px)</span>
                </label>
                <div class="col">
                  <div class="input-group">
                    <UploadImage
                      class="form-control"
                      @change="
                        () => {
                          uploadImg.check = uploadImg.value.length > 0;
                        }
                      "
                      @upload="onRegistComRegPhoto"
                      :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                      :compType="'banner'"
                      :placeholder="uploadImg.value || '이미지를 선택해 주세요.'"
                      disabled />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label"
                  >이미지(모바일)<br />
                  <span style="font-size: 0.7rem" class="text-danger">(추천 가로 961px)</span>
                </label>
                <div class="col">
                  <div class="input-group">
                    <UploadImage
                      class="form-control"
                      @change="
                        () => {
                          uploadImgM.check = uploadImgM.value.length > 0;
                        }
                      "
                      @upload="onRegistComRegPhotoM"
                      :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                      :compType="'banner'"
                      :placeholder="uploadImgM.value || '이미지를 선택해 주세요.'"
                      disabled />
                  </div>
                </div>
              </div>
              <div class="row align-items-center border-0 mb-2">
                <label class="col-lg-2 col-form-label">링크 유형</label>
                <div class="col">
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_banner_l_f" type="radio" class="form-check-input" name="radio_bannerLType_f" value="full" v-model="newCompInfo.banner.link_type" />
                    <label class="form-check-label" for="radio_banner_l_f">외부링크</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_banner_l_theme" type="radio" class="form-check-input" name="radio_bannerLType_t" value="theme" v-model="newCompInfo.banner.link_type" />
                    <label class="form-check-label" for="radio_banner_l_theme">테마링크</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_banner_l_n" type="radio" class="form-check-input" name="radio_bannerLType_n" value="" v-model="newCompInfo.banner.link_type" />
                    <label class="form-check-label" for="radio_banner_l_n">사용안함</label>
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center" v-if="newCompInfo.banner.link_type === 'full'">
                <label class="col-lg-2 col-form-label">외부링크</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="페이지 이동시 사용할 외부링크를 입력해주세요. (URL 전체)" v-model.trim="newCompInfo.banner.full_link" />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center" v-else-if="newCompInfo.banner.link_type === 'theme'">
                <label class="col-lg-2 col-form-label">링크(테마)</label>
                <div class="col">
                  <select class="form-select sel_theme_link" v-model="selLinkTheme1" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "링크(테마)를 선택해주세요."}'>
                    <option value="0" disabled selected>링크(테마)를 선택해주세요.</option>
                    <option v-for="t in linkThemeList" :key="t.id" v-text="t.pid ? `&nbsp;&nbsp;└&nbsp;${t.name}` : t.name" :value="t.id"></option>
                  </select>
                </div>
              </div>
            </div>
            <div class="video_banner" v-if="newBannerType === 'video' || newBannerType === 'video-vimeo'">
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label text-nowrap">영상 링크</label>
                <div class="col">
                  <div class="input-group">
                    <input class="form-control input-video" :placeholder="newBannerType === 'video' ? `영상 링크 (예시 : https://www.youtube.com/watch?v=IpkzCH5FByw)` : `영상 링크 (예시 : https://vimeo.com/903260788)`" v-model.trim="newCompInfo.banner.v_link" />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label">타이틀</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="제목을 입력해주세요." v-model.trim="newCompInfo.banner.title" maxlength="20" />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label">설명</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="설명을 입력해주세요." v-model.trim="newCompInfo.banner.description" maxlength="100" />
                  </div>
                </div>
              </div>
            </div>
            <div class="text_banner" v-if="newBannerType === 'text'">
              <div class="col mb-2">
                <CKEditorCustom @receiveData="newReceiveData" ref="newCkeditorCustomB" :removeItems="removeItems" :editor-data="editorData" />
              </div>
            </div>
            <div class="row mb-2 align-items-center">
              <label class="col-lg-2 col-form-label">노출여부</label>
              <div class="col">
                <div class="row align-items-center form-control border-0">
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_banner_visible_y" type="radio" class="form-check-input" name="radio_banner_visible" value="Y" v-model="newCompInfo.banner.visible" />
                    <label class="form-check-label" for="radio_banner_visible_y">노출</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_banner_visible_n" type="radio" class="form-check-input" name="radio_banner_visible" value="N" v-model="newCompInfo.banner.visible" />
                    <label class="form-check-label" for="radio_banner_visible_n">비노출</label>
                  </div>
                </div>
              </div>
            </div>
            <SetPeriodDateComp :s-date="newCompInfo.banner.start_date" :e-date="newCompInfo.banner.end_date" @return-date="returnDate" ref="bannerDateRef" />
            <div class="text-end">
              <button type="button" class="btn btn-sm btn-info" @click.prevent="addNewBanner" v-if="!isMod">배너 추가</button>
              <button type="button" class="btn btn-sm btn-info" @click.prevent="modBannerData" v-else>배너 수정</button>
            </div>
          </div>
          <div class="new-column-info p-0 m-0" v-if="props.compData.compType.includes('column') && showAddInfo.column">
            <div class="columns mb-3">{{ isMod ? '[아이템 수정]' : '[아이템 추가]' }}</div>
            <div class="col mb-2 align-items-center" v-if="isAvailableProd">
              <label class="col-lg-2 col-form-label">유형</label>
              <div class="row form-control border-0">
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_n" type="radio" class="form-check-input" name="radio_columnType_c" value="normal" v-model="newColumnType" @change="columnTypeChange" />
                  <label class="form-check-label" for="radio_column_n">일반</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_p" type="radio" class="form-check-input" name="radio_columnType_c" value="product" v-model="newColumnType" @change="columnTypeChange" />
                  <label class="form-check-label" for="radio_column_p">상품</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_v" type="radio" class="form-check-input" name="radio_columnType_c" value="video" v-model="newColumnType" @change="columnTypeChange" />
                  <label class="form-check-label" for="radio_column_v">영상(YOUTUBE)</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_vv" type="radio" class="form-check-input" name="radio_columnType_c" value="video-vimeo" v-model="newColumnType" @change="columnTypeChange" />
                  <label class="form-check-label" for="radio_column_vv">영상(VIMEO)</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_s" type="radio" class="form-check-input" name="radio_columnType_c" value="shop" v-model="newColumnType" @change="columnTypeChange" />
                  <label class="form-check-label" for="radio_column_s">매장</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_t" type="radio" class="form-check-input" name="radio_columnType_c" value="text" v-model="newColumnType" @change="columnTypeChange" />
                  <label class="form-check-label" for="radio_column_t">텍스트</label>
                </div>
              </div>
            </div>
            <div class="columns-view-type row align-items-center mb-3" v-if="newColumnType === 'product'">
              <label class="col-lg-2 col-form-label">상품 표시방식</label>
              <div class="col-md-auto">
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_vt_g" type="radio" class="form-check-input" name="radio_column_view_type_g" value="" v-model="newCompInfo.column.view_type" />
                  <label class="form-check-label" for="radio_column_vt_g">기본형</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_column_vt_l" type="radio" class="form-check-input" name="radio_column_view_type_l" value="list" v-model="newCompInfo.column.view_type" />
                  <label class="form-check-label" for="radio_column_vt_l">리스트형</label>
                </div>
              </div>
            </div>
            <div class="normal-column" v-if="newColumnType === 'normal'">
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label"
                  >이미지<br />
                  <span v-if="props.compData.compType.includes('column-2')" style="font-size: 0.7rem" class="text-danger"
                    >(추천 가로 611px , <br />
                    권장 비율 16:9)</span
                  >
                  <span v-if="props.compData.compType.includes('column-4')" style="font-size: 0.7rem" class="text-danger"
                    >(추천 가로 301.5 , <br />
                    고정 비율 1:1)</span
                  >
                </label>
                <div class="col">
                  <div class="input-group">
                    <UploadImage
                      class="form-control"
                      @change="
                        () => {
                          uploadImg2.check = uploadImg2.value.length > 0;
                        }
                      "
                      @upload="onRegistComRegPhoto"
                      :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                      :compType="'column'"
                      :placeholder="uploadImg2.value || '이미지를 선택해 주세요.'"
                      disabled />
                  </div>
                </div>
              </div>
              <div class="row align-items-center border-0 mb-2">
                <label class="col-lg-2 col-form-label">링크 유형</label>
                <div class="col">
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_column_l_f" type="radio" class="form-check-input" name="radio_columnLType_f" value="full" v-model="newCompInfo.column.link_type" />
                    <label class="form-check-label" for="radio_column_l_f">외부링크</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_column_l_theme" type="radio" class="form-check-input" name="radio_columnLType_t" value="theme" v-model="newCompInfo.column.link_type" />
                    <label class="form-check-label" for="radio_column_l_theme">테마링크</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_column_l_n" type="radio" class="form-check-input" name="radio_columnLType_n" value="" v-model="newCompInfo.column.link_type" />
                    <label class="form-check-label" for="radio_column_l_n">사용안함</label>
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center" v-if="newCompInfo.column.link_type === 'full'">
                <label class="col-lg-2 col-form-label">외부링크</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="페이지 이동시 사용할 외부링크를 입력해주세요. (URL 전체)" v-model.trim="newCompInfo.column.full_link" />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center" v-else-if="newCompInfo.column.link_type === 'theme'">
                <label class="col-lg-2 col-form-label">링크(테마)</label>
                <div class="col">
                  <select class="form-select sel_theme_link" v-model.trim="selLinkTheme2" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "링크(테마)를 선택해주세요."}'>
                    <option value="0" disabled selected>링크(테마)를 선택해주세요.</option>
                    <option v-for="t in linkThemeList" :key="t.id" v-text="t.pid ? `&nbsp;&nbsp;└&nbsp;${t.name}` : t.name" :value="t.id"></option>
                  </select>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label">타이틀</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="제목을 입력해주세요." v-model.trim="newCompInfo.column.title" maxlength="20" />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label">설명</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="설명을 입력해주세요." v-model.trim="newCompInfo.column.description" maxlength="100" />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label">클릭 시 행동</label>
                <div class="col">
                  <div class="row form-control border-0">
                    <div class="col-auto form-check form-check-inline">
                      <input id="radio_event_l" type="radio" class="form-check-input" name="radio_normal_event" value="link" v-model="newCompInfo.column.event" />
                      <label class="form-check-label" for="radio_event_l">링크</label>
                    </div>
                    <div class="col-auto form-check form-check-inline">
                      <input id="radio_event_z" type="radio" class="form-check-input" name="radio_normal_event" value="zoom" v-model="newCompInfo.column.event" />
                      <label class="form-check-label" for="radio_event_z">확대</label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="product-column" v-else-if="newColumnType === 'product'">
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label">상품선택</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="상품을 선택해주세요." v-model="newCompInfo.column.name" readonly />
                    <button type="button" class="btn btn-secondary" @click.prevent="showProductList">상품선택</button>
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center" v-if="checkProductType">
                <label class="col-lg-2 col-form-label"
                  >이미지<br />
                  <span v-if="props.compData.compType.includes('column-2')" style="font-size: 0.7rem" class="text-danger"
                    >(추천 가로 611px , <br />
                    권장 비율 16:9)</span
                  >
                  <span v-if="props.compData.compType.includes('column-4')" style="font-size: 0.7rem" class="text-danger"
                    >(추천 가로 301.5 , <br />
                    고정 비율 1:1)</span
                  >
                </label>
                <div class="col">
                  <div class="input-group">
                    <UploadImage
                      class="form-control"
                      @change="
                        () => {
                          uploadImg2.check = uploadImg2.value.length > 0;
                        }
                      "
                      @upload="onRegistComRegPhoto"
                      :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
                      :compType="'column'"
                      :placeholder="uploadImg2.value || '이미지를 선택해 주세요.'"
                      disabled />
                  </div>
                </div>
              </div>
            </div>
            <div class="product-column" v-else-if="newColumnType === 'video' || newColumnType === 'video-vimeo'">
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label text-nowrap">영상 링크</label>
                <div class="col">
                  <div class="input-group">
                    <input class="form-control input-video" :placeholder="newColumnType === 'video' ? `영상 링크 (예시 : https://www.youtube.com/watch?v=IpkzCH5FByw)` : `영상 링크 (예시 : https://vimeo.com/903260788)`" v-model.trim="newCompInfo.column.v_link" />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label">타이틀</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="제목을 입력해주세요." v-model.trim="newCompInfo.column.title" maxlength="20" />
                  </div>
                </div>
              </div>
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label">설명</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="설명을 입력해주세요." v-model.trim="newCompInfo.column.description" maxlength="100" />
                  </div>
                </div>
              </div>
            </div>
            <div class="normal-column" v-else-if="newColumnType === 'shop'">
              <div class="row mb-2 align-items-center">
                <label class="col-lg-2 col-form-label">매장선택</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" placeholder="매장을 선택해주세요." v-model="newCompInfo.column.name" readonly />
                    <button type="button" class="btn btn-secondary" @click.prevent="showShopList">매장선택</button>
                  </div>
                </div>
              </div>
            </div>
            <div class="normal-column" v-else-if="newColumnType === 'text'">
              <div class="col mb-2">
                <CKEditorCustom @receiveData="newReceiveData" ref="newCkeditorCustomC" :removeItems="removeItems" :editor-data="editorData" />
              </div>
            </div>
            <div class="row mb-2 align-items-center">
              <label class="col-lg-2 col-form-label">노출여부</label>
              <div class="col">
                <div class="row form-control border-0">
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_column_visible_y" type="radio" class="form-check-input" name="radio_column_visible" value="Y" v-model="newCompInfo.column.visible" />
                    <label class="form-check-label" for="radio_column_visible_y">노출</label>
                  </div>
                  <div class="col-auto form-check form-check-inline">
                    <input id="radio_column_visible_n" type="radio" class="form-check-input" name="radio_column_visible" value="N" v-model="newCompInfo.column.visible" />
                    <label class="form-check-label" for="radio_column_visible_n">비노출</label>
                  </div>
                </div>
              </div>
            </div>
            <SetPeriodDateComp :s-date="newCompInfo.column.start_date" :e-date="newCompInfo.column.end_date" @return-date="returnDate" ref="columnDateRef" />
            <div class="text-end">
              <button type="button" class="btn btn-sm btn-info" @click.prevent="addNewColumn" v-if="!isMod">아이템 추가</button>
              <button type="button" class="btn btn-sm btn-info" @click.prevent="modColumnData" v-else>아이템 수정</button>
            </div>
          </div>
          <div class="clink-info p-0 m-0" v-if="props.compData.compType.includes('column') && showAddInfo.link">
            <div class="clink-info mb-3">[텍스트 링크 설정]</div>
            <div class="row mb-2 align-items-center">
              <label class="col-lg-2 col-form-label">표시명</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="링크에 보일 텍스트를 입력해주세요. (예: 전체보기, 더보기 등)" v-model.trim="newCompInfo.link.title" maxlength="20" />
                </div>
              </div>
            </div>
            <div class="row align-items-center border-0 mb-2">
              <label class="col-lg-2 col-form-label">링크 유형</label>
              <div class="col">
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_link_l_f" type="radio" class="form-check-input" name="radio_linkLType_f" value="full" v-model="newCompInfo.link.link_type" />
                  <label class="form-check-label" for="radio_link_l_f">외부링크</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_link_l_theme" type="radio" class="form-check-input" name="radio_linkLType_t" value="theme" v-model="newCompInfo.link.link_type" />
                  <label class="form-check-label" for="radio_link_l_theme">테마링크</label>
                </div>
                <div class="col-auto form-check form-check-inline">
                  <input id="radio_link_l_n" type="radio" class="form-check-input" name="radio_linkLType_n" value="" v-model="newCompInfo.link.link_type" />
                  <label class="form-check-label" for="radio_link_l_n">사용안함</label>
                </div>
              </div>
            </div>
            <div class="row mb-2 align-items-center" v-if="newCompInfo.link.link_type === 'full'">
              <label class="col-lg-2 col-form-label">외부링크</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="페이지 이동시 사용할 외부링크를 입력해주세요. (URL 전체)" v-model.trim="newCompInfo.link.full_link" />
                </div>
              </div>
            </div>
            <div class="row mb-2 align-items-center" v-else-if="newCompInfo.link.link_type === 'theme'">
              <label class="col-lg-2 col-form-label">링크(테마)</label>
              <div class="col">
                <select class="form-select sel_theme_link" v-model="selLinkTheme3" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "링크(테마)를 선택해주세요."}'>
                  <option value="0" disabled selected>링크(테마)를 선택해주세요.</option>
                  <option v-for="t in linkThemeList" :key="t.id" v-text="t.pid ? `&nbsp;&nbsp;└&nbsp;${t.name}` : t.name" :value="t.id"></option>
                </select>
              </div>
            </div>
            <div class="text-end">
              <button type="button" class="btn btn-sm btn-info" @click.prevent="changeLink">텍스트링크 설정</button>
            </div>
          </div>
        </div>
        <div class="card-footer"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref, watch } from 'vue';
import type { PropType } from 'vue';
import UploadImage from '@/components/comm/uploadImage.vue';
import apis from '@/apis';
import type { Theme } from 'ThemeInfoModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import draggable from 'vuedraggable';
import CKEditorCustom from '@/pages/settings/product/common/list/detail/CKEditorCustom.vue';
import SetPeriodDateComp from '@/pages/store/list/detail/theme/layout/comp/SetPeriodDateComp.vue';

const mallHost = import.meta.env.VITE_MALL_HOST;
const checkProductType = ref(true);
let compColumnProducts = reactive([] as { id: string; img: string; name: string }[]);

const selLinkTheme1 = ref(0);
const selLinkTheme2 = ref(0);
const selLinkTheme3 = ref(0);

const showAddInfo = reactive({
  id: false,
  memo: false,
  background: false,
  button: false,
  slide: false,
  banner: false,
  column: false,
  link: false,
});

const isMod = ref(false);

const showAddInfoArea = (type: string, flag: boolean) => {
  clearNewCompInfo();
  isMod.value = false;
  currentCompInfo.id = props.compData.compId;
  showAddInfo.id = showAddInfo.memo = showAddInfo.background = showAddInfo.button = showAddInfo.slide = showAddInfo.banner = showAddInfo.column = showAddInfo.link = false;
  type === 'id'
    ? (showAddInfo.id = flag)
    : type === 'memo'
    ? (showAddInfo.memo = flag)
    : type === 'background'
    ? (showAddInfo.background = flag)
    : type === 'button'
    ? (showAddInfo.button = flag)
    : type === 'slide'
    ? (showAddInfo.slide = flag)
    : type === 'banner'
    ? (showAddInfo.banner = flag)
    : type === 'column'
    ? (showAddInfo.column = flag)
    : type === 'link'
    ? (showAddInfo.link = flag)
    : (showAddInfo.id = showAddInfo.memo = showAddInfo.background = showAddInfo.button = showAddInfo.slide = showAddInfo.banner = showAddInfo.column = showAddInfo.link = flag);

  if (!type) {
    isMod.value = false;
    selModIdx.value = -1;
    editorData.value = '';
  }
};

const props = defineProps({
  storeCode: String,
  compData: {} as any,
  themeList: [] as PropType<Theme[]>,
});

const linkThemeList = ref([] as Theme[]);

const buttonDateRef = ref();
const slideDateRef = ref();
const bannerDateRef = ref();
const columnDateRef = ref();

const newColumnType = ref('product');
const newBannerType = ref('img');
const newButtonType = ref('anchor');

interface ButtonInfo {
  type: string;
  target?: string;
  name?: string;
  view_type?: string;
  view_src?: string;
  full_link?: string;
  link?: string;
  visible?: string;
  start_date?: string;
  end_date?: string;
  link_type?: string;
}

interface SlideInfo {
  img?: string | null;
  img_m?: string | null;
  full_link: string;
  link: string;
  visible?: string;
  start_date?: string;
  end_date?: string;
  link_type?: string;
}

interface BannerInfo {
  type: string;
  img?: string | null;
  img_m?: string | null;
  full_link?: string | null;
  link?: string | null;
  v_link?: string | null;
  title?: string | null;
  description?: string | null;
  text?: string | null;
  visible?: string;
  start_date?: string;
  end_date?: string;
  link_type?: string;
}

interface ColumnInfo {
  type: string;
  view_type?: string;
  img?: string | null;
  thumbnail?: string | null;
  full_link?: string | null;
  v_link?: string | null;
  link?: string | null;
  title?: string | null;
  description?: string | null;
  id?: string | null;
  name?: string | null;
  text?: string | null;
  event?: string | null;
  visible?: string;
  start_date?: string;
  end_date?: string;
  link_type?: string;
}

const currentCompInfo = reactive({
  id: '',
  memo: '',
  background: '',
  top: [] as string[],
  buttons: [] as ButtonInfo[],
  slides: [] as SlideInfo[],
  banners: [] as BannerInfo[],
  columns: [] as ColumnInfo[],
  link: {} as any,
});

const newCompInfo = reactive({
  button: {
    type: '',
    name: '',
    view_type: '',
    view_src: '',
    target: '',
    full_link: '',
    link: '',
    visible: 'Y',
    start_date: '',
    end_date: '',
    link_type: '',
  },
  slide: {
    img: '',
    img_m: '',
    full_link: '',
    link: '',
    visible: 'Y',
    start_date: '',
    end_date: '',
    link_type: '',
  },
  banner: {
    type: '',
    img: '',
    img_m: '',
    v_link: '',
    full_link: '',
    link: '',
    title: '',
    description: '',
    text: '',
    visible: 'Y',
    start_date: '',
    end_date: '',
    link_type: '',
  },
  column: {
    type: '',
    view_type: '',
    img: '',
    thumbnail: '',
    full_link: '',
    v_link: '',
    link: '',
    title: '',
    description: '',
    id: '',
    name: '',
    text: '',
    event: '',
    visible: 'Y',
    start_date: '',
    end_date: '',
    link_type: '',
  },
  link: {
    title: '',
    full_link: '',
    link: '',
    link_type: '',
  },
});

const isAvailableProd = computed(() => {
  return props.compData.compType === 'banner-column-2' || props.compData.compType === 'banner-column-4' || props.compData.compType === 'column-2' || props.compData.compType === 'column-4';
});

// eslint-disable-next-line vue/return-in-computed-property
const convertType = computed(() => {
  switch (props.compData.compType) {
    case 'button-grp':
      return '버튼 그룹';
    case 'slide-lg':
      return '슬라이드(L)';
    case 'slide-md':
      return '슬라이드(M)';
    case 'banner':
      return '배너';
    case 'banner-column-2':
      return '배너 및 아이템2';
    case 'banner-column-4':
      return '배너 및 아이템4';
    case 'column-2':
      return '아이템2';
    case 'column-4':
      return '아이템4';
  }
});
// 이미지
const uploadImg = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});

// 이미지
const uploadImg2 = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});

const uploadImgM = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});

// 아이템 배경이미지
const uploadImgBack = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});

// 버튼 이미지
const uploadImgB = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});

// 에디터
const editorData = ref('');
const removeItems = ref(['link']);
const newCkeditorCustomC = ref();
const newCkeditorCustomB = ref();

const handleInput = (event: any) => {
  // eslint-disable-next-line no-self-assign
  event.target.value.length > 11 ? (event.target.value = event.target.value.slice(0, 11)) : (event.target.value = event.target.value);
};

const newReceiveData = (data: string) => {
  if (showAddInfo.banner) {
    newCompInfo.banner.text = data;
    return;
  }
  if (showAddInfo.column) {
    newCompInfo.column.text = data;
  }
};

const onRegistComRegPhoto = (files: File, target: string) => {
  apis.store.uploadPhoto(files).then(res => {
    apiResponseCheck(res, () => {
      switch (target) {
        case 'slide':
          newCompInfo.slide.img = res.uri;
          uploadImg.value = files.name;
          uploadImg.fileData = files;
          break;
        case 'banner':
          newCompInfo.banner.img = res.uri;
          uploadImg.value = files.name;
          uploadImg.fileData = files;
          break;
        case 'column':
          if (newColumnType.value === 'product') {
            newCompInfo.column.thumbnail = res.uri;
            uploadImg2.value = files.name;
            uploadImg2.fileData = files;
          } else {
            newCompInfo.column.img = res.uri;
            uploadImg2.value = files.name;
            uploadImg2.fileData = files;
          }
          break;
        case 'back':
          currentCompInfo.background = res.uri;
          uploadImgBack.value = files.name;
          uploadImgBack.fileData = files;
          break;
      }
    });
  });
};

const onRegistComRegPhotoM = (files: File, target: string) => {
  apis.store.uploadPhoto(files).then(res => {
    apiResponseCheck(res, () => {
      switch (target) {
        case 'slide':
          newCompInfo.slide.img_m = res.uri;
          uploadImgM.value = files.name;
          uploadImgM.fileData = files;
          break;
        case 'banner':
          newCompInfo.banner.img_m = res.uri;
          uploadImgM.value = files.name;
          uploadImgM.fileData = files;
          break;
      }
    });
  });
};

const onRegistComRegPhotoB = (files: File, target: string) => {
  apis.store.uploadPhoto(files).then(res => {
    apiResponseCheck(res, () => {
      newCompInfo.button.view_src = res.uri;
      uploadImgB.value = files.name;
      uploadImgB.fileData = files;
    });
  });
};

const emit = defineEmits(['passToCompInfo', 'deleteBackImg', 'openProdModal']);
const saveClicked = () => {
  if (props.compData.compType === 'button-grp') {
    if (currentCompInfo.top.length > 0) {
      // eslint-disable-next-line vue/no-mutating-props
      props.compData.top = 'Y';
    } else {
      // eslint-disable-next-line vue/no-mutating-props
      props.compData.top = '';
    }
  }
  emit('passToCompInfo', props.compData);
};

const receiveProduct = (id: number, name: string, photo: string | undefined) => {
  newCompInfo.column.id = id.toString();
  newCompInfo.column.name = name;
  newCompInfo.column.img = photo ? photo : '';

  checkProductType.value = true;
};

const receiveProducts = (product: any[]) => {
  compColumnProducts = [];

  for (let i in product) {
    compColumnProducts.push({
      id: product[i].product.id,
      name: product[i].product.name,
      img: product[i].product?.photos[0]?.uri,
    });
  }

  newCompInfo.column.name = compColumnProducts.length > 1 ? `${compColumnProducts[0].name} 외 ${compColumnProducts.length - 1}건` : compColumnProducts[0].name;
  checkProductType.value = false;
};

const receiveShop = (id: number, name: string, image: string) => {
  newCompInfo.column.id = id.toString();
  newCompInfo.column.name = name;
  newCompInfo.column.img = image;
};

const getProdInfo = async (id: number | string) => {
  try {
    const product = await apis.product.getProduct(id as number);
    let obj = {};
    if (product.photos.length) {
      obj = { uri: product.photos[0].uri, name: product.name };
    } else {
      obj = { uri: '', name: product.name };
    }
    return obj;
  } catch (err) {
    showLogConsole(err, 'err');
  }
};

const remakeThemeList = (arr: Theme[]) => {
  if (arr) {
    for (const t of arr) {
      linkThemeList.value.push(t);
      if (t.sub?.length > 0) {
        remakeThemeList(t.sub);
      }
    }
  }
};

const showCompInfo = async () => {
  clearCurrentCompInfo();
  linkThemeList.value = [];
  remakeThemeList(props.themeList);
  currentCompInfo.id = props.compData.compId;
  if (props.compData.background) currentCompInfo.background = props.compData.background;
  if (props.compData.memo) currentCompInfo.memo = props.compData.memo;
  switch (props.compData.compType) {
    case 'button-grp':
      currentCompInfo.buttons = props.compData.data.buttons;
      if (props.compData.top === 'Y') {
        currentCompInfo.top.push(props.compData.top);
      }
      break;
    case 'slide-lg':
    case 'slide-md':
      currentCompInfo.slides = props.compData.data.slides;
      break;
    case 'banner':
      currentCompInfo.banners = props.compData.data.banners;
      break;
    case 'banner-column-2':
    case 'banner-column-4':
      currentCompInfo.banners = props.compData.data.banners;
      currentCompInfo.columns = props.compData.data.columns;
      if (props.compData.data.link) currentCompInfo.link = props.compData.data.link;
      break;
    case 'column-2':
    case 'column-4':
      currentCompInfo.columns = props.compData.data.columns;
      if (props.compData.data.link) currentCompInfo.link = props.compData.data.link;
      break;
  }

  if (props.compData.compType?.includes('column')) {
    // TODO: 상품인경우 이미지 가져오기
    for (const i in currentCompInfo.columns) {
      const item = currentCompInfo.columns[i];
      if (item.type === 'product') {
        const prod: any = await getProdInfo(item.id!);
        item.img = prod.uri;
        item.name = prod.name;
      }
    }
  }
};

defineExpose({ saveClicked, receiveProduct, receiveProducts, receiveShop, showCompInfo });

const clearCurrentCompInfo = () => {
  currentCompInfo.id = '';
  currentCompInfo.top = [];
  currentCompInfo.background = '';
  currentCompInfo.memo = '';
  currentCompInfo.link = null;
  currentCompInfo.slides = [];
  currentCompInfo.columns = [];
  currentCompInfo.banners = [];
  currentCompInfo.buttons = [];

  clearNewCompInfo();

  showAddInfo.id = showAddInfo.memo = showAddInfo.button = showAddInfo.slide = showAddInfo.banner = showAddInfo.column = showAddInfo.link = false;
};

const clearNewCompInfo = () => {
  selLinkTheme1.value = 0;
  selLinkTheme2.value = 0;
  selLinkTheme3.value = 0;
  uploadImg.value = '';
  uploadImg.fileData = undefined;
  uploadImg2.value = '';
  uploadImg2.fileData = undefined;
  uploadImgM.value = '';
  uploadImgM.fileData = undefined;
  uploadImgB.value = '';
  uploadImgB.fileData = undefined;
  editorData.value = '';
  newCompInfo.button = { type: '', link: '', full_link: '', name: '', target: '', visible: 'Y', start_date: '', end_date: '', view_src: '', view_type: '', link_type: '' };
  newButtonType.value = 'anchor';
  newCompInfo.slide = { img: '', img_m: '', full_link: '', link: '', visible: 'Y', start_date: '', end_date: '', link_type: '' };
  newBannerType.value = 'img';
  newCompInfo.banner = { type: '', img: '', img_m: '', v_link: '', full_link: '', link: '', title: '', description: '', text: '', visible: 'Y', start_date: '', end_date: '', link_type: '' };
  newColumnType.value = 'product';
  newCompInfo.column = { type: '', view_type: '', img: '', thumbnail: '', full_link: '', v_link: '', link: '', title: '', description: '', id: '', name: '', text: '', event: '', visible: 'Y', start_date: '', end_date: '', link_type: '' };
};

const columnTypeChange = () => {
  newCompInfo.column = { type: '', view_type: '', img: '', thumbnail: '', full_link: '', v_link: '', link: '', title: '', description: '', id: '', name: '', text: '', event: 'link', visible: 'Y', start_date: '', end_date: '', link_type: '' };
  uploadImg2.value = '';
  uploadImg2.fileData = undefined;
  editorData.value = '';
  selLinkTheme2.value = 0;
};

const bannerTypeChange = () => {
  newCompInfo.banner = { type: '', img: '', img_m: '', full_link: '', link: '', v_link: '', title: '', description: '', text: '', visible: 'Y', start_date: '', end_date: '', link_type: '' };
  uploadImg.value = '';
  uploadImg.fileData = undefined;
  editorData.value = '';
  selLinkTheme1.value = 0;
};

const buttonTypeChange = () => {
  newCompInfo.button = { type: '', full_link: '', link: '', name: '', target: '', visible: 'Y', start_date: '', end_date: '', view_src: '', view_type: '', link_type: '' };
  selLinkTheme1.value = 0;
  uploadImgB.value = '';
  uploadImgB.fileData = undefined;
};

const changeLink = (add: boolean = true) => {
  showConfirm(add ? '텍스트 링크 정보를 설정하시겠습니까?' : '텍스트 링크 정보를 수정하시겠습니까?', () => {
    if (newCompInfo.link.link_type === 'theme' && selLinkTheme3.value <= 0) {
      showAlert('테마를 선택해주세요.', 'warning');
      return;
    }

    if (selLinkTheme3.value > 0) newCompInfo.link.link = `/theme/${selLinkTheme3.value}`;
    currentCompInfo.link = { title: newCompInfo.link.title, full_link: newCompInfo.link.link_type === 'full' ? newCompInfo.link.full_link : '', link: newCompInfo.link.link_type === 'theme' ? newCompInfo.link.link : '', link_type: newCompInfo.link.link_type };
    // eslint-disable-next-line vue/no-mutating-props
    props.compData.data.link = currentCompInfo.link;
    newCompInfo.link = { title: '', full_link: '', link: '', link_type: '' };
    selLinkTheme3.value = 0;
    showAddInfo.link = false;
    if (!add) {
      isMod.value = false;
    }
  });
};

const addNewColumn = () => {
  columnDateRef.value.editFinish('column');
  if (!checkDate('column')) {
    showAlert('노출기간을 확인해주세요.', 'warning');
    return;
  }
  if (newColumnType.value === 'text') {
    newCkeditorCustomC.value.saveClicked();
  }

  //컴포넌트 구성 갯수 체크
  let checkCompLen = currentCompInfo.columns.length;
  const countLimit = 20;
  if (newColumnType.value === 'product' && !checkProductType.value) {
    if (checkCompLen + compColumnProducts.length > countLimit) {
      showAlert(`아이템은 총 ${countLimit}개까지만 구성이 가능합니다.`, 'warning');
      return;
    }
  } else {
    if (checkCompLen > countLimit - 1) {
      showAlert(`아이템은 총 ${countLimit}개까지만 구성이 가능합니다.`, 'warning');
      return;
    }
  }

  //TODO: 데이터 체크
  showConfirm('아이템을 추가하시겠습니까?', () => {
    if (selLinkTheme2.value > 0) newCompInfo.column.link = `/theme/${selLinkTheme2.value}`;
    if (newColumnType.value === 'normal') {
      currentCompInfo.columns.push({
        type: newColumnType.value,
        img: newCompInfo.column.img,
        full_link: newCompInfo.column.link_type === 'full' ? newCompInfo.column.full_link : '',
        v_link: newCompInfo.column.v_link,
        link: newCompInfo.column.link_type === 'theme' ? newCompInfo.column.link : '',
        title: newCompInfo.column.title,
        description: newCompInfo.column.description,
        event: newCompInfo.column.event,
        visible: newCompInfo.column.visible,
        start_date: newCompInfo.column.start_date,
        end_date: newCompInfo.column.end_date,
        link_type: newCompInfo.column.link_type,
      });
    } else if (newColumnType.value === 'product') {
      if (newCompInfo.column.thumbnail) {
        if (newCompInfo.column.view_type === 'list') {
          currentCompInfo.columns.push({
            type: newColumnType.value,
            view_type: newCompInfo.column.view_type,
            img: newCompInfo.column.img,
            thumbnail: newCompInfo.column.thumbnail,
            id: newCompInfo.column.id,
            name: newCompInfo.column.name,
            visible: newCompInfo.column.visible,
            start_date: newCompInfo.column.start_date,
            end_date: newCompInfo.column.end_date,
          });
        } else {
          currentCompInfo.columns.push({
            type: newColumnType.value,
            img: newCompInfo.column.img,
            thumbnail: newCompInfo.column.thumbnail,
            id: newCompInfo.column.id,
            name: newCompInfo.column.name,
            visible: newCompInfo.column.visible,
            start_date: newCompInfo.column.start_date,
            end_date: newCompInfo.column.end_date,
          });
        }
      } else {
        if (checkProductType.value) {
          //선택버튼
          if (newCompInfo.column.view_type === 'list') {
            currentCompInfo.columns.push({
              type: newColumnType.value,
              view_type: newCompInfo.column.view_type,
              img: newCompInfo.column.img,
              id: newCompInfo.column.id,
              name: newCompInfo.column.name,
              visible: newCompInfo.column.visible,
              start_date: newCompInfo.column.start_date,
              end_date: newCompInfo.column.end_date,
            });
          } else {
            currentCompInfo.columns.push({ type: newColumnType.value, img: newCompInfo.column.img, id: newCompInfo.column.id, name: newCompInfo.column.name, visible: newCompInfo.column.visible, start_date: newCompInfo.column.start_date, end_date: newCompInfo.column.end_date });
          }
        } else {
          //체크선택버튼
          for (let i in compColumnProducts) {
            if (newCompInfo.column.view_type === 'list') {
              currentCompInfo.columns.push({
                type: newColumnType.value,
                view_type: newCompInfo.column.view_type,
                id: compColumnProducts[i].id,
                name: compColumnProducts[i].name,
                img: compColumnProducts[i].img,
                visible: newCompInfo.column.visible,
                start_date: newCompInfo.column.start_date,
                end_date: newCompInfo.column.end_date,
              });
            } else {
              currentCompInfo.columns.push({
                type: newColumnType.value,
                id: compColumnProducts[i].id,
                name: compColumnProducts[i].name,
                img: compColumnProducts[i].img,
                visible: newCompInfo.column.visible,
                start_date: newCompInfo.column.start_date,
                end_date: newCompInfo.column.end_date,
              });
            }
          }
        }
      }
    } else if (newColumnType.value.startsWith('video')) {
      currentCompInfo.columns.push({
        type: newColumnType.value,
        v_link: newCompInfo.column.v_link,
        title: newCompInfo.column.title,
        description: newCompInfo.column.description,
        visible: newCompInfo.column.visible,
        start_date: newCompInfo.column.start_date,
        end_date: newCompInfo.column.end_date,
      });
    } else if (newColumnType.value === 'shop') {
      currentCompInfo.columns.push({ type: newColumnType.value, id: newCompInfo.column.id, img: newCompInfo.column.img, name: newCompInfo.column.name, visible: newCompInfo.column.visible, start_date: newCompInfo.column.start_date, end_date: newCompInfo.column.end_date });
    } else {
      currentCompInfo.columns.push({ type: newColumnType.value, text: newCompInfo.column.text, visible: newCompInfo.column.visible, start_date: newCompInfo.column.start_date, end_date: newCompInfo.column.end_date });
    }
    newColumnType.value = 'product';
    newCompInfo.column = { type: '', view_type: '', img: '', thumbnail: '', full_link: '', v_link: '', link: '', title: '', description: '', id: '', name: '', text: '', event: '', visible: 'Y', start_date: '', end_date: '', link_type: '' };
    selLinkTheme2.value = 0;
    uploadImg2.value = '';
    showAddInfo.column = false;
    checkProductType.value = true;
  });
};

const addNewBanner = () => {
  bannerDateRef.value.editFinish('banner');
  if (!checkDate('banner')) {
    showAlert('노출기간을 확인해주세요.', 'warning');
    return;
  }
  if (newBannerType.value === 'text') {
    newCkeditorCustomB.value.saveClicked();
  }

  if (newBannerType.value === 'img' && !newCompInfo.banner.img && !newCompInfo.banner.img_m) {
    showAlert('설정할 이미지를 업로드해주세요.', 'warning');
    return;
  }

  // TODO: 데이터 체크
  showConfirm('배너를 추가하시겠습니까?', () => {
    if (selLinkTheme1.value > 0) newCompInfo.banner.link = `/theme/${selLinkTheme1.value}`;
    if (newBannerType.value === 'img') {
      const data = {} as BannerInfo;
      data.type = newBannerType.value;
      if (newCompInfo.banner.img) data.img = newCompInfo.banner.img;
      if (newCompInfo.banner.img_m) data.img_m = newCompInfo.banner.img_m;
      data.full_link = newCompInfo.banner.link_type === 'full' ? newCompInfo.banner.full_link : '';
      data.link = newCompInfo.banner.link_type === 'theme' ? newCompInfo.banner.link : '';
      data.visible = newCompInfo.banner.visible;
      data.start_date = newCompInfo.banner.start_date;
      data.end_date = newCompInfo.banner.end_date;
      data.link_type = newCompInfo.banner.link_type;
      currentCompInfo.banners.push(data);
    } else if (newBannerType.value.startsWith('video')) {
      currentCompInfo.banners.push({
        type: newBannerType.value,
        v_link: newCompInfo.banner.v_link,
        title: newCompInfo.banner.title,
        description: newCompInfo.banner.description,
        visible: newCompInfo.banner.visible,
        start_date: newCompInfo.banner.start_date,
        end_date: newCompInfo.banner.end_date,
      });
    } else {
      currentCompInfo.banners.push({ type: newBannerType.value, text: newCompInfo.banner.text, visible: newCompInfo.banner.visible, start_date: newCompInfo.banner.start_date, end_date: newCompInfo.banner.end_date });
    }

    newBannerType.value = 'img';
    newCompInfo.banner = { type: '', img: '', img_m: '', full_link: '', link: '', v_link: '', title: '', description: '', text: '', visible: 'Y', start_date: '', end_date: '', link_type: '' };
    selLinkTheme1.value = 0;
    uploadImg.value = '';
    uploadImg.fileData = undefined;
    uploadImgM.value = '';
    uploadImgM.fileData = undefined;
    showAddInfo.banner = false;
  });
};

const addNewSlide = () => {
  slideDateRef.value.editFinish('slide');
  if (!checkDate('slide')) {
    showAlert('노출기간을 확인해주세요.', 'warning');
    return;
  }
  // TODO: 데이터 체크
  if (!newCompInfo.slide.img && !newCompInfo.slide.img_m) {
    showAlert('설정할 이미지를 업로드해주세요.', 'warning');
    return;
  }
  showConfirm('슬라이드를 추가하시겠습니까?', () => {
    if (selLinkTheme1.value > 0) newCompInfo.slide.link = `/theme/${selLinkTheme1.value}`;
    const data = {} as SlideInfo;
    if (newCompInfo.slide.img) data.img = newCompInfo.slide.img;
    if (newCompInfo.slide.img_m) data.img_m = newCompInfo.slide.img_m;
    data.full_link = newCompInfo.slide.link_type === 'full' ? newCompInfo.slide.full_link : '';
    data.link = newCompInfo.slide.link_type === 'theme' ? newCompInfo.slide.link : '';
    data.visible = newCompInfo.slide.visible;
    data.start_date = newCompInfo.slide.start_date;
    data.end_date = newCompInfo.slide.end_date;
    data.link_type = newCompInfo.slide.link_type;
    currentCompInfo.slides.push(JSON.parse(JSON.stringify(data)));

    newCompInfo.slide = { img: '', img_m: '', full_link: '', link: '', visible: 'Y', start_date: '', end_date: '', link_type: '' };
    selLinkTheme1.value = 0;
    uploadImg.value = '';
    uploadImg.fileData = undefined;
    uploadImgM.value = '';
    uploadImgM.fileData = undefined;
    showAddInfo.banner = false;
    showAddInfo.slide = false;
  });
};

const addNewButton = () => {
  buttonDateRef.value.editFinish('button');
  if (!checkDate('button')) {
    showAlert('노출기간을 확인해주세요.', 'warning');
    return;
  }
  if (newButtonType.value === 'anchor') {
    // TODO: 앵커 데이터 체크
    const reg = /[^a-zA-Z0-9]/gi;
    if (newCompInfo.button.view_type === 'img') {
      if (!newCompInfo.button.view_src) {
        showAlert('앵커버튼 이미지를 선택해주세요.', 'warning');
        return;
      }
    } else {
      if (!newCompInfo.button.name) {
        showAlert('앵커버튼 이름을 입력해주세요.', 'warning');
        return;
      }
    }

    if (!newCompInfo.button.target) {
      showAlert('앵커 타겟 아이디를 입력해주세요.', 'warning');
      return;
    }

    if (reg.test(newCompInfo.button.target)) {
      showAlert('타겟 아이디는 영문자와 숫자만 입력가능합니다.', 'warning');
      return;
    }

    showConfirm('앵커 버튼을 추가하시겠습니까?', () => {
      if (newCompInfo.button.view_type === 'img') {
        currentCompInfo.buttons.push(
          JSON.parse(
            JSON.stringify({
              type: newButtonType.value,
              view_type: newCompInfo.button.view_type,
              view_src: newCompInfo.button.view_src,
              target: newCompInfo.button.target,
              visible: newCompInfo.button.visible,
              start_date: newCompInfo.button.start_date,
              end_date: newCompInfo.button.end_date,
            }),
          ),
        );
      } else {
        currentCompInfo.buttons.push(
          JSON.parse(JSON.stringify({ type: newButtonType.value, name: newCompInfo.button.name, target: newCompInfo.button.target, visible: newCompInfo.button.visible, start_date: newCompInfo.button.start_date, end_date: newCompInfo.button.end_date })),
        );
      }

      newCompInfo.button = { type: 'anchor', name: '', target: '', full_link: '', link: '', visible: 'Y', start_date: '', end_date: '', view_type: '', view_src: '', link_type: '' };
      showAddInfo.button = false;
    });
  } else {
    // TODO: 버튼 데이터 체크
    if (newCompInfo.button.view_type === 'img') {
      if (!newCompInfo.button.view_src) {
        showAlert('링크버튼 이미지를 선택해주세요.', 'warning');
        return;
      }
    } else {
      if (!newCompInfo.button.name) {
        showAlert('링크버튼 이름을 입력해주세요.', 'warning');
        return;
      }
    }

    showConfirm('링크 버튼을 추가하시겠습니까?', () => {
      if (selLinkTheme1.value > 0) newCompInfo.button.link = `/theme/${selLinkTheme1.value}`;
      const data = {} as ButtonInfo;
      data.type = newButtonType.value;
      if (newCompInfo.button.view_type === 'img') {
        data.view_type = newCompInfo.button.view_type;
        data.view_src = newCompInfo.button.view_src;
      } else {
        data.name = newCompInfo.button.name;
      }
      data.full_link = newCompInfo.button.link_type === 'full' ? newCompInfo.button.full_link : '';
      data.link = newCompInfo.button.link_type === 'theme' ? newCompInfo.button.link : '';
      data.visible = newCompInfo.button.visible;
      data.start_date = newCompInfo.button.start_date;
      data.end_date = newCompInfo.button.end_date;
      data.link_type = newCompInfo.button.link_type;
      currentCompInfo.buttons.push(JSON.parse(JSON.stringify(data)));
      newCompInfo.button = { type: 'link', name: '', target: '', full_link: '', link: '', visible: 'Y', start_date: '', end_date: '', view_type: '', view_src: '', link_type: '' };
      showAddInfo.button = false;
    });
  }
};

// const checkTargetId = (e: any) => {
//   const reg = /[^a-zA-Z0-9]/gi;
//   if (reg.test(e.target.value)) {
//     showAlert('영문자와 숫자만 입력할 수 있습니다.', 'warning', () => {
//       e.target.focus();
//     });
//   }
// };

const deleteInfo = (type: string, i: number = 0) => {
  if (isMod.value) {
    showAlert('수정 작업 중에는 삭제를 진행할 수 없습니다.\n수정작업 완료 후 진행해주세요.', 'warning');
    return;
  }
  showConfirm('삭제하시겠습니까?', () => {
    switch (type) {
      case 'button':
        currentCompInfo.buttons.splice(i, 1);
        break;
      case 'slide':
        currentCompInfo.slides.splice(i, 1);
        break;
      case 'banner':
        currentCompInfo.banners.splice(i, 1);
        break;
      case 'column':
        currentCompInfo.columns.splice(i, 1);
        break;
      case 'link':
        currentCompInfo.link = null;
    }
  });
};

const deleteBackgroundImg = () => {
  // eslint-disable-next-line vue/no-mutating-props
  props.compData.background = '';
  currentCompInfo.background = '';
  emit('deleteBackImg', props.compData);
};

const checkCompId = () => {
  if (!currentCompInfo.id) {
    showAlert('컴포넌트 아이디를 입력해주세요.', 'warning');
    return;
  }
  // eslint-disable-next-line vue/no-mutating-props
  props.compData.compId = currentCompInfo.id;
  showAddInfo.id = false;
};

const checkCompMemo = () => {
  // eslint-disable-next-line vue/no-mutating-props
  props.compData.memo = currentCompInfo.memo;
  showAddInfo.memo = false;
};

const checkBackImg = () => {
  if (!currentCompInfo.background) {
    showAlert('배경이미지를 선택해주세요.', 'warning');
    return;
  }
  // eslint-disable-next-line vue/no-mutating-props
  props.compData.background = currentCompInfo.background;
  showAddInfo.background = false;
};

const showProductList = () => {
  // showModal('getProductListModal')
  emit('openProdModal', isMod.value);
};

const showShopList = () => {
  showModal('getShopListModal');
};

/**
 * 컴포넌트 수정 작업
 * */
const selModIdx = ref(-1);
// 아이템 수정 Start
const modSelColumn = (c: ColumnInfo, idx: number) => {
  clearNewCompInfo();
  showAddInfo.id = showAddInfo.memo = showAddInfo.background = showAddInfo.button = showAddInfo.slide = showAddInfo.banner = showAddInfo.column = false;
  selModIdx.value = idx;
  isMod.value = true;
  showAddInfo.column = true;
  newColumnType.value = c.type;
  newCompInfo.column.visible = c.visible ? c.visible : 'Y';
  newCompInfo.column.start_date = c.start_date ? c.start_date : '';
  newCompInfo.column.end_date = c.end_date ? c.end_date : '';
  switch (c.type) {
    case 'normal':
      newCompInfo.column.link_type = c.link_type ? c.link_type : c.full_link ? 'full' : c.link ? 'theme' : '';
      newCompInfo.column.img = c.img ? c.img : '';
      newCompInfo.column.full_link = c.full_link ? c.full_link : '';
      if (c.link) {
        newCompInfo.column.link = c.link;
        selLinkTheme2.value = parseInt(c.link.replace('/theme/', ''));
      }
      newCompInfo.column.title = c.title ? c.title : '';
      newCompInfo.column.description = c.description ? c.description : '';
      newCompInfo.column.event = c.event ? c.event : 'link';
      break;
    case 'product':
      newCompInfo.column.name = c.name ? c.name : '';
      newCompInfo.column.id = c.id ? c.id : '';
      newCompInfo.column.img = c.img ? c.img : '';
      newCompInfo.column.thumbnail = c.thumbnail ? c.thumbnail : '';
      newCompInfo.column.view_type = c.view_type ? c.view_type : '';
      break;
    case 'video':
      newCompInfo.column.v_link = c.v_link ? c.v_link : '';
      newCompInfo.column.title = c.title ? c.title : '';
      newCompInfo.column.description = c.description ? c.description : '';
      break;
    case 'shop':
      newCompInfo.column.id = c.id ? c.id : '';
      newCompInfo.column.name = c.name ? c.name : '';
      newCompInfo.column.img = c.img ? c.img : '';
      break;
    case 'text':
      editorData.value = c.text ? c.text : '';
      break;
  }
};

const modColumnData = () => {
  columnDateRef.value.editFinish('column');
  if (!checkDate('column')) {
    showAlert('노출기간을 확인해주세요.', 'warning');
    return;
  }
  if (selModIdx.value < 0) {
    return;
  }
  if (newColumnType.value === 'text') {
    newCkeditorCustomC.value.saveClicked();
  }

  showConfirm('수정하시겠습니까?', () => {
    const target = props.compData.data.columns[selModIdx.value];
    target.type = newColumnType.value;
    target.visible = newCompInfo.column.visible;
    target.start_date = newCompInfo.column.start_date;
    target.end_date = newCompInfo.column.end_date;

    switch (newColumnType.value) {
      case 'normal':
        target.img = newCompInfo.column.img;
        target.full_link = newCompInfo.column.link_type === 'full' ? newCompInfo.column.full_link : '';
        if (selLinkTheme2.value > 0) newCompInfo.column.link = `/theme/${selLinkTheme2.value}`;
        target.link = newCompInfo.column.link_type === 'theme' ? newCompInfo.column.link : '';
        target.title = newCompInfo.column.title;
        target.description = newCompInfo.column.description;
        target.event = newCompInfo.column.event;
        target.link_type = newCompInfo.column.link_type;
        break;
      case 'product':
        target.id = newCompInfo.column.id;
        target.name = newCompInfo.column.name;
        target.img = newCompInfo.column.img;
        if (newCompInfo.column.thumbnail) {
          target.thumbnail = newCompInfo.column.thumbnail;
        }
        if (newCompInfo.column.view_type) {
          target.view_type = newCompInfo.column.view_type;
        } else {
          delete target.view_type;
        }
        break;
      case 'video':
        target.v_link = newCompInfo.column.v_link;
        target.title = newCompInfo.column.title;
        target.description = newCompInfo.column.description;
        break;
      case 'shop':
        target.id = newCompInfo.column.id;
        target.name = newCompInfo.column.name;
        target.img = newCompInfo.column.img;
        break;
      case 'text':
        target.text = newCompInfo.column.text;
        break;
    }

    clearNewCompInfo();

    selModIdx.value = -1;
    isMod.value = false;
    showAddInfo.column = false;
  });
};
// 아이템 수정 End

// 배너 수정 Start
const modSelBanner = (b: BannerInfo, idx: number) => {
  clearNewCompInfo();
  showAddInfo.id = showAddInfo.memo = showAddInfo.background = showAddInfo.button = showAddInfo.slide = showAddInfo.banner = showAddInfo.column = false;
  selModIdx.value = idx;
  isMod.value = true;
  showAddInfo.banner = true;

  newBannerType.value = b.type;
  newCompInfo.banner.visible = b.visible ? b.visible : 'Y';
  newCompInfo.banner.start_date = b.start_date ? b.start_date : '';
  newCompInfo.banner.end_date = b.end_date ? b.end_date : '';

  switch (b.type) {
    case 'img':
      newCompInfo.banner.link_type = b.link_type ? b.link_type : b.full_link ? 'full' : b.link ? 'theme' : '';
      newCompInfo.banner.img = b.img ? b.img : '';
      newCompInfo.banner.img_m = b.img_m ? b.img_m : '';
      newCompInfo.banner.full_link = b.full_link ? b.full_link : '';
      if (b.link) {
        newCompInfo.banner.link = b.link;
        selLinkTheme1.value = parseInt(b.link.replace('/theme/', ''));
      }
      break;
    case 'video':
      newCompInfo.banner.v_link = b.v_link ? b.v_link : '';
      newCompInfo.banner.title = b.title ? b.title : '';
      newCompInfo.banner.description = b.description ? b.description : '';
      break;
    case 'text':
      editorData.value = b.text ? b.text : '';
      break;
  }
};

const modBannerData = () => {
  bannerDateRef.value.editFinish('banner');
  if (!checkDate('banner')) {
    showAlert('노출기간을 확인해주세요.', 'warning');
    return;
  }
  if (selModIdx.value < 0) {
    return;
  }
  if (newBannerType.value === 'text') {
    newCkeditorCustomB.value.saveClicked();
  }

  showConfirm('수정하시겠습니까?', () => {
    const target = props.compData.data.banners[selModIdx.value];
    target.type = newBannerType.value;
    target.visible = newCompInfo.banner.visible;
    target.start_date = newCompInfo.banner.start_date;
    target.end_date = newCompInfo.banner.end_date;

    switch (newBannerType.value) {
      case 'img':
        if (newCompInfo.banner.img) target.img = newCompInfo.banner.img;
        if (newCompInfo.banner.img_m) target.img_m = newCompInfo.banner.img_m;
        target.full_link = newCompInfo.banner.link_type === 'full' ? newCompInfo.banner.full_link : '';
        if (selLinkTheme1.value > 0) newCompInfo.banner.link = `/theme/${selLinkTheme1.value}`;
        target.link = newCompInfo.banner.link_type === 'theme' ? newCompInfo.banner.link : '';
        target.link_type = newCompInfo.banner.link_type;
        break;
      case 'video':
        target.v_link = newCompInfo.banner.v_link;
        target.title = newCompInfo.banner.title;
        target.description = newCompInfo.banner.description;
        break;
      case 'text':
        target.text = newCompInfo.banner.text;
        break;
    }

    clearNewCompInfo();

    selModIdx.value = -1;
    isMod.value = false;
    showAddInfo.banner = false;
  });
};
// 배너 수정 End

// 슬라이드 수정 Start
const modSelSlide = (s: SlideInfo, idx: number) => {
  clearNewCompInfo();
  showAddInfo.id = showAddInfo.memo = showAddInfo.background = showAddInfo.button = showAddInfo.slide = showAddInfo.banner = showAddInfo.column = false;
  selModIdx.value = idx;
  isMod.value = true;
  showAddInfo.slide = true;

  newCompInfo.slide.link_type = s.link_type ? s.link_type : s.full_link ? 'full' : s.link ? 'theme' : '';
  newCompInfo.slide.img = s.img ? s.img : '';
  newCompInfo.slide.img_m = s.img_m ? s.img_m : '';
  newCompInfo.slide.full_link = s.full_link ? s.full_link : '';
  newCompInfo.slide.visible = s.visible ? s.visible : 'Y';
  newCompInfo.slide.start_date = s.start_date ? s.start_date : '';
  newCompInfo.slide.end_date = s.end_date ? s.end_date : '';

  if (s.link) {
    newCompInfo.slide.link = s.link;
    selLinkTheme1.value = parseInt(s.link.replace('/theme/', ''));
  }
};

const modSlideData = () => {
  slideDateRef.value.editFinish('slide');
  if (!checkDate('slide')) {
    showAlert('노출기간을 확인해주세요.', 'warning');
    return;
  }
  if (selModIdx.value < 0) {
    return;
  }
  showConfirm('수정하시겠습니까?', () => {
    const target = props.compData.data.slides[selModIdx.value];
    if (newCompInfo.slide.img) target.img = newCompInfo.slide.img;
    if (newCompInfo.slide.img_m) target.img_m = newCompInfo.slide.img_m;
    target.full_link = newCompInfo.slide.link_type === 'full' ? newCompInfo.slide.full_link : '';
    if (selLinkTheme1.value > 0) newCompInfo.slide.link = `/theme/${selLinkTheme1.value}`;
    target.link = newCompInfo.slide.link_type === 'theme' ? newCompInfo.slide.link : '';
    target.link_type = newCompInfo.slide.link_type;

    target.visible = newCompInfo.slide.visible;
    target.start_date = newCompInfo.slide.start_date;
    target.end_date = newCompInfo.slide.end_date;

    clearNewCompInfo();

    selModIdx.value = -1;
    isMod.value = false;
    showAddInfo.slide = false;
  });
};
// 슬라이드 수정 End

// 버튼그룹 수정 Start
const modSelButton = (b: ButtonInfo, idx: number) => {
  showAddInfo.id = showAddInfo.memo = showAddInfo.background = showAddInfo.button = showAddInfo.slide = showAddInfo.banner = showAddInfo.column = false;
  clearNewCompInfo();
  newCompInfo.button = { type: '', name: '', target: '', full_link: '', link: '', visible: 'Y', start_date: '', end_date: '', view_type: '', view_src: '', link_type: '' };

  selModIdx.value = idx;
  isMod.value = true;
  showAddInfo.button = true;

  newButtonType.value = b.type;

  newCompInfo.button.view_type = b.view_type ? b.view_type : '';
  newCompInfo.button.visible = b.visible ? b.visible : 'Y';
  newCompInfo.button.start_date = b.start_date ? b.start_date : '';
  newCompInfo.button.end_date = b.end_date ? b.end_date : '';

  switch (b.type) {
    case 'anchor':
      newCompInfo.button.view_src = b.view_src ? b.view_src : '';
      newCompInfo.button.name = b.name ? b.name : '';
      newCompInfo.button.target = b.target ? b.target : '';
      break;
    case 'link':
      newCompInfo.button.link_type = b.link_type ? b.link_type : b.full_link ? 'full' : b.link ? 'theme' : '';
      newCompInfo.button.view_src = b.view_src ? b.view_src : '';
      newCompInfo.button.name = b.name ? b.name : '';
      newCompInfo.button.full_link = b.full_link ? b.full_link : '';
      if (b.link) {
        newCompInfo.banner.link = b.link;
        selLinkTheme1.value = parseInt(b.link.replace('/theme/', ''));
      }
      break;
  }
};

const modButtonData = () => {
  buttonDateRef.value.editFinish('button');
  if (!checkDate('button')) {
    showAlert('노출기간을 확인해주세요.', 'warning');
    return;
  }

  if (selModIdx.value < 0) {
    return;
  }

  if (newButtonType.value === 'anchor') {
    // TODO: 앵커 데이터 체크
    const reg = /[^a-zA-Z0-9]/gi;
    if (newCompInfo.button.view_type === 'img') {
      if (!newCompInfo.button.view_src) {
        showAlert('앵커버튼 이미지를 선택해주세요.', 'warning');
        return;
      }
    } else {
      if (!newCompInfo.button.name) {
        showAlert('앵커버튼 이름을 입력해주세요.', 'warning');
        return;
      }
    }
    if (!newCompInfo.button.target) {
      showAlert('앵커 타겟 아이디를 입력해주세요.', 'warning');
      return;
    }

    if (reg.test(newCompInfo.button.target)) {
      showAlert('타겟 아이디는 영문자와 숫자만 입력가능합니다.', 'warning');
      return;
    }
    showConfirm('수정하시겠습니까?', () => {
      const target = props.compData.data.buttons[selModIdx.value];
      target.type = newButtonType.value;
      if (newCompInfo.button.view_type === 'img') {
        target.view_type = newCompInfo.button.view_type;
        target.view_src = newCompInfo.button.view_src;
        target.name = '';
      } else {
        target.name = newCompInfo.button.name;
        target.view_src = '';
        target.view_type = '';
      }
      target.target = newCompInfo.button.target;
      target.visible = newCompInfo.button.visible;
      target.start_date = newCompInfo.button.start_date;
      target.end_date = newCompInfo.button.end_date;

      newCompInfo.button = { type: 'anchor', name: '', target: '', full_link: '', link: '', visible: 'Y', start_date: '', end_date: '', view_type: '', view_src: '', link_type: '' };

      selModIdx.value = -1;
      isMod.value = false;
      showAddInfo.button = false;
    });
  } else {
    if (newCompInfo.button.view_type === 'img') {
      if (!newCompInfo.button.view_src) {
        showAlert('링크버튼 이미지를 선택해주세요.', 'warning');
        return;
      }
    } else {
      if (!newCompInfo.button.name) {
        showAlert('링크버튼 이름을 입력해주세요.', 'warning');
        return;
      }
    }
    showConfirm('수정하시겠습니까?', () => {
      const target = props.compData.data.buttons[selModIdx.value];
      target.type = newButtonType.value;
      if (selLinkTheme1.value > 0) newCompInfo.button.link = `/theme/${selLinkTheme1.value}`;
      if (newCompInfo.button.view_type === 'img') {
        target.view_type = newCompInfo.button.view_type;
        target.view_src = newCompInfo.button.view_src;
        target.name = '';
      } else {
        target.name = newCompInfo.button.name;
        target.view_src = '';
        target.view_type = '';
      }
      target.full_link = newCompInfo.button.link_type === 'full' ? newCompInfo.button.full_link : '';
      target.link = newCompInfo.button.link_type === 'theme' ? newCompInfo.button.link : '';
      target.visible = newCompInfo.button.visible;
      target.start_date = newCompInfo.button.start_date;
      target.end_date = newCompInfo.button.end_date;
      target.link_type = newCompInfo.button.link_type;

      newCompInfo.button = { type: 'anchor', name: '', target: '', full_link: '', link: '', visible: 'Y', start_date: '', end_date: '', view_type: '', view_src: '', link_type: '' };

      selModIdx.value = -1;
      isMod.value = false;
      showAddInfo.button = false;
    });
  }
};
// 버튼 그룹 수정 End

// 아이템 텍스트 링크 수정 Start
const modColumnLink = () => {
  newCompInfo.link = { title: '', full_link: '', link: '', link_type: '' };
  selLinkTheme3.value = 0;

  showAddInfo.id = showAddInfo.memo = showAddInfo.background = showAddInfo.button = showAddInfo.slide = showAddInfo.banner = showAddInfo.column = false;

  isMod.value = true;
  showAddInfo.link = true;

  newCompInfo.link.title = currentCompInfo.link.title;
  newCompInfo.link.link_type = currentCompInfo.link.link_type ? currentCompInfo.link.link_type : currentCompInfo.link.full_link ? 'full' : 'theme';
  newCompInfo.link.full_link = currentCompInfo.link.link_type === 'full' ? currentCompInfo.link.full_link : '';
  if (currentCompInfo.link.link) {
    newCompInfo.link.link = currentCompInfo.link.link;
    selLinkTheme3.value = parseInt(currentCompInfo.link.link.replace('/theme/', ''));
  }
};
// 아이템 텍스트 링크 수정 End

const deleteColumnLink = () => {
  if (isMod.value) {
    showAlert('수정 작업 중에는 삭제를 진행할 수 없습니다.\n수정작업 완료 후 진행해주세요.', 'warning');
    return;
  }
  showConfirm('텍스트 링크 정보를 삭제하시겠습니까?', () => {
    // eslint-disable-next-line vue/no-mutating-props
    delete props.compData.data.link;
    currentCompInfo.link = null;
    newCompInfo.link = { title: '', full_link: '', link: '' };
    selLinkTheme3.value = 0;
  });
};

const returnDate = (sDate: string, eDate: string, type: string) => {
  switch (type) {
    case 'button':
      newCompInfo.button.start_date = sDate;
      newCompInfo.button.end_date = eDate;
      break;
    case 'slide':
      newCompInfo.slide.start_date = sDate;
      newCompInfo.slide.end_date = eDate;
      break;
    case 'banner':
      newCompInfo.banner.start_date = sDate;
      newCompInfo.banner.end_date = eDate;
      break;
    case 'column':
      newCompInfo.column.start_date = sDate;
      newCompInfo.column.end_date = eDate;
      break;
  }
};

const checkDate = (type: string): boolean => {
  let result = true;

  switch (type) {
    case 'button':
      if (newCompInfo.button.start_date && newCompInfo.button.end_date && newCompInfo.button.start_date > newCompInfo.button.end_date) {
        result = false;
      }
      break;
    case 'slide':
      if (newCompInfo.slide.start_date && newCompInfo.slide.end_date && newCompInfo.slide.start_date > newCompInfo.slide.end_date) {
        result = false;
      }
      break;
    case 'banner':
      if (newCompInfo.banner.start_date && newCompInfo.banner.end_date && newCompInfo.banner.start_date > newCompInfo.banner.end_date) {
        result = false;
      }
      break;
    case 'column':
      if (newCompInfo.column.start_date && newCompInfo.column.end_date && newCompInfo.column.start_date > newCompInfo.column.end_date) {
        result = false;
      }
      break;
  }

  return result;
};

onMounted(() => {
  //@ts-ignore
  document.getElementById('setComponentData').addEventListener('show.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('setComponentData').addEventListener('hide.bs.modal', function (event) {
    clearCurrentCompInfo();
  });
});
onUnmounted(() => {});
</script>

<style scoped>
input.input-video::placeholder {
  font-size: 0.7rem;
}

.chkb-ex:checked {
  background-color: #dc3545 !important;
  border-color: #dc3545 !important;
}
</style>
