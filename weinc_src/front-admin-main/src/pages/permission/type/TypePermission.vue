<template>
  <PageNavigator :before_link="[]" :current="'타입별 권한 설정'" />
  <div class="card col-md-8">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">타입별 권한 설정</div>
    </div>
    <div class="card-body">
      <div class="text-end mb-3">
        <!-- <button type="button" class="btn btn-sm btn-primary" @click.prevent="showModal('makeTypeModal')">타입 생성</button> -->
      </div>
      <div class="table-responsive">
        <table class="table table-nowrap table-align-middle border card-table table-vertical-border-striped table-bordered">
          <thead class="thead-light">
            <tr class="text-center">
              <th>타입명</th>
              <th>타입설명</th>
              <th v-if="checkPermission('read:menu')">메뉴설정</th>
              <th>권한설정</th>
              <th>타입삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(c, i) in classList" :key="JSON.stringify(c)">
              <td>{{ c.name }}</td>
              <td>{{ c.description }}</td>
              <td v-if="checkPermission('read:menu')">
                <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="router.push({ path: `/permission/type/menu`, state: { code: c.code } })">설정</button>
              </td>
              <td>
                <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="router.push({ path: `/permission/type/detail`, state: { code: c.code } })">설정</button>
              </td>
              <td>
                <button type="button" class="btn btn-sm btn-outline-danger" @click.prevent="removeClass(c.code)">삭제</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Pagination -->
      <div class="d-flex justify-content-center justify-content-sm-end">
        <nav id="datatableWithPaginationPagination" aria-label="Activity pagination"></nav>
      </div>
    </div>
  </div>

  <!-- 타입 생성 Modal -->
  <Modal :id="'makeTypeModal'" :title="'타입 생성'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">타입생성 기본정보</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <form class="mb-6">
              <div class="row col mb-4 align-items-center">
                <label class="col-md-3 col-form-label text-nowrap">타입 코드</label>
                <div class="col">
                  <div class="input-group">
                    <input
                      type="text"
                      class="form-control"
                      v-model="newType.code.value"
                      placeholder="타입 코드를 입력해주세요."
                      @keyup.prevent="
                        () => {
                          newType.code.check = false;
                        }
                      " />
                    <button type="button" class="btn btn-sm btn-info input-group-append" @click.prevent="checkClassCode" :disabled="newType.code.check === true">중복체크</button>
                  </div>
                </div>
              </div>
              <div class="row col mb-4 align-items-center">
                <label class="col-md-3 col-form-label text-nowrap">타입 이름</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" v-model="newType.name" placeholder="타입 이름을 입력해주세요." />
                  </div>
                </div>
              </div>
              <div class="row col mb-4 align-items-center">
                <label class="col-md-3 col-form-label text-nowrap">타입 설명</label>
                <div class="col">
                  <div class="input-group">
                    <textarea type="text" class="form-control" rows="5" v-model="newType.description" placeholder="타입에 대한 설명을 입력해주세요." />
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="addType">타입 생성</button>
    </template>
  </Modal>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Modal from '@/components/comm/modal.vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useRouter } from 'vue-router';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal, checkPermission } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import { useUserStore } from '@/stores/user';
const router = useRouter();

const classList = ref([]);
const newType = ref({
  code: {
    value: '',
    check: false,
  },
  name: '',
  description: '',
});

const getClassList = () => {
  apis.user.get_class().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      classList.value = res;
      return true;
    });
  });
};

const checkClassCode = () => {
  if (newType.value.code.value) {
    apis.permission.check_class_code_exist(newType.value.code.value).then(res => {
      apiResponseCheck(res, () => {
        if (!res.exist) {
          showAlert('생성할 수 있는 타입 코드 입니다.', 'info');
          newType.value.code.check = true;
        } else showAlert('이미 존재하는 타입 코드 입니다.', 'error');
      });
    });
  } else {
    showAlert('타입 코드를 입력해주세요.', 'warning');
  }
};

const addType = () => {
  if (!newType.value.code.check) {
    showAlert('타입 코드 중복체크를 진행해주세요.', 'warning');
    return;
  }
  if (!newType.value.name) {
    showAlert('타입 이름을 입력해주세요.', 'warning');
    return;
  }
  if (!newType.value.description) {
    showAlert('타입 설명을 입력해주세요.', 'warning');
    return;
  }

  showConfirm('타입을 생성하시겠습니까?', () => {
    apis.permission.add_class(newType.value.code.value, newType.value.name, newType.value.description).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('새로운 타입이 생성되었습니다.', 'success');
          newType.value.code.value = '';
          newType.value.code.check = false;
          newType.value.name = '';
          newType.value.description = '';

          hideModal('makeTypeModal');
          getClassList();
        },
        (num?: number) => {
          if (num === 403) {
            hideModal('makeTypeModal');
          }
        },
      );
    });
  });
};

const removeClass = (code: string) => {
  showAlert('기능 준비중입니다.', 'info');
};
onMounted(() => {
  getClassList();
});
</script>

<style scoped></style>
