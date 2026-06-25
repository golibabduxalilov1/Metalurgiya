import axios from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
})

// Request interceptor - attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - handle token refresh and errors
let isRefreshing = false
let failedQueue = []

function processQueue(error, token = null) {
  failedQueue.forEach(p => error ? p.reject(error) : p.resolve(token))
  failedQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }

    // If a refresh is already in progress — queue this request
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      }).then(token => {
        originalRequest.headers.Authorization = `Bearer ${token}`
        return api(originalRequest)
      }).catch(err => Promise.reject(err))
    }

    originalRequest._retry = true
    isRefreshing = true

    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      isRefreshing = false
      processQueue(error)
      router.push('/login')
      return Promise.reject(error)
    }

    try {
      const res = await axios.post(`${originalRequest.baseURL || '/api/v1'}/auth/refresh/`, {
        refresh: refreshToken,
      })
      const { access } = res.data
      localStorage.setItem('access_token', access)
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`
      processQueue(null, access)
      originalRequest.headers.Authorization = `Bearer ${access}`
      return api(originalRequest)
    } catch (err) {
      processQueue(err)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      router.push('/login')
      return Promise.reject(err)
    } finally {
      isRefreshing = false
    }
  }
)

export default api

// ============================================================
// API Service modules
// ============================================================

export const authApi = {
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: (refresh) => api.post('/auth/logout/', { refresh }),
  refresh: (refresh) => api.post('/auth/refresh/', { refresh }),
  me: () => api.get('/auth/me/'),
  changePassword: (data) => api.post('/auth/change-password/', data),
}

export const usersApi = {
  list: (params) => api.get('/users/', { params }),
  get: (id) => api.get(`/users/${id}/`),
  create: (data) => api.post('/users/', data),
  update: (id, data) => api.patch(`/users/${id}/`, data),
  delete: (id) => api.delete(`/users/${id}/`),
  activate: (id) => api.post(`/users/${id}/activate/`),
  resetPassword: (id, data) => api.post(`/users/${id}/reset_password/`, data),
}

export const machinesApi = {
  list: (params) => api.get('/machines/', { params }),
  get: (id) => api.get(`/machines/${id}/`),
  create: (data) => api.post('/machines/', data),
  update: (id, data) => api.patch(`/machines/${id}/`, data),
  delete: (id) => api.delete(`/machines/${id}/`),
  restore: (id) => api.post(`/machines/${id}/restore/`),
  changeStatus: (id, data) => api.post(`/machines/${id}/change-status/`, data),
  statusHistory: (id) => api.get(`/machines/${id}/status-history/`),
  upload: (id, formData) => api.post(`/machines/${id}/upload/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  assignOperator: (id, data) => api.post(`/machines/${id}/assign-operator/`, data),
  periodStats: (params) => api.get('/machines/period-stats/', { params }),
  exportExcel: (params) => api.get('/machines/export-excel/', {
    params, responseType: 'blob'
  }),
  importExcel: (formData) => api.post('/machines/import-excel/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  importTemplate: () => api.get('/machines/import-template/', { responseType: 'blob' }),
  deleteAttachment: (attachmentId) => api.delete(`/attachments/${attachmentId}/`),
}

export const machineTypesApi = {
  list: (params) => api.get('/machine-types/', { params }),
  create: (data) => api.post('/machine-types/', data),
  update: (id, data) => api.patch(`/machine-types/${id}/`, data),
  delete: (id) => api.delete(`/machine-types/${id}/`),
}

export const statusesApi = {
  list: (params) => api.get('/statuses/', { params }),
  create: (data) => api.post('/statuses/', data),
  update: (id, data) => api.patch(`/statuses/${id}/`, data),
  delete: (id) => api.delete(`/statuses/${id}/`),
}

export const workshopsApi = {
  list: (params) => api.get('/workshops/', { params }),
  create: (data) => api.post('/workshops/', data),
  update: (id, data) => api.patch(`/workshops/${id}/`, data),
  delete: (id) => api.delete(`/workshops/${id}/`),
  sections: (params) => api.get('/workshops/sections/', { params }),
  createSection: (data) => api.post('/workshops/sections/', data),
  updateSection: (id, data) => api.patch(`/workshops/sections/${id}/`, data),
  deleteSection: (id) => api.delete(`/workshops/sections/${id}/`),
}

export const employeesApi = {
  list: (params) => api.get('/employees/', { params }),
  get: (id) => api.get(`/employees/${id}/`),
  create: (data) => api.post('/employees/', data),
  update: (id, data) => api.patch(`/employees/${id}/`, data),
  delete: (id) => api.delete(`/employees/${id}/`),
}

export const auditApi = {
  list: (params) => api.get('/audit/', { params }),
}

export const dashboardApi = {
  get: () => api.get('/dashboard/'),
}

export const unitsApi = {
  list: (params) => api.get('/spare-parts/units/', { params }),
  create: (data) => api.post('/spare-parts/units/', data),
  update: (id, data) => api.patch(`/spare-parts/units/${id}/`, data),
  delete: (id) => api.delete(`/spare-parts/units/${id}/`),
}

export const warehouseApi = {
  list: (params) => api.get('/spare-parts/', { params }),
  get: (id) => api.get(`/spare-parts/${id}/`),
  create: (data) => api.post('/spare-parts/', data),
  update: (id, data) => api.patch(`/spare-parts/${id}/`, data),
  delete: (id) => api.delete(`/spare-parts/${id}/`),
}

export const maintenanceApi = {
  alerts: () => api.get('/maintenance/alerts/'),
  all: () => api.get('/maintenance/alerts/', { params: { all: 'true' } }),
  get: (machineId) => api.get(`/machines/${machineId}/maintenance/`),
  set: (machineId, data) => api.post(`/machines/${machineId}/maintenance/`, data),
  update: (machineId, data) => api.patch(`/machines/${machineId}/maintenance/`, data),
  delete: (machineId) => api.delete(`/machines/${machineId}/maintenance/`),
  startRepair: (machineId) => api.post(`/machines/${machineId}/maintenance/start-repair/`),
  history: (machineId) => api.get(`/machines/${machineId}/maintenance-history/`),
  tasks: (machineId) => api.get(`/machines/${machineId}/maintenance/tasks/`),
  addTask: (machineId, data) => api.post(`/machines/${machineId}/maintenance/tasks/`, data),
  toggleTask: (machineId, taskId, data) => api.patch(`/machines/${machineId}/maintenance/tasks/${taskId}/`, data),
  deleteTask: (machineId, taskId) => api.delete(`/machines/${machineId}/maintenance/tasks/${taskId}/`),
  taskSpareParts: (machineId, taskId) => api.get(`/machines/${machineId}/maintenance/tasks/${taskId}/spare-parts/`),
  addTaskSparePart: (machineId, taskId, data) => api.post(`/machines/${machineId}/maintenance/tasks/${taskId}/spare-parts/`, data),
  removeTaskSparePart: (machineId, taskId, usageId) => api.delete(`/machines/${machineId}/maintenance/tasks/${taskId}/spare-parts/${usageId}/`),
  complete: (machineId, data) => api.post(`/machines/${machineId}/maintenance/complete/`, data),
}
