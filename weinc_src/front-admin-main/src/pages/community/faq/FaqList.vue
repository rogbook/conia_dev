<template>
  <PageNavigator :before_link="[]" :current="'FAQ'" />
  <div class="card col-lg-6">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">FAQ 목록</div>
    </div>
    <div class="card-body">
      <!-- Nav -->
      <div class="category-area">
        <ul class="nav nav-segment nav-pills mb-4" role="tablist">
          <li class="nav-item" v-for="(cate, i) in Object.keys(faqCateList)" :key="JSON.stringify(cate)">
            <a class="nav-link" :id="`nav-${convertID(cate)}-tab`" :href="`#nav-${convertID(cate)}`" data-bs-toggle="pill" :data-bs-target="`#nav-${convertID(cate)}`" role="tab" :aria-controls="`#nav-${convertID(cate)}`" aria-selected="true" :class="{ active: i === 0 }">{{
              cate
            }}</a>
          </li>
        </ul>
      </div>
      <!-- End Nav -->

      <!-- Tab Content -->
      <div class="tab-content" v-for="(cate, i) in Object.keys(faqCateList)" :key="JSON.stringify(cate)">
        <div class="tab-pane fade show" :id="`nav-${convertID(cate)}`" role="tabpanel" :aria-labelledby="`nav-${convertID(cate)}-tab`" :class="{ active: i === 0 }">
          <div class="accordion" :id="`faqList-${convertID(cate)}-${i}`">
            <div class="accordion-item" v-for="(faq, i) in faqCateList[cate]" :key="JSON.stringify(faq)">
              <div class="accordion-header" :id="`${faq.id}`">
                <a class="accordion-button" role="button" data-bs-toggle="collapse" :data-bs-target="`#faq_content_${convertID(cate)}_${i}`" aria-expanded="true" :aria-controls="`#faq_content_${convertID(cate)}_${i}`"> Q. {{ faq.title }} </a>
              </div>
              <div :id="`faq_content_${convertID(cate)}_${i}`" class="accordion-collapse collapse" :aria-labelledby="`${faq.id}`" :data-bs-parent="`#faqList-${convertID(cate)}-${i}`">
                <div class="accordion-body">
                  A.
                  <div v-html="faq.contents"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- End Tab Content -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { computed, onMounted, ref } from 'vue';
import type { FaqInfo } from 'BoardInfoModule';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert } from '@/utils/common-utils';
import { useUserStore } from '@/stores/user';
import PageNavigator from '@/components/title/PageNavigator.vue';

const faqList = ref([] as FaqInfo[]);

const router = useRouter();

const convertID = (id: string) => {
  return id.replace('/', '-');
};

const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

const currentTarget = computed(() => {
  return !userClass.value ? 'customer' : userClass.value.includes('CM') ? 'admin' : 'partner';
});

const faqCateList = ref({} as any);

// const page_no = ref(1);
// const offset = computed(() => (page_no.value - 1) * limit.value);
// const limit = ref(10);
// const total_page = computed(() => Math.ceil(faqList.value.total / limit.value));

const getFqaList = () => {
  if (!currentTarget.value) {
    return;
  }

  let query = `target=${currentTarget.value}&`;

  apis.community.get_faq_list(query).then(res => {
    apiResponseCheck(res, () => {
      faqList.value = res;
      makeFaqCateList();
    });
  });
};

const makeFaqCateList = () => {
  if (faqList.value.length > 0) {
    for (const faq of faqList.value) {
      if (Object.keys(faqCateList.value).includes(faq.category)) {
        faqCateList.value[faq.category].push(faq);
      } else {
        faqCateList.value[faq.category] = [faq];
      }
    }
  }
};

const conventContents = (data: string): string => {
  const contents = data.replace(/<[^>]*>?/g, '');

  if (contents.length > 150) {
    return contents.slice(0, 150) + '...';
  } else {
    return contents;
  }
};

onMounted(() => {
  getFqaList();
});
</script>

<style scoped></style>
