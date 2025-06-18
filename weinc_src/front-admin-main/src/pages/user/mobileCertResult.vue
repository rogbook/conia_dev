<template>
  <div></div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRoute } from 'vue-router';

export default defineComponent({
  mounted() {
    const token_version_id = useRoute().query.token_version_id;
    const enc_data = useRoute().query.enc_data;
    const integrity_value = useRoute().query.integrity_value;
    const closePopup = () => {
      if (token_version_id && enc_data && integrity_value) {
        window.opener.postMessage({
          token_version_id: token_version_id,
          enc_data: enc_data,
          integrity_value: integrity_value,
        });
        window.close();
      }
    };
    closePopup();
  },
});
</script>

<style scoped></style>
