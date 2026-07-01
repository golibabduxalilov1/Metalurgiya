import ru from './ru'

export function useI18n() {
  function t(key) {
    return key.split('.').reduce((obj, k) => obj?.[k], ru) ?? key
  }

  return { t }
}
