<template>
  <PageNavigator :before_link="['개별권한설정']" :current="'개별권한설정 상세'" />
  <div class="card col-md-7">
    <div class="card-header">
      <div class="form-control-borderless h2">개별권한설정 - [{{ member.name }} / {{ member.email }}]</div>
    </div>
    <div class="card-body">
      <div class="row mb-4 justify-content-center">
        <div class="col-md-5">
          <div class="list-group list-group-sm" id="mPermissionList">
            <label class="list-group-item active-info">
              <input class="form-check-input me-4 all" type="checkbox" value="" v-if="false" />
              개인 권한
            </label>
            <label class="list-group-item" v-for="mPermission in memberPermission.Member" :key="JSON.stringify(mPermission)">
              <div class="row align-items-center">
                <div class="col">
                  <input class="form-check-input p-radio me-4" type="radio" name="radio_permission" :id="mPermission.name" :value="mPermission.permission_code" />
                  <span>{{ mPermission.name }}</span>
                </div>
                <div class="col-auto">
                  <input class="form-check-input chkb-ex me-2 text-danger" type="checkbox" name="chkb_exclude" :checked="mPermission.exclude === 'Y'" @change="exclude_change($event, mPermission)" />
                  <span class="text-danger">제외</span>
                </div>
              </div>
            </label>
          </div>
          <div class="mt-4">
            <div class="list-group list-group-sm" v-for="classes in memberPermission.Class" :key="JSON.stringify(classes)">
              <label class="list-group-item ps-4 active-warning">{{ classes.class_code }} 권한 </label>
              <label class="list-group-item ps-4" v-for="p in classes.permissions" :key="JSON.stringify(p)">{{ p.name }}</label>
            </div>
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
import type { PermissionInfo, Permission, AvailablePermission } from 'PermissionInfoModule';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import { useUserStore } from '@/stores/user';
const excludeAdminPermission = ['read:commission_conia', 'write:commission_conia', 'read:menu', 'link:menu'];
const memberPermission = ref({} as PermissionInfo);
const availablePermissionList = ref(Array<AvailablePermission>());
const memberId = ref();
const member = reactive({
  name: '-',
  email: '-',
});

const getUserInfo = (id: string) => {
  apis.user.get_user(id, 'member').then(res => {
    apiResponseCheck(res, () => {
      member.name = res.name;
      member.email = res.email;
    });
  });
};

const getMemberPermission = async () => {
  await apis.permission.get_list(`member_id=${memberId.value}`).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      memberPermission.value = res;
      if (memberPermission.value.Member) {
        memberPermission.value.Member.sort((a, b) => a.name.localeCompare(b.name));
      }
      if (memberPermission.value.Class) {
        memberPermission.value.Class.sort((a, b) => a.class_code.localeCompare(b.class_code));
      }
      memberPermission.value.Class.map(item => {
        if (item.permissions) {
          item.permissions.sort((a, b) => a.name.localeCompare(b.name));
        }
      });
      getAllPermission();
    });
  });
};

const getAllPermission = async () => {
  await apis.permission.get_list().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      if (memberPermission.value.Member) {
        availablePermissionList.value = res.filter((item: AvailablePermission) => {
          return !memberPermission.value.Member.some(i => i.permission_code === item.code);
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
    apis.permission.link_permission(code, '*', `member_id=${memberId.value}`).then(res => {
      apiResponseCheck(res, () => {
        showAlert('권한 설정이 완료되었습니다.', 'success');
        // choice.prop('checked', false);
        // choice.parent().appendTo('#mPermissionList');
        getMemberPermission();
      });
    });
  } else {
    apis.permission.unlink_permission(code, `member_id=${memberId.value}`).then(res => {
      apiResponseCheck(res, () => {
        showAlert('권한 설정이 완료되었습니다.', 'success');
        // choice.prop('checked', false);
        // choice.parent().appendTo('#availablePermissionList');
        getMemberPermission();
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
    let items = window.$("#mPermissionList input.p-radio:checked:not('.all')");
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

const exclude_change = (event: any, permission: Permission) => {
  const checked = event.target.checked;
  if (checked) {
    if (permission.exclude === 'N' || permission.exclude === null) {
      showConfirm(
        `[${permission.name}] 권한을 개인권한에서 제외시키겠습니까?`,
        () => {
          excludePermission('Y', permission);
        },
        () => {
          event.target.checked = false;
        },
      );
    }
  } else {
    if (permission.exclude === 'Y') {
      showConfirm(
        `[${permission.name}] 권한을 개인권한에서 포함시키겠습니까?`,
        () => {
          excludePermission('N', permission);
        },
        () => {
          event.target.checked = true;
        },
      );
    }
  }
};

const excludePermission = (flag: string, permission: Permission) => {
  apis.permission.exclude_permission(permission.permission_code, memberId.value, flag).then(res => {
    apiResponseCheck(res, () => {
      showAlert(`[${permission.name}] 권한의 ${flag === 'Y' ? '제외' : '포함'} 설정이 변경되었습니다.`, 'success', () => {
        getMemberPermission();
      });
    });
  });
};

onMounted(() => {
  // INITIALIZATION OF SORTABLE
  // @ts-ignore
  HSCore.components.HSSortable.init('.js-sortable');

  initializeListGroup();

  memberId.value = history.state.id;
  if (memberId.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }
  getUserInfo(memberId.value);
  getMemberPermission();
});
</script>

<style scoped>
.v-center {
  min-height: 200px;
  display: flex;
  justify-content: center;
  flex-flow: column wrap;
}

.chkb-ex:checked {
  background-color: #dc3545 !important;
  border-color: #dc3545 !important;
}
</style>
