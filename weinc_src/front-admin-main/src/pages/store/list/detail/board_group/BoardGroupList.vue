<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세'] : ['상점 관리', '상점관리 상세']" :current="'상점 게시판 관리'" />
  <div class="card">
    <div class="card-header">
      <div class="row justify-content-between align-items-center">
        <div class="form-control-borderless h2 col-auto mb-0">상점 게시판 관리</div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-info" @click.prevent="showModal('addBoardGroupModal')">상점 게시판 생성</button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <table class="table table-align-middle border card-table table-vertical-border-striped table-bordered">
        <thead class="thead-light">
          <tr class="text-center">
            <th>제목</th>
            <th style="width: 10%">노출타입</th>
            <th style="width: 10%">메뉴 노출여부</th>
            <th style="width: 10%">순서</th>
            <th style="width: 5%">수정</th>
            <th style="width: 5%">삭제</th>
            <th style="width: 5%">관리</th>
          </tr>
        </thead>
        <tbody>
          <tr class="text-center" v-for="(item, i) in mStoreBoardGroupList.datas" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.view_type === 'thumbnail' ? '썸네일' : '배너' }}</td>
            <td>{{ item.menu_visible === 'Y' ? '노출' : '비노출' }}</td>
            <td>{{ item.sort }}</td>
            <td>
              <button type="button" class="btn btn-sm btn-success" @click.prevent="modBoardGroup(i)">수정</button>
            </td>
            <td>
              <button type="button" class="btn btn-sm btn-danger" @click.prevent="deleteBoardGroup(i)">삭제</button>
            </td>
            <td>
              <router-link :to="{ path: `/store/detail/board`, state: { code: storeCode, groupId: item.id, groupName: item.name } }"> <button type="button" class="btn btn-sm btn-primary">관리</button></router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <Modal :id="'addBoardGroupModal'" :title="'상점 게시판 등록/수정'">
    <template #body>
      <BoardGroupDetail :storeCode="storeCode" :selectedBoardGroup="selectBoardGroup" @closeBoardGroupModal="closeBoardGroupModal" />
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import { useRoute, useRouter } from 'vue-router';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import type { BoardGroup, BoardGroupListInfo } from 'StoreBoardGroupInfoModule';
import Modal from '@/components/comm/modal.vue';
import BoardGroupDetail from '@/pages/store/list/detail/board_group/modal/BoardGroupDetail.vue';

const router = useRouter();
const storeCode = ref();
const selectBoardGroup = ref({} as BoardGroup | null);
const mStoreBoardGroupList = ref({} as BoardGroupListInfo);

onMounted(() => {
  selectBoardGroup.value = null;
  const code = history.state.code;
  if (code) {
    storeCode.value = code;
    getStoreBoardGroupList();
  } else {
    showAlert('비정상적인 접근입니다.');
    useRouter().back();
  }

  //@ts-ignore
  document.getElementById('addBoardGroupModal').addEventListener('hide.bs.modal', function (event) {
    selectBoardGroup.value = null;
  });
});

const getStoreBoardGroupList = () => {
  apis.store.get_store_board_group_list(storeCode.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mStoreBoardGroupList.value.total = res.total;
      mStoreBoardGroupList.value.datas = res.datas;
    });
  });
};

const modBoardGroup = (idx: number) => {
  selectBoardGroup.value = mStoreBoardGroupList.value.datas[idx];
  setTimeout(() => {
    showModal('addBoardGroupModal');
  }, 100);
};

const deleteBoardGroup = (idx: number) => {
  const board = mStoreBoardGroupList.value.datas[idx];
  showConfirm(`[${board.name}] 게시판을 삭제하시겠습니까?`, () => {
    apis.store.delete_store_board_group(storeCode.value, board.id).then(res => {
      apiResponseCheck(res, () => {
        showAlert('게시판이 삭제되었습니다.', 'success', () => {
          getStoreBoardGroupList();
        });
      });
    });
  });
};
const closeBoardGroupModal = () => {
  hideModal('addBoardGroupModal');
  getStoreBoardGroupList();
};
</script>

<style scoped></style>
