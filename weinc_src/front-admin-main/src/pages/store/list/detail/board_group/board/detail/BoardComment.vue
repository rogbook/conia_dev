<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세', '이벤트 관리', '이벤트 상세'] : ['상점 관리', '상점관리 상세', '이벤트 관리', '이벤트 상세']" :current="'이벤트 댓글'" />
  <div class="card col-md-8">
    <div class="card-header">
      <div class="row justify-content-between align-items-center">
        <div class="col-auto">
          <div class="form-control-borderless h2">이벤트 댓글</div>
          <div class="form-control-borderless h4">[{{ boardTitle }}]</div>
        </div>
        <div class="col-auto">
          <div class="text-end">
            <button type="button" class="btn btn-primary form-control-borderless h4" @click="downloadExcel">고객 댓글 엑셀 다운로드</button>
          </div>
        </div>
      </div>
    </div>

    <div class="card-body">
      <label for="comment" class="form-label fw-bold">댓글작성</label>
      <div class="d-flex">
        <textarea class="form-control rounded-start" rows="3" v-model="boardComment.comment" placeholder="댓글을 작성해 주세요." maxlength="300"></textarea>
        <button type="button" class="btn btn-dark px-3 ms-1" style="writing-mode: horizontal-tb; white-space: nowrap" @click.prevent="regBoardComment()">등록</button>
      </div>
      <div class="mt-3 border-top" v-if="comments.total">
        <div v-for="comment in comments.datas" :key="comment.id">
          <div class="p-3 border-bottom">
            <div class="d-flex justify-content-between">
              <div>
                <span class="fw-bold me-2">{{ comment.customer_id ? comment.customer.name : '관리자' }}</span>
                <small class="text-muted">{{ dateTimeFormatConverter(comment.mod_date) }}</small>
              </div>
              <div>
                <a v-if="!comment.customer_id" class="text-muted fs-sm me-3" @click.prevent="openModCommentModal(comment.id, comment.p_id, comment.comment)" style="cursor: pointer">수정</a>
                <a class="text-danger fs-sm" @click.prevent="deleteBoardComment(comment.id)" style="cursor: pointer">삭제</a>
              </div>
            </div>
            <div class="mt-2 px-1">{{ comment.comment }}</div>
            <div class="mt-3">
              <a class="text-muted" style="cursor: pointer" @click.prevent="showReplyArea(comment.id)">답글작성</a>
            </div>
          </div>

          <div class="d-flex bg-light ps-5 pe-3 py-3 border-bottom" v-if="isShowReplyArea && comment.id === commentId">
            <div class="me-1">└</div>
            <textarea class="form-control rounded-start" rows="3" v-model="boardReply.comment" placeholder="답글을 작성해 주세요." maxlength="300"></textarea>
            <button type="button" class="btn btn-dark px-3 ms-1" style="writing-mode: horizontal-tb; white-space: nowrap" @click.prevent="regBoardReply(comment.id)">등록</button>
          </div>

          <div v-if="replies.datas.length">
            <div v-for="reply in replies.datas">
              <div class="ps-5 pe-3 py-5 border-bottom bg-light" v-if="comment.id === reply.p_id">
                <div class="d-flex justify-content-between">
                  <div>
                    <span class="fw-bold me-2">관리자</span>
                    <small class="text-muted">{{ dateTimeFormatConverter(reply.mod_date) }}</small>
                  </div>
                  <div>
                    <a v-if="!reply.customer_id" class="text-muted fs-sm me-3" @click.prevent="openModCommentModal(reply.id, reply.p_id, reply.comment)" style="cursor: pointer">수정</a>
                    <a class="text-danger fs-sm" @click.prevent="deleteBoardComment(reply.id)" style="cursor: pointer">삭제</a>
                  </div>
                </div>
                <div class="d-flex gap-1 mt-2">
                  <div class="me-1">└</div>
                  <div style="white-space: pre-line; overflow-y: auto">{{ reply.comment }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="text-center py-7" v-else>표시할 항목이 없습니다.</div>
    </div>
  </div>

  <Modal :id="'openModCommentModal'" :title="`${commentInfo.commentType} 수정`">
    <template #body>
      <ModBoardComment :storeCode="storeCode" :commentInfo="commentInfo" @closeModCommentModal="closeModCommentModal" />
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import Pagination from '@/components/comm/Pagination.vue';
import { useRoute, useRouter } from 'vue-router';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import type { BoardComment, BoardCommentListInfo } from 'StoreBoardCommentInfoModule';
import { useUserStore } from '@/stores/user';
import Modal from '@/components/comm/modal.vue';
import ModBoardComment from '@/pages/store/list/detail/board_group/board/modal/ModBoardComment.vue';

const router = useRouter();
const a_member_id = ref(useUserStore().user.id as number);
const storeCode = ref();
const boardId = ref();
const boardTitle = ref('');
const comments = ref({} as BoardCommentListInfo);
const replies = ref({} as BoardCommentListInfo);
const isShowReplyArea = ref(false);
const commentId = ref();

const commentInfo = reactive({
  commentId: 0,
  commentType: '',
  commentString: '',
});

const boardComment = reactive({
  comment: '',
  store_board_id: 0,
  member_id: 0,
});
const boardReply = reactive({
  comment: '',
  store_board_id: 0,
  member_id: 0,
  p_id: 0,
});

onMounted(() => {
  const code = history.state.code;
  if (code) {
    storeCode.value = code;
    boardId.value = history.state.boardId;
    boardTitle.value = history.state.boardTitle;
    getStoreBoardCommentList();
  } else {
    showAlert('비정상적인 접근입니다.');
    useRouter().back();
  }
});

const openModCommentModal = (comment_id: number, p_id: number, comment: string) => {
  // if (p_id) {
  //   commentInfo.commentType = '답글';
  // } else {
  //   commentInfo.commentType = '댓글';
  // }
  commentInfo.commentType = p_id ? '답글' : '댓글';
  commentInfo.commentId = comment_id;
  commentInfo.commentString = comment;
  showModal('openModCommentModal');
};

const showReplyArea = (idx: number) => {
  if (isShowReplyArea.value === false) {
    isShowReplyArea.value = true;
  } else {
    if (commentId.value === idx) {
      isShowReplyArea.value = false;
    } else {
      isShowReplyArea.value = true;
    }
  }
  // isShowReplyArea.value = !isShowReplyArea.value;
  boardReply.comment = '';
  commentId.value = idx;
};

const getStoreBoardCommentList = () => {
  let query = '';

  if (query) {
    query = query.concat('&');
  }

  apis.store.get_store_board_comment(storeCode.value, boardId.value, query).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      comments.value.total = res.total;
      comments.value.datas = [];
      replies.value.datas = [];

      for (let value of res.datas) {
        if (value.p_id) {
          replies.value.datas.push(value);
        } else {
          comments.value.datas.push(value);
        }
      }
    });
  });
};

const regBoardComment = () => {
  if (!boardComment.comment) {
    showAlert('댓글 내용을 입력해주세요', 'warning');
    return;
  }

  boardComment.store_board_id = boardId.value;
  boardComment.member_id = a_member_id.value;

  showConfirm('댓글을 등록하시겠습니까?', () => {
    apis.store.reg_store_board_comment(storeCode.value, boardComment).then(res => {
      apiResponseCheck(res, () => {
        if (res.msg === 'success') {
          showAlert('댓글이 등록되었습니다.', 'success');
          boardComment.comment = '';
          getStoreBoardCommentList();
        }
      });
    });
  });
};

const regBoardReply = (commentId: number) => {
  if (!boardReply.comment) {
    showAlert('답글 내용을 입력해주세요', 'warning');
    return;
  }

  boardReply.store_board_id = boardId.value;
  boardReply.member_id = a_member_id.value;
  boardReply.p_id = commentId;

  showConfirm('답글을 등록하시겠습니까?', () => {
    apis.store.reg_store_board_comment(storeCode.value, boardReply).then(res => {
      apiResponseCheck(res, () => {
        if (res.msg === 'success') {
          showAlert('답글이 등록되었습니다.', 'success');
          boardReply.comment = '';
          isShowReplyArea.value = false;
          getStoreBoardCommentList();
        }
      });
    });
  });
};

const deleteBoardComment = (boardId: number) => {
  showConfirm(`해당 댓글을 삭제하시겠습니까?`, () => {
    apis.store.delete_store_board_comment(storeCode.value, boardId).then(res => {
      apiResponseCheck(res, () => {
        showAlert('댓글이 삭제되었습니다.', 'success', () => {
          getStoreBoardCommentList();
        });
      });
    });
  });
};

const downloadExcel = () => {
  showConfirm(`엑셀을 다운로드 하시겠습니까?`, () => {
    apis.store.get_store_board_comment_excel(storeCode.value, boardId.value).then(res => {
      apiResponseCheck(res, async () => {
        const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${boardTitle.value} 댓글 목록.xlsx`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      });
    });
  });
};

const closeModCommentModal = () => {
  hideModal('openModCommentModal');
  getStoreBoardCommentList();
};
</script>
