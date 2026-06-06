<template>
  <div class="app-layout">
    <!-- Sidebar -->
    <aside
      class="fixed top-0 left-0 h-full z-40 flex flex-col transition-all duration-300"
      :class="sidebarCollapsed ? 'w-[72px]' : 'w-[260px]'"
      style="background: #0F172A;"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-4 py-5 border-b border-slate-800">
        <div class="flex-shrink-0 w-9 h-9 bg-primary-600 rounded-xl flex items-center justify-center">
          <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <Transition name="fade">
          <div v-if="!sidebarCollapsed" class="overflow-hidden">
            <div class="text-white font-bold text-sm leading-tight">Учёт станков</div>
            <div class="text-slate-500 text-xs">Реестр оборудования</div>
          </div>
        </Transition>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto py-4 px-2 space-y-0.5">
        <!-- Main -->
        <div v-if="!sidebarCollapsed" class="px-3 mb-2">
          <span class="text-[10px] font-semibold text-slate-600 uppercase tracking-widest">Главное</span>
        </div>
        <NavItem v-for="item in mainNavItems" :key="item.name"
          :item="item" :collapsed="sidebarCollapsed" />

        <!-- Reference -->
        <template v-if="auth.isAdmin || auth.isMaster">
          <div v-if="!sidebarCollapsed" class="px-3 mt-4 mb-2">
            <span class="text-[10px] font-semibold text-slate-600 uppercase tracking-widest">Управление</span>
          </div>
          <div v-else class="border-t border-slate-800 my-2"></div>
          <NavItem v-for="item in managementNavItems" :key="item.name"
            :item="item" :collapsed="sidebarCollapsed" />
        </template>

        <!-- Admin only -->
        <template v-if="auth.isAdmin">
          <div v-if="!sidebarCollapsed" class="px-3 mt-4 mb-2">
            <span class="text-[10px] font-semibold text-slate-600 uppercase tracking-widest">Администрирование</span>
          </div>
          <div v-else class="border-t border-slate-800 my-2"></div>
          <NavItem v-for="item in adminNavItems" :key="item.name"
            :item="item" :collapsed="sidebarCollapsed" />
        </template>
      </nav>

      <!-- User section -->
      <div class="border-t border-slate-800 p-3">
        <RouterLink to="/profile" class="flex items-center gap-3 p-2 rounded-lg hover:bg-slate-800 transition-colors group">
          <div class="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center flex-shrink-0">
            <span class="text-white text-xs font-bold">{{ userInitials }}</span>
          </div>
          <Transition name="fade">
            <div v-if="!sidebarCollapsed" class="overflow-hidden flex-1 min-w-0">
              <div class="text-white text-sm font-medium truncate">{{ auth.userFullName }}</div>
              <div class="text-slate-500 text-xs">{{ auth.userRole }}</div>
            </div>
          </Transition>
        </RouterLink>
        <button v-if="!sidebarCollapsed"
          @click="auth.logout"
          class="mt-1 w-full flex items-center gap-2 px-2 py-1.5 text-slate-500 hover:text-red-400
                 hover:bg-slate-800 rounded-lg text-sm transition-colors">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Выйти
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <div class="flex-1 flex flex-col min-h-screen transition-all duration-300"
      :style="{ marginLeft: sidebarCollapsed ? '72px' : '260px' }">

      <!-- Top bar -->
      <header class="fixed top-0 right-0 z-30 h-16 bg-white border-b border-slate-200 flex items-center px-6 gap-4 shadow-sm"
        :style="{ left: sidebarCollapsed ? '72px' : '260px' }">
        <!-- Toggle sidebar -->
        <button @click="toggleSidebar"
          class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 hover:text-slate-700 transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <!-- Breadcrumb -->
        <div class="flex items-center gap-2 text-sm">
          <span class="text-slate-400">Главная</span>
          <span class="text-slate-300">/</span>
          <span class="text-slate-700 font-medium">{{ currentPageTitle }}</span>
        </div>

        <div class="flex-1"></div>

        <!-- Role badge -->
        <div :class="roleBadgeClass">{{ auth.userRole }}</div>

        <!-- Notifications placeholder -->
        <button class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 transition-colors relative">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </button>

        <!-- User avatar -->
        <RouterLink to="/profile" class="flex items-center gap-2 p-1.5 rounded-lg hover:bg-slate-100 transition-colors">
          <div class="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center">
            <span class="text-white text-xs font-bold">{{ userInitials }}</span>
          </div>
          <span class="text-sm font-medium text-slate-700 hidden md:block">{{ auth.userFullName }}</span>
        </RouterLink>
      </header>

      <!-- Page content -->
      <main class="flex-1 pt-16">
        <div class="p-6">
          <RouterView v-slot="{ Component, route }">
            <Transition name="fade" mode="out-in">
              <component :is="Component" :key="route.path" />
            </Transition>
          </RouterView>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import NavItem from '@/components/common/NavItem.vue'

const auth = useAuthStore()
const route = useRoute()
const sidebarCollapsed = ref(false)

function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const userInitials = computed(() => {
  const name = auth.userFullName
  if (!name) return '?'
  const parts = name.split(' ')
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase()
  return name[0].toUpperCase()
})

const currentPageTitle = computed(() => route.meta?.title || '')

const roleBadgeClass = computed(() => {
  const role = auth.user?.role
  if (role === 'admin') return 'role-admin'
  if (role === 'master') return 'role-master'
  return 'role-operator'
})

const mainNavItems = computed(() => [
  { name: 'Dashboard', label: 'Главная', icon: 'home', to: '/dashboard' },
  { name: 'Machines', label: 'Реестр станков', icon: 'cog', to: '/machines' },
])

const managementNavItems = computed(() => {
  const items = []
  if (auth.isAdmin || auth.isMaster) {
    items.push({ name: 'Employees', label: 'Сотрудники', icon: 'users', to: '/employees' })
  }
  return items
})

const adminNavItems = computed(() => [
  { name: 'Directories', label: 'Справочники', icon: 'book', to: '/directories' },
  { name: 'Users', label: 'Пользователи', icon: 'user-group', to: '/users' },
  { name: 'Audit', label: 'Журнал аудита', icon: 'document', to: '/audit' },
])
</script>
