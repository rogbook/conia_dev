<template>
  <FolderContent :key="folder.id" v-for="folder in homeFolders" :folder="folder" :children-of="childrenOf" />
</template>

<script setup lang="ts">
import { computed, onMounted, reactive } from 'vue';
import FolderContent from '@/components/comm/fileSystem/folderContent.vue';
import type { IFileSystem, IItem } from '@/components/comm/types';

onMounted(() => {
  createFolder('의류', null);
  createFolder('유아동', null);
  createFolder('화장품', null);
  createFolder('인테리어', null);
  createFolder('가전', null);

  createFile('캐시미어 목도리', '의류');
  createFolder('드레스', '의류');
  createFile('Chrome.app', '드레스');
  createFile('Firefox.app', '드레스');

  createFile('cat.jpg', '가전');
  createFile('big-cat.jpg', '가전');
  createFile('small-cat.jpg', '가전');

  createFile('cat-vs-mouse.mp4', '인테리어');
  createFile('cat-vs-dog.mp4', '인테리어');
  createFile('cat-celebration-ceremony.mp4', '인테리어');

  createFolder('장난감', '유아동');
  createFolder('2018', '장난감');
  'Jan Feb Mar Apr May'.split(' ').forEach(name => createFolder(name, '2018'));
  createFolder('2017', '장난감');
  'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ').forEach(name => createFolder(name, '2017'));

  createFolder('2023', '화장품');
  createFolder('특가상품', '2023');
  createFolder('Super Duper Secret', '특가상품');
  createFile('passwords.txt', 'Super Duper Secret');
});
const fileSystem = reactive<IFileSystem>({ items: [], nextFolderId: 0 });

const createFolder = (name: string, parent: string | null) => {
  fileSystem.items.push({
    id: fileSystem.nextFolderId + 1,
    folder: true,
    name,
    parent,
  });
};

const createFile = (name: string, parent: string) => {
  fileSystem.items.push({
    folder: false,
    name,
    parent,
  });
};
const childrenOf = (folder: IItem) => fileSystem.items.filter(item => item.parent === folder.name);

const homeFolders = computed(() => fileSystem.items.filter(item => item.folder && item.parent === null));

const homeFolder = computed(() => fileSystem.items[0]);
</script>

<style scoped></style>
