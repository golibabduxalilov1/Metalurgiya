<template>
  <div class="animate-fade-in max-w-2xl mx-auto">
    <div class="page-header">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-indigo-100 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
        </div>
        <h1 class="page-title">{{ t('profile.title') }}</h1>
      </div>
    </div>

    <!-- Profile card -->
    <div class="card p-6 mb-5">
      <!-- Avatar + name -->
      <div class="flex items-center gap-5 mb-6 pb-6 border-b border-slate-100">
        <div class="relative flex-shrink-0">
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-500
            flex items-center justify-center shadow-md shadow-indigo-200/50">
            <span class="text-white text-2xl font-bold select-none">{{ initials }}</span>
          </div>
          <div class="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-emerald-400 border-2 border-white
            shadow-sm" title="Активен"></div>
        </div>
        <div>
          <h2 class="text-xl font-bold text-slate-900 leading-tight">{{ auth.userFullName }}</h2>
          <div class="mt-1.5">
            <span :class="`role-${auth.user?.role}`">{{ auth.userRole }}</span>
          </div>
        </div>
      </div>

      <!-- Info grid -->
      <div class="grid grid-cols-2 gap-3">
        <div class="bg-slate-50/70 rounded-xl p-3.5 border border-slate-100">
          <dt class="text-xs font-medium text-slate-400 uppercase tracking-wide mb-1">{{ t('profile.login_label') }}</dt>
          <dd class="text-sm font-semibold text-slate-800 font-mono">{{ auth.user?.username || '—' }}</dd>
        </div>
        <div class="bg-slate-50/70 rounded-xl p-3.5 border border-slate-100">
          <dt class="text-xs font-medium text-slate-400 uppercase tracking-wide mb-1">{{ t('common.email') }}</dt>
          <dd class="text-sm font-medium text-slate-700 truncate">{{ auth.user?.email || '—' }}</dd>
        </div>
        <div class="bg-slate-50/70 rounded-xl p-3.5 border border-slate-100">
          <dt class="text-xs font-medium text-slate-400 uppercase tracking-wide mb-1">{{ t('common.phone') }}</dt>
          <dd class="text-sm font-medium text-slate-700">{{ auth.user?.phone || '—' }}</dd>
        </div>
        <div class="bg-slate-50/70 rounded-xl p-3.5 border border-slate-100">
          <dt class="text-xs font-medium text-slate-400 uppercase tracking-wide mb-1">{{ t('profile.last_login') }}</dt>
          <dd class="text-sm font-medium text-slate-700 tabular-nums">{{ formatDate(auth.user?.last_activity) }}</dd>
        </div>
      </div>
    </div>

    <!-- Change password -->
    <div class="card p-6">
      <div class="flex items-center gap-3 mb-5 pb-4 border-b border-slate-100">
        <div class="w-7 h-7 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
          <svg class="w-3.5 h-3.5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
        </div>
        <h3 class="text-sm font-semibold text-slate-700">{{ t('profile.change_password') }}</h3>
      </div>

      <form @submit.prevent="changePassword" class="space-y-4 max-w-sm">
        <div>
          <label class="form-label">{{ t('profile.current_password') }}</label>
          <input v-model="pwForm.old_password" type="password" class="form-input"
            placeholder="••••••••" required />
        </div>
        <div>
          <label class="form-label">{{ t('profile.new_password') }}</label>
          <input v-model="pwForm.new_password" type="password" class="form-input"
            placeholder="••••••••" required />
        </div>
        <div>
          <label class="form-label">{{ t('profile.confirm_password') }}</label>
          <input v-model="pwForm.new_password_confirm" type="password"
            :class="['form-input', pwError ? 'border-rose-400 focus:ring-rose-300' : '']"
            placeholder="••••••••" required />
        </div>

        <div v-if="pwError" class="form-error">
          <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.834-2.694-.834-3.464 0L3.34 16.5C2.57 18.333 3.532 20 5.072 20z"/>
          </svg>
          {{ pwError }}
        </div>

        <button type="submit" :disabled="saving"
          class="btn-md btn-primary inline-flex items-center gap-2">
          <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
          </svg>
          <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
          {{ saving ? t('common.saving') : t('profile.save_password_btn') }}
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
import { useI18n } from '@/i18n'

const auth = useAuthStore()
const toast = useToast()
const { t } = useI18n()
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
    pwError.value = t('profile.passwords_mismatch'); return
  }
  saving.value = true
  try {
    await authApi.changePassword(pwForm)
    toast.success(t('toast.password_changed'))
    Object.assign(pwForm, { old_password: '', new_password: '', new_password_confirm: '' })
  } catch (e) {
    pwError.value = e.response?.data?.message || t('toast.password_error')
  } finally { saving.value = false }
}
</script>
