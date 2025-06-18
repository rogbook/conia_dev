<template>
  <PageNavigator :before_link="[]" :current="'Option Value 관리'" />
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">Option Value 관리</h4>
          <small>환경설정값 Option Value를 관리합니다.</small>
          <div class="text-danger mt-2"><b>* 시스템에 영향을 미칠 수 있으므로 작업에 유의해주세요.</b></div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <table class="table table-nowrap table-align-middle border card-table table-bordered mt-3">
        <thead class="table-light">
          <tr class="text-center">
            <th>타입코드</th>
            <th>항목명</th>
            <th>항목값</th>
            <th>정렬순서</th>
            <th style="width: 10%">
              <button type="button" class="btn btn-sm btn-primary" @click.prevent="showAddOptionValue">추가등록</button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, i) in optionValueInfoList" :key="item.id">
            <td><input type="text" class="form-control" v-model="item.type" placeholder="타입코드를 정확히 입력해주세요." /></td>
            <td><input type="text" class="form-control" v-model="item.name" placeholder="항목명을 정확히 입력해주세요." /></td>
            <td><input type="text" class="form-control" v-model="item.value" placeholder="항목값을 정확히 입력해주세요." /></td>
            <td><input type="text" class="form-control" v-model="item.sort" placeholder="항목의 설명을 입력해주세요." /></td>
            <td class="text-center">
              <button type="button" class="btn btn-sm btn-warning" @click.prevent="modOptionValue(i)">수정</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <Modal :id="'addOptionValueModal'" :title="'OptionValue 신규 등록'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">OptionValue를 신규 등록합니다.</div>
        <div class="card">
          <div class="card-body">
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">타입코드</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control col" v-model="newOptionValue.type" placeholder="타입코드를 입력해주세요." />
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">항목명</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control col" v-model="newOptionValue.name" placeholder="항목명을 입력해주세요." />
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">항목값</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control col" v-model="newOptionValue.value" placeholder="항목값을 입력해주세요." />
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">정렬순서</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control col" v-model="newOptionValue.sort" placeholder="정렬순서를 입력해주세요." />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="addNewOptionValue">등록</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import PageNavigator from '@/components/title/PageNavigator.vue';
import { onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import type { OptionValue } from 'SettingValueModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import Modal from '@/components/comm/modal.vue';

const newOptionValue = reactive({
  type: '',
  name: '',
  value: '',
  sort: 0,
});
const optionValueInfoList = ref([] as OptionValue[]);
const originOptionValueInfoList = ref([] as OptionValue[]);

const showAddOptionValue = () => {
  newOptionValue.type = '';
  newOptionValue.name = '';
  newOptionValue.value = '';
  newOptionValue.sort = 99;

  showModal('addOptionValueModal');
};

const addNewOptionValue = () => {
  if (!newOptionValue.type) {
    showAlert('타입코드를 입력해주세요.', 'warning');
    return;
  }
  if (!newOptionValue.name) {
    showAlert('항목명를 입력해주세요.', 'warning');
    return;
  }
  if (!newOptionValue.value) {
    showAlert('항목값를 입력해주세요.', 'warning');
    return;
  }
  let data = {} as OptionValue;
  data.type = newOptionValue.type;
  data.name = newOptionValue.name;
  data.value = newOptionValue.value;
  data.sort = newOptionValue.sort;

  showConfirm('신규 등록하시겠습니까?', () => {
    apis.master.add_option_value(data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('성공적으로 등록되었습니다.', 'success', () => {
          hideModal('addOptionValueModal');
          getOptionValueList();
        });
      });
    });
  });
};

const getOptionValueList = () => {
  optionValueInfoList.value = [];
  originOptionValueInfoList.value = [];
  apis.master.get_option_value_list().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      optionValueInfoList.value = res;
      originOptionValueInfoList.value = JSON.parse(JSON.stringify(res));
    });
  });
};

const modOptionValue = (idx: number) => {
  //TODO: 데이터 체크
  const current = optionValueInfoList.value[idx];
  const origin = originOptionValueInfoList.value[idx];

  if (!current.type) {
    showAlert('타입코드를 입력해주세요.', 'warning');
    return;
  }
  if (!current.name) {
    showAlert('항목명를 입력해주세요.', 'warning');
    return;
  }
  if (!current.value) {
    showAlert('항목값를 입력해주세요.', 'warning');
    return;
  }

  let data = {} as OptionValue;
  let msg = '\n';
  if (current.type !== origin.type) {
    data.type = current.type;
    msg = msg.concat(`[타입코드] ${origin.type} >> ${current.type}<br/>`);
  }
  if (current.name !== origin.name) {
    data.name = current.name;
    msg = msg.concat(`[항목명] ${origin.name} >> ${current.name}<br/>`);
  }
  if (current.value !== origin.value) {
    data.value = current.value;
    msg = msg.concat(`[항목값] ${origin.value} >> ${current.value}<br/>`);
  }
  if (current.sort !== origin.sort) {
    data.sort = current.sort;
    msg = msg.concat(`[항목설명] ${origin.sort} >> ${current.sort}<br/>`);
  }

  if (Object.keys(data).length === 0) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  showConfirm(`변경사항${msg}<br/>위 변경사항을 수정하시겠습니까?`, () => {
    apis.master.mod_option_value(current.id!, data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('성공적으로 변경되었습니다.', 'success', () => {
          getOptionValueList();
        });
      });
    });
  });
};
onMounted(() => {
  getOptionValueList();
});
</script>

<style scoped></style>
