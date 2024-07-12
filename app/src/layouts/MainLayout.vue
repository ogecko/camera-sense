<template>
  <q-layout view="hHh lpr fFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat icon="menu" @click="toggleLeftDrawer" >Menu</q-btn>
        <q-space />
        <q-toolbar-title>Pi Zero Capture App</q-toolbar-title>
        <q-btn flat icon="style" >Review</q-btn>
        <q-btn flat icon="camera" >Capture</q-btn>
        <q-btn flat icon="description" href="/api/docs" >Docs</q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <CaptureForm />
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  
  </q-layout>

</template>

<script setup>
import { ref } from 'vue'
import CaptureForm from 'components/CaptureForm.vue'

defineOptions({
  name: 'MainLayout'
})

const leftDrawerOpen = ref(false)

function toggleLeftDrawer () {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
