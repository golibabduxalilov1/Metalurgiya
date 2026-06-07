import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLangStore = defineStore('lang', () => {
  const lang = ref(localStorage.getItem('app_lang') || 'ru')

  function setLang(newLang) {
    lang.value = newLang
    localStorage.setItem('app_lang', newLang)
  }

  function toggle() {
    setLang(lang.value === 'ru' ? 'uz' : 'ru')
  }

  return { lang, setLang, toggle }
})
