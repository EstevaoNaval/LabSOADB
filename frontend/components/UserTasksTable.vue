<template>
    <main>
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
                <tr v-for="task in userTasksStore.tasks" :key="task.id" class="hover">
                    <td>{{ task.id }}</td>
                    <td>{{ utils.truncateString(task.label) }}</td>
                    <td>
                        <time :datetime="task.created_at">
                            {{ utils.formatTimestamp(task.created_at) }}
                        </time>
                    </td>
                    <td :class="getTaskColorClass(task.status)">{{ task.status }}</td>
                    <td class="grid grid-cols-2">
                        
                        <svg v-if="task.result && isTaskSuccessful(task.status)" xmlns="http://www.w3.org/2000/svg" role="button" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="cursor-pointer transition-transform duration-150 hover:scale-110 active:scale-90 size-8 m-auto">
                            <title>Download output file</title>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m.75 12 3 3m0 0 3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                        </svg>
                        <svg 
                            v-if="!task.result && !isTaskSuccessful(task.status)" 
                            xmlns="http://www.w3.org/2000/svg" 
                            role="button" 
                            fill="none" 
                            viewBox="0 0 24 24" 
                            stroke-width="1.5"
                            stroke="currentColor" 
                            :class="themeStore.isDarkMode ? 'text-slate-500 cursor-pointer size-8 m-auto' : 'text-gray-300 cursor-pointer size-8 m-auto'"
                        >
                            <title>Download output file</title>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m.75 12 3 3m0 0 3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                        </svg>
                        <svg v-if="isTaskBeingProcessed(task.status)" @click="revokeTask(task.task_id)" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="cursor-pointer transition-transform duration-150 hover:scale-110 active:scale-90 size-8 m-auto">
                            <title>Revoke task</title>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                        </svg>
                        <svg 
                            v-if="!isTaskBeingProcessed(task.status)" 
                            xmlns="http://www.w3.org/2000/svg" 
                            fill="none" 
                            viewBox="0 0 24 24" 
                            stroke-width="1.5" 
                            stroke="currentColor" 
                            :class="themeStore.isDarkMode ? 'text-slate-500 cursor-pointer size-8 m-auto' : 'text-gray-300 cursor-pointer size-8 m-auto'"
                        >
                            <title>Task already concluded</title>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                        </svg>
                        
                    </td>
                </tr>
            </tbody>
        </table>
    </main>
</template>

<script setup>
    import utils from '~/utils/util'
    import { onBeforeMount, onUnmounted } from 'vue';
    import { useThemeStore } from '~/stores/theme';
    import { useUserTasksStore } from '~/stores/userTasks';
    import { useToast } from 'vue-toastification';

    const themeStore = useThemeStore()
    const userTasksStore = useUserTasksStore()

    const toast = useToast();

    const getTaskColorClass = computed(() => {
        return (taskStatus) => {
            const MAP_TASK_STATUS_TO_COLOR_STYLE_CLASS = {
                'SUCCESS': themeStore.isDarkMode ? 'text-success' : 'text-green-500',
                'PENDING': themeStore.isDarkMode ? 'text-warning' : 'text-amber-500',
                'RETRY': themeStore.isDarkMode ? 'text-warning' : 'text-amber-500',
                'FAILURE': themeStore.isDarkMode ? 'text-error' : 'text-rose-500',
                'REVOKED': themeStore.isDarkMode ? 'text-error' : 'text-rose-500',
            };

            return MAP_TASK_STATUS_TO_COLOR_STYLE_CLASS[taskStatus] || '';
        };
    });

    const taskStatusColorStyleClass = ref(null)

    async function revokeTask(taskId) {
        await userTasksStore.revokeTask(taskId)
        toast.success("Task revoked successfully")
        fetchUserTasks(1)
    }

    function isTaskBeingProcessed(taskStatus) {
        return taskStatus === 'PENDING' || taskStatus === 'RETRY' ? true : false
    }

    function isTaskSuccessful(taskStatus) {
        return taskStatus === 'SUCCESS' ? true : false
    }

    async function fetchUserTasks(page) {
        await userTasksStore.fetchTasksPerUser({ page: page })
    }

    watch(() => themeStore.theme, () => {
        taskStatusColorStyleClass.value 
    })

    onBeforeMount(() => {
        fetchUserTasks(1)
    })

    onUnmounted(() => {
        userTasksStore.$reset()
    })
</script>