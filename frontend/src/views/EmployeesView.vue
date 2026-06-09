<template>
  <div class="animate-fade-in space-y-5">

    <!-- Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">{{ t('employees.title') }}</h1>
        <p class="page-subtitle">{{ t('employees.subtitle') }}</p>
      </div>
      <button v-if="auth.isAdmin" @click="openCreate"
        class="btn-md btn-primary shadow-lg shadow-indigo-500/25
               hover:shadow-indigo-500/40 hover:-translate-y-px transition-all duration-200">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        {{ t('employees.add_btn') }}
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
            :placeholder="t('employees.search_ph')"
            class="form-input pl-9 h-9 text-sm bg-slate-50 hover:border-slate-300
                   focus:bg-white transition-all duration-200" />
        </div>
        <div class="relative w-full sm:w-auto">
          <select v-model="workshopFilter" @change="loadEmployees"
            class="form-input h-9 w-full sm:w-44 text-sm bg-slate-50 border-slate-200 pl-3 pr-8
                   hover:border-slate-300 transition-colors duration-150
                   appearance-none cursor-pointer rounded-lg">
            <option value="">{{ t('employees.all_workshops') }}</option>
            <option v-for="w in workshops" :key="w.id" :value="w.id">{{ w.name }}</option>
          </select>
          <svg class="absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5
                      text-slate-400 pointer-events-none"
            fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
          </svg>
        </div>
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
      <div v-else-if="employees.length === 0"
        class="flex flex-col items-center justify-center py-20 text-center">
        <div class="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
        </div>
        <div class="text-lg font-semibold text-slate-700 mb-1">{{ t('employees.not_found') }}</div>
        <div class="text-sm text-slate-400">{{ t('employees.not_found_hint') }}</div>
      </div>

      <template v-else>
      <!-- Mobile cards -->
      <div class="sm:hidden divide-y divide-slate-100">
        <div v-for="emp in employees" :key="emp.id"
          :class="['px-4 py-3.5', !emp.is_active ? 'opacity-55' : '']">
          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-3 min-w-0">
              <div class="emp-avatar flex-shrink-0">
                <span class="text-indigo-700 text-xs font-bold">{{ (emp.first_name || '?')[0].toUpperCase() }}</span>
              </div>
              <div class="min-w-0">
                <div class="font-semibold text-slate-900 text-sm truncate">{{ emp.first_name }}</div>
                <div class="text-xs text-slate-500 truncate">{{ emp.position || '—' }}</div>
              </div>
            </div>
            <div class="flex items-center gap-2 flex-shrink-0">
              <span class="px-2 py-0.5 rounded-full bg-indigo-50 border border-indigo-100 text-xs font-bold text-indigo-700">
                {{ emp.assigned_machines_count }}
              </span>
              <button v-if="auth.isAdmin" @click="openEdit(emp)" class="action-btn hover:text-amber-600 hover:bg-amber-50">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
              </button>
              <button v-if="auth.isAdmin" @click="confirmDelete(emp)" class="action-btn hover:text-rose-600 hover:bg-rose-50">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7V4a1 1 0 011-1h4a1 1 0 011 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>
          <div class="mt-1.5 ml-11 grid grid-cols-2 gap-x-4 gap-y-0.5 text-xs text-slate-500">
            <div><span class="text-slate-400">{{ t('employees.workshop_prefix') }}</span>{{ emp.workshop_name || '—' }}</div>
            <div v-if="emp.phone"><span class="text-slate-400">{{ t('employees.phone_prefix') }}</span>{{ emp.phone }}</div>
            <div v-if="emp.email" class="col-span-2 truncate text-slate-400">{{ emp.email }}</div>
          </div>
        </div>
      </div>

      <!-- Desktop table (sm+) -->
      <div class="hidden sm:block overflow-x-auto">
        <table class="w-full text-sm min-w-[600px]">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50/80">
              <th class="th-col">{{ t('employees.col_name') }}</th>
              <th class="th-col">{{ t('employees.col_position') }}</th>
              <th class="th-col">{{ t('employees.col_workshop') }}</th>
              <th class="th-col">{{ t('employees.col_contacts') }}</th>
              <th class="th-col text-center">{{ t('employees.col_machines') }}</th>
              <th v-if="auth.isAdmin" class="th-col text-right">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100/80">
            <tr v-for="emp in employees" :key="emp.id"
              :class="['emp-row', !emp.is_active ? 'opacity-55' : '']">

              <!-- Name + avatar -->
              <td class="td-col">
                <div class="flex items-center gap-3">
                  <div class="emp-avatar flex-shrink-0">
                    <span class="text-indigo-700 text-xs font-bold">{{ (emp.first_name || '?')[0].toUpperCase() }}</span>
                  </div>
                  <div>
                    <div class="font-semibold text-slate-900 leading-snug">{{ emp.first_name }}</div>
                    <div v-if="!emp.is_active"
                      class="inline-flex items-center gap-1 text-xs text-rose-500 font-medium mt-0.5">
                      <span class="w-1.5 h-1.5 rounded-full bg-rose-400 inline-block"></span>
                      {{ t('employees.inactive') }}
                    </div>
                  </div>
                </div>
              </td>

              <td class="td-col text-slate-600">{{ emp.position || '—' }}</td>
              <td class="td-col text-slate-600">{{ emp.workshop_name || '—' }}</td>

              <td class="td-col">
                <div v-if="emp.phone" class="text-sm text-slate-700 font-medium">{{ emp.phone }}</div>
                <div v-if="emp.email" class="text-xs text-slate-400 mt-0.5">{{ emp.email }}</div>
                <div v-if="!emp.phone && !emp.email" class="text-xs text-slate-300 italic">—</div>
              </td>

              <td class="td-col text-center">
                <span class="inline-flex items-center justify-center min-w-[1.75rem] px-2 py-0.5
                             rounded-full bg-indigo-50 border border-indigo-100
                             text-xs font-bold text-indigo-700 tabular-nums">
                  {{ emp.assigned_machines_count }}
                </span>
              </td>

              <td v-if="auth.isAdmin" class="td-col">
                <div class="flex items-center justify-end gap-1">
                  <button @click="openEdit(emp)"
                    class="action-btn hover:text-amber-600 hover:bg-amber-50"
                    :title="t('common.edit')">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button @click="confirmDelete(emp)"
                    class="action-btn hover:text-rose-600 hover:bg-rose-50"
                    :title="t('common.delete')">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7V4a1 1 0 011-1h4a1 1 0 011 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      </template>
    </div>

    <!-- Modal -->
    <Transition name="modal-fade">
      <div v-if="showModal"
        class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50
               flex items-center justify-center p-4"
        @click.self="showModal = false">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg
                    flex flex-col max-h-[90vh] overflow-hidden modal-enter">

          <!-- Modal header -->
          <div class="flex items-center gap-3 px-6 py-5 border-b border-slate-100">
            <div class="w-9 h-9 rounded-xl bg-indigo-50 flex items-center justify-center flex-shrink-0">
              <svg class="w-4.5 h-4.5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
            </div>
            <h3 class="text-base font-semibold text-slate-900 flex-1">
              {{ editEmp ? t('employees.modal_edit') : t('employees.modal_new') }}
            </h3>
            <button @click="showModal = false"
              class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600
                     hover:bg-slate-100 transition-colors cursor-pointer">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- Modal body -->
          <div class="flex-1 overflow-y-auto px-4 sm:px-6 py-5 space-y-4">
            <div class="grid grid-cols-1 min-[480px]:grid-cols-2 gap-4">
              <div>
                <label class="form-label">{{ t('employees.form_last') }} <span class="text-rose-500">*</span></label>
                <input v-model="form.last_name" type="text" class="form-input"
                  :placeholder="t('employees.form_ph_last')" />
              </div>
              <div>
                <label class="form-label">{{ t('employees.form_first') }} <span class="text-rose-500">*</span></label>
                <input v-model="form.first_name" type="text" class="form-input"
                  :placeholder="t('employees.form_ph_first')" />
              </div>
            </div>
            <div>
              <label class="form-label">{{ t('employees.form_patron') }}</label>
              <input v-model="form.patronymic" type="text" class="form-input"
                :placeholder="t('employees.form_ph_patron')" />
            </div>
            <div>
              <label class="form-label">{{ t('employees.form_position') }}</label>
              <input v-model="form.position" type="text" class="form-input"
                :placeholder="t('employees.form_ph_position')" />
            </div>
            <div>
              <label class="form-label">{{ t('employees.form_workshop') }}</label>
              <div class="relative">
                <select v-model="form.workshop"
                  class="form-select pr-8 appearance-none cursor-pointer">
                  <option value="">{{ t('common.not_selected') }}</option>
                  <option v-for="w in workshops" :key="w.id" :value="w.id">{{ w.name }}</option>
                </select>
                <svg class="absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5
                            text-slate-400 pointer-events-none"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
                </svg>
              </div>
            </div>
            <div class="grid grid-cols-1 min-[480px]:grid-cols-2 gap-4">
              <div>
                <label class="form-label">{{ t('common.phone') }}</label>
                <input v-model="form.phone" type="tel" class="form-input"
                  placeholder="+998 90 000 00 00" />
              </div>
              <div>
                <label class="form-label">{{ t('common.email') }}</label>
                <input v-model="form.email" type="email" class="form-input"
                  placeholder="ivan@example.com" />
              </div>
            </div>
            <div>
              <label class="form-label">{{ t('common.notes') }}</label>
              <textarea v-model="form.notes" class="form-textarea" rows="2"
                :placeholder="t('employees.form_ph_notes')"></textarea>
            </div>
            <label class="flex items-center gap-2.5 text-sm cursor-pointer select-none
                          px-3 py-2.5 rounded-xl border border-slate-200 hover:bg-slate-50
                          transition-colors duration-150">
              <input type="checkbox" v-model="form.is_active"
                class="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500/30"/>
              <div>
                <div class="font-medium text-slate-700">{{ t('employees.form_active') }}</div>
                <div class="text-xs text-slate-400 mt-0.5">{{ t('employees.form_active_hint') }}</div>
              </div>
            </label>
          </div>

          <!-- Modal footer -->
          <div class="flex items-center justify-end gap-3 px-6 py-4
                      border-t border-slate-100 bg-slate-50/60">
            <button @click="showModal = false" class="btn-md btn-secondary">{{ t('common.cancel') }}</button>
            <button @click="handleSave" :disabled="saving || !canSave"
              class="btn-md btn-primary min-w-[120px] shadow-md shadow-indigo-500/20
                     hover:-translate-y-px transition-all duration-200
                     disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0">
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

    <!-- Delete confirm modal -->
    <ConfirmModal v-if="deleteTarget"
      :title="t('employees.delete_title')"
      :message="`${deleteTarget.full_name || deleteTarget.first_name} ${t('employees.delete_msg_suffix')}`"
      :confirm-label="t('employees.delete_confirm')"
      confirm-class="btn-danger"
      @confirm="doDelete"
      @cancel="deleteTarget = null" />

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '@/store/auth'
import { useI18n } from '@/i18n'
import { employeesApi, workshopsApi } from '@/api'
import { useDebounceFn } from '@vueuse/core'
import ConfirmModal from '@/components/common/ConfirmModal.vue'

const auth = useAuthStore()
const toast = useToast()
const { t } = useI18n()
const employees = ref([])
const workshops = ref([])
const loading = ref(true)
const search = ref('')
const workshopFilter = ref('')
const showModal = ref(false)
const editEmp = ref(null)
const deleteTarget = ref(null)
const saving = ref(false)
const form = reactive({ last_name: '', first_name: '', patronymic: '', position: '', workshop: '', phone: '', email: '', notes: '', is_active: true })

const canSave = computed(() => form.last_name.trim() !== '' && form.first_name.trim() !== '')

const debouncedLoad = useDebounceFn(loadEmployees, 400)

async function loadEmployees() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (workshopFilter.value) params.workshop = workshopFilter.value
    const res = await employeesApi.list(params)
    employees.value = res.data.results || res.data
  } catch { toast.error(t('toast.load_error')) }
  finally { loading.value = false }
}

function openCreate() {
  editEmp.value = null
  Object.assign(form, { last_name: '', first_name: '', patronymic: '', position: '', workshop: '', phone: '', email: '', notes: '', is_active: true })
  showModal.value = true
}
function openEdit(emp) {
  editEmp.value = emp
  Object.assign(form, emp)
  showModal.value = true
}
function confirmDelete(emp) { deleteTarget.value = emp }

async function doDelete() {
  try {
    await employeesApi.delete(deleteTarget.value.id)
    toast.success(t('toast.delete_success'))
    deleteTarget.value = null
    loadEmployees()
  } catch {
    toast.error(t('toast.delete_error'))
  }
}

async function handleSave() {
  saving.value = true
  try {
    if (editEmp.value) { await employeesApi.update(editEmp.value.id, form); toast.success(t('toast.update_success')) }
    else { await employeesApi.create(form); toast.success(t('toast.create_success')) }
    showModal.value = false
    loadEmployees()
  } catch (e) { toast.error(e.response?.data?.message || t('toast.error')) }
  finally { saving.value = false }
}

onMounted(async () => {
  const wRes = await workshopsApi.list({ page_size: 100 })
  workshops.value = wRes.data.results || wRes.data
  loadEmployees()
})
</script>

<style scoped>
.th-col {
  @apply px-4 py-3 text-left text-xs font-semibold text-slate-500
         uppercase tracking-wide whitespace-nowrap select-none;
}
.td-col {
  @apply px-4 py-3 align-middle text-slate-700;
}
.emp-row {
  border-left: 2px solid transparent;
  transition: background-color 100ms ease, border-color 150ms ease;
}
.emp-row:hover {
  background-color: rgba(99, 102, 241, 0.03);
  border-left-color: rgba(99, 102, 241, 0.3);
}
.emp-avatar {
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
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
@media (prefers-reduced-motion: reduce) {
  .modal-enter, .emp-row { animation: none; transition: none; }
}
</style>
