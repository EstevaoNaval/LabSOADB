import { useChemicalStore } from '~/stores/chemicalStore'
import { useChemicalSummaryStore } from '~/stores/chemicalSummaryStore'
import { useSelectedChemicalStore } from '~/stores/selectedChemicalStore'

export function createChemicalService(mode) {
  const chemicalStore = useChemicalStore()
  const chemicalSummaryStore = useChemicalSummaryStore()
  const selectedChemicalStore = useSelectedChemicalStore()

  if (mode === 'summary') {
    return {
      fetchSearch: () => chemicalSummaryStore.fetchSearchSummary(),
      fetchAll: () => chemicalSummaryStore.fetchAllChemicalsSummary()
    }
  } else {
    return {
      fetchSearch: () => chemicalStore.fetchSearch(),
      fetchAll: () => chemicalStore.fetchAllChemicals(),
      fetchSelectedChemical: (id) => selectedChemicalStore.fetchSelectedChemical(id)
    }
  }
}
