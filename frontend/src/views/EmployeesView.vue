<template>
  <div class="animate-fade-in">
    <div class="page-header">
      <div>
        <h1 class="page-title">Сотрудники</h1>
        <p class="page-subtitle">Справочник операторов и персонала</p>
      </div>
      <button v-if="auth.isAdmin" @click="openCreate" class="btn-md btn-primary">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        Добавить сотрудника
      </button>
    </div>

    <div class="card p-4 mb-5 flex flex-wrap items-center gap-3">
      <input v-model="search" @input="debouncedLoad" type="text"
        placeholder="Поиск по ФИО, должности..." class="form-input h-9 flex-1 min-w-[200px]" />
      <select v-model="workshopFilter" @change="loadEmployees" class="form-select h-9 w-44">
        <option value="">Все цеха</option>
        <option v-for="w in workshops" :key="w.id" :value="w.id">{{ w.name }}</option>
      </select>
    </div>

    <div class="card overflow-hidden">
      <div v-if="loading" class="p-8 space-y-3">
        <div v-for="i in 6" :key="i" class="skeleton h-14 rounded-lg"></div>
      </div>
      <div v-else-if="employees.length === 0" class="empty-state">
        <div class="empty-state-title">Сотрудники не найдены</div>
      </div>
      <div v-else class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ФИО</th>
              <th>Должность</th>
              <th>Цех</th>
              <th>Контакты</th>
              <th>Станков</th>
              <th v-if="auth.isAdmin" class="text-right">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="emp in employees" :key="emp.id" :class="!emp.is_active ? 'opacity-60' : ''">
              <td>
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0">
                    <span class="text-emerald-700 text-xs font-bold">{{ emp.full_name[0] }}</span>
                  </div>
                  <div>
                    <div class="font-medium text-slate-900">{{ emp.full_name }}</div>
                    <div v-if="!emp.is_active" class="text-xs text-red-500">Неактивен</div>
                  </div>
                </div>
              </td>
              <td class="text-sm text-slate-600">{{ emp.position || '—' }}</td>
              <td class="text-sm text-slate-600">{{ emp.workshop_name || '—' }}</td>
              <td>
                <div class="text-sm text-slate-600">{{ emp.phone || '' }}</div>
                <div class="text-xs text-slate-400">{{ emp.email || '' }}</div>
              </td>
              <td>
                <span class="text-sm font-medium text-primary-700">{{ emp.assigned_machines_count }}</span>
              </td>
              <td v-if="auth.isAdmin">
                <div class="flex items-center justify-end gap-1">
                  <button @click="openEdit(emp)" class="p-1.5 rounded-lg text-slate-400 hover:text-amber-600 hover:bg-amber-50 transition-colors">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-backdrop" @click.self="showModal = false">
      <div class="modal-box max-w-lg">
        <div class="modal-header">
          <h3 class="text-lg font-semibold">{{ editEmp ? 'Редактировать сотрудника' : 'Новый сотрудник' }}</h3>
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
          <div><label class="form-label">Отчество</label><input v-model="form.patronymic" type="text" class="form-input" /></div>
          <div><label class="form-label">Должность</label><input v-model="form.position" type="text" class="form-input" /></div>
          <div>
            <label class="form-label">Цех</label>
            <select v-model="form.workshop" class="form-select">
              <option value="">— не выбрано —</option>
              <option v-for="w in workshops" :key="w.id" :value="w.id">{{ w.name }}</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div><label class="form-label">Телефон</label><input v-model="form.phone" type="tel" class="form-input" /></div>
            <div><label class="form-label">Email</label><input v-model="form.email" type="email" class="form-input" /></div>
          </div>
          <div><label class="form-label">Примечания</label><textarea v-model="form.notes" class="form-textarea" rows="2"></textarea></div>
          <label class="flex items-center gap-2 text-sm cursor-pointer">
            <input type="checkbox" v-model="form.is_active" class="rounded border-slate-300 text-primary-600"/>
            <span class="text-slate-700">Активный сотрудник</span>
          </label>
        </div>
        <div class="modal-footer">
          <button @click="showModal = false" class="btn-md btn-secondary">Отмена</button>
          <button @click="handleSave" :disabled="saving" class="btn-md btn-primary">{{ saving ? 'Сохранение...' : 'Сохранить' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '@/store/auth'
import { employeesApi, workshopsApi } from '@/api'
import { useDebounceFn } from '@vueuse/core'

const auth = useAuthStore()
const toast = useToast()
const employees = ref([])
const workshops = ref([])
const loading = ref(true)
const search = ref('')
const workshopFilter = ref('')
const showModal = ref(false)
const editEmp = ref(null)
const saving = ref(false)
const form = reactive({ last_name: '', first_name: '', patronymic: '', position: '', workshop: '', phone: '', email: '', notes: '', is_active: true })

const debouncedLoad = useDebounceFn(loadEmployees, 400)

async function loadEmployees() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (workshopFilter.value) params.workshop = workshopFilter.value
    const res = await employeesApi.list(params)
    employees.value = res.data.results || res.data
  } catch { toast.error('Ошибка загрузки') }
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
async function handleSave() {
  saving.value = true
  try {
    if (editEmp.value) { await employeesApi.update(editEmp.value.id, form); toast.success('Обновлено') }
    else { await employeesApi.create(form); toast.success('Создан') }
    showModal.value = false
    loadEmployees()
  } catch (e) { toast.error(e.response?.data?.message || 'Ошибка') }
  finally { saving.value = false }
}

onMounted(async () => {
  const wRes = await workshopsApi.list({ page_size: 100 })
  workshops.value = wRes.data.results || wRes.data
  loadEmployees()
})
</script>
