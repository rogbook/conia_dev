<template>
  <div class="card">
    <div class="card-header py-2">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">[{{ props.store_title }}] 상점 이용가능자 목록</div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-primary me-2" @click.prevent="showOnRegModal">개별등록</button>
          <UploadExcel class="form-control" @upload="uploadExcel" :btn="{ btnName: '엑셀 일괄 업로드', btnClass: 'btn btn-sm btn-info' }" disabled />
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card">
        <div class="card-body">
          <!-- 세부검색어 입력 -->
          <div class="row col">
            <label class="col-md-2 col-form-label text-nowrap">이용가능자 검색</label>
            <div class="col-lg-2 mb-1">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
                </select>
              </div>
              <!-- End Select -->
            </div>
            <div class="col-lg-4">
              <div class="input-group">
                <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getAbleTargetList()" />
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer py-2">
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-secondary me-2" @click.prevent="refreshList">초기화</button>
            <button type="button" class="btn btn-sm btn-primary" @click.prevent="getAbleTargetList(true)">검색</button>
          </div>
        </div>
      </div>
      <span class="divider-center py-4">검색결과</span>
      <div class="row mb-2 align-items-center justify-content-between">
        <div class="col-auto">
          <span v-if="mAbleTargetList.total > 0">총 : {{ mAbleTargetList.total }}개</span>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table table-sm table-borderless table-thead-bordered table-align-middle card-table">
          <thead class="thead-light">
            <tr class="text-center">
              <th>이름</th>
              <th>전화번호</th>
              <th>회원식별값(예시: 사번 등)</th>
              <th>사용여부</th>
              <th>수정</th>
              <th>삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(t, i) in mAbleTargetList.datas" :key="t.id">
              <td>
                {{ t.name }}
              </td>
              <td>{{ t.mobile }}</td>
              <td>{{ t.unique_value }}</td>
              <td>{{ t.used === 'Y' ? '사용' : '미사용' }}</td>
              <td>
                <button type="button" class="btn btn-sm btn-warning" @click.prevent="modAbleTarget(t)">수정</button>
              </td>
              <td>
                <button type="button" class="btn btn-sm btn-danger" @click.prevent="deleteAbleTarget(t.id)">삭제</button>
              </td>
            </tr>
            <tr class="text-center" v-if="mAbleTargetList.total === 0">
              <td colspan="6">검색 결과가 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="table-footer-area" v-if="mAbleTargetList.total > 0">
        <div class="row" v-if="total_page > 1">
          <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import apis from '@/apis';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import type { AbleTargetList, AbleTarget } from 'StoreAbleTargetModule';
import Pagination from '@/components/comm/Pagination.vue';
import UploadExcel from '@/components/comm/UploadExcel.vue';

const props = defineProps<{ store_code: string; store_title: string }>();
const emits = defineEmits(['openOneRegPopup', 'openModTargetPopup']);

const mStoreCode = ref('');
const mAbleTargetList = ref({} as AbleTargetList);

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mAbleTargetList.value.total / limit.value));

const selDetailSearch = reactive({
  items: [
    { name: '이름', value: 'name' },
    { name: '회원식별값', value: 'unique_value' },
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
    case 'unique_value':
      selDetailSearch.placeholder = '검색할 식별값(예: 사번 등) 입력해주세요.';
      break;
  }
};

const getAbleTargetList = (clear: boolean = false) => {
  if (clear) {
    page_no.value = 1;
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

  apis.store.get_able_target_list(props.store_code, query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mAbleTargetList.value = res;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getAbleTargetList();
};

const deleteAbleTarget = (id: number) => {
  showConfirm('해당 이용자를 상점 이용가능자 목록에서 삭제하시겠습니까?', () => {
    apis.store.delete_able_target(props.store_code, id).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상점 이용가능자 목록에서 삭제되었습니다.');
        refreshList();
      });
    });
  });
};

const modAbleTarget = (target: AbleTarget) => {
  emits('openModTargetPopup', target);
};

const uploadExcel = (file: File) => {
  showConfirm('엑셀 파일을 업로드 하시겠습니까?', () => {
    apis.store.add_able_target(props.store_code, file).then(res => {
      apiResponseCheck(res, () => {
        showAlert('엑셀 파일이 성공적으로 업로드 되었습니다.');
        refreshList();
      });
    });
  });
};

const refreshList = () => {
  selDetailSearch.q = '';
  getAbleTargetList();
};

const showOnRegModal = () => {
  //@ts-ignore
  emits('openOneRegPopup');
};

defineExpose({ refreshList });

onMounted(() => {
  const code = history.state.code as string;
  if (code) {
    mStoreCode.value = code;
  }

  //@ts-ignore
  document.getElementById('ableTargetListModal').addEventListener('show.bs.modal', () => {
    getAbleTargetList(true);
  });
  //@ts-ignore
  document.getElementById('ableTargetListModal').addEventListener('hide.bs.modal', () => {});
});
</script>

<style scoped></style>
