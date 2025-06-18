<template>
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">추가정보</h4>
          <small>상품의 추가적인 정보를 작성합니다.</small>
        </div>
        <div class="nav-item ms-auto">
          <button type="button" class="btn btn-warning" @click.prevent="saveProdExtraInfo">저장</button>
        </div>
      </div>
    </div>
    <!-- 상품추가정보 -->
    <div class="card-body">
      <table class="table table-nowrap table-align-middle border card-table table-vertical-border-striped table-bordered mt-3">
        <thead class="table-light">
          <tr class="text-center">
            <th style="width: 40%">항목명</th>
            <th style="width: 50%">정보</th>
            <th style="width: 10%">
              <button type="button" class="btn btn-sm table-text-center text-primary py-0" @click.prevent="addItem"><i class="bi-plus-circle" style="font-size: 1rem"></i></button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, i) in extraInfoList" :key="item.id">
            <td><input type="text" class="form-control" v-model.trim="item.category" placeholder="항목명을 입력해주세요." @change="changeInput(i, $event)" /></td>
            <td><input type="text" class="form-control" v-model.trim="item.contents" placeholder="항목의 정보를 입력해주세요." @change="changeInput(i, $event)" /></td>
            <td class="text-center">
              <button type="button" class="btn btn-sm table-text-center text-danger" @click.prevent="removeItem(i)"><i class="bi-x-circle" style="font-size: 1rem"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- 상품추가정보 END -->
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
const props = defineProps<{ productId: number; reg: boolean }>();
const emits = defineEmits(['saveFinish', 'changedProdInfo']);

interface ExtraInfoData {
  id?: number;
  product_id?: number;
  category: string;
  contents: string;
}

const extraInfoList = ref([] as ExtraInfoData[]);
const originExtraInfoList = ref([] as ExtraInfoData[]);

const changedIndex = new Set<number>();
const addedIndex = new Set<number>();

const addItem = () => {
  extraInfoList.value.push({ product_id: props.productId, category: '', contents: '' });
};
const removeItem = (index: number) => {
  if (extraInfoList.value[index].id) {
    const ids = [] as number[];
    ids.push(extraInfoList.value[index].id!);
    showConfirm('해당 항목을 삭제하시겠습니까?', () => {
      apis.product.delete_prod_extra_info(props.productId, ids).then(res => {
        apiResponseCheck(res, () => {
          showAlert('삭제되었습니다.', 'success');
          extraInfoList.value.splice(index, 1);
          originExtraInfoList.value.splice(index, 1);
        });
      });
    });
  } else {
    extraInfoList.value.splice(index, 1);
  }
};

const changeInput = (index: number, event: any) => {
  if (extraInfoList.value[index].id) {
    changedIndex.add(index);
  } else {
    addedIndex.add(index);
  }
};

const saveProdExtraInfo = () => {
  for (const item of extraInfoList.value) {
    if (!item.category || !item.contents) {
      if (!props.reg) {
        showAlert('항목 및 정보내용을 빠짐없이 입력해주세요.', 'warning');
        return;
      }
    }
  }

  if (originExtraInfoList.value.length > 0) {
    if (changedIndex.size === 0 && addedIndex.size === 0) {
      if (props.reg) {
        emits('saveFinish', 'extra');
        return;
      }
      showAlert('변경사항이 없습니다.', 'warning');
      return;
    } else {
      showConfirm('상품 추가정보를 저장하시겠습니까?', () => {
        //수정
        const mod = modExtraInfo();
        //추가
        const add = modAddExtraInfo();

        Promise.all([mod, add]).then(() => {
          showAlert('저장되었습니다.', 'success', () => {
            clearInitInfo();
          });
        });
      });
    }
  } else {
    showConfirm('상품 추가정보를 저장하시겠습니까?', () => {
      addExtraInfo();
    });
  }
};

const addExtraInfo = () => {
  apis.product.add_prod_extra_info(props.productId, extraInfoList.value).then(res => {
    apiResponseCheck(res, () => {
      showAlert('상품 추가정보가 저장되었습니다.', 'success', () => {
        emits('saveFinish', 'extra');
        clearInitInfo();
      });
    });
  });
};

const modAddExtraInfo = () => {
  if (addedIndex.size === 0) {
    return;
  }
  const addedList: any[] = [];
  addedIndex.forEach(index => {
    const tmp = JSON.parse(JSON.stringify(extraInfoList.value[index]));
    addedList.push(tmp);
  });
  apis.product.add_prod_extra_info(props.productId, addedList).then(res => {
    apiResponseCheck(res, () => {
      return true;
    });
  });
};

const modExtraInfo = () => {
  if (changedIndex.size === 0) {
    return;
  }
  const changedList: any[] = [];
  changedIndex.forEach(index => {
    const tmp = JSON.parse(JSON.stringify(extraInfoList.value[index]));
    changedList.push(tmp);
  });
  apis.product.mod_prod_extra_info(props.productId, changedList).then(res => {
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

const convertItemList = (list: ExtraInfoData[]) => {
  extraInfoList.value = [];
  originExtraInfoList.value = [];

  for (const i of list) {
    const item = { id: i.id, product_id: i.product_id, category: i.category, contents: i.contents };
    extraInfoList.value.push(item);
    originExtraInfoList.value.push(item);
  }
};
const getProdExtraInfo = () => {
  apis.product.get_prod_extra_info(props.productId).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      convertItemList(res);
    });
  });
};

const clearInitInfo = () => {
  changedIndex.clear();
  addedIndex.clear();
  getProdExtraInfo();
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
