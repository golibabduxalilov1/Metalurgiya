import { useLangStore } from '@/store/lang'
import ru from './ru'
import uz from './uz'

const messages = { ru, uz }

export function useI18n() {
  const langStore = useLangStore()

  function t(key) {
    const dict = messages[langStore.lang] || messages.ru
    return key.split('.').reduce((obj, k) => obj?.[k], dict) ?? key
  }

  return { t, langStore }
}
