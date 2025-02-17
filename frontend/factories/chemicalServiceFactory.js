import { createChemicalService } from '~/services/chemicalService'

export function getChemicalService(mode) {
    return createChemicalService(mode)
}
