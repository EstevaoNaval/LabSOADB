// /composables/usePagination.js
import { reactive } from 'vue';

export function usePagination(initialPage = 1, pageSize = 10, totalItems = 0) {
    const state = reactive({
        page: initialPage,
        pageSize: pageSize,
        totalItems: totalItems
    });

    const setTotalItems = (total) => {
        state.totalItems = total
    };

    const setPageSize = (size) => {
        state.pageSize = size
    };

    const getTotalPages = () => {
        return Math.ceil(state.totalItems / state.pageSize)
    };

    const nextPage = () => {
        let totalPages = getTotalPages()

        if (state.page < totalPages) {
            state.page++
        }
    };

    const prevPage = () => {
        if (state.page > 1) {
            state.page--
        }
    };

    const setPage = (page) => {
        let totalPages = getTotalPages()

        if (page >= 1 && page <= totalPages) {
            state.page = page
        }
    }

    return { state, setTotalItems, setPageSize, getTotalPages, nextPage, prevPage, setPage };
}
