import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const loading = ref(false)
  const initialized = ref(false)

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isMaster = computed(() => user.value?.role === 'master')
  const isOperator = computed(() => user.value?.role === 'operator')
  const canWrite = computed(() => ['admin', 'master'].includes(user.value?.role))
  const userFullName = computed(() => user.value?.first_name || user.value?.username || '')
  const userRole = computed(() => user.value?.role_display || '')

  async function login(credentials) {
    loading.value = true
    try {
      const response = await authApi.login(credentials)
      const { access, refresh, user: userData } = response.data

      accessToken.value = access
      refreshToken.value = refresh
      user.value = userData

      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)

      return { success: true }
    } catch (error) {
      const msg = error.response?.data?.message ||
                  error.response?.data?.detail ||
                  'Неверный логин или пароль'
      return { success: false, error: msg }
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      if (refreshToken.value) {
        await authApi.logout(refreshToken.value)
      }
    } catch { /* ignore */ }

    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push('/login')
  }

  async function fetchMe() {
    if (!accessToken.value) {
      initialized.value = true
      return
    }
    try {
      const response = await authApi.me()
      user.value = response.data
    } catch {
      user.value = null
      accessToken.value = null
      localStorage.removeItem('access_token')
    } finally {
      initialized.value = true
    }
  }

  function hasRole(...roles) {
    return roles.includes(user.value?.role)
  }

  return {
    user, accessToken, refreshToken, loading, initialized,
    isAuthenticated, isAdmin, isMaster, isOperator, canWrite,
    userFullName, userRole,
    login, logout, fetchMe, hasRole
  }
})
