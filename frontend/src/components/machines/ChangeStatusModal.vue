<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-box max-w-md">
      <div class="modal-header">
        <h3 class="text-lg font-semibold text-slate-900">{{ t('modals.change_status_title') }}</h3>
        <button @click="$emit('close')" class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <div class="modal-body space-y-4">
        <!-- Status selection -->
        <div>
          <label class="form-label">{{ t('modals.new_status_label') }} <span class="text-red-500">*</span></label>
          <div class="grid grid-cols-2 gap-2 mt-2">
            <button v-for="s in statuses" :key="s.id" type="button"
              @click="selectedStatus = s"
              :class="[
                'flex items-center gap-2 p-3 rounded-xl border-2 transition-all text-left',
                selectedStatus?.id === s.id
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-slate-200 hover:border-slate-300 bg-white'
              ]">
              <span :class="['status-dot flex-shrink-0', `status-dot-${s.color}`]"></span>
              <span class="text-sm font-medium text-slate-800">{{ s.name }}</span>
            </button>
          </div>
        </div>

        <!-- Comment -->
        <div>
          <label class="form-label">
            {{ t('modals.comment_label') }}
            <span v-if="selectedStatus?.requires_comment" class="text-red-500">*</span>
          </label>
          <textarea v-model="comment" class="form-textarea" rows="3"
            :placeholder="selectedStatus?.requires_comment
              ? t('modals.comment_ph_required')
              : t('modals.comment_ph')"
          </textarea>
        </div>
      </div>

      <div class="modal-footer">
        <button @click="$emit('close')" class="btn-md btn-secondary">{{ t('common.cancel') }}</button>
        <button @click="handleSave" :disabled="saving || !selectedStatus" class="btn-md btn-primary">
          <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          {{ saving ? t('common.saving') : t('modals.change_status_btn') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { machinesApi, statusesApi } from '@/api'
import { useI18n } from '@/i18n'

const props = defineProps({ machineId: [String, Number] })
const emit = defineEmits(['updated', 'close'])
const toast = useToast()
const { t } = useI18n()

const statuses = ref([])
const selectedStatus = ref(null)
const comment = ref('')
const saving = ref(false)

async function loadStatuses() {
  const res = await statusesApi.list()
  statuses.value = (res.data.results || res.data).filter(s => s.is_active)
}

async function handleSave() {
  if (!selectedStatus.value) return
  if (selectedStatus.value.requires_comment && !comment.value.trim()) {
    toast.error(t('toast.comment_required'))
    return
  }
  saving.value = true
  try {
    await machinesApi.changeStatus(props.machineId, {
      status_id: selectedStatus.value.id,
      comment: comment.value
    })
    toast.success(t('toast.status_changed'))
    emit('updated')
  } catch (e) {
    toast.error(e.response?.data?.message || t('toast.status_error'))
  } finally {
    saving.value = false
  }
}

onMounted(loadStatuses)
</script>
