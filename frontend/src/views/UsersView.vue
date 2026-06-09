<template>
  <div class="animate-fade-in space-y-5">

    <!-- Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">{{ t('users.title') }}</h1>
        <p class="page-subtitle">{{ t('users.subtitle') }}</p>
      </div>
      <button @click="openCreate"
        class="btn-md btn-primary shadow-lg shadow-indigo-500/25
               hover:shadow-indigo-500/40 hover:-translate-y-px transition-all duration-200">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        {{ t('users.add_btn') }}
      </button>
    </div>

    <!-- Filters -->
    <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
      <div class="flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:items-center sm:gap-3">
        <div class="relative w-full sm:flex-1">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none"
            fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input v-model="search" @input="debouncedLoad" type="text"
            :placeholder="t('users.search_ph')"
            class="form-input pl-9 h-9 text-sm bg-slate-50 hover:border-slate-300
                   focus:bg-white transition-all duration-200" />
        </div>
        <div class="relative w-full sm:w-auto">
          <select v-model="roleFilter" @change="loadUsers"
            class="form-input h-9 w-full sm:w-44 text-sm bg-slate-50 border-slate-200 pl-3 pr-8
                   hover:border-slate-300 appearance-none cursor-pointer rounded-lg
                   transition-colors duration-150">
            <option value="">{{ t('users.all_roles') }}</option>
            <option value="admin">{{ t('users.role_admin') }}</option>
            <option value="master">{{ t('users.role_master') }}</option>
            <option value="operator">{{ t('users.role_operator') }}</option>
          </select>
          <svg class="absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5
                      text-slate-400 pointer-events-none"
            fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
          </svg>
        </div>
        <label class="flex items-center gap-2 text-sm text-slate-600 cursor-pointer select-none
                      px-3 py-1.5 rounded-lg hover:bg-slate-50 transition-colors duration-150">
          <input type="checkbox" v-model="showInactive" @change="loadUsers"
            class="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500/30"/>
          {{ t('users.show_inactive') }}
        </label>
      </div>
    </div>

    <!-- Table card -->
    <div class="bg-white border border-slate-200 rounded-xl shadow-sm">

      <!-- Loading -->
      <div v-if="loading" class="p-6 space-y-2.5">
        <div v-for="i in 6" :key="i" class="skeleton h-14 rounded-lg"
          :style="{ animationDelay: `${(i - 1) * 50}ms` }"></div>
      </div>

      <!-- Empty -->
      <div v-else-if="users.length === 0"
        class="flex flex-col items-center justify-center py-20 text-center">
        <div class="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
        </div>
        <div class="text-lg font-semibold text-slate-700 mb-1">{{ t('users.not_found') }}</div>
        <div class="text-sm text-slate-400">{{ t('users.not_found_hint') }}</div>
      </div>

      <template v-else>
      <!-- Mobile cards -->
      <div class="sm:hidden divide-y divide-slate-100">
        <div v-for="user in users" :key="user.id"
          :class="['px-4 py-3.5', !user.is_active ? 'opacity-55' : '']">
          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-3 min-w-0">
              <div class="user-avatar flex-shrink-0">
                <span class="text-indigo-700 text-xs font-bold">{{ (user.first_name || user.username || '?')[0].toUpperCase() }}</span>
              </div>
              <div class="min-w-0">
                <div class="font-semibold text-slate-900 text-sm truncate">{{ user.first_name || user.username }}</div>
                <div class="font-mono text-xs text-slate-500 truncate">{{ user.username }}</div>
              </div>
            </div>
            <div class="flex items-center gap-2 flex-shrink-0">
              <span :class="`role-${user.role}`">{{ user.role_display }}</span>
              <span :class="user.is_active ? 'w-2 h-2 rounded-full bg-emerald-400' : 'w-2 h-2 rounded-full bg-slate-300'"></span>
            </div>
          </div>
          <div class="mt-2 ml-11 flex items-center justify-between gap-2">
            <div class="text-xs text-slate-400">{{ user.last_activity ? formatDate(user.last_activity) : '—' }}</div>
            <div class="flex items-center gap-1">
              <template v-if="canManage(user)">
                <button @click="openEdit(user)" class="action-btn hover:text-amber-600 hover:bg-amber-50">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                  </svg>
                </button>
                <button @click="openResetPassword(user)" class="action-btn hover:text-indigo-600 hover:bg-indigo-50">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                  </svg>
                </button>
                <button v-if="user.is_active && canDeactivate(user)" @click="confirmDeactivate(user)" class="action-btn hover:text-rose-600 hover:bg-rose-50">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                  </svg>
                </button>
                <button v-else @click="handleActivate(user)" class="action-btn hover:text-emerald-600 hover:bg-emerald-50">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </button>
              </template>
              <span v-else class="text-xs text-slate-300">—</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Desktop table (sm+) -->
      <div class="hidden sm:block overflow-x-auto">
        <table class="w-full text-sm min-w-[650px]">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50/80">
              <th class="th-col">{{ t('users.col_user') }}</th>
              <th class="th-col">{{ t('users.col_login') }}</th>
              <th class="th-col">{{ t('users.col_role') }}</th>
              <th class="th-col">{{ t('users.col_last_activity') }}</th>
              <th class="th-col">{{ t('users.col_status') }}</th>
              <th class="th-col text-right">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100/80">
            <tr v-for="user in users" :key="user.id"
              :class="['user-row', !user.is_active ? 'opacity-55' : '']">

              <td class="td-col">
                <div class="flex items-center gap-3">
                  <div class="user-avatar flex-shrink-0">
                    <span class="text-indigo-700 text-xs font-bold">{{ (user.first_name || user.username || '?')[0].toUpperCase() }}</span>
                  </div>
                  <span class="font-semibold text-slate-900">{{ user.first_name || user.username }}</span>
                </div>
              </td>

              <td class="td-col">
                <div class="font-mono text-sm text-slate-800 font-medium tracking-tight">
                  {{ user.username }}
                </div>
                <div class="text-xs text-slate-400 mt-0.5">{{ user.email }}</div>
              </td>

              <td class="td-col">
                <span :class="`role-${user.role}`">{{ user.role_display }}</span>
              </td>

              <td class="td-col text-xs text-slate-400 tabular-nums">
                {{ user.last_activity ? formatDate(user.last_activity) : '—' }}
              </td>

              <td class="td-col">
                <span :class="user.is_active
                  ? 'status-badge status-green'
                  : 'status-badge status-gray'">
                  <span :class="user.is_active
                    ? 'status-dot status-dot-green'
                    : 'status-dot status-dot-gray'"></span>
                  {{ user.is_active ? t('users.active') : t('users.inactive') }}
                </span>
              </td>

              <td class="td-col">
                <div class="flex items-center justify-end gap-1">
                  <template v-if="canManage(user)">
                    <button @click="openEdit(user)"
                      class="action-btn hover:text-amber-600 hover:bg-amber-50"
                      :title="t('common.edit')">
                      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                      </svg>
                    </button>
                    <button @click="openResetPassword(user)"
                      class="action-btn hover:text-indigo-600 hover:bg-indigo-50"
                      :title="t('users.reset_title')">
                      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                      </svg>
                    </button>
                    <button v-if="user.is_active && canDeactivate(user)" @click="confirmDeactivate(user)"
                      class="action-btn hover:text-rose-600 hover:bg-rose-50"
                      :title="t('users.deactivate_btn')">
                      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                      </svg>
                    </button>
                    <button v-else @click="handleActivate(user)"
                      class="action-btn hover:text-emerald-600 hover:bg-emerald-50">
                      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                    </button>
                  </template>
                  <span v-else class="text-xs text-slate-300">—</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      </template>
    </div>

    <!-- Create/Edit Modal -->
    <Transition name="modal-fade">
      <div v-if="showModal"
        class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50
               flex items-center justify-center p-4"
        @click.self="showModal = false">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg
                    flex flex-col max-h-[90vh] overflow-hidden modal-enter">

          <div class="flex items-center gap-3 px-6 py-5 border-b border-slate-100">
            <div class="w-9 h-9 rounded-xl bg-indigo-50 flex items-center justify-center flex-shrink-0">
              <svg class="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
            </div>
            <h3 class="text-base font-semibold text-slate-900 flex-1">
              {{ editUser ? t('users.modal_edit') : t('users.modal_new') }}
            </h3>
            <button @click="showModal = false"
              class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600
                     hover:bg-slate-100 transition-colors cursor-pointer">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <div class="flex-1 overflow-y-auto px-4 sm:px-6 py-5 space-y-4">
            <div class="grid grid-cols-1 min-[480px]:grid-cols-2 gap-4">
              <div>
                <label class="form-label">{{ t('users.form_last') }} <span class="text-rose-500">*</span></label>
                <input v-model="form.last_name" type="text" class="form-input" placeholder="Иванов"/>
              </div>
              <div>
                <label class="form-label">{{ t('users.form_first') }} <span class="text-rose-500">*</span></label>
                <input v-model="form.first_name" type="text" class="form-input" placeholder="Иван"/>
              </div>
            </div>
            <div>
              <label class="form-label">{{ t('users.form_patron') }}</label>
              <input v-model="form.patronymic" type="text" class="form-input" placeholder="Иванович"/>
            </div>
            <div>
              <label class="form-label">
                {{ t('users.form_login') }} <span class="text-rose-500">*</span>
                <span v-if="!!editUser" class="text-xs font-normal text-slate-400 ml-1">{{ t('users.form_login_readonly') }}</span>
              </label>
              <input v-model="form.username" type="text"
                :class="['form-input font-mono tracking-wide',
                         !!editUser ? 'bg-slate-50 text-slate-400 cursor-not-allowed' : '']"
                :disabled="!!editUser" placeholder="ivan_operator"/>
            </div>
            <div>
              <label class="form-label">{{ t('common.email') }} <span class="text-rose-500">*</span></label>
              <input v-model="form.email" type="email" class="form-input" placeholder="ivan@example.com"/>
            </div>
            <div>
              <label class="form-label">{{ t('users.form_role') }} <span class="text-rose-500">*</span></label>
              <div class="relative">
                <select v-model="form.role" class="form-select pr-8 appearance-none cursor-pointer">
                  <option value="admin">{{ t('users.role_admin') }}</option>
                  <option value="master">{{ t('users.role_master') }}</option>
                  <option value="operator">{{ t('users.role_operator') }}</option>
                </select>
                <svg class="absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5
                            text-slate-400 pointer-events-none"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
                </svg>
              </div>
            </div>
            <div>
              <label class="form-label">{{ t('common.phone') }}</label>
              <input v-model="form.phone" type="tel" class="form-input" placeholder="+998 90 000 00 00"/>
            </div>
            <template v-if="!editUser">
              <div class="pt-1 border-t border-slate-100">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3">{{ t('users.form_password_section') }}</p>
                <div class="space-y-3">
                  <div>
                    <label class="form-label">{{ t('users.form_password') }} <span class="text-rose-500">*</span></label>
                    <input v-model="form.password" type="password" class="form-input"
                      :placeholder="t('users.form_password_ph')"/>
                  </div>
                  <div>
                    <label class="form-label">{{ t('users.form_confirm') }} <span class="text-rose-500">*</span></label>
                    <input v-model="form.password_confirm" type="password" class="form-input"
                      :placeholder="t('users.form_confirm_ph')"/>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <div class="flex items-center justify-end gap-3 px-6 py-4
                      border-t border-slate-100 bg-slate-50/60">
            <button @click="showModal = false" class="btn-md btn-secondary">{{ t('common.cancel') }}</button>
            <button @click="handleSave" :disabled="saving"
              class="btn-md btn-primary min-w-[120px] shadow-md shadow-indigo-500/20
                     hover:-translate-y-px transition-all duration-200
                     disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:translate-y-0">
              <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
              </svg>
              {{ saving ? t('common.saving') : t('common.save') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Reset password modal -->
    <Transition name="modal-fade">
      <div v-if="resetTarget"
        class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50
               flex items-center justify-center p-4"
        @click.self="resetTarget = null">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm
                    flex flex-col overflow-hidden modal-enter">

          <div class="flex items-center gap-3 px-6 py-5 border-b border-slate-100">
            <div class="w-9 h-9 rounded-xl bg-indigo-50 flex items-center justify-center flex-shrink-0">
              <svg class="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
              </svg>
            </div>
            <h3 class="text-base font-semibold text-slate-900 flex-1">{{ t('users.reset_title') }}</h3>
            <button @click="resetTarget = null"
              class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600
                     hover:bg-slate-100 transition-colors cursor-pointer">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <div class="px-6 py-5 space-y-4">
            <p class="text-sm text-slate-600">
              {{ t('users.reset_for') }}
              <span class="font-semibold text-slate-900">{{ resetTarget.first_name }}</span>
            </p>
            <div>
              <label class="form-label">{{ t('users.reset_new') }}</label>
              <input v-model="newPassword" type="password" class="form-input"
                :placeholder="t('users.form_password_ph')"/>
            </div>
          </div>

          <div class="flex items-center justify-end gap-3 px-6 py-4
                      border-t border-slate-100 bg-slate-50/60">
            <button @click="resetTarget = null" class="btn-md btn-secondary">{{ t('common.cancel') }}</button>
            <button @click="doResetPassword" :disabled="saving"
              class="btn-md btn-primary shadow-md shadow-indigo-500/20
                     hover:-translate-y-px transition-all duration-200
                     disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:translate-y-0">
              <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              {{ t('users.reset_btn') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <ConfirmModal v-if="deactivateTarget"
      :title="t('users.deactivate_title')"
      :message="`${t('users.role_operator')} «${deactivateTarget.first_name}» ${t('users.deactivate_msg_suffix')}`"
      :confirm-label="t('users.deactivate_btn')"
      confirm-class="btn-danger"
      @confirm="doDeactivate"
      @cancel="deactivateTarget = null" />

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { usersApi } from '@/api'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import { useDebounceFn } from '@vueuse/core'
import dayjs from 'dayjs'
import { useAuthStore } from '@/store/auth'
import { useI18n } from '@/i18n'

const authStore = useAuthStore()
const toast = useToast()
const { t } = useI18n()

const users = ref([])
const loading = ref(true)
const search = ref('')
const roleFilter = ref('')
const showInactive = ref(false)
const showModal = ref(false)
const editUser = ref(null)
const saving = ref(false)
const resetTarget = ref(null)
const newPassword = ref('')
const deactivateTarget = ref(null)

const form = reactive({
  username: '', email: '', first_name: '', last_name: '', patronymic: '',
  role: 'operator', phone: '', password: '', password_confirm: ''
})

const debouncedLoad = useDebounceFn(loadUsers, 400)

function formatDate(d) { return dayjs(d).format('DD.MM.YYYY HH:mm') }

async function loadUsers() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (roleFilter.value) params.role = roleFilter.value
    if (!showInactive.value) params.is_active = true
    const res = await usersApi.list(params)
    users.value = res.data.results || res.data
  } catch { toast.error(t('toast.load_error')) }
  finally { loading.value = false }
}

function openCreate() {
  editUser.value = null
  Object.assign(form, { username: '', email: '', first_name: '', last_name: '', patronymic: '', role: 'operator', phone: '', password: '', password_confirm: '' })
  showModal.value = true
}

function openEdit(user) {
  editUser.value = user
  Object.assign(form, { ...user, password: '', password_confirm: '' })
  showModal.value = true
}

async function handleSave() {
  saving.value = true
  try {
    if (editUser.value) {
      const { password, password_confirm, ...data } = form
      await usersApi.update(editUser.value.id, data)
      toast.success(t('toast.user_updated'))
    } else {
      await usersApi.create(form)
      toast.success(t('toast.user_created'))
    }
    showModal.value = false
    loadUsers()
  } catch (e) {
    toast.error(e.response?.data?.message || t('toast.error'))
  } finally { saving.value = false }
}

function canManage(user) {
  const me = authStore.user
  // Superadmin can manage anyone
  if (me?.is_superuser) return true
  // Nobody (except superadmin) can touch a superadmin account
  if (user.is_superuser) return false
  // Regular admin cannot manage another admin
  if (user.role === 'admin' && user.id !== me?.id) return false
  return true
}

function canDeactivate(user) {
  const me = authStore.user
  // Cannot deactivate yourself
  if (user.id === me?.id) return false
  // Superadmin can deactivate any admin
  if (me?.is_superuser) return true
  // Regular admin cannot deactivate another admin
  if (user.role === 'admin') return false
  return true
}

function openResetPassword(user) { resetTarget.value = user; newPassword.value = '' }

async function doResetPassword() {
  if (!newPassword.value) { toast.error(t('toast.enter_new_password')); return }
  saving.value = true
  try {
    await usersApi.resetPassword(resetTarget.value.id, { new_password: newPassword.value })
    toast.success(t('toast.password_reset'))
    resetTarget.value = null
  } catch { toast.error(t('toast.password_reset_error')) }
  finally { saving.value = false }
}

function confirmDeactivate(user) { deactivateTarget.value = user }
async function doDeactivate() {
  try {
    await usersApi.delete(deactivateTarget.value.id)
    toast.success(t('toast.user_deactivated'))
    deactivateTarget.value = null
    loadUsers()
  } catch { toast.error(t('toast.error')) }
}

async function handleActivate(user) {
  try {
    await usersApi.activate(user.id)
    toast.success(t('toast.user_activated'))
    loadUsers()
  } catch { toast.error(t('toast.error')) }
}

onMounted(loadUsers)
</script>

<style scoped>
.th-col {
  @apply px-4 py-3 text-left text-xs font-semibold text-slate-500
         uppercase tracking-wide whitespace-nowrap select-none;
}
.td-col {
  @apply px-4 py-3 align-middle;
}
.user-row {
  border-left: 2px solid transparent;
  transition: background-color 100ms ease, border-color 150ms ease;
}
.user-row:hover {
  background-color: rgba(99, 102, 241, 0.03);
  border-left-color: rgba(99, 102, 241, 0.3);
}
.user-avatar {
  @apply w-9 h-9 rounded-full bg-indigo-100 flex items-center justify-center;
}
.action-btn {
  @apply p-1.5 rounded-lg text-slate-400 transition-colors duration-150
         cursor-pointer inline-flex items-center justify-center;
}
.modal-enter {
  animation: modalSlideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes modalSlideUp {
  from { opacity: 0; transform: translateY(16px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
.modal-fade-enter-active,
.modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from,
.modal-fade-leave-to { opacity: 0; }
@media (prefers-reduced-motion: reduce) {
  .modal-enter, .user-row { animation: none; transition: none; }
}
</style>
