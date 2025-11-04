// composables/useAdvancedFilters.ts
import { ref, computed, reactive } from 'vue';

export interface FilterState {
  // Main query filters
  query: string;
  representation_type: string;
  search_type: string;
  similarity_threshold: number;
  
  // Citation filters
  citation: string;
  citation_type: string;
  
  // Literature filters
  doi: string;
  title: string;
  publication_date_after: string;
  publication_date_before: string;
  
  // Physical properties (ranges)
  molecular_weight__gte: number | null;
  molecular_weight__lte: number | null;
  volume__gte: number | null;
  volume__lte: number | null;
  count_atom__gte: number | null;
  count_atom__lte: number | null;
  count_heteroatom__gte: number | null;
  count_heteroatom__lte: number | null;
  count_heavy_atom__gte: number | null;
  count_heavy_atom__lte: number | null;
  count_aromatic_heavy_atom__gte: number | null;
  count_aromatic_heavy_atom__lte: number | null;
  count_rotatable_bond__gte: number | null;
  count_rotatable_bond__lte: number | null;
  count_h_bond_acceptor__gte: number | null;
  count_h_bond_acceptor__lte: number | null;
  count_h_bond_donor__gte: number | null;
  count_h_bond_donor__lte: number | null;
  count_ring__gte: number | null;
  count_ring__lte: number | null;
  count_carbon__gte: number | null;
  count_carbon__lte: number | null;
  mp_lower_bound__gte: number | null;
  mp_upper_bound__lte: number | null;
  state_of_matter: string;
  color: string;
  color_hexadecimal: string;
  
  // Physicochemical properties
  fraction_csp3__gte: number | null;
  fraction_csp3__lte: number | null;
  molar_refractivity__gte: number | null;
  molar_refractivity__lte: number | null;
  tpsa__gte: number | null;
  tpsa__lte: number | null;
  
  // Partition coefficients
  wildman_crippen_logp__gte: number | null;
  wildman_crippen_logp__lte: number | null;
  xlogp__gte: number | null;
  xlogp__lte: number | null;
  jplogp__gte: number | null;
  jplogp__lte: number | null;
  mouriguchi_logp__gte: number | null;
  mouriguchi_logp__lte: number | null;
  
  // Solubility
  esol_logs__gte: number | null;
  esol_logs__lte: number | null;
  filter_it_logs__lte: number | null;
  filter_it_logs__gte: number | null;
  
  // QSAR scores
  qed_score__gte: number | null;
  qed_score__lte: number | null;
  synthetic_accessibility_score__gte: number | null;
  synthetic_accessibility_score__lte: number | null;
  natural_product_score__gte: number | null;
  natural_product_score__lte: number | null;
  
  // Drug-like rules
  count_lipinski_violation__gte: number | null;
  count_lipinski_violation__lte: number | null;
  count_ghose_violation__gte: number | null;
  count_ghose_violation__lte: number | null;
  count_veber_violation__gte: number | null;
  count_veber_violation__lte: number | null;
  count_egan_violation__gte: number | null;
  count_egan_violation__lte: number | null;
  count_muegge_violation__gte: number | null;
  count_muegge_violation__lte: number | null;
  
  // Pharmacokinetics (boolean)
  gastrointestinal_absorption: boolean | null;
  blood_brain_barrier_permeation: boolean | null;
  
  // P450 inhibition (boolean)
  cyp1a2_inhibitor: boolean | null;
  cyp2c9_inhibitor: boolean | null;
  cyp2c19_inhibitor: boolean | null;
  cyp2d6_inhibitor: boolean | null;
  cyp3a4_inhibitor: boolean | null;
  
  // Undesirable substructure alerts
  count_pains_alert__gte: number | null;
  count_pains_alert__lte: number | null;
  count_brenk_alert__gte: number | null;
  count_brenk_alert__lte: number | null;
}

export const useAdvancedFilters = () => {
  const filters = reactive<FilterState>({
    // Main query
    query: '',
    representation_type: '',
    search_type: '',
    similarity_threshold: 0.51,
    
    // Citation
    citation: '',
    citation_type: '',
    
    // Literature
    doi: '',
    title: '',
    publication_date_after: '',
    publication_date_before: '',
    
    // Physical properties
    molecular_weight__gte: null,
    molecular_weight__lte: null,
    volume__gte: null,
    volume__lte: null,
    count_atom__gte: null,
    count_atom__lte: null,
    count_heteroatom__gte: null,
    count_heteroatom__lte: null,
    count_heavy_atom__gte: null,
    count_heavy_atom__lte: null,
    count_aromatic_heavy_atom__gte: null,
    count_aromatic_heavy_atom__lte: null,
    count_rotatable_bond__gte: null,
    count_rotatable_bond__lte: null,
    count_h_bond_acceptor__gte: null,
    count_h_bond_acceptor__lte: null,
    count_h_bond_donor__gte: null,
    count_h_bond_donor__lte: null,
    count_ring__gte: null,
    count_ring__lte: null,
    count_carbon__gte: null,
    count_carbon__lte: null,
    mp_lower_bound__gte: null,
    mp_upper_bound__lte: null,
    state_of_matter: '',
    color: '',
    color_hexadecimal: '',
    
    // Physicochemical
    fraction_csp3__gte: null,
    fraction_csp3__lte: null,
    molar_refractivity__gte: null,
    molar_refractivity__lte: null,
    tpsa__gte: null,
    tpsa__lte: null,
    
    // Partition coefficients
    wildman_crippen_logp__gte: null,
    wildman_crippen_logp__lte: null,
    xlogp__gte: null,
    xlogp__lte: null,
    jplogp__gte: null,
    jplogp__lte: null,
    mouriguchi_logp__gte: null,
    mouriguchi_logp__lte: null,
    
    // Solubility
    esol_logs__gte: null,
    esol_logs__lte: null,
    filter_it_logs__gte: null,
    filter_it_logs__lte: null,
    
    // QSAR
    qed_score__gte: null,
    qed_score__lte: null,
    synthetic_accessibility_score__gte: null,
    synthetic_accessibility_score__lte: null,
    natural_product_score__gte: null,
    natural_product_score__lte: null,
    
    // Drug-like rules
    count_lipinski_violation__gte: null,
    count_lipinski_violation__lte: null,
    count_ghose_violation__gte: null,
    count_ghose_violation__lte: null,
    count_veber_violation__gte: null,
    count_veber_violation__lte: null,
    count_egan_violation__gte: null,
    count_egan_violation__lte: null,
    count_muegge_violation__gte: null,
    count_muegge_violation__lte: null,
    
    // Pharmacokinetics
    gastrointestinal_absorption: null,
    blood_brain_barrier_permeation: null,
    
    // P450
    cyp1a2_inhibitor: null,
    cyp2c9_inhibitor: null,
    cyp2c19_inhibitor: null,
    cyp2d6_inhibitor: null,
    cyp3a4_inhibitor: null,
    
    // Alerts
    count_pains_alert__gte: null,
    count_pains_alert__lte: null,
    count_brenk_alert__gte: null,
    count_brenk_alert__lte: null,
  });
  
  const activeFiltersCount = computed(() => {
    let count = 0;
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== '' && value !== false) {
        count++;
      }
    });
    return count;
  });
  
  const getQueryParams = computed(() => {
    const params: Record<string, any> = {};
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== '' && value !== false) {
        params[key] = value;
      }
    });
    
    return params;
  });
  
  const resetFilters = () => {
    Object.keys(filters).forEach((key) => {
      const typedKey = key as keyof FilterState;
      if (typeof filters[typedKey] === 'boolean') {
        (filters[typedKey] as boolean | null) = null;
      } else if (typeof filters[typedKey] === 'number') {
        (filters[typedKey] as number | null) = null;
      } else {
        (filters[typedKey] as string | number) = '';
      }
    });
    
    // Reset defaults
    filters.similarity_threshold = 0.51;
  };
  
  const resetSection = (section: 'query' | 'literature' | 'physical' | 'physicochemical' | 'partition' | 'solubility' | 'qsar' | 'druglike' | 'pharmacokinetics' | 'p450' | 'alerts') => {
    const sectionMap: Record<string, (keyof FilterState)[]> = {
      query: ['query', 'representation_type', 'search_type', 'similarity_threshold', 'citation', 'citation_type'],
      literature: ['doi', 'title', 'publication_date_after', 'publication_date_before'],
      physical: ['molecular_weight__gte', 'molecular_weight__lte', 'volume__gte', 'volume__lte', 'count_atom__gte', 'count_atom__lte', 'count_heteroatom__gte', 'count_heteroatom__lte', 'count_heavy_atom__gte', 'count_heavy_atom__lte', 'count_aromatic_heavy_atom__gte', 'count_aromatic_heavy_atom__lte', 'count_rotatable_bond__gte', 'count_rotatable_bond__lte', 'count_h_bond_acceptor__gte', 'count_h_bond_acceptor__lte', 'count_h_bond_donor__gte', 'count_h_bond_donor__lte', 'count_ring__gte', 'count_ring__lte', 'count_carbon__gte', 'count_carbon__lte', 'mp_lower_bound__gte', 'mp_upper_bound__lte', 'state_of_matter', 'color', 'color_hexadecimal'],
      physicochemical: ['fraction_csp3__gte', 'fraction_csp3__lte', 'molar_refractivity__gte', 'molar_refractivity__lte', 'tpsa__gte', 'tpsa__lte'],
      partition: ['wildman_crippen_logp__gte', 'wildman_crippen_logp__lte', 'xlogp__gte', 'xlogp__lte', 'jplogp__gte', 'jplogp__lte', 'mouriguchi_logp__gte', 'mouriguchi_logp__lte'],
      solubility: ['esol_logs__gte', 'esol_logs__lte', 'filter_it_logs__gte', 'filter_it_logs__lte'],
      qsar: ['qed_score__gte', 'qed_score__lte', 'synthetic_accessibility_score__gte', 'synthetic_accessibility_score__lte', 'natural_product_score__gte', 'natural_product_score__lte'],
      druglike: ['count_lipinski_violation__gte', 'count_lipinski_violation__lte', 'count_ghose_violation__gte', 'count_ghose_violation__lte', 'count_veber_violation__gte', 'count_veber_violation__lte', 'count_egan_violation__gte', 'count_egan_violation__lte', 'count_muegge_violation__gte', 'count_muegge_violation__lte'],
      pharmacokinetics: ['gastrointestinal_absorption', 'blood_brain_barrier_permeation'],
      p450: ['cyp1a2_inhibitor', 'cyp2c9_inhibitor', 'cyp2c19_inhibitor', 'cyp2d6_inhibitor', 'cyp3a4_inhibitor'],
      alerts: ['count_pains_alert__gte', 'count_pains_alert__lte', 'count_brenk_alert__gte', 'count_brenk_alert__lte'],
    };
    
    const keys = sectionMap[section] || [];
    keys.forEach((key) => {
      if (typeof filters[key] === 'boolean') {
        (filters[key] as boolean | null) = null;
      } else if (typeof filters[key] === 'number') {
        (filters[key] as number | null) = null;
      } else {
        (filters[key] as string | number) = '';
      }
    });
  };
  
  return {
    filters,
    activeFiltersCount,
    getQueryParams,
    resetFilters,
    resetSection,
  };
};
