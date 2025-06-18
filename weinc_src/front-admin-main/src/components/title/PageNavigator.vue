<template>
  <div class="row justify-content-between">
    <div class="col-auto mb-3" @click.prevent="router.back()">
      <button type="button" class="btn btn-sm btn-outline-dark">뒤로가기</button>
    </div>

    <div class="col-auto align-items-center p-0 me-3 mt-3">
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
          <li class="breadcrumb-item">
            <a href="/dashboard">Home</a>
          </li>
          <li class="breadcrumb-item" v-for="(link, i) in before_link" :key="JSON.stringify(link)">
            <a
              href=""
              @click.prevent="
                () => {
                  router.go((before_link.length - i) * -1);
                }
              "
              >{{ link }}</a
            >
          </li>
          <li class="breadcrumb-item active" aria-current="page" v-if="current">{{ current }}</li>
        </ol>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';
import { showLogConsole } from '@/utils/common-utils';

const props = defineProps({
  before_link: {
    type: Array<string>,
    default: [],
  },
  current: {
    type: String,
  },
});

const router = useRouter();
onMounted(() => {
  showLogConsole(props.before_link);
});
</script>

<style scoped>
.btn-circle {
  width: 30px;
  height: 30px;
  padding: 6px 0px;
  border-radius: 15px;
  text-align: center;
  font-size: 12px;
  line-height: 1.42857;
}
</style>
