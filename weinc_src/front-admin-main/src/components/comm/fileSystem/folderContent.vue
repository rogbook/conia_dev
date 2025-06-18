<template>
  <details>
    <summary>
      <i class="bi bi-folder2-open"></i>
      {{ folder.name }}
    </summary>
    <ul class="list-unstyled text-dark text-nowrap">
      <li :key="item.id" v-for="item in childrenOf(folder)">
        <FolderContent v-if="item.folder" :folder="item" :childrenOf="childrenOf"></FolderContent>
        <FileItem :item="item" v-else> </FileItem>
      </li>
    </ul>
  </details>
</template>

<script setup lang="ts">
import type { UnwrapRef } from 'vue';
import FileItem from '@/components/comm/fileSystem/fileItem.vue';
import type { IItem } from '@/components/comm/types';

defineProps<{ folder: UnwrapRef<IItem>; childrenOf: (folder: IItem) => UnwrapRef<IItem>[] }>();
</script>

<style scoped>
ul {
  list-style: none;
  margin: 0;
}
details > ul {
  padding-left: 1.5rem;
}
</style>
