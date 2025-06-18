<template>
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">상품정보제공고시 정보</h4>
          <small>상품의 정보제공고시 정보를 작성합니다.</small>
        </div>
        <div class="nav-item ms-auto">
          <button type="button" class="btn btn-warning" @click.prevent="saveProdNoticeInfo">저장</button>
        </div>
      </div>
    </div>
    <!-- 상품정보제공고시 -->
    <div class="card-body">
      <div class="row align-items-center mb-3">
        <div class="col-auto">
          <label>상품 품목 선택</label>
        </div>
        <div class="col-auto">
          <div class="tom-select-custom col-auto">
            <select class="form-select" v-model="selectedNoticeId" @change="noticeChanged" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option value="-1" disabled>품목을 선택해주세요</option>
              <option v-for="(notice, i) in noticeTemplateTitleList" :key="JSON.stringify(notice)" v-text="notice" :value="i"></option>
            </select>
          </div>
        </div>
        <div class="d-lg-none mt-1"></div>
        <div class="col-auto">
          <div class="nav-item ms-auto">
            <button type="button" class="btn btn-outline-info" @click.prevent="allInfoDefaultSetting">전체항목 '상세설명참조'로 표기</button>
          </div>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table table-nowrap table-align-middle border card-table table-vertical-border-striped table-bordered mt-3">
          <thead class="table-light">
            <tr class="text-center">
              <th style="width: 40%; min-width: 200px">항목</th>
              <th style="width: 50%; min-width: 200px">정보</th>
              <th style="width: 10%">
                <button type="button" class="btn btn-sm table-text-center text-primary py-0" @click.prevent="addItem"><i class="bi-plus-circle" style="font-size: 1rem"></i></button>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, i) in noticeTemplateItemList" :key="item.id">
              <td><input type="text" maxlength="255" class="form-control" v-model.trim="item.item" placeholder="항목명을 입력해주세요." @change="changeInput(i, $event)" /></td>
              <td><input type="text" maxlength="255" class="form-control" v-model.trim="item.contents" placeholder="항목의 정보를 입력해주세요." @change="changeInput(i, $event)" /></td>
              <td class="text-center">
                <button type="button" class="btn btn-sm table-text-center text-danger" @click.prevent="removeItem(i)"><i class="bi-x-circle" style="font-size: 1rem"></i></button>
              </td>
            </tr>
            <tr v-if="noticeTemplateItemList.length === 0">
              <td colspan="3" class="text-center">품목을 선택해주세요.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- 상품정보제공고시 END -->
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import type { PropType } from 'vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
const props = defineProps<{ productId: number }>();
const emits = defineEmits(['saveFinish', 'changedProdInfo']);

const newCreateNotice = ref(false);

interface NoticeInfoData {
  id?: number;
  product_id?: number;
  item: string;
  category: string;
  contents: string;
  sort: number;
}

const noticeTemplateTitleList = ref([] as string[]);
const noticeTemplateItemList = ref([] as NoticeInfoData[]);
const originNoticeItemList = ref([] as NoticeInfoData[]);
const selectedNoticeId = ref(-1);
const originTitle = ref('');

const changedIndex = new Set<number>();
const addedIndex = new Set<number>();

const addItem = () => {
  if (selectedNoticeId.value < 0) {
    showAlert('품목을 선택 후 추가해주세요.', 'warning');
    return;
  }
  noticeTemplateItemList.value.push({ product_id: props.productId, item: '', category: noticeTemplateTitleList.value[selectedNoticeId.value], contents: '', sort: 0 });
};
const removeItem = (index: number) => {
  if (noticeTemplateItemList.value[index].id) {
    const ids = [] as number[];
    ids.push(noticeTemplateItemList.value[index].id!);
    showConfirm('해당 항목을 삭제하시겠습니까?', () => {
      apis.product.deleteProdNoticeInfo(props.productId, ids).then(res => {
        apiResponseCheck(res, () => {
          showAlert('삭제되었습니다.', 'success');
          noticeTemplateItemList.value.splice(index, 1);
          originNoticeItemList.value.splice(index, 1);
        });
      });
    });
  } else {
    noticeTemplateItemList.value.splice(index, 1);
  }
};

const allInfoDefaultSetting = () => {
  for (const i of noticeTemplateItemList.value) {
    i.contents = '상세설명참조';
  }
};

const changeInput = (index: number, event: any) => {
  if (noticeTemplateItemList.value[index].id) {
    changedIndex.add(index);
  } else {
    addedIndex.add(index);
  }
};

const saveProdNoticeInfo = () => {
  //항목이 없습니다.

  if (selectedNoticeId.value < 0) {
    showAlert('품목을 선택해주세요.', 'warning');
    return;
  }
  if (noticeTemplateItemList.value.length === 0) {
    showAlert('상품정보제공고시 정보 항목이 없습니다.', 'warning');
    return;
  }

  for (const item of noticeTemplateItemList.value) {
    if (!item.category || !item.contents) {
      showAlert('항목 및 정보내용을 빠짐없이 입력해주세요.', 'warning');
      return;
    }
  }

  if (originNoticeItemList.value.length > 0) {
    if (originTitle.value != '' && originTitle.value != noticeTemplateTitleList.value[selectedNoticeId.value]) {
      showConfirm('기존 상품정보제공고시 정보는 삭제됩니다. 저장하시겠습니까?', () => {
        Promise.resolve(deleteOriginNotice()).then(res => {
          if (res) {
            addNoticeInfo();
          }
        });
      });
    } else if (originTitle.value != '' && originTitle.value == noticeTemplateTitleList.value[selectedNoticeId.value]) {
      if (changedIndex.size === 0 && addedIndex.size === 0) {
        showAlert('변경사항이 없습니다.', 'warning');
        return;
      } else {
        showConfirm('상품정보제공고시 정보를 저장하시겠습니까?', () => {
          //수정
          const mod = modNoticeInfo();
          //추가
          const add = modAddNoticeInfo();

          Promise.all([mod, add]).then(() => {
            showAlert('저장되었습니다.', 'success');
            changedIndex.clear();
            addedIndex.clear();
          });
        });
      }
    }
  } else {
    showConfirm('상품정보제공고시 정보를 저장하시겠습니까?', () => {
      addNoticeInfo();
    });
  }
};

const deleteOriginNotice = async () => {
  const ids = [] as number[];
  for (const notice of originNoticeItemList.value) {
    ids.push(notice.id!);
  }

  const result = await apis.product.deleteProdNoticeInfo(props.productId, ids).then(res => {
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      return false;
    } else {
      return true;
    }
  });
  return result;
};

const addNoticeInfo = () => {
  apis.product.addProdNoticeInfo(props.productId, noticeTemplateItemList.value).then(res => {
    apiResponseCheck(res, () => {
      showAlert('상품정보제공고시 정보가 저장되었습니다.', 'success', () => {
        emits('saveFinish', 'notice');
        clearInitInfo();
      });
    });
  });
};

const modAddNoticeInfo = () => {
  if (addedIndex.size === 0) {
    return;
  }
  const addedList: any[] = [];
  addedIndex.forEach(index => {
    const tmp = JSON.parse(JSON.stringify(noticeTemplateItemList.value[index]));
    addedList.push(tmp);
  });
  apis.product.addProdNoticeInfo(props.productId, addedList).then(res => {
    apiResponseCheck(res, () => {
      getProdNoticeInfo();
      return true;
    });
  });
};

const modNoticeInfo = () => {
  if (changedIndex.size === 0) {
    return;
  }
  const changedList: any[] = [];
  changedIndex.forEach(index => {
    const tmp = JSON.parse(JSON.stringify(noticeTemplateItemList.value[index]));
    tmp['notice_id'] = tmp['id'];
    delete tmp.id;
    changedList.push(tmp);
  });
  apis.product.modProdNoticeInfo(props.productId, changedList).then(res => {
    if (res instanceof AxiosError) {
      const error = res.response?.data;
      if (error.msg) showAlert(`에러 메시지: ${error.msg}\n관리자에게 문의해주세요.`, 'error');
      else showAlert('오류가 발생하였습니다.\n관리자에게 문의해주세요.', 'error');
      return false;
    } else {
      return true;
    }
  });
};
const noticeChanged = () => {
  getNoticeInfoTemplate(noticeTemplateTitleList.value[selectedNoticeId.value]);
};

const getNoticeInfoTemplate = (cate: string = '') => {
  let query = '';
  if (cate) {
    query = `?category=${cate}`;
  }
  apis.common.getNoticeInfo(query).then(res => {
    apiResponseCheck(res, () => {
      if (cate) {
        makeItemList(res);
      } else {
        noticeTemplateTitleList.value = res;
        if (props.productId) {
          getProdNoticeInfo();
        }
      }
    });
  });
};

const makeItemList = (list: string[]) => {
  noticeTemplateItemList.value = [];
  const itemValue = noticeTemplateTitleList.value[selectedNoticeId.value];
  for (const i of list) {
    const item = { item: i, product_id: props.productId, category: itemValue, contents: '', sort: 0 };
    noticeTemplateItemList.value.push(item);
  }
};

const convertItemList = (list: NoticeInfoData[]) => {
  noticeTemplateItemList.value = [];
  originNoticeItemList.value = [];

  for (const i of list) {
    const item = { id: i.id, product_id: i.product_id, item: i.item, category: i.category, contents: i.contents, sort: i.sort };
    noticeTemplateItemList.value.push(item);
    originNoticeItemList.value.push(item);
  }
  noticeTemplateTitleList.value.map((item, index) => {
    if (originNoticeItemList.value[0]?.category == item) {
      originTitle.value = item;
      selectedNoticeId.value = index;
      return;
    }
  });
};
const getProdNoticeInfo = () => {
  apis.product.getProdNoticeInfo(props.productId).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      convertItemList(res);
    });
  });
};

const clearInitInfo = () => {
  changedIndex.clear();
  addedIndex.clear();
  getNoticeInfoTemplate();
};

const onStepActive = () => {
  clearInitInfo();
};

defineExpose({ onStepActive });

onMounted(() => {
  // INITIALIZATION OF SORTABLE
  // @ts-ignore
  HSCore.components.HSSortable.init('.js-sortable');
});
</script>

<style scoped></style>
