<template>
  <div class="animate-fade-in max-w-4xl mx-auto">

    <!-- Header -->
    <div class="flex items-center gap-4 mb-7">
      <button @click="$router.back()"
        class="p-2 rounded-xl text-slate-500 hover:text-slate-700 hover:bg-slate-100
               border border-transparent hover:border-slate-200
               transition-all duration-200 cursor-pointer flex-shrink-0">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      <div>
        <h1 class="page-title">{{ isEdit ? t('machines.form_title_edit') : t('machines.form_title_add') }}</h1>
        <p v-if="isEdit" class="page-subtitle flex items-center gap-1.5 mt-0.5">
          {{ t('machines.form_inv_prefix') }}
          <span class="font-mono text-xs font-semibold text-indigo-700
                       bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-md">
            {{ route.params.id }}
          </span>
        </p>
        <p v-else class="page-subtitle">{{ t('machines.form_new_record') }}</p>
      </div>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">

      <!-- Main info -->
      <div class="card p-6">
        <div class="section-header mb-5 pb-4 border-b border-slate-100">
          <div class="section-icon bg-indigo-50">
            <svg class="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          <h2 class="section-title">{{ t('machines.form_basic') }}</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div class="md:col-span-2">
            <label class="form-label">
              {{ t('machines.form_name') }} <span class="text-rose-500">*</span>
            </label>
            <input v-model="form.name" type="text"
              :class="['form-input', errors.name ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/20' : '']"
              :placeholder="t('machines.form_ph_name')" required />
            <div v-if="errors.name" class="form-error">
              <svg class="w-3 h-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              {{ errors.name }}
            </div>
          </div>

          <div>
            <label class="form-label">
              {{ t('machines.form_inv') }} <span class="text-rose-500">*</span>
            </label>
            <input v-model="form.inventory_number" type="text"
              :class="['form-input font-mono tracking-wide', errors.inventory_number ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/20' : '']"
              :placeholder="t('machines.form_ph_inv')" required />
            <div v-if="errors.inventory_number" class="form-error">
              <svg class="w-3 h-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              {{ errors.inventory_number }}
            </div>
          </div>

          <div>
            <label class="form-label">{{ t('machines.form_type') }}</label>
            <div class="relative">
              <select v-model="form.machine_type" class="form-select pr-8 appearance-none cursor-pointer">
                <option value="">{{ t('common.not_selected') }}</option>
                <option v-for="tp in types" :key="tp.id" :value="tp.id">{{ tp.name }}</option>
              </select>
              <svg class="select-chevron text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
              </svg>
            </div>
          </div>

          <div>
            <label class="form-label">{{ t('machines.form_model') }}</label>
            <input v-model="form.model" type="text" class="form-input" placeholder="16К20" />
          </div>

          <div>
            <label class="form-label">{{ t('machines.form_manufacturer') }}</label>
            <input v-model="form.manufacturer" type="text" class="form-input" />
          </div>

          <div>
            <label class="form-label">{{ t('machines.form_year') }}</label>
            <input v-model="form.year_manufactured" type="number" class="form-input"
              placeholder="2020" min="1900" :max="currentYear" />
          </div>

          <div>
            <label class="form-label">{{ t('machines.form_commissioned') }}</label>
            <input v-model="form.commissioned_date" type="date" class="form-input" />
          </div>
        </div>

        <div class="mt-5 pt-5 border-t border-slate-100">
          <label class="form-label">{{ t('machines.form_desc') }}</label>
          <textarea v-model="form.description" class="form-textarea" rows="3"
            :placeholder="t('machines.form_desc_ph')"></textarea>
        </div>
      </div>

      <!-- Location -->
      <div class="card p-6">
        <div class="section-header mb-5 pb-4 border-b border-slate-100">
          <div class="section-icon bg-emerald-50">
            <svg class="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          <h2 class="section-title">{{ t('machines.form_location') }}</h2>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5">
          <div>
            <label class="form-label">{{ t('machines.form_workshop') }}</label>
            <div class="relative">
              <select v-model="form.workshop" @change="onWorkshopChange"
                class="form-select pr-8 appearance-none cursor-pointer">
                <option value="">{{ t('common.not_selected') }}</option>
                <option v-for="w in workshops" :key="w.id" :value="w.id">{{ w.name }}</option>
              </select>
              <svg class="select-chevron text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
              </svg>
            </div>
          </div>
          <div>
            <label class="form-label">
              {{ t('machines.form_section') }}
              <span v-if="!form.workshop" class="text-xs font-normal text-slate-400 ml-1">{{ t('machines.form_section_hint') }}</span>
            </label>
            <div class="relative">
              <select v-model="form.section" :disabled="!form.workshop"
                class="form-select pr-8 appearance-none
                       disabled:bg-slate-50 disabled:text-slate-400 disabled:cursor-not-allowed">
                <option value="">{{ t('common.not_selected') }}</option>
                <option v-for="s in filteredSections" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
              <svg class="select-chevron" :class="!form.workshop ? 'text-slate-300' : 'text-slate-400'"
                fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
              </svg>
            </div>
          </div>
          <div>
            <label class="form-label">{{ t('machines.form_workplace') }}</label>
            <input v-model="form.workplace" type="text" class="form-input" :placeholder="t('machines.form_ph_workplace')" />
          </div>
        </div>
      </div>

      <!-- Status & operator -->
      <div class="card p-6">
        <div class="section-header mb-5 pb-4 border-b border-slate-100">
          <div class="section-icon bg-amber-50">
            <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h2 class="section-title">{{ t('machines.form_status_op') }}</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label class="form-label">{{ t('machines.form_status') }}</label>
            <div class="relative">
              <select v-model="form.current_status" class="form-select pr-8 appearance-none cursor-pointer">
                <option value="">{{ t('common.not_defined') }}</option>
                <option v-for="s in statuses" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
              <svg class="select-chevron text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
              </svg>
            </div>
          </div>
          <div>
            <label class="form-label">{{ t('machines.form_operator') }}</label>
            <div class="relative">
              <select v-model="form.assigned_operator" class="form-select pr-8 appearance-none cursor-pointer">
                <option value="">{{ t('machines.form_not_assigned') }}</option>
                <option v-for="e in employees" :key="e.id" :value="e.id">{{ e.first_name }}</option>
              </select>
              <svg class="select-chevron text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
              </svg>
            </div>
          </div>
          <div class="md:col-span-2">
            <label class="form-label">
              {{ t('machines.form_brigade') }}
              <span class="text-xs font-normal text-slate-400 ml-1">{{ t('machines.form_brigade_hint') }}</span>
            </label>
            <input v-model="form.assigned_brigade" type="text" class="form-input" />
          </div>
        </div>
      </div>

      <!-- Cost & Amortization -->
      <div class="card p-6">
        <div class="section-header mb-5 pb-4 border-b border-slate-100">
          <div class="section-icon bg-violet-50">
            <svg class="w-4 h-4 text-violet-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h2 class="section-title">{{ t('machines.form_cost_section') }}</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 items-end">
          <div>
            <label class="form-label">{{ t('machines.form_initial_cost') }}</label>
            <div class="relative">
              <input v-model="form.initial_cost" type="number" min="0" step="0.01"
                class="form-input pr-12"
                :placeholder="t('machines.form_initial_cost_ph')" />
              <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400 pointer-events-none">
                {{ t('machines.amort_currency') }}
              </span>
            </div>
          </div>

          <div>
            <label class="form-label">{{ t('machines.form_useful_life') }}</label>
            <input v-model="form.useful_life_years" type="number" min="1" max="100"
              class="form-input"
              :placeholder="t('machines.form_useful_life_ph')" />
          </div>

          <div>
            <label class="form-label">{{ t('machines.form_residual_value') }}</label>
            <p class="text-xs text-slate-400 mb-1.5">{{ t('machines.form_residual_hint') }}</p>
            <div class="relative">
              <input v-model="form.residual_value" type="number" min="0" step="0.01"
                class="form-input pr-12"
                :placeholder="t('machines.form_residual_value_ph')" />
              <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400 pointer-events-none">
                {{ t('machines.amort_currency') }}
              </span>
            </div>
          </div>
        </div>

        <!-- Amortization preview -->
        <div class="mt-5 pt-5 border-t border-slate-100">
          <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
            {{ t('machines.amort_preview') }}
          </p>
          <div v-if="amortCalc" class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="rounded-xl bg-violet-50 border border-violet-100 px-4 py-3">
              <p class="text-xs text-violet-500 mb-1">{{ t('machines.amort_annual') }}</p>
              <p class="text-sm font-semibold text-violet-800">{{ formatMoney(amortCalc.annual) }}</p>
            </div>
            <div class="rounded-xl bg-slate-50 border border-slate-100 px-4 py-3">
              <p class="text-xs text-slate-500 mb-1">{{ t('machines.amort_years_used') }}</p>
              <p class="text-sm font-semibold text-slate-700">{{ amortCalc.yearsUsed }}</p>
            </div>
            <div class="rounded-xl bg-orange-50 border border-orange-100 px-4 py-3">
              <p class="text-xs text-orange-500 mb-1">{{ t('machines.amort_accumulated') }}</p>
              <p class="text-sm font-semibold text-orange-800">{{ formatMoney(amortCalc.accumulated) }}</p>
            </div>
            <div class="rounded-xl bg-emerald-50 border border-emerald-100 px-4 py-3">
              <p class="text-xs text-emerald-500 mb-1">{{ t('machines.amort_book_value') }}</p>
              <p class="text-sm font-semibold text-emerald-800">{{ formatMoney(amortCalc.bookValue) }}</p>
            </div>
          </div>
          <p v-else class="text-xs text-slate-400 italic">{{ t('machines.amort_no_data') }}</p>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-between pt-1 pb-2">
        <button type="button" @click="$router.back()"
          class="btn-md btn-secondary inline-flex items-center gap-2
                 hover:border-slate-300 transition-all duration-200">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          {{ t('common.cancel') }}
        </button>
        <button type="submit" :disabled="saving || !canSave"
          class="btn-md btn-primary min-w-[140px] sm:min-w-[180px] shadow-lg shadow-indigo-500/25
                 hover:shadow-indigo-500/40 hover:-translate-y-px
                 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0
                 transition-all duration-200">
          <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
          </svg>
          {{ saving ? t('common.saving') : (isEdit ? t('machines.form_save_changes') : t('machines.add')) }}
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
import { useI18n } from '@/i18n'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const { t } = useI18n()

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
  initial_cost: '', useful_life_years: '', residual_value: '',
})

const types = ref([])
const statuses = ref([])
const workshops = ref([])
const sections = ref([])
const employees = ref([])

const filteredSections = computed(() =>
  sections.value.filter(s => s.workshop === form.workshop || s.workshop === Number(form.workshop))
)

const canSave = computed(() => form.name.trim() !== '' && form.inventory_number.trim() !== '')

const amortCalc = computed(() => {
  const cost = parseFloat(form.initial_cost)
  const years = parseInt(form.useful_life_years)
  if (!cost || !years || cost <= 0 || years <= 0) return null

  const residual = parseFloat(form.residual_value) || 0
  const annual = (cost - residual) / years

  let yearsUsed = 0
  if (form.commissioned_date) {
    const start = new Date(form.commissioned_date)
    const now = new Date()
    const days = (now - start) / (1000 * 60 * 60 * 24)
    yearsUsed = Math.min(days / 365.25, years)
  }

  const accumulated = annual * yearsUsed
  const bookValue = Math.max(cost - accumulated, residual)

  return {
    annual: annual.toFixed(2),
    yearsUsed: yearsUsed.toFixed(2),
    accumulated: accumulated.toFixed(2),
    bookValue: bookValue.toFixed(2),
  }
})

function formatMoney(val) {
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

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
      initial_cost: m.initial_cost || '',
      useful_life_years: m.useful_life_years || '',
      residual_value: m.residual_value || '',
    })
  } catch {
    toast.error(t('toast.load_data_error'))
    router.push('/machines')
  }
}

async function handleSubmit() {
  errors.value = {}
  saving.value = true

  const payload = { ...form }
  // Convert empty strings to null only for fields that accept null on the backend
  // (model, manufacturer, workplace, assigned_brigade, description must stay as empty strings)
  const nullableFields = ['year_manufactured', 'commissioned_date', 'machine_type',
    'current_status', 'workshop', 'section', 'assigned_operator',
    'initial_cost', 'useful_life_years', 'residual_value']
  nullableFields.forEach(k => {
    if (payload[k] === '') payload[k] = null
  })

  try {
    if (isEdit.value) {
      await machinesApi.update(route.params.id, payload)
      toast.success(t('toast.machine_updated'))
      router.push(`/machines/${route.params.id}`)
    } else {
      const res = await machinesApi.create(payload)
      toast.success(t('toast.machine_added'))
      router.push(`/machines/${res.data.id}`)
    }
  } catch (e) {
    const data = e.response?.data
    if (data?.errors) {
      errors.value = data.errors
      toast.error(t('toast.form_check'))
    } else {
      toast.error(data?.message || t('toast.error'))
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

<style scoped>
/* ── Section header ── */
.section-header {
  @apply flex items-center gap-3;
}
.section-icon {
  @apply w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0;
}
.section-title {
  @apply text-sm font-semibold text-slate-700;
}

/* ── Custom select chevron ── */
.select-chevron {
  @apply absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none;
}

/* ── Reduced motion ── */
@media (prefers-reduced-motion: reduce) {
  .btn-md, .btn-sm { transition: none; }
}
</style>
