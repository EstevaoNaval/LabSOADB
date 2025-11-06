import { defineStore } from 'pinia';

export const useHistogramRangeSliderStore = defineStore('histogramRangeSliderStore', {
    state: () => ({
        recentFilteredHistogram: null,
        properties: {
            jplogp: {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            },
            molecular_weight: {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            },
            tpsa: {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            },
            melting_point: {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            },
            h_bond_acceptor: {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            },
            h_bond_donor: {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            },
            heavy_atom: {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            },
            rotatable_bond: {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            },
            lipinski_violation: {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            },
            pains_alert: {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            },
        }
    }),

    actions: {
        roundToFlooringFiveMultiple(number) {
            return Math.floor(number / 5) * 5
        },

        roundToCeilingFiveMultiple(number) {
            return Math.ceil(number / 5) * 5
        },

        getArrMinValue(arr) {
            var minValue = Math.min(...arr)
            if (Math.abs(minValue) > 10) {
                minValue = this.roundToFlooringFiveMultiple(minValue)
            }
            return minValue
        },

        getArrMaxValue(arr) {
            var maxValue = Math.max(...arr)
            if (Math.abs(maxValue) > 10) {
                maxValue = this.roundToCeilingFiveMultiple(maxValue)
            }
            return maxValue
        },

        setInitialProperty(propName, propArr) {
            if (this.recentFilteredHistogram === propName) {
                return;
            }

            var minValue = this.getArrMinValue(propArr)
            var maxValue = this.getArrMaxValue(propArr)

            this.properties[propName].arr = propArr
            this.properties[propName].min = minValue
            this.properties[propName].max = maxValue
            this.properties[propName].minSelected = minValue
            this.properties[propName].maxSelected = maxValue
        },

        setFilterActivated(propName, isFilterActivated) {
            this.properties[propName].filterActivated = isFilterActivated
        },

        resetProperty(propName) {
            this.recentFilteredHistogram = null;
            this.properties[propName] = {
                filterActivated: false,
                arr: [],
                min: null,
                max: null,
                minSelected: null,
                maxSelected: null
            };
        },
    },
    persist: {
        storage: piniaPluginPersistedstate.localStorage(), // ✅ Correto
        omit: [ // ✅ Não persiste arrays grandes
          'properties.jplogp.arr',
          'properties.molecular_weight.arr',
          'properties.tpsa.arr',
          'properties.melting_point.arr',
          'properties.h_bond_acceptor.arr',
          'properties.h_bond_donor.arr',
          'properties.heavy_atom.arr',
          'properties.rotatable_bond.arr',
          'properties.lipinski_violation.arr',
          'properties.pains_alert.arr'
        ]
    }
})