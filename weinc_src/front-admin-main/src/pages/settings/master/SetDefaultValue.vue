<template>
  <PageNavigator :before_link="[]" :current="'기본 설정값 관리'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center">
        <div class="col-auto">
          <div class="form-control-borderless h2">기본 설정값 관리</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card">
        <div class="card-header py-2">
          <span class="icon icon-xs icon-dark icon-circle" style="width: 0.5rem; height: 0.5rem"></span>
          기본정보
        </div>
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-1 col-form-label"><span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 이름</label>
            <div class="col-md-4">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="값" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-1 col-form-label"><span class="text-danger" style="width: 0.2rem; height: 0.2rem">*</span> 이름</label>
            <div class="col-md-4">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="값" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import PageNavigator from '@/components/title/PageNavigator.vue';
</script>

<style scoped></style>
