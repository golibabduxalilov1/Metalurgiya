<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-box max-w-md">
      <div class="modal-header">
        <h3 class="text-lg font-semibold text-slate-900">{{ t('modals.assign_operator_title') }}</h3>
        <button @click="$emit('close')" class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <div class="modal-body space-y-4">
        <div>
          <label class="form-label">{{ t('modals.operator_label') }}</label>
          <div class="relative">
            <input v-model="search" type="text" :placeholder="t('modals.search_emp_ph')"
              class="form-input mb-2" />
          </div>
          <div class="max-h-52 overflow-y-auto border border-slate-200 rounded-lg divide-y divide-slate-100">
            <button type="button" @click="selectedOperator = null"
              :class="[
                'w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-slate-50 transition-colors',
                selectedOperator === null ? 'bg-primary-50' : ''
              ]">
              <div class="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center">
                <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                </svg>
              </div>
              <span class="text-sm text-slate-500 italic">{{ t('modals.detach_operator') }}</span>
            </button>
            <button v-for="emp in filteredEmployees" :key="emp.id" type="button"
              @click="selectedOperator = emp"
              :class="[
                'w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-slate-50 transition-colors',
                selectedOperator?.id === emp.id ? 'bg-primary-50' : ''
              ]">
              <div class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0">
                <span class="text-primary-700 text-xs font-semibold">{{ (emp.first_name || '?')[0].toUpperCase() }}</span>
              </div>
              <div>
                <div class="text-sm font-medium text-slate-900">{{ emp.first_name }}</div>
                <div class="text-xs text-slate-400">{{ emp.position }}</div>
              </div>
            </button>
          </div>
        </div>

        <div>
          <label class="form-label">{{ t('modals.notes_label') }}</label>
          <textarea v-model="notes" class="form-textarea" rows="2" :placeholder="t('modals.notes_ph')"></textarea>
        </div>
      </div>

      <div class="modal-footer">
        <button @click="$emit('close')" class="btn-md btn-secondary">{{ t('common.cancel') }}</button>
        <button @click="handleSave" :disabled="saving" class="btn-md btn-primary">
          {{ saving ? t('common.saving') : t('common.save') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { machinesApi, employeesApi } from '@/api'
import { useI18n } from '@/i18n'

const props = defineProps({ machine: Object })
const emit = defineEmits(['updated', 'close'])
const toast = useToast()
const { t } = useI18n()

const employees = ref([])
const selectedOperator = ref(props.machine?.assigned_operator
  ? { id: props.machine.assigned_operator } : null)
const search = ref('')
const notes = ref('')
const saving = ref(false)

const filteredEmployees = computed(() => {
  if (!search.value) return employees.value
  const q = search.value.toLowerCase()
  return employees.value.filter(e =>
    e.first_name.toLowerCase().includes(q) || (e.position || '').toLowerCase().includes(q)
  )
})

async function handleSave() {
  saving.value = true
  try {
    await machinesApi.assignOperator(props.machine.id, {
      operator_id: selectedOperator.value?.id || null,
      notes: notes.value
    })
    toast.success(selectedOperator.value ? t('toast.operator_assigned') : t('toast.operator_detached'))
    emit('updated')
  } catch {
    toast.error(t('toast.operator_error'))
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  const res = await employeesApi.list({ page_size: 500, is_active: true })
  employees.value = res.data.results || res.data
})
</script>
