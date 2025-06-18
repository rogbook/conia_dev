<template>
  <Modal :id="`OptionCreateModal`" :title="`옵션생성`" :xlarge="true">
    <template #body>
      <div class="row col align-items-center justify-content-between mb-2 ms-0">
        <button type="button" @click.prevent="addOption" class="btn btn-sm btn-info col-auto">옵션추가</button>
        <div class="text-danger col-auto"><b>&#8251;</b> 옵션명을 제외한 값들은 쉼표(,)로 구분하여 복수입력가능합니다.</div>
      </div>

      <div class="table-responsive">
        <table class="table table-thead-bordered table-align-middle card-table">
          <thead class="table-secondary">
            <tr class="text-center">
              <th style="width: 18%; min-width: 150px">옵션선택</th>
              <th style="min-width: 150px">옵션명</th>
              <th style="min-width: 150px">옵션코드</th>
              <th style="min-width: 150px">옵션값</th>
              <th style="min-width: 150px">옵션가격</th>
              <th style="width: 8%">추가/삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(op, i) in optionList" :key="op.id">
              <td>
                <select v-model="op.type.value" class="form-select" @change.prevent="opTypeChange(i, $event)">
                  <option v-for="option_type in optionTypeList" :value="option_type.value" :key="JSON.stringify(option_type)">{{ option_type.name }}</option>
                </select>
              </td>
              <td style="padding-left: 10px; padding-right: 10px">
                <!-- 옵션이 직접선택 -->
                <input type="text" class="form-control" placeholder="예시) 색상" v-model="op.name" />
                <!-- 옵션이 직접선택 아닌 경우 -->
              </td>
              <td style="padding-left: 10px; padding-right: 10px">
                <input type="text" class="form-control" placeholder="예시) BLACK,WHITE" v-model.lazy="op.code" oninput="this.value = this.value.replace(/[^a-zA-Z0-9,]/gi,'')" />
              </td>
              <td style="padding-left: 10px; padding-right: 10px">
                <input type="text" class="form-control" placeholder="예시) 블랙,화이트" v-model="op.value" />
              </td>
              <td style="padding-left: 10px; padding-right: 10px">
                <input type="text" class="form-control" placeholder="예시) 10000,15000" v-model="op.price" oninput="this.value = this.value.replace(/[^0-9,]/gi,'')" />
              </td>
              <td>
                <button type="button" class="btn btn-sm btn-warning" @click.prevent="deleteProp(i)">삭제</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-primary" @click.prevent="createProperty">생성</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import { onMounted, ref, Ref } from 'vue';
import type { Opt, OptionType } from 'ProductListModule';
import { apiResponseCheck, showAlert, showConfirm, showModal, hideModal } from '@/utils/common-utils';
import apis from '@/apis';
import { AxiosError } from 'axios';
import type { FavOpt } from 'FavOptListInfo';

const props = defineProps({
  hasOrigin: {
    type: Boolean,
    default: false,
  },
});

const emits = defineEmits(['cancelUseOption', 'setProdProp']);

const id = ref(1);

const def = {
  type: { value: '1', name: '직접입력' },
  name: '',
  value: '',
  price: '',
};
const optionList: Ref<Opt[]> = ref([]);

const favoriteOptionList = ref([] as FavOpt[]);

const optionTypeList = ref([] as OptionType[]);

const addOption = () => {
  if (optionList.value.length === 0) {
    optionList.value.push({ type: { value: 'custom', name: '직접입력' }, code: '', name: '', value: '', price: '' });
    return;
  }
  const last = optionList.value[optionList.value.length - 1];

  if (!last.name || !last.value || !last.price) {
    showAlert('모든 내용을 입력 후 새로운 옵션을 추가해주세요.', 'warning');
    return;
  }

  if (last.value.trim().split(',').length !== last.price.trim().split(',').length) {
    showAlert('옵션값과 옵션가격의 개수가 다릅니다.\n작성한 내용 확인 후 새로운 옵션을 추가해주세요.', 'warning');
    return;
  }

  if (optionList.value.length >= 5) {
    showAlert('옵션은 최대 5개까지만 생성할 수 있습니다.', 'warning');
    return;
  }

  optionList.value.push({ type: { value: 'custom', name: '직접입력' }, code: '', name: '', value: '', price: '' });
};

const createProperty = () => {
  for (const op of optionList.value) {
    if (!op.name || !op.value || !op.price || !op.code) {
      showAlert('모든 내용을 입력해야 합니다.', 'warning');
      return;
    }

    if (op.value.trim().split(',').length !== op.price.trim().split(',').length) {
      showAlert('옵션값과 옵션가격의 개수가 다릅니다.\n작성한 내용 확인해주세요.', 'warning');
      return;
    }
    if (op.value.trim().split(',').length !== op.code.trim().split(',').length) {
      showAlert('옵션값과 옵션코드의 개수가 다릅니다.\n작성한 내용 확인해주세요.', 'warning');
      return;
    }
  }
  if (props.hasOrigin) {
    showConfirm('옵션 신규 생성시 기존에 사용중인 옵션은 삭제됩니다.\n옵션을 신규 생성하시겠습니까?', () => {
      hideModal('OptionCreateModal');
      emits('setProdProp', optionList.value);
    });
  } else {
    hideModal('OptionCreateModal');
    emits('setProdProp', optionList.value);
  }
};

const deleteProp = (i: number) => {
  optionList.value.splice(i, 1);
};

const opTypeChange = (idx: number, event: any) => {
  const target = optionList.value[idx];

  if (event.target.value === 'custom') {
    target.name = '';
    target.code = '';
    target.value = '';
    target.price = '';
  } else {
    favoriteOptionList.value.map(item => {
      if (item.name === event.target.value) {
        const codes = [];
        const values = [];
        const prices = [];
        for (const prop of item.propertys) {
          codes.push(prop.code);
          values.push(prop.value);
          prices.push(prop.price);
        }
        target.name = item.name;
        target.code = codes.join(',');
        target.value = values.join(',');
        target.price = prices.join(',');
        return;
      }
    });
  }
};

const getFavoriteOptionList = () => {
  apis.common.getFavoriteOptionList().then(res => {
    apiResponseCheck(res, () => {
      favoriteOptionList.value = res;

      for (const favOpt of res) {
        optionTypeList.value.push({ value: favOpt.name, name: favOpt.name });
      }
    });
  });
};

onMounted(() => {
  //@ts-ignore
  document.getElementById('OptionCreateModal').addEventListener('show.bs.modal', function (event) {
    optionTypeList.value = [{ value: 'custom', name: '직접입력' }];

    getFavoriteOptionList();

    optionList.value = [];
    optionList.value.push({ type: { value: 'custom', name: '직접입력' }, code: '', name: '', value: '', price: '' });
    // optionList.value.push({ type: { value: 'custom', name: '직접입력' }, code: 'WHITE,BLACK,RED', name: '색상', value: '화이트,블랙,레드', price: '10000,10000,12000' });
    // optionList.value.push({ type: { value: 'custom', name: '직접입력' }, code: 'S,M,L,XL', name: '사이즈', value: 'S,M,L,XL', price: '1000,1000,2000,2000' });
  });
});
</script>

<style scoped></style>
