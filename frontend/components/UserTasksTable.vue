<template>
    <table class="ml-auto table table-auto table-zebra table-pin-rows">
        <!-- head -->
        <thead class="text-sm md:text-lg">
            <tr>
                <th>ID</th>
                <th>Description</th>
                <th>Created At</th>
                <th>Status</th>
                <th></th>
            </tr>
        </thead>
        <tbody class="text-sm md:text-lg font-normal">
            <tr v-for="task in userTasks.tasks" :key="task.id" class="hover">
                <td>{{ task.id }}</td>
                <td>{{ utils.truncateString(task.label) }}</td>
                <td>
                    <time :datetime="task.created_at">
                        {{ utils.formatTimestamp(task.created_at) }}
                    </time>
                </td>
                <td :class="MAP_TASK_STATUS_TO_COLOR_STYLE_CLASS[task.status]">{{ task.status }}</td>
                <td>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8 mx-auto">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                    </svg>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script setup>
    import utils from '~/utils/util'
    import { onBeforeMount } from 'vue';
    import { useThemeStore } from '~/stores/theme';
    import { useUserTaskStore } from '~/stores/userTasks';
    
    const themeStore = useThemeStore()
    const userTasks = useUserTaskStore()

    const MAP_TASK_STATUS_TO_COLOR_STYLE_CLASS = {
        'SUCCESS': themeStore.isDarkMode ? 'text-success' : 'text-green-500',
        'PENDING': themeStore.isDarkMode ? 'text-warning' : 'text-amber-500',
        'RETRY': themeStore.isDarkMode ? 'text-warning' : 'text-amber-500',
        'FAILURE': themeStore.isDarkMode ? 'text-error' : 'text-rose-500',
        'REVOKED': themeStore.isDarkMode ? 'text-error' : 'text-rose-500',
    }

    onBeforeMount(() => {
        userTasks.fetchTasksPerUser()
    })
</script>