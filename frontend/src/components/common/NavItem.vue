<template>
  <RouterLink
    :to="item.to"
    class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium
           transition-all duration-150 cursor-pointer group"
    :class="isActive
      ? 'bg-indigo-50 text-indigo-700 ring-1 ring-indigo-100/80'
      : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'"
    :title="collapsed ? item.label : ''"
  >
    <!-- Active indicator dot -->
    <span v-if="isActive" class="active-dot"></span>

    <component
      :is="iconComponent"
      :class="['w-5 h-5 flex-shrink-0 transition-all duration-150',
        isActive ? 'text-indigo-600 scale-110' : 'text-slate-400 group-hover:text-slate-600']"
    />

    <Transition name="fade">
      <span v-if="!collapsed" class="truncate leading-none">{{ item.label }}</span>
    </Transition>

    <Transition name="fade">
      <span v-if="!collapsed && item.badge"
        class="ml-auto text-xs bg-rose-500 text-white rounded-full px-1.5 py-0.5
               leading-none font-semibold tabular-nums ring-1 ring-rose-400/30">
        {{ item.badge }}
      </span>
    </Transition>
  </RouterLink>
</template>

<script setup>
import { computed, h } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  item: { type: Object, required: true },
  collapsed: { type: Boolean, default: false }
})

const route = useRoute()
const isActive = computed(() => route.path.startsWith(props.item.to))

const svgPaths = {
  home: [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })],
  cog: [
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }),
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z' })
  ],
  users: [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z' })],
  book: [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' })],
  'user-group': [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' })],
  document: [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })],
}

const iconComponent = computed(() => {
  const paths = svgPaths[props.item.icon] || svgPaths.cog
  return (iconProps) => h('svg', { fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor', 'stroke-width': '2', ...iconProps }, paths)
})
</script>

<style scoped>
.active-dot {
  @apply absolute left-0 w-[3px] h-5 bg-indigo-500 rounded-r-full;
}
.nav-item {
  position: relative;
  overflow: hidden;
}
</style>
