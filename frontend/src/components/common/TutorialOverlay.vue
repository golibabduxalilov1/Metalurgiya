<template>
  <Teleport to="body">
    <div v-if="modelValue" class="tutorial-root">
      <!-- Spotlight cutout -->
      <div v-if="rect" class="tutorial-spotlight" :style="spotlightStyle"></div>
      <!-- Full dim when no target found -->
      <div v-else class="tutorial-dim"></div>

      <!-- Tooltip -->
      <div class="tutorial-tooltip" :style="tooltipStyle" ref="tooltipRef">
        <div class="flex items-start justify-between gap-3 mb-2">
          <h4 class="text-sm font-bold text-slate-900">{{ currentStep?.title }}</h4>
          <span class="text-[11px] font-semibold text-slate-400 tabular-nums flex-shrink-0">{{ stepIndex + 1 }} / {{ steps.length }}</span>
        </div>
        <p class="text-sm text-slate-600 leading-relaxed">{{ currentStep?.text }}</p>

        <div class="flex items-center justify-between mt-4 gap-2">
          <button v-if="!isLast" @click="skip" class="text-xs text-slate-400 hover:text-slate-600 transition-colors cursor-pointer">
            {{ skipLabel }}
          </button>
          <span v-else></span>
          <div class="flex items-center gap-2">
            <button v-if="stepIndex > 0" @click="prev"
              class="px-3 py-1.5 text-xs font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors cursor-pointer">
              {{ prevLabel }}
            </button>
            <button @click="next"
              class="px-3.5 py-1.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors cursor-pointer">
              {{ isLast ? finishLabel : nextLabel }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, nextTick, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  steps: { type: Array, required: true },
  prevLabel: { type: String, default: 'Назад' },
  nextLabel: { type: String, default: 'Далее' },
  skipLabel: { type: String, default: 'Пропустить' },
  finishLabel: { type: String, default: 'Начать' },
})
const emit = defineEmits(['update:modelValue', 'finish', 'skip'])

const stepIndex = ref(0)
const rect = ref(null)
const tooltipRef = ref(null)
const tooltipSize = ref({ width: 320, height: 160 })

const currentStep = computed(() => props.steps[stepIndex.value] || null)
const isLast = computed(() => stepIndex.value === props.steps.length - 1)

function resolveTarget(step) {
  if (!step) return null
  const selectors = Array.isArray(step.target) ? step.target : [step.target]
  for (const sel of selectors) {
    if (!sel) continue
    const el = document.querySelector(sel)
    if (el) return el
  }
  return null
}

async function measure() {
  await nextTick()
  const step = currentStep.value
  const el = resolveTarget(step)
  if (!el) {
    rect.value = null
    return
  }
  el.scrollIntoView({ block: 'center', behavior: 'instant' in window ? 'instant' : 'auto' })
  await new Promise(r => setTimeout(r, 60))
  const r = el.getBoundingClientRect()
  const pad = step.padding ?? 8
  rect.value = {
    top: r.top - pad,
    left: r.left - pad,
    width: r.width + pad * 2,
    height: r.height + pad * 2,
  }
  await nextTick()
  if (tooltipRef.value) {
    const tr = tooltipRef.value.getBoundingClientRect()
    tooltipSize.value = { width: tr.width, height: tr.height }
  }
}

function reposition() {
  if (props.modelValue) measure()
}

watch(() => props.modelValue, (v) => {
  if (v) {
    stepIndex.value = 0
    measure()
    window.addEventListener('resize', reposition)
    window.addEventListener('scroll', reposition, true)
  } else {
    window.removeEventListener('resize', reposition)
    window.removeEventListener('scroll', reposition, true)
  }
})

watch(stepIndex, () => measure())

onBeforeUnmount(() => {
  window.removeEventListener('resize', reposition)
  window.removeEventListener('scroll', reposition, true)
})

const spotlightStyle = computed(() => {
  if (!rect.value) return {}
  return {
    top: `${rect.value.top}px`,
    left: `${rect.value.left}px`,
    width: `${rect.value.width}px`,
    height: `${rect.value.height}px`,
  }
})

const tooltipStyle = computed(() => {
  const margin = 14
  const vw = window.innerWidth
  const vh = window.innerHeight
  const { width: tw, height: th } = tooltipSize.value

  if (!rect.value) {
    return {
      top: `${Math.max(margin, (vh - th) / 2)}px`,
      left: `${Math.max(margin, (vw - tw) / 2)}px`,
    }
  }

  const r = rect.value
  let top
  if (r.top + r.height + margin + th <= vh) {
    top = r.top + r.height + margin
  } else if (r.top - margin - th >= 0) {
    top = r.top - margin - th
  } else {
    top = Math.max(margin, vh - th - margin)
  }

  let left = r.left + r.width / 2 - tw / 2
  left = Math.min(Math.max(left, margin), vw - tw - margin)

  return { top: `${top}px`, left: `${left}px` }
})

function next() {
  if (isLast.value) {
    finish()
  } else {
    stepIndex.value++
  }
}
function prev() {
  if (stepIndex.value > 0) stepIndex.value--
}
function skip() {
  emit('update:modelValue', false)
  emit('skip')
}
function finish() {
  emit('update:modelValue', false)
  emit('finish')
}
</script>

<style scoped>
.tutorial-root {
  position: fixed;
  inset: 0;
  z-index: 1000;
}
.tutorial-dim {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
}
.tutorial-spotlight {
  position: fixed;
  border-radius: 14px;
  box-shadow: 0 0 0 9999px rgba(15, 23, 42, 0.65);
  pointer-events: none;
  transition: top 0.25s ease, left 0.25s ease, width 0.25s ease, height 0.25s ease;
  border: 2px solid rgba(99, 102, 241, 0.85);
}
.tutorial-tooltip {
  position: fixed;
  width: 320px;
  max-width: calc(100vw - 28px);
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.35);
  padding: 16px 18px;
  transition: top 0.25s ease, left 0.25s ease;
}
</style>
