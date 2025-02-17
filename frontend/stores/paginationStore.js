import { defineStore } from 'pinia'

export const usePaginationStore = defineStore('pagination', {
    state: () => ({
        page: 1,
        pageSize: 10,
        totalItems: 0,
        totalPages: 0
    }),
    actions: {
        setTotalItems(total) {
            this.totalItems = total
        },
        setPageSize(size) {
            this.pageSize = size
        },
        calcTotalPages() {
            this.totalPages = Math.ceil(this.totalItems / this.pageSize)
        },
        nextPage() {
            if (this.page < this.totalPages) {
                this.page++
            }
        },
        prevPage() {
            if (this.page > 1) {
                this.page--
            }
        },
        setPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.page = page
            }
        }
    },
    persist: true
})
