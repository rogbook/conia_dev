<template>
  <PageNavigator :before_link="[]" :current="'회원계층'" />
  <div class="card col-md-6">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">회원계층 <span class="h5">(오늘 0시 기준)</span></div>
    </div>
    <div class="card-body">
      <div>
        <tree-view v-for="(item, i) in hierarchy" :key="i" :name="item.name" :company="item.company_name" :sub="item.sub" :isRoot="false"> </tree-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, computed, ref, watch } from 'vue';
import { getUserClassStr, dateTimeFormatConverter, showAlert, showLogConsole, apiResponseCheck } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import { useRouter } from 'vue-router';
import TreeView from '@/components/user/hierarchy/TreeView.vue';
import apis from '@/apis';

const router = useRouter();
const hierarchy = ref();

const getUserHierarchy = (reset: boolean = true) => {
  apis.common.getSettingValueOne('member_hierarchy').then(res => {
    apiResponseCheck(res, () => {
      hierarchy.value = JSON.parse(res.value);
      hierarchy.value.sort(ascendingName).sort(ascendingSub);
    });
  });
};
interface hierarchyObj {
  name: string;
  sub: object[];
}
const ascendingName = (a: hierarchyObj, b: hierarchyObj) => {
  if (a.name < b.name) return -1;
  // else if (a.name == b.name) return 0;
  // else return 1;
};
const ascendingSub = (a: hierarchyObj, b: hierarchyObj) => {
  if (a.sub > b.sub) return -1;
};
onMounted(() => {
  getUserHierarchy();
});
</script>
