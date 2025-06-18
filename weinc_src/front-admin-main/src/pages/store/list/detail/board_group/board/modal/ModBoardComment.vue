<template>
  <div class="row">
    <div class="card">
      <div class="card-header">
        <div class="text-start">{{ props.commentInfo.commentType }} 수정</div>
      </div>
      <div class="card-body row">
        <div class="col">
          <div class="row col mb-2 align-items-center">
            <label class="col-2 col-form-label">내용</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control col" placeholder="내용을 입력해주세요." v-model="comment" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-footer pb-2">
    <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    <button type="button" class="btn btn-warning" @click.prevent="modBoardComment">수정</button>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import apis from '@/apis';
import { apiResponseCheck, showAlert, showConfirm } from '@/utils/common-utils';
import type { BoardGroup } from 'StoreBoardGroupInfoModule';

const props = defineProps<{
  storeCode: string;
  commentInfo: {
    commentId: number;
    commentType: string;
    commentString: string;
  };
}>();
const emits = defineEmits(['closeModCommentModal']);
const comment = ref('');

onMounted(() => {
  //@ts-ignore
  document.getElementById('openModCommentModal').addEventListener('show.bs.modal', function (event) {
    comment.value = props.commentInfo.commentString;
  });
});

const modBoardComment = () => {
  if (!comment.value) {
    showAlert(`${props.commentInfo.commentType} 내용을 입력해주세요`, 'warning');
    return;
  }
  if (comment.value === props.commentInfo.commentString) {
    showAlert(`변경사항이 없습니다.`, 'warning');
    return;
  }

  const params: object = {
    comment: comment.value,
  };

  showConfirm(`해당 댓글을 수정하시겠습니까?`, () => {
    apis.store.mod_store_board_comment(props.storeCode, props.commentInfo.commentId, params).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('댓글이 수정되었습니다.', 'success', () => {
            emits('closeModCommentModal');
          });
        },
        (num?: number) => {
          if (num === 403) {
            emits('closeModCommentModal');
          }
        },
      );
    });
  });
};
</script>
