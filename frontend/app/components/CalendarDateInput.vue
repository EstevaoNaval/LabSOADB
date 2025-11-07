<!-- components/CalendarDateInput.vue -->
<template>
    <div>
        <label v-if="label" class="label py-1">
            <span class="label-text text-xs">{{ label }}</span>
        </label>

        <!-- Native date input with calendar button -->
        <div class="relative">
            <input ref="dateInputRef" v-model="localValue" @change="handleDateChange" type="date" :min="minDate"
                :max="maxDate" class="input input-bordered input-sm w-full pr-8"
                :class="{ 'opacity-0': showCalendar }" />

            <!-- Custom calendar button overlay -->
            <button v-if="!useNativeOnly" :popovertarget="`cally-${componentId}`"
                class="btn btn-ghost btn-sm btn-square absolute right-0 top-0"
                :style="{ anchorName: `--cally-${componentId}` }" type="button" title="Open calendar">
                <CalendarIcon class="h-4 w-4" />
            </button>
        </div>

        <!-- Cally calendar popover (optional enhanced picker) -->
        <div v-if="!useNativeOnly" :id="`cally-${componentId}`" popover
            class="dropdown dropdown-end dropdown-top bg-base-100 rounded-box shadow-lg border border-base-300 p-4"
            :style="{ positionAnchor: `--cally-${componentId}` }">

            <calendar-date ref="callyRef" :locale="locale" class="cally" :value="localValue"
                @change="handleCalendarChange">

                <!-- Previous/Next month buttons - using raw SVG for web component slots -->
                <svg slot="previous" aria-label="Previous" xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-4 w-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
                </svg>

                <svg slot="next" aria-label="Next" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                    stroke-width="1.5" stroke="currentColor" class="h-4 w-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5L15.75 12l-7.5 7.5" />
                </svg>

                <!-- Year selector with dropdown AND prev/next buttons -->
                <div slot="heading" class="flex items-center justify-center gap-2 px-2">
                    <button @click.stop="changeYear(-1)" type="button" class="btn btn-ghost btn-xs"
                        title="Previous year">
                        <ChevronDoubleLeftIcon class="h-4 w-4" />
                    </button>

                    <select :value="currentYear" @change="handleYearSelect"
                        class="select select-bordered select-xs w-20 text-center font-semibold" title="Select year">
                        <option v-for="year in yearRange" :key="year" :value="year">
                            {{ year }}
                        </option>
                    </select>

                    <button @click.stop="changeYear(1)" type="button" class="btn btn-ghost btn-xs" title="Next year">
                        <ChevronDoubleRightIcon class="h-4 w-4" />
                    </button>
                </div>

                <calendar-month></calendar-month>
            </calendar-date>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { CalendarIcon, ChevronDoubleLeftIcon, ChevronDoubleRightIcon } from '@heroicons/vue/24/outline'

interface Props {
    modelValue: string
    label?: string
    locale?: string
    minYear?: number
    maxYear?: number
    useNativeOnly?: boolean
}

const props = withDefaults(defineProps<Props>(), {
    label: '',
    locale: 'pt-BR',
    minYear: 1900,
    maxYear: () => new Date().getFullYear() + 10,
    useNativeOnly: false
})

const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
}>()

const componentId = ref(`${Math.random().toString(36).substr(2, 9)}`)
const callyRef = ref<HTMLElement | null>(null)
const dateInputRef = ref<HTMLInputElement | null>(null)
const localValue = ref(props.modelValue)
const showCalendar = ref(false)

// Min and max dates for native input
const minDate = computed(() => `${props.minYear}-01-01`)
const maxDate = computed(() => `${props.maxYear}-12-31`)

// Year range for dropdown
const yearRange = computed(() => {
    return Array.from(
        { length: props.maxYear - props.minYear + 1 },
        (_, i) => props.minYear + i
    ).reverse()
})

// Current year for display
const currentYear = computed(() => {
    if (!localValue.value) return new Date().getFullYear()
    const date = new Date(localValue.value + 'T00:00:00')
    return date.getFullYear()
})

/**
 * Handle native date input change
 */
function handleDateChange(event: Event) {
    const target = event.target as HTMLInputElement
    const value = target.value

    localValue.value = value
    emit('update:modelValue', value)

    if (callyRef.value && value) {
        (callyRef.value as any).focusedDate = value
    }
}

/**
 * Handle Cally calendar date change
 */
function handleCalendarChange(event: Event) {
    const target = event.target as any
    const selectedDate = target.value

    localValue.value = selectedDate
    emit('update:modelValue', selectedDate)

    const popover = document.getElementById(`cally-${componentId.value}`)
    if (popover) popover.hidePopover()
}

/**
 * Handle year dropdown selection
 */
function handleYearSelect(event: Event) {
    const target = event.target as HTMLSelectElement
    const newYear = parseInt(target.value)

    const currentDate = localValue.value
        ? new Date(localValue.value + 'T00:00:00')
        : new Date()

    currentDate.setFullYear(newYear)

    const newDateString = toISOString(currentDate)
    localValue.value = newDateString

    if (callyRef.value) {
        (callyRef.value as any).focusedDate = newDateString
    }
}

/**
 * Change year with buttons
 */
function changeYear(offset: number) {
    const currentDate = localValue.value
        ? new Date(localValue.value + 'T00:00:00')
        : new Date()

    const newYear = currentDate.getFullYear() + offset

    if (newYear < props.minYear || newYear > props.maxYear) {
        return
    }

    currentDate.setFullYear(newYear)

    const newDateString = toISOString(currentDate)
    localValue.value = newDateString

    if (callyRef.value) {
        (callyRef.value as any).focusedDate = newDateString
    }
}

/**
 * Convert Date to ISO string (YYYY-MM-DD)
 */
function toISOString(date: Date): string {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
}

// Watch for external changes
watch(() => props.modelValue, (newVal) => {
    localValue.value = newVal
}, { immediate: true })

// Import Cally on mount
onMounted(async () => {
    if (!props.useNativeOnly && typeof window !== 'undefined' && !customElements.get('calendar-date')) {
        await import('cally')
    }
})
</script>
