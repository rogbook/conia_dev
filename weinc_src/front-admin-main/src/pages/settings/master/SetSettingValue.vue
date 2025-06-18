<template>
  <PageNavigator :before_link="[]" :current="'Setting Value 관리'" />
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">Setting Value 관리</h4>
          <small>환경설정값 Setting Value를 관리합니다.</small>
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
            <th>항목설명</th>
            <th style="width: 10%">
              <button type="button" class="btn btn-sm btn-primary" @click.prevent="showAddSettingValue">추가등록</button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, i) in settingValueInfoList" :key="item.id">
            <td><input type="text" class="form-control" v-model="item.type" placeholder="타입코드를 정확히 입력해주세요." /></td>
            <td><input type="text" class="form-control" v-model="item.name" placeholder="항목명을 정확히 입력해주세요." /></td>
            <td><input type="text" class="form-control" v-model="item.value" placeholder="항목값을 정확히 입력해주세요." /></td>
            <td><input type="text" class="form-control" v-model="item.description" placeholder="항목의 설명을 입력해주세요." /></td>
            <td class="text-center">
              <button type="button" class="btn btn-sm btn-warning" @click.prevent="modSettingValue(i)">수정</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <Modal :id="'addSettingValueModal'" :title="'SettingValue 신규 등록'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">SettingValue를 신규 등록합니다.</div>
        <div class="card">
          <div class="card-body">
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">타입코드</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control col" v-model="newSettingValue.type" placeholder="타입코드를 입력해주세요." />
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">항목명</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control col" v-model="newSettingValue.name" placeholder="항목명을 입력해주세요." />
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">항목값</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control col" v-model="newSettingValue.value" placeholder="항목값을 입력해주세요." />
                </div>
              </div>
            </div>
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label">항목설명</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control col" v-model="newSettingValue.description" placeholder="항목설명을 입력해주세요." />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="addNewSettingValue">등록</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import PageNavigator from '@/components/title/PageNavigator.vue';
import { onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import type { SettingValue } from 'SettingValueModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import Modal from '@/components/comm/modal.vue';

const newSettingValue = reactive({
  type: '',
  name: '',
  value: '',
  description: '',
});
const settingValueInfoList = ref([] as SettingValue[]);
const originSettingValueInfoList = ref([] as SettingValue[]);

const showAddSettingValue = () => {
  newSettingValue.type = '';
  newSettingValue.name = '';
  newSettingValue.value = '';
  newSettingValue.description = '';

  showModal('addSettingValueModal');
};

const addNewSettingValue = () => {
  if (!newSettingValue.type) {
    showAlert('타입코드를 입력해주세요.', 'warning');
    return;
  }
  if (!newSettingValue.name) {
    showAlert('항목명를 입력해주세요.', 'warning');
    return;
  }
  if (!newSettingValue.value) {
    showAlert('항목값를 입력해주세요.', 'warning');
    return;
  }
  let data = {} as SettingValue;
  data.type = newSettingValue.type;
  data.name = newSettingValue.name;
  data.value = newSettingValue.value;
  if (newSettingValue.description) data.description = newSettingValue.description;

  showConfirm('신규 등록하시겠습니까?', () => {
    apis.master.add_setting_value(data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('성공적으로 등록되었습니다.', 'success', () => {
          hideModal('addSettingValueModal');
          getSettingValueList();
        });
      });
    });
  });
};

const getSettingValueList = () => {
  settingValueInfoList.value = [];
  originSettingValueInfoList.value = [];
  apis.master.get_setting_value_list().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      settingValueInfoList.value = res;
      originSettingValueInfoList.value = JSON.parse(JSON.stringify(res));
    });
  });
};

const modSettingValue = (idx: number) => {
  //TODO: 데이터 체크
  const current = settingValueInfoList.value[idx];
  const origin = originSettingValueInfoList.value[idx];

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

  let data = {} as SettingValue;
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
  if (current.description !== origin.description) {
    data.description = current.description;
    msg = msg.concat(`[항목설명] ${origin.description ? origin.description : "''"} >> ${current.description}<br/>`);
  }

  if (Object.keys(data).length === 0) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  showConfirm(`변경사항${msg}<br/>위 변경사항을 수정하시겠습니까?`, () => {
    apis.master.mod_setting_value(current.id!, data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('성공적으로 변경되었습니다.', 'success', () => {
          getSettingValueList();
        });
      });
    });
  });
};
onMounted(() => {
  getSettingValueList();
});
</script>
₩

<style scoped></style>
