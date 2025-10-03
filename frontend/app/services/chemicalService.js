import { useChemicalStore } from '~/stores/chemicalStore'
import { useChemicalSummaryStore } from '~/stores/chemicalSummaryStore'
import { useSelectedChemicalStore } from '~/stores/selectedChemicalStore'

export function createChemicalService(mode) {
  const chemicalStore = useChemicalStore()
  const chemicalSummaryStore = useChemicalSummaryStore()
  const selectedChemicalStore = useSelectedChemicalStore()

  if (mode === 'summary') {
    return {
      fetchSearch: (params = {}) => chemicalSummaryStore.fetchSearchSummary(params),
      fetchAll: (params = {}) => chemicalSummaryStore.fetchAllChemicalsSummary(params)
    }
  } else {
    return {
      fetchSearch: (params = {}) => chemicalStore.fetchSearch(params),
      fetchAll: (params = {}) => chemicalStore.fetchAllChemicals(params),
      fetchSelectedChemical: (id) => selectedChemicalStore.fetchSelectedChemical(id)
    }
  }
}
