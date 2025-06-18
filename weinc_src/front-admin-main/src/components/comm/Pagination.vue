<template>
  <nav aria-label="Page navigation" class="pt-3">
    <ul class="pagination">
      <li>
        <a class="page-link" @click="onPageChange(1)">
          <i class="bi bi-chevron-double-left"></i>
        </a>
      </li>
      <li>
        <a class="page-link" aria-label="Previous" @click="onPageChange(currentPage - 1)">
          <i class="bi bi-chevron-left"></i>
          <span class="visually-hidden">Previous</span>
        </a>
      </li>
      <li v-for="paging in pages" :key="JSON.stringify(paging)" @click="onPageChange(paging)" :class="paging === currentPage ? 'active' : ''">
        <a class="page-link">{{ paging }}</a>
      </li>
      <li>
        <a class="page-link" aria-label="Next" @click="onPageChange(currentPage + 1)">
          <i class="bi bi-chevron-right"></i>
          <span class="visually-hidden">Next</span>
        </a>
      </li>
      <li>
        <a class="page-link" @click="onPageChange(totalPages)">
          <i class="bi bi-chevron-double-right"></i>
        </a>
      </li>
    </ul>
  </nav>
</template>

<script lang="ts">
import { showAlert } from '@/utils/common-utils';

export default {
  name: 'Pagination',
  props: ['currentPage', 'totalPages', 'pageChange'],
  data() {
    return {};
  },
  computed: {
    pages: function () {
      const list = [];
      for (let index = this.startPage; index <= this.endPage; index += 1) {
        list.push(index);
      }
      return list;
    },
    startPage(): number {
      return (Math.ceil(parseInt(this.currentPage) / 5) - 1) * 5 + 1;
    },
    endPage(): number {
      let lastPage = Math.ceil(parseInt(this.currentPage) / 5) * 5;
      return lastPage <= this.totalPages ? lastPage : this.totalPages;
    },
  },
  methods: {
    onPageChange(val: number) {
      if (val < 1) {
        showAlert('첫 페이지입니다.', 'warning');
        return;
      }
      if (val > this.totalPages) {
        showAlert('마지막 페이지입니다.', 'warning');
        return;
      }
      const param = {
        requestPage: val,
      };
      this.pageChange(param.requestPage);
    },
  },
};
</script>

<style scoped>
currentPage {
  font-weight: bold;
}
</style>
