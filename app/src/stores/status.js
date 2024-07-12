import { defineStore } from 'pinia'
import { apiGetStatus } from '../api/api.js'

function onlyUnique(value, index, array) {
  return (value!='Test')&&(array.indexOf(value) === index);
}
export const useStatusStore = defineStore('status', {
  state: () => ({
    isSuccess: true,    // from fetchApi axios call
    errMessage: "",     // from fetchApi axioos call
    hydrateID: null,    // timerID for hydration polling

    IP: "" ,            // from /api/status response.data
    Port: "", 
    isRecording: false,
    idleSeconds: 0,
    imgUrls: [],
    lastUrl: "",
    Magic: 0, 
  }),

  getters: {
    doubleCount (state) {
      return state.idleSeconds * 2
    },
    imgList: (state) => state.imgUrls.map(x => ([x, ...x.split('_')])), 
    imgNames: (state) => state.imgList.map(x => x[1]).filter(onlyUnique),
    imgRecords: (state) => (name) => state.imgList.filter(x => x[1]==name).map(x => x[2]).filter(onlyUnique),
    imgFiles: (state) => (name, rec) => state.imgList.filter(x => x[1]==name && x[2]==rec).map(x => x[0]).sort(),
  },

  actions: {
    increment () {
      this.idleSeconds++
    },
    hydrateStore () {
      const ref = this
      // define the polling function
      const pollStatus = () => {
        apiGetStatus().then( response => { 
          ref.$patch(response)
          ref.hydrateID = setTimeout(pollStatus, response.isSuccess ? 1000 : 10000)
        })
      }
      // if its not already hydrating, kick off the polling of /api/status
      if (!ref.hydrateID) {
        ref.hydrateID = setTimeout(pollStatus, 1000) 
      }
    },
    dehydrateStore () {
      clearTimeout(this.hydrateID)
    },
  }
})
