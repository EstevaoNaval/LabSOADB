import { defineStore } from 'pinia';

export const useSortStore = defineStore('sort', {
    state: () => ({
        currSortOptionId: 0,
        ascDirection: true,
        sortOptions: [
            {
                id: 0,
                name: 'Relevance',
                value: '',
            },
            {
                id: 1,
                name: 'Chemical ID',
                value: 'api_id'
            },
            {
                id: 2,
                name: 'Molecular Weight',
                value: 'physical_properties__molecular_weight'
            },
            {
                id: 3,
                name: 'Melting Point',
                value: 'physical_properties__mp_lower_bound'
            },
            {
                id: 4,
                name: "Lipinski's Rule of Five Count",
                value: 'druglike_rules__count_lipinski_violation'
            },
            {
                id: 5,
                name: 'PAINS Alert Count',
                value: 'count_pains_alert'
            },
            {
                id: 6,
                name: 'H-Bond Acceptor Count',
                value: 'physical_properties__count_h_bond_acceptor'
            },
            {
                id: 7,
                name: 'H-Bond Donor Count',
                value: 'physical_properties__count_h_bond_donor'
            },
            {
                id: 8,
                name: 'Heavy Atom Count',
                value: 'physical_properties__count_heavy_atom'
            },
            {
                id: 9,
                name: 'Polar Area',
                value: 'physicochemical_properties__tpsa'
            },
            {
                id: 10,
                name: 'Rotatable Bond Count',
                value: 'physical_properties__count_rotatable_bond'
            },
            {
                id: 11,
                name: 'JPLogP',
                value: 'partition_coefficients__jplogp'
            },
            {
                id: 12,
                name: 'Create Date',
                value: 'created_at'
            },
        ]
    }),
    actions: {
        setCurrSortOptionId(sortOptionId) {
            this.currSortOptionId = sortOptionId
        },
        setSortDirection(sortDirection) {
            this.ascDirection = sortDirection;
        },
        getCurrSortOption() {
            return this.ascDirection === true ? this.sortOptions[this.currSortOptionId].value : `-${this.sortOptions[this.currSortOptionId].value}`
        },
        toggleSortDirection() {
            this.ascDirection = !this.ascDirection;
        }
    },
    persist: true
});