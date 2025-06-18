<template>
  <PageNavigator :before_link="[]" :current="'상품옵션관리'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">상품옵션관리 - 자주쓰는옵션</div>
    </div>
    <div class="card-body">
      <div class="text-end mb-3">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="showModal('OptionCreateModal')">자주쓰는 옵션 생성</button>
      </div>
      <div class="table-responsive">
        <table class="table table-nowrap table-align-middle border card-table table-vertical-border-striped table-bordered">
          <thead class="thead-light">
            <tr class="text-center">
              <th>옵션명</th>
              <th>옵션값</th>
              <th>옵션가격</th>
              <th>삭제</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in favOptionList" :key="item.id">
              <td>{{ item.name }}</td>
              <td>{{ item.value }}</td>
              <td>{{ item.price }}</td>
              <td>
                <button type="button" class="btn btn-sm btn-outline-danger" @click.prevent="deleteFavOpt(item)">삭제</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- 옵션 생성 Modal -->
  <Modal :id="'OptionCreateModal'" :title="`자주쓰는 옵션 생성`" :xlarge="true">
    <template #body>
      <div class="row col mb-3 align-items-center">
        <label class="col-md-2 col-form-label text-md-center">자주쓰는옵션 이름</label>
        <div class="col-md-5">
          <div class="input-group">
            <input type="text" class="form-control col" v-model.trim="favOptName" maxlength="20" placeholder="자주쓰는옵션 이름을 입력해주세요. 예)색상 또는 사이즈 등" />
          </div>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table table-thead-bordered table-align-middle card-table table-nowrap">
          <thead class="table-secondary">
            <tr class="text-center">
              <th>옵션코드</th>
              <th>옵션값</th>
              <th>옵션가격</th>
              <th style="width: 8%"><button type="button" @click.prevent="addOption" class="btn btn-sm btn-info col-auto m-0 p-1">옵션추가</button></th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(op, i) in optionList" :key="(op, i)">
              <td>
                <input type="text" class="form-control" placeholder="예시) Code1" v-model.trim="op.code" />
              </td>
              <td>
                <input type="text" class="form-control" placeholder="예시) 옵션값1" v-model.trim="op.value" />
              </td>
              <td>
                <div class="input-group">
                  <input type="number" class="form-control text-end" placeholder="예시) 10000" v-model.lazy="op.price" oninput="this.value.length > 8 ? this.value = this.value.slice(0,8) : this.value = this.value" />
                  <span class="input-group-text">원</span>
                </div>
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
import { onMounted, Ref, ref } from 'vue';
import { apiResponseCheck, showAlert, showConfirm, showModal, hideModal } from '@/utils/common-utils';
import type { FavOpt, FavProperty } from 'FavOptListInfo';
import apis from '@/apis';
import { AxiosError } from 'axios';
import PageNavigator from '@/components/title/PageNavigator.vue';

interface ShowFavOptModel {
  id: number;
  name: string;
  value: string;
  price: string;
}

const favOptionList = ref([] as ShowFavOptModel[]);

const favOptName = ref('');
const optionList: Ref<FavProperty[]> = ref([]);

const setProdProp = (list: FavProperty[]) => {};

const addOption = () => {
  if (optionList.value.length === 0) {
    optionList.value.push({ code: '', value: '', price: 0 });
    return;
  }
  const last = optionList.value[optionList.value.length - 1];

  if (!last.code || !last.value || !last.price) {
    showAlert('모든 내용을 입력 후 새로운 옵션을 추가해주세요.', 'warning');
    return;
  }

  optionList.value.push({ code: '', value: '', price: 0 });
};

const deleteProp = (i: number) => {
  optionList.value.splice(i, 1);
};

const createProperty = () => {
  if (!favOptName.value) {
    showAlert('자주쓰는옵션 이름을 입력해주세요.', 'warning');
    return;
  }

  for (const op of optionList.value) {
    if (!op.value || !op.price || !op.code) {
      showAlert('모든 내용을 입력해야 합니다.', 'warning');
      return;
    }
  }

  showConfirm('자주쓰는옵션을 생성하시겠습니까?', () => {
    const data: FavOpt = { name: favOptName.value, type: '', propertys: optionList.value };
    apis.common.regFavoriteOption(data).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('자주쓰는옵션이 생성되었습니다.', 'success', () => {
            getFavOptList();
            hideModal('OptionCreateModal');
          });
        },
        (num?: number) => {
          if (num === 403) {
            //@ts-ignore
            hideModal('OptionCreateModal');
          }
        },
      );
    });
  });
};

const getFavOptList = () => {
  apis.common.getFavoriteOptionList().then(res => {
    apiResponseCheck(res, () => {
      favOptionList.value = [];
      for (const favOpt of res) {
        const fOp = {} as ShowFavOptModel;
        fOp.id = favOpt.id;
        fOp.name = favOpt.name;
        const tmpValue = [];
        const tmpPrice = [];
        for (const prop of favOpt.propertys) {
          tmpPrice.push(prop.price);
          tmpValue.push(prop.value);
        }
        fOp.price = tmpPrice.join(', ');
        fOp.value = tmpValue.join(', ');
        favOptionList.value.push(fOp);
      }
    });
  });
};

const deleteFavOpt = (opt: ShowFavOptModel) => {
  showConfirm(`[${opt.name}] 옵션을 삭제하시겠습니까?`, () => {
    apis.common.deleteFavoriteOption(opt.id).then(res => {
      apiResponseCheck(res, () => {
        showAlert('삭제되었습니다.', 'success');
        getFavOptList();
      });
    });
  });
};

onMounted(() => {
  getFavOptList();

  //@ts-ignore
  document.getElementById('OptionCreateModal').addEventListener('show.bs.modal', function (event) {
    optionList.value = [];
    optionList.value.push({ code: '', value: '', price: 0 });
  });

  //@ts-ignore
  document.getElementById('OptionCreateModal').addEventListener('hide.bs.modal', function (event) {});
});
</script>

<style scoped></style>
