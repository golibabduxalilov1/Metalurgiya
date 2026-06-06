<template>
  <div class="animate-fade-in max-w-4xl mx-auto">
    <!-- Header -->
    <div class="flex items-center gap-4 mb-6">
      <button @click="$router.back()" class="p-2 rounded-lg text-slate-500 hover:bg-slate-200 transition-colors">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      <div>
        <h1 class="page-title">{{ isEdit ? 'Редактировать станок' : 'Добавить станок' }}</h1>
        <p class="page-subtitle">{{ isEdit ? `Инв. № ${route.params.id}` : 'Новая запись в реестре' }}</p>
      </div>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Main info -->
      <div class="card p-6">
        <h2 class="text-sm font-semibold text-slate-700 mb-5 pb-3 border-b border-slate-100">
          Основная информация
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="md:col-span-2">
            <label class="form-label">Наименование <span class="text-red-500">*</span></label>
            <input v-model="form.name" type="text" class="form-input" placeholder="Токарный станок 16К20" required />
            <div v-if="errors.name" class="form-error">{{ errors.name }}</div>
          </div>

          <div>
            <label class="form-label">Инвентарный номер <span class="text-red-500">*</span></label>
            <input v-model="form.inventory_number" type="text" class="form-input font-mono"
              placeholder="ИНВ-001" required />
            <div v-if="errors.inventory_number" class="form-error">{{ errors.inventory_number }}</div>
          </div>

          <div>
            <label class="form-label">Тип станка</label>
            <select v-model="form.machine_type" class="form-select">
              <option value="">— не выбрано —</option>
              <option v-for="t in types" :key="t.id" :value="t.id">{{ t.name }}</option>
            </select>
          </div>

          <div>
            <label class="form-label">Модель</label>
            <input v-model="form.model" type="text" class="form-input" placeholder="16К20" />
          </div>

          <div>
            <label class="form-label">Производитель</label>
            <input v-model="form.manufacturer" type="text" class="form-input" placeholder="Красный Пролетарий" />
          </div>

          <div>
            <label class="form-label">Год выпуска</label>
            <input v-model="form.year_manufactured" type="number" class="form-input"
              placeholder="2020" min="1900" :max="currentYear" />
          </div>

          <div>
            <label class="form-label">Дата ввода в эксплуатацию</label>
            <input v-model="form.commissioned_date" type="date" class="form-input" />
          </div>
        </div>

        <div class="mt-4">
          <label class="form-label">Описание / Комментарий</label>
          <textarea v-model="form.description" class="form-textarea" rows="3"
            placeholder="Дополнительная информация о станке..."></textarea>
        </div>
      </div>

      <!-- Location -->
      <div class="card p-6">
        <h2 class="text-sm font-semibold text-slate-700 mb-5 pb-3 border-b border-slate-100">
          Расположение
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="form-label">Цех</label>
            <select v-model="form.workshop" @change="onWorkshopChange" class="form-select">
              <option value="">— не выбрано —</option>
              <option v-for="w in workshops" :key="w.id" :value="w.id">{{ w.name }}</option>
            </select>
          </div>
          <div>
            <label class="form-label">Участок</label>
            <select v-model="form.section" class="form-select" :disabled="!form.workshop">
              <option value="">— не выбрано —</option>
              <option v-for="s in filteredSections" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div>
            <label class="form-label">Рабочее место</label>
            <input v-model="form.workplace" type="text" class="form-input" placeholder="РМ-5" />
          </div>
        </div>
      </div>

      <!-- Status & operator -->
      <div class="card p-6">
        <h2 class="text-sm font-semibold text-slate-700 mb-5 pb-3 border-b border-slate-100">
          Статус и оператор
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="form-label">Текущий статус</label>
            <select v-model="form.current_status" class="form-select">
              <option value="">— не задан —</option>
              <option v-for="s in statuses" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div>
            <label class="form-label">Оператор</label>
            <select v-model="form.assigned_operator" class="form-select">
              <option value="">— не назначен —</option>
              <option v-for="e in employees" :key="e.id" :value="e.id">{{ e.full_name }}</option>
            </select>
          </div>
          <div>
            <label class="form-label">Бригада (если нет конкретного оператора)</label>
            <input v-model="form.assigned_brigade" type="text" class="form-input" placeholder="Бригада №3" />
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-end gap-3">
        <button type="button" @click="$router.back()" class="btn-md btn-secondary">Отмена</button>
        <button type="submit" :disabled="saving" class="btn-md btn-primary">
          <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          {{ saving ? 'Сохранение...' : (isEdit ? 'Сохранить изменения' : 'Добавить станок') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { machinesApi, machineTypesApi, statusesApi, workshopsApi, employeesApi } from '@/api'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const isEdit = computed(() => !!route.params.id && route.name === 'MachineEdit')
const currentYear = new Date().getFullYear()
const saving = ref(false)
const errors = ref({})

const form = reactive({
  name: '', inventory_number: '', model: '', manufacturer: '',
  year_manufactured: '', commissioned_date: '', description: '',
  machine_type: '', current_status: '',
  workshop: '', section: '', workplace: '',
  assigned_operator: '', assigned_brigade: '',
})

const types = ref([])
const statuses = ref([])
const workshops = ref([])
const sections = ref([])
const employees = ref([])

const filteredSections = computed(() =>
  sections.value.filter(s => s.workshop === form.workshop || s.workshop === Number(form.workshop))
)

function onWorkshopChange() { form.section = '' }

async function loadOptions() {
  const [tRes, sRes, wRes, eRes] = await Promise.all([
    machineTypesApi.list({ page_size: 200 }),
    statusesApi.list(),
    workshopsApi.list({ page_size: 100 }),
    employeesApi.list({ page_size: 500, is_active: true }),
  ])
  types.value = tRes.data.results || tRes.data
  statuses.value = sRes.data.results || sRes.data
  workshops.value = wRes.data.results || wRes.data
  employees.value = eRes.data.results || eRes.data

  // Load all sections
  const allSections = []
  for (const w of workshops.value) {
    if (w.sections) allSections.push(...w.sections)
  }
  sections.value = allSections
}

async function loadMachine() {
  if (!isEdit.value) return
  try {
    const res = await machinesApi.get(route.params.id)
    const m = res.data
    Object.assign(form, {
      name: m.name || '',
      inventory_number: m.inventory_number || '',
      model: m.model || '',
      manufacturer: m.manufacturer || '',
      year_manufactured: m.year_manufactured || '',
      commissioned_date: m.commissioned_date || '',
      description: m.description || '',
      machine_type: m.machine_type || '',
      current_status: m.current_status || '',
      workshop: m.workshop || '',
      section: m.section || '',
      workplace: m.workplace || '',
      assigned_operator: m.assigned_operator || '',
      assigned_brigade: m.assigned_brigade || '',
    })
  } catch {
    toast.error('Ошибка загрузки данных')
    router.push('/machines')
  }
}

async function handleSubmit() {
  errors.value = {}
  saving.value = true

  const payload = { ...form }
  // Clean empty values
  Object.keys(payload).forEach(k => {
    if (payload[k] === '' || payload[k] === null) payload[k] = null
  })

  try {
    if (isEdit.value) {
      await machinesApi.update(route.params.id, payload)
      toast.success('Станок обновлён')
      router.push(`/machines/${route.params.id}`)
    } else {
      const res = await machinesApi.create(payload)
      toast.success('Станок добавлен')
      router.push(`/machines/${res.data.id}`)
    }
  } catch (e) {
    const data = e.response?.data
    if (data?.errors) {
      errors.value = data.errors
      toast.error('Проверьте заполнение формы')
    } else {
      toast.error(data?.message || 'Ошибка сохранения')
    }
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await loadOptions()
  await loadMachine()
})
</script>
