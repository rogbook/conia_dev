<template>
  <PageNavigator :before_link="['공지사항']" :current="'공지사항 상세'" />
  <div class="card col-md-8">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center" v-if="noticeId">
        <div class="col-auto">
          <div class="form-control-borderless h2">공지사항</div>
          <div class="form-control-borderless h4">제목 : [{{ noticeInfo.title }}]</div>
        </div>
      </div>
      <div class="row justify-content-between align-items-center" v-else>
        <div class="col-auto">
          <div class="form-control-borderless h2">공지사항 신규등록</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <CKEditorCustom @receiveData="newReceiveData" ref="newCkeditorCustom" :removeItems="removeItems" :editor-data="editorData" :disabled="true" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import { apiResponseCheck, showAlert, showConfirm } from '@/utils/common-utils';
import CKEditorCustom from '@/pages/settings/product/common/list/detail/CKEditorCustom.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';

const router = useRouter();

const noticeId = ref();
const noticeInfo = reactive({
  title: '',
  contents: '',
  target: '',
  pin: 'N',
  sort: 99,
  reg_date: '',
  mod_date: '',
  store_code: '',
});
const newCkeditorCustom = ref();
const removeItems = ref(['heading', '|', 'bold', 'italic', 'fontSize', 'fontColor', 'fontFamily', 'fontBackgroundColor', '|', 'bulletedList', 'numberedList', '|', 'imageUpload', 'mediaEmbed', 'insertTable', 'link', '|', 'undo', 'redo']);
const editorData = ref('');

const newReceiveData = (data: string) => {
  noticeInfo.contents = data;
};

const getNoticeInfo = () => {
  apis.community.get_notice(noticeId.value).then(res => {
    apiResponseCheck(res, () => {
      noticeInfo.title = res.title;
      noticeInfo.contents = res.contents;
      editorData.value = res.contents;
      noticeInfo.pin = res.pin;
      noticeInfo.sort = res.sort;
      noticeInfo.reg_date = res.reg_date;
      noticeInfo.mod_date = res.mod_date;
      if (res.store_code) {
        noticeInfo.store_code = res.store_code;
      }
    });
  });
};

onMounted(() => {
  const id = history.state.id;
  if (id) {
    noticeId.value = id;
    getNoticeInfo();
  }
});
</script>

<style scoped></style>
