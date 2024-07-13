<template>
  <q-page>
    <div class="row">
      <div class="col-12 col-sm-7 col-md-8 col-lg-9 col-xl-10">
        <q-img :src="imageUrl" fit="contain" spinner-color="white">
          <div class="absolute-top text-center">
            {{ imageName }}
          </div>
        </q-img>
      </div>
      <div class="col-12 col-sm-5 col-md-4 col-lg-3 col-xl-2">
        <CaptureForm />
      </div>
    </div>    
  </q-page>
</template>

<script setup>

  import { useQuasar } from 'quasar'
  import { useRoute } from 'vue-router'
  import { ref, computed } from 'vue'
  import { useStatusStore } from '../stores/status'
  import CaptureForm from 'components/CaptureForm.vue'


  defineOptions({
    name: 'IndexPage'
  });

  const status = useStatusStore()
  const $router = useRoute()

  const imageName = computed(() => ($router.query.img ? $router.query.img : status.lastUrl) )
  const imageUrl = computed(() => (imageName.value ? `/img/${imageName.value}` : '') )

</script>
