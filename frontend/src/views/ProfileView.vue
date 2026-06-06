<template>
  <div class="animate-fade-in max-w-2xl mx-auto">
    <div class="page-header">
      <h1 class="page-title">Мой профиль</h1>
    </div>

    <div class="card p-6 mb-6">
      <div class="flex items-center gap-5 mb-6">
        <div class="w-16 h-16 rounded-2xl bg-primary-600 flex items-center justify-center flex-shrink-0">
          <span class="text-white text-2xl font-bold">{{ initials }}</span>
        </div>
        <div>
          <h2 class="text-xl font-bold text-slate-900">{{ auth.userFullName }}</h2>
          <span :class="`role-${auth.user?.role}`">{{ auth.userRole }}</span>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <InfoField label="Логин" :value="auth.user?.username" mono />
        <InfoField label="Email" :value="auth.user?.email" />
        <InfoField label="Телефон" :value="auth.user?.phone || '—'" />
        <InfoField label="Последний вход" :value="formatDate(auth.user?.last_activity)" />
      </div>
    </div>

    <!-- Change password -->
    <div class="card p-6">
      <h3 class="text-sm font-semibold text-slate-700 mb-5 pb-3 border-b border-slate-100">Смена пароля</h3>
      <form @submit.prevent="changePassword" class="space-y-4 max-w-sm">
        <div>
          <label class="form-label">Текущий пароль</label>
          <input v-model="pwForm.old_password" type="password" class="form-input" required />
        </div>
        <div>
          <label class="form-label">Новый пароль</label>
          <input v-model="pwForm.new_password" type="password" class="form-input" required />
        </div>
        <div>
          <label class="form-label">Подтвердите пароль</label>
          <input v-model="pwForm.new_password_confirm" type="password" class="form-input" required />
        </div>
        <div v-if="pwError" class="text-sm text-red-600">{{ pwError }}</div>
        <button type="submit" :disabled="saving" class="btn-md btn-primary">
          {{ saving ? 'Сохранение...' : 'Сменить пароль' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '@/store/auth'
import { authApi } from '@/api'
import InfoField from '@/components/common/InfoField.vue'
import dayjs from 'dayjs'

const auth = useAuthStore()
const toast = useToast()
const saving = ref(false)
const pwError = ref('')

const pwForm = reactive({ old_password: '', new_password: '', new_password_confirm: '' })

const initials = computed(() => {
  const n = auth.userFullName
  if (!n) return '?'
  const parts = n.split(' ')
  return parts.length >= 2 ? (parts[0][0] + parts[1][0]).toUpperCase() : n[0].toUpperCase()
})

function formatDate(d) { return d ? dayjs(d).format('DD.MM.YYYY HH:mm') : '—' }

async function changePassword() {
  pwError.value = ''
  if (pwForm.new_password !== pwForm.new_password_confirm) {
    pwError.value = 'Пароли не совпадают'; return
  }
  saving.value = true
  try {
    await authApi.changePassword(pwForm)
    toast.success('Пароль успешно изменён')
    Object.assign(pwForm, { old_password: '', new_password: '', new_password_confirm: '' })
  } catch (e) {
    pwError.value = e.response?.data?.message || 'Ошибка при смене пароля'
  } finally { saving.value = false }
}
</script>
