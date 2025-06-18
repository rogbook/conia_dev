<template>
  <PageNavigator :before_link="['타입별 메뉴설정']" :current="'타입메뉴설정'" />
  <div class="card col-md-6">
    <div class="card-header">
      <div class="form-control-borderless h2">타입메뉴설정 - [{{ classCode }}]</div>
    </div>
    <div class="card-body">
      <ul>
        <li v-for="m in menuTree" :key="m.name">
          <div class="row align-items-center mb-4">
            <div class="col-auto" style="font-size: 1rem">[{{ m.name }}]</div>
            <div class="col-auto">
              <div class="form-check form-switch">
                <input type="checkbox" class="form-check-input is-valid" :id="`menu_${m.id}`" @click.prevent="checkClick(m.id, $event)" :disabled="!checkPermission('link:menu')" />
              </div>
            </div>
          </div>
          <ul v-if="m.sub?.length > 0">
            <li v-for="m2 in m.sub" :key="m2.name">
              <div class="row align-items-center mb-4">
                <div class="col-auto">
                  {{ m2.name }}
                </div>
                <div class="col-auto">
                  <div class="form-check form-switch">
                    <input type="checkbox" class="form-check-input" :id="`menu_${m2.id}`" @click.prevent="checkClick(m2.id, $event)" :disabled="!checkPermission('link:menu')" />
                  </div>
                </div>
              </div>
              <ul v-if="m2.sub?.length > 0">
                <li v-for="m3 in m2.sub" :key="m3.name">
                  <div class="row align-items-center mb-4">
                    <div class="col-auto">
                      {{ m3.name }}
                    </div>
                    <div class="col-auto">
                      <div class="form-check form-switch">
                        <input type="checkbox" class="form-check-input" :id="`menu_${m3.id}`" @click.prevent="checkClick(m3.id, $event)" :disabled="!checkPermission('link:menu')" />
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import apis from '@/apis';
import { apiResponseCheck, checkPermission, showAlert, showConfirm } from '@/utils/common-utils';
import { useRouter } from 'vue-router';

interface Menu {
  id: number;
  name: string;
  depth: number;
  menu_id: number;
}

const classCode = ref();
const mMenuList = ref([] as any[]);
const mClassMenuList = ref([] as any[]);

const menuTree = ref([] as any[]);

const getMenuList = () => {
  mMenuList.value = [];
  mClassMenuList.value = [];
  menuTree.value = [];
  apis.permission.get_menu().then(res => {
    apiResponseCheck(res, () => {
      mMenuList.value = res;
      makeMenuTree();
    });
  });
};

const makeMenuTree = () => {
  const depth1 = {} as any;
  const depth2 = {} as any;
  const depth3 = {} as any;
  mMenuList.value.map(item => {
    if (item.depth < 3) {
      item['sub'] = [];
    }

    // 상위 메뉴
    if (item.depth === 1) {
      depth1[item.id] = item;
    }
    // 하위 메뉴
    else if (item.depth === 2) {
      if (Object.keys(depth2).includes(item.menu_id.toString())) {
        depth2[item.menu_id.toString()].push(item);
      } else {
        depth2[item.menu_id] = [];
        depth2[item.menu_id].push(item);
      }
    }
    // 하위 하위 메뉴
    else if (item.depth === 3) {
      if (Object.keys(depth3).includes(item.menu_id.toString())) {
        depth3[item.menu_id.toString()].push(item);
      } else {
        depth3[item.menu_id] = [];
        depth3[item.menu_id].push(item);
      }
    }
  });

  for (const d2 of Object.keys(depth2)) {
    depth2[d2].map((item: any) => {
      if (Object.keys(depth3).includes(item.id.toString())) {
        item['sub'] = depth3[item.id];
      }
    });
  }

  for (const d1 of Object.keys(depth1)) {
    depth1[d1].sub = depth2[d1];
    menuTree.value.push(depth1[d1]);
  }
  getClassMenu();
};

const makeClassMenuTree = () => {
  for (const m of mClassMenuList.value) {
    //@ts-ignore
    window.$(`#menu_${m.menu.id}`).prop('checked', true);
  }
};

const getClassMenu = () => {
  apis.permission.get_class_menu(classCode.value).then(res => {
    apiResponseCheck(res, () => {
      mClassMenuList.value = res;
      makeClassMenuTree();
    });
  });
};

const checkClick = (menu_id: number, event: any) => {
  console.log(event.target.checked);
  if (!event.target.checked) {
    showConfirm('해당 메뉴를 보이지 않도록 설정하시겠습니까?', () => {
      apis.permission.unlink_menu(classCode.value, menu_id).then(res => {
        apiResponseCheck(res, () => {
          showAlert('메뉴 설정이 완료되었습니다.', 'success', () => {
            getMenuList();
          });
        });
      });
    });
  } else {
    showConfirm('해당 메뉴를 보이도록 설정하시겠습니까?', () => {
      apis.permission.link_menu(classCode.value, menu_id).then(res => {
        apiResponseCheck(res, () => {
          showAlert('메뉴 설정이 완료되었습니다.', 'success', () => {
            getMenuList();
          });
        });
      });
    });
  }
};

onMounted(() => {
  classCode.value = history.state.code;
  if (classCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error', () => {
      useRouter().back();
    });
  }
  getMenuList();
});
</script>

<style scoped></style>
