<template>
  <PageNavigator :before_link="['타입별 권한설정']" :current="'타입권한설정'" />
  <div class="card col-md-7">
    <div class="card-header">
      <div class="form-control-borderless h2">타입권한설정 - [{{ classCode }}]</div>
    </div>
    <div class="card-body">
      <div class="row mb-4 justify-content-center">
        <div class="col-md-5">
          <div class="list-group list-group-sm" id="mPermissionList">
            <label class="list-group-item active-info">
              <input class="form-check-input me-4 all" type="checkbox" value="" v-if="false" />
              타입 권한
            </label>
            <label class="list-group-item" v-for="mPermission in classPermission" :key="JSON.stringify(mPermission)">
              <input class="form-check-input me-4" type="radio" name="radio_permission" :id="mPermission.name" :value="mPermission.permission_code" />
              {{ mPermission.name }}
            </label>
          </div>
        </div>
        <div class="col-auto v-center">
          <button type="button" class="btn btn-sm btn-white remove mb-2"><i class="bi bi-chevron-double-right"></i></button>
          <button type="button" class="btn btn-sm btn-white add"><i class="bi bi-chevron-double-left"></i></button>
        </div>
        <div class="col-md-5">
          <div class="list-group list-group-sm" id="availablePermissionList">
            <label class="list-group-item active">
              <input class="form-check-input me-4 all" type="checkbox" value="" v-if="false" />
              추가 가능 권한
            </label>
            <label class="list-group-item" v-for="ap in availablePermissionList" :key="JSON.stringify(ap)">
              <input class="form-check-input me-4" type="radio" name="radio_permission" :id="ap.name" :value="ap.code" />
              {{ ap.name }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import type { Permission, AvailablePermission } from 'PermissionInfoModule';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import { useUserStore } from '@/stores/user';

const excludeAdminPermission = ['read:commission_conia', 'write:commission_conia', 'read:menu', 'link:menu'];

const classPermission = ref([] as Permission[]);
const availablePermissionList = ref(Array<AvailablePermission>());
const classCode = ref();

const getClassPermission = async () => {
  await apis.permission.get_list(`class_code=${classCode.value}`).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      classPermission.value = res;
      if (classPermission.value) {
        classPermission.value.sort((a, b) => a.name.localeCompare(b.name));
      }
      getAllPermission();
    });
  });
};

const getAllPermission = async () => {
  await apis.permission.get_list().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      if (classPermission.value) {
        availablePermissionList.value = res.filter((item: AvailablePermission) => {
          return !classPermission.value.some(i => i.permission_code === item.code);
        });
      } else {
        availablePermissionList.value = res;
      }
      if (useUserStore().user.admin !== 'Y') {
        // admin이 아닌 경우 commission_admin, menu 권한 제거
        availablePermissionList.value = availablePermissionList.value.filter(item => !excludeAdminPermission.includes(item.code));
      }
      if (availablePermissionList.value) {
        availablePermissionList.value.sort((a, b) => a.name.localeCompare(b.name));
      }
    });
  });
};

const setPermission = (code: string, choice: any, method: string): boolean | any => {
  if (method === 'add') {
    apis.permission.link_permission(code, '*', `class_code=${classCode.value}`).then(res => {
      apiResponseCheck(res, () => {
        showAlert('권한 설정이 완료되었습니다.', 'success');
        // choice.prop('checked', false);
        // choice.parent().appendTo('#mPermissionList');
        getClassPermission();
      });
    });
  } else {
    apis.permission.unlink_permission(code, `class_code=${classCode.value}`).then(res => {
      apiResponseCheck(res, () => {
        showAlert('권한 설정이 완료되었습니다.', 'success');
        // choice.prop('checked', false);
        // choice.parent().appendTo('#availablePermissionList');
        getClassPermission();
      });
    });
  }
};

const initializeListGroup = () => {
  //@ts-ignore
  window.$('.add').click(function () {
    //@ts-ignore
    window.$('.all').prop('checked', false);
    //@ts-ignore
    let items = window.$("#availablePermissionList input:checked:not('.all')");
    //@ts-ignore
    items.each(function (idx, item) {
      //@ts-ignore
      let choice = window.$(item);
      const code = choice.val();
      const pName = choice.attr('id');
      showConfirm(`[${pName}] 권한을 부여하시겠습니까?`, () => {
        setPermission(code, choice, 'add');
      });
    });
  });

  //@ts-ignore
  window.$('.remove').click(function () {
    //@ts-ignore
    window.$('.all').prop('checked', false);
    //@ts-ignore
    let items = window.$("#mPermissionList input:checked:not('.all')");
    //@ts-ignore
    items.each(function (idx, item) {
      //@ts-ignore
      let choice = window.$(item);
      const code = choice.val();
      const pName = choice.attr('id');
      showConfirm(`[${pName}] 권한을 제거하시겠습니까?`, () => {
        setPermission(code, choice, 'delete');
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

  classCode.value = history.state.code;
  if (classCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error', () => {
      useRouter().back();
    });
  }
  getClassPermission();
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
