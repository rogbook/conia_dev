<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세'] : ['상점 관리', '상점관리 상세']" :current="'상점 마이메뉴 관리'" />
  <div class="card col-md-7">
    <div class="card-header">
      <div class="form-control-borderless h2">상점 마이메뉴 관리 - [상점명 : {{ storeInfo.title }}]</div>
    </div>
    <div class="card-body">
      <div class="row mb-4 justify-content-center">
        <div class="col-md-5">
          <div class="list-group list-group-sm" id="mStoreCurrentMenu">
            <label class="list-group-item active-info">
              <input class="form-check-input me-4 all" type="checkbox" value="" v-if="false" />
              상점 마이 메뉴
            </label>
            <label class="list-group-item" v-for="sm in mStoreCurrentMenu" :key="JSON.stringify(sm)">
              <input class="form-check-input me-4" type="checkbox" name="chk_current_menu" :id="sm.name" :value="sm.value" />
              {{ sm.name }}
            </label>
            <label class="list-group-item text-center" v-if="mStoreCurrentMenu.length === 0"> 상점 마이메뉴 없음 </label>
          </div>
        </div>
        <div class="col-auto v-center">
          <button type="button" class="btn btn-sm btn-white remove mb-2"><i class="bi bi-chevron-double-right"></i></button>
          <button type="button" class="btn btn-sm btn-white add"><i class="bi bi-chevron-double-left"></i></button>
        </div>
        <div class="col-md-5">
          <div class="list-group list-group-sm" id="mStoreExcludeMenu">
            <label class="list-group-item active-danger">
              <input class="form-check-input me-4 all" type="checkbox" value="" v-if="false" />
              제외된 메뉴 (사용자에게 보이지 않음)
            </label>
            <label class="list-group-item" v-for="em in mExcludeStoreMenu" :key="JSON.stringify(em)">
              <input class="form-check-input me-4" type="checkbox" name="chk_exclude_menu" :id="em.name" :value="em.value" />
              {{ em.name }}
            </label>
            <label class="list-group-item text-center" v-if="mExcludeStoreMenu.length === 0"> 제외된 메뉴 없음 </label>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer text-center py-2">
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="saveStoreExcludeMenu">저장</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import apis from '@/apis';
import { apiResponseCheck, getUserClassStr, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import type { Store } from 'StoreListInfoModule';

interface Menu {
  id?: number;
  name: string;
  value: string;
}

const storeCode = ref();
const storeInfo = ref({} as Store);

const mStoreMenu = ref([] as Menu[]);
const mStoreCurrentMenu = ref([] as Menu[]);
const mStoreOriginExclude = ref('');
const mExcludeStoreMenu = ref([] as Menu[]);

const getStoreInfo = async (code: string) => {
  await apis.store.get_store(code).then(res => {
    apiResponseCheck(res, () => {
      storeInfo.value = res;
      showLogConsole(res);
    });
  });
};

const getStoreMenu = () => {
  apis.common.getOptionValue('store_menu').then(res => {
    apiResponseCheck(res, () => {
      mStoreMenu.value = res;
      checkStoreExcludeMenu();
    });
  });
};

const checkStoreExcludeMenu = () => {
  mExcludeStoreMenu.value = [];
  mStoreCurrentMenu.value = [];
  let exclude = [] as any[];
  if (storeInfo.value.exclude_menu) {
    exclude = storeInfo.value.exclude_menu.split(',');
  }
  for (const m of mStoreMenu.value) {
    if (!exclude.includes(m.value)) {
      mStoreCurrentMenu.value.push(m);
    } else {
      mExcludeStoreMenu.value.push(m);
    }
  }
};

const saveStoreExcludeMenu = () => {
  const exclude = [] as any;
  mExcludeStoreMenu.value.map(item => {
    exclude.push(item.value);
  });
  let excludeMenu = exclude.toString();
  if (!excludeMenu) {
    excludeMenu = '_null_';
  }
  showConfirm('설정된 마이메뉴를 저장하시겠습니까?', () => {
    apis.store.mod_store(storeCode.value, { exclude_menu: excludeMenu }).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상점 마이메뉴 설정이 저장되었습니다.', 'success', () => {
          Promise.resolve(getStoreInfo(storeCode.value)).then(res => {
            getStoreMenu();
          });
        });
      });
    });
  });
};

const initializeListGroup = () => {
  //@ts-ignore
  window.$('.remove').click(function () {
    //@ts-ignore
    window.$('.all').prop('checked', false);
    //@ts-ignore
    let items = window.$("#mStoreCurrentMenu input:checked:not('.all')");
    //@ts-ignore
    items.each(function (idx, item) {
      //@ts-ignore
      let choice = window.$(item);
      const value = choice.val();
      const pName = choice.attr('id');
      mExcludeStoreMenu.value.push({ name: pName, value: value });
      mStoreCurrentMenu.value.forEach((item, index) => {
        if (item.value === value) {
          mStoreCurrentMenu.value.splice(index, 1);
        }
      });
    });
  });

  //@ts-ignore
  window.$('.add').click(function () {
    //@ts-ignore
    window.$('.all').prop('checked', false);
    //@ts-ignore
    let items = window.$("#mStoreExcludeMenu input:checked:not('.all')");
    //@ts-ignore
    items.each(function (idx, item) {
      //@ts-ignore
      let choice = window.$(item);
      const value = choice.val();
      const pName = choice.attr('id');
      mStoreCurrentMenu.value.push({ name: pName, value: value });
      mExcludeStoreMenu.value.forEach((item, index) => {
        if (item.value === value) {
          mExcludeStoreMenu.value.splice(index, 1);
        }
      });
    });
  });

  /* toggle all checkboxes in group */
  //@ts-ignore
  window.$('.all').click(function (e) {
    e.stopPropagation();
    //@ts-ignore
    let $this = window.$(this);
    if ($this.is(':checked')) {
      $this.parents('.list-group').find('[type=checkbox]').prop('checked', true);
    } else {
      $this.parents('.list-group').find('[type=checkbox]').prop('checked', false);
      $this.prop('checked', false);
    }
  });

  //@ts-ignore
  window.$('[type=checkbox]').click(function (e) {
    e.stopPropagation();
  });

  /* toggle checkbox when list group item is clicked */
  //@ts-ignore
  window.$('.list-group a').click(function (e) {
    e.stopPropagation();
    //@ts-ignore
    let $this = window.$(this).find('[type=checkbox]');
    if ($this.is(':checked')) {
      $this.prop('checked', false);
    } else {
      $this.prop('checked', true);
    }

    if ($this.hasClass('all')) {
      $this.trigger('click');
    }
  });
};

onMounted(() => {
  // INITIALIZATION OF SORTABLE
  // @ts-ignore
  HSCore.components.HSSortable.init('.js-sortable');

  initializeListGroup();

  storeCode.value = history.state.code;
  if (storeCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error', () => {
      useRouter().back();
    });
  }
  Promise.resolve(getStoreInfo(storeCode.value)).then(res => {
    getStoreMenu();
  });
});
</script>

<style scoped>
.v-center {
  min-height: 200px;
  display: flex;
  justify-content: center;
  flex-flow: column wrap;
}
</style>
