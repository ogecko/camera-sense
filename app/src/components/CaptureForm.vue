<template>
    <div class="q-pt-lg q-pa-md">
      <q-banner v-if="!status.isSuccess" rounded class="q-mb-md bg-orange text-white">
        You have lost device connection.
        <q-spinner />
        {{status.errMessage}}
      </q-banner>

      <div v-if="!status.isRecording" class="q-gutter-md">
        <q-btn-group>
          <q-btn @click="onTest" icon="photo_camera"  color="deep-orange-10"  :to="'/'"/>
          <q-btn @click="onStart" icon="circle"   label="Rec" color="deep-orange-7"  />
          <q-btn @click="onReset"  icon="restore"  label="Reset" color="teal-9" />
        </q-btn-group>
      </div>
      <div v-if="status.isRecording" class="q-gutter-md">
        <q-btn @click="onStop" icon="square" label="Stop" color="deep-orange" />
        <q-spinner-facebook  size="md" color="deep-orange" />
        <q-btn  :label="Math.floor(status.idleSeconds)" />
      </div>
    </div>
    <div class="q-pa-md">
      <q-input v-model="name" label="Recording Name" filled></q-input>
      <div class="row q-pt-xs q-col-gutter-xs">
        <div class="col-6"><q-input v-model.number="duration" label="Duration" type="number" suffix="minutes" filled></q-input></div>
        <div class="col-6"><q-input v-model.number="interval" label="Interval" type="number" suffix="seconds" filled></q-input></div> 
      </div>
    </div>
    
    <q-list v-if="status"  dense>
      <q-item-label header>Images Captured</q-item-label>
      <q-expansion-item v-for="(name,idx1) in status.imgNames" :key="idx1" expand-separator icon="folder" :label="name" :caption="` Recordings`" default-closed>

        <q-expansion-item v-for="(rec,idx2) in status.imgRecords(name)" :key="idx2"  icon="camera" :label="rec" :header-inset-level="0.3" dense default-closeed group="recordings">
          <q-btn-group class="q-pl-md">
            <q-btn color="blue-grey-10" icon="skip_previous" :to="`/?img=${status.imgFiles(name,rec)[0]}`" />
            <q-btn color="blue-grey-10" icon="fast_rewind" />
            <q-btn color="blue-grey-10" icon="play_arrow" :to="`/`"/>
            <q-btn color="blue-grey-10" icon="fast_forward" />
            <q-btn color="blue-grey-10" icon="skip_next"/>
          </q-btn-group>
          <div class="row q-pl-md">
            <div v-for="(item,idx3) in status.imgFiles(name,rec)" :key="idx3">
              <q-btn :to="`/?img=${item}`" :label="item.split('_')[2].slice(0,4)"/>
            </div>
          </div>
        </q-expansion-item>
        
      </q-expansion-item>

    </q-list>
</template>

<script>
import { useQuasar } from 'quasar'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { apiRequestTest, apiRequestStart, apiRequestStop, apiRequestReset } from '../api/api.js'
import { useStatusStore } from '../stores/status'

export default {
  setup () {
    const $q = useQuasar()
    const status = useStatusStore()
    const name = ref(null)
    const duration = ref(null)
    const interval = ref(null)

    onMounted ( () => status.hydrateStore() ),
    onUnmounted ( () => status.dehydrateStore() )

    return {
      status,
      name,
      duration,
      interval,

      onTest () {
        apiRequestTest().then( response => console.log(response))
      },

      onStart () {
        apiRequestStart({ name: name.value, duration: duration.value, interval: interval.value }).then( response => console.log(response) )
      },

      onStop () {
        apiRequestStop().then( response => console.log(response))
      },

      onReset () {
        name.value = 'Bread'
        duration.value = 480
        interval.value = 60
        // apiRequestReset().then( response => console.log(response))

      },
    }
  },
}
</script>