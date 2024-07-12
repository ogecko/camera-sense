<template>
  <q-page class="flex flex-center">
    <!-- <q-img
      src="proof_2024-05-06_11h38_00115-tagged.jpg"
      fit="contain" spinner-color="white"
    /> -->
    <q-img :src="imageUrl" fit="contain" spinner-color="white">
      <div class="absolute-top text-center">
        {{ imageName }}
      </div>
    </q-img>
  </q-page>
</template>

<script setup>

  import { useQuasar } from 'quasar'
  import { useRoute } from 'vue-router'
  import { ref, computed } from 'vue'
  import { useStatusStore } from '../stores/status'


  defineOptions({
    name: 'IndexPage'
  });

  const status = useStatusStore()
  const $router = useRoute()

  const imageName = computed(() => ($router.query.img ? $router.query.img : status.lastUrl) )
  const imageUrl = computed(() => (imageName.value ? `/img/${imageName.value}` : '') )

</script>
