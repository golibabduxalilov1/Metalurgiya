<template>
  <div class="modal-backdrop" @click.self="$emit('cancel')">
    <div class="modal-box max-w-md">
      <div class="modal-header">
        <h3 class="text-lg font-semibold text-slate-900">{{ title }}</h3>
        <button @click="$emit('cancel')" class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
      <div class="modal-body">
        <p class="text-slate-600">{{ message }}</p>
      </div>
      <div class="modal-footer">
        <button @click="$emit('cancel')" class="btn-md btn-secondary">Отмена</button>
        <button @click="$emit('confirm')" :class="['btn-md', confirmClass || 'btn-primary']">
          {{ confirmLabel || 'Подтвердить' }}
        </button>
      </div>
    </div>
  </div>
</template>
<script setup>
defineProps({ title: String, message: String, confirmLabel: String, confirmClass: String })
defineEmits(['confirm', 'cancel'])
</script>
