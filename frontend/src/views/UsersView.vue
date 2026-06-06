<template>
  <div class="animate-fade-in">
    <div class="page-header">
      <div>
        <h1 class="page-title">Пользователи</h1>
        <p class="page-subtitle">Управление учётными записями системы</p>
      </div>
      <button @click="openCreate" class="btn-md btn-primary">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        Добавить пользователя
      </button>
    </div>

    <!-- Filters -->
    <div class="card p-4 mb-5 flex flex-wrap items-center gap-3">
      <input v-model="search" @input="debouncedLoad" type="text"
        placeholder="Поиск по имени, логину..." class="form-input h-9 flex-1 min-w-[200px]" />
      <select v-model="roleFilter" @change="loadUsers" class="form-select h-9 w-40">
        <option value="">Все роли</option>
        <option value="admin">Администратор</option>
        <option value="master">Мастер</option>
        <option value="operator">Оператор</option>
      </select>
      <label class="flex items-center gap-2 text-sm text-slate-600 cursor-pointer">
        <input type="checkbox" v-model="showInactive" @change="loadUsers" class="rounded border-slate-300 text-primary-600"/>
        Показать неактивных
      </label>
    </div>

    <!-- Table -->
    <div class="card overflow-hidden">
      <div v-if="loading" class="p-8">
        <div class="space-y-3">
          <div v-for="i in 6" :key="i" class="skeleton h-14 rounded-lg"></div>
        </div>
      </div>
      <div v-else-if="users.length === 0" class="empty-state">
        <svg class="empty-state-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
        </svg>
        <div class="empty-state-title">Пользователи не найдены</div>
      </div>
      <div v-else class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Пользователь</th>
              <th>Логин / Email</th>
              <th>Роль</th>
              <th>Последняя активность</th>
              <th>Статус</th>
              <th class="text-right">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id" :class="!user.is_active ? 'opacity-60' : ''">
              <td>
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0">
                    <span class="text-primary-700 text-xs font-bold">{{ user.full_name[0] }}</span>
                  </div>
                  <span class="font-medium text-slate-900">{{ user.full_name }}</span>
                </div>
              </td>
              <td>
                <div class="text-sm text-slate-700 font-mono">{{ user.username }}</div>
                <div class="text-xs text-slate-400">{{ user.email }}</div>
              </td>
              <td>
                <span :class="`role-${user.role}`">{{ user.role_display }}</span>
              </td>
              <td class="text-xs text-slate-400">
                {{ user.last_activity ? formatDate(user.last_activity) : 'Нет' }}
              </td>
              <td>
                <span :class="user.is_active ? 'status-badge status-green' : 'status-badge status-gray'">
                  {{ user.is_active ? 'Активен' : 'Неактивен' }}
                </span>
              </td>
              <td>
                <div class="flex items-center justify-end gap-1">
                  <button @click="openEdit(user)" class="p-1.5 rounded-lg text-slate-400 hover:text-amber-600 hover:bg-amber-50 transition-colors" title="Редактировать">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button @click="openResetPassword(user)" class="p-1.5 rounded-lg text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors" title="Сбросить пароль">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                    </svg>
                  </button>
                  <button v-if="user.is_active" @click="confirmDeactivate(user)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition-colors" title="Деактивировать">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                    </svg>
                  </button>
                  <button v-else @click="handleActivate(user)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 transition-colors" title="Активировать">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal-backdrop" @click.self="showModal = false">
      <div class="modal-box max-w-lg">
        <div class="modal-header">
          <h3 class="text-lg font-semibold">{{ editUser ? 'Редактировать пользователя' : 'Новый пользователь' }}</h3>
          <button @click="showModal = false" class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="modal-body space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="form-label">Фамилия *</label>
              <input v-model="form.last_name" type="text" class="form-input" />
            </div>
            <div>
              <label class="form-label">Имя *</label>
              <input v-model="form.first_name" type="text" class="form-input" />
            </div>
          </div>
          <div>
            <label class="form-label">Отчество</label>
            <input v-model="form.patronymic" type="text" class="form-input" />
          </div>
          <div>
            <label class="form-label">Логин *</label>
            <input v-model="form.username" type="text" class="form-input font-mono" :disabled="!!editUser" />
          </div>
          <div>
            <label class="form-label">Email *</label>
            <input v-model="form.email" type="email" class="form-input" />
          </div>
          <div>
            <label class="form-label">Роль *</label>
            <select v-model="form.role" class="form-select">
              <option value="admin">Администратор</option>
              <option value="master">Мастер</option>
              <option value="operator">Оператор</option>
            </select>
          </div>
          <div>
            <label class="form-label">Телефон</label>
            <input v-model="form.phone" type="tel" class="form-input" />
          </div>
          <template v-if="!editUser">
            <div>
              <label class="form-label">Пароль *</label>
              <input v-model="form.password" type="password" class="form-input" />
            </div>
            <div>
              <label class="form-label">Подтвердите пароль *</label>
              <input v-model="form.password_confirm" type="password" class="form-input" />
            </div>
          </template>
        </div>
        <div class="modal-footer">
          <button @click="showModal = false" class="btn-md btn-secondary">Отмена</button>
          <button @click="handleSave" :disabled="saving" class="btn-md btn-primary">
            {{ saving ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Reset password modal -->
    <div v-if="resetTarget" class="modal-backdrop" @click.self="resetTarget = null">
      <div class="modal-box max-w-sm">
        <div class="modal-header">
          <h3 class="text-lg font-semibold">Сброс пароля</h3>
          <button @click="resetTarget = null" class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="modal-body space-y-3">
          <p class="text-slate-600 text-sm">Установите новый пароль для <strong>{{ resetTarget.full_name }}</strong></p>
          <div>
            <label class="form-label">Новый пароль</label>
            <input v-model="newPassword" type="password" class="form-input" placeholder="Минимум 8 символов" />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="resetTarget = null" class="btn-md btn-secondary">Отмена</button>
          <button @click="doResetPassword" :disabled="saving" class="btn-md btn-primary">Установить пароль</button>
        </div>
      </div>
    </div>

    <ConfirmModal v-if="deactivateTarget"
      title="Деактивировать пользователя?"
      :message="`Пользователь «${deactivateTarget.full_name}» потеряет доступ к системе.`"
      confirm-label="Деактивировать"
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

const toast = useToast()
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
  } catch { toast.error('Ошибка загрузки') }
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
      toast.success('Пользователь обновлён')
    } else {
      await usersApi.create(form)
      toast.success('Пользователь создан')
    }
    showModal.value = false
    loadUsers()
  } catch (e) {
    toast.error(e.response?.data?.message || 'Ошибка сохранения')
  } finally { saving.value = false }
}

function openResetPassword(user) { resetTarget.value = user; newPassword.value = '' }

async function doResetPassword() {
  if (!newPassword.value) { toast.error('Введите новый пароль'); return }
  saving.value = true
  try {
    await usersApi.resetPassword(resetTarget.value.id, { new_password: newPassword.value })
    toast.success('Пароль сброшен')
    resetTarget.value = null
  } catch { toast.error('Ошибка при сбросе пароля') }
  finally { saving.value = false }
}

function confirmDeactivate(user) { deactivateTarget.value = user }
async function doDeactivate() {
  try {
    await usersApi.delete(deactivateTarget.value.id)
    toast.success('Пользователь деактивирован')
    deactivateTarget.value = null
    loadUsers()
  } catch { toast.error('Ошибка') }
}

async function handleActivate(user) {
  try {
    await usersApi.activate(user.id)
    toast.success('Пользователь активирован')
    loadUsers()
  } catch { toast.error('Ошибка') }
}

onMounted(loadUsers)
</script>
