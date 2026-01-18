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
                    <th class="text-center">Actions</th>
                </tr>
            </thead>
            <tbody class="text-sm md:text-lg font-normal">
                <tr v-for="[idx, task] of userTasksStore.tasks.entries()" :key="task.id" class="hover">
                    <td>{{ task.id }}</td>
                    <td>{{ utils.truncateString(task.label) }}</td>
                    <td>
                        <time :datetime="task.created_at">
                            {{ utils.formatTimestamp(task.created_at) }}
                        </time>
                    </td>
                    <td :class="getTaskColorClass(task.status)">{{ task.status }}</td>
                    <td class="xl:hidden">
                        <div
                            :class="isPageLastElement(userTasksStore.tasks.length, idx) ? 'dropdown dropdown-top dropdown-end' : 'dropdown dropdown-down dropdown-end'">
                            <div class="flex justify-center items-center" tabindex="0" role="button">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor"
                                    class="cursor-pointer transition-transform duration-150 hover:scale-110 active:scale-90 size-6 md:size-8 ">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                                </svg>
                            </div>
                            <ul tabindex="0"
                                class="dropdown-content menu bg-base-200 rounded-box z-[1] w-44 p-2 shadow">
                                <li class="flex">
                                    <a :href="task.data_file"
                                        class="mr-auto cursor-pointer transition-transform duration-150 hover:scale-100 active:scale-90"
                                        v-if="isTaskSuccessful(task.status)">
                                        <svg xmlns="http://www.w3.org/2000/svg" role="button" fill="none"
                                            viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                            class="size-6 m-auto">
                                            <title>Download output file</title>
                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m.75 12 3 3m0 0 3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                                        </svg>
                                        Download File
                                    </a>
                                    <a :class="themeStore.isDarkMode ? 'text-slate-500 cursor-pointer mr-auto' : 'text-gray-300 cursor-pointer mr-auto'"
                                        v-if="!isTaskSuccessful(task.status)">
                                        <svg xmlns="http://www.w3.org/2000/svg" role="button" fill="none"
                                            viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                            class="size-6 m-auto">
                                            <title>Download output file</title>
                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m.75 12 3 3m0 0 3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                                        </svg>
                                        Download File
                                    </a>
                                </li>
                                <li class="flex">
                                    <a class="mr-auto cursor-pointer transition-transform duration-150 hover:scale-100 active:scale-90"
                                        v-if="isTaskBeingProcessed(task.status)" @click="revokeTask(task.task_id)">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                            stroke-width="1.5" stroke="currentColor" class="size-6 m-auto">
                                            <title>Revoke task</title>
                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                d="M6 18 18 6M6 6l12 12" />
                                        </svg>
                                        Revoke Task
                                    </a>
                                    <a :class="themeStore.isDarkMode ? 'text-slate-500 cursor-pointer mr-auto' : 'text-gray-300 cursor-pointer mr-auto'"
                                        v-if="!isTaskBeingProcessed(task.status)">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                            stroke-width="1.5" stroke="currentColor" class="size-6 m-auto">
                                            <title>Task already concluded</title>
                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                d="M6 18 18 6M6 6l12 12" />
                                        </svg>
                                        Revoke Task
                                    </a>
                                </li>
                            </ul>
                        </div>

                    </td>
                    <td class="hidden xl:grid xl:grid-cols-2">
                        <a :href="task.data_file"
                            class="cursor-pointer transition-transform duration-150 hover:scale-110 active:scale-90"
                            v-if="isTaskSuccessful(task.status)">
                            <svg xmlns="http://www.w3.org/2000/svg" role="button" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.5" stroke="currentColor" class="size-6 xl:size-8 m-auto">
                                <title>Download output file</title>
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m.75 12 3 3m0 0 3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                            </svg>
                        </a>

                        <a :class="themeStore.isDarkMode ? 'text-slate-500 cursor-pointer' : 'text-gray-300 cursor-pointer'"
                            v-if="!isTaskSuccessful(task.status)">
                            <svg xmlns="http://www.w3.org/2000/svg" role="button" fill="none" viewBox="0 0 24 24"
                                stroke-width="1.5" stroke="currentColor" class="size-6 xl:size-8 m-auto">
                                <title>Download output file</title>
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m.75 12 3 3m0 0 3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                            </svg>
                        </a>
                        <a v-if="isTaskBeingProcessed(task.status)" @click="revokeTask(task.task_id)"
                            class="cursor-pointer transition-transform duration-150 hover:scale-110 active:scale-90">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6 xl:size-8 m-auto">
                                <title>Revoke task</title>
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                            </svg>
                        </a>

                        <a v-if="!isTaskBeingProcessed(task.status)"
                            :class="themeStore.isDarkMode ? 'text-slate-500 cursor-pointer' : 'text-gray-300 cursor-pointer'">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6 xl:size-8 m-auto">
                                <title>Task already concluded</title>
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                            </svg>
                        </a>

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

function isPageLastElement(pgSize, elementIdx) {
    return pgSize - 1 === elementIdx ? true : false
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