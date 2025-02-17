export default class ChemicalDataProcessor {
    constructor(chemicalData) {
        this.chemicalData = chemicalData; // Array of results
    }

    // Function to group properties, including flattening of melting point range
    groupByProperty() {
        return {
            
            molecular_weight: this.extractPropertyValues('physical_property.molecular_weight'),
            //count_rotatable_bond: this.extractPropertyValues('physical_property.count_rotatable_bond'),
            //tpsa: this.extractPropertyValues('physicochemical_property.tpsa'),
            // Flatten mp_lower_bound and mp_upper_bound into one array
            melting_point: this.flattenRangeValues(
                'physical_property.mp_lower_bound', 
                'physical_property.mp_upper_bound'
            ),
            //jplogp: this.extractPropertyValues('partition_coefficient.jplogp')
        };
    }

    // Function to extract normal properties
    extractPropertyValues(propertyPath) {
        return this.chemicalData.map(chemical => this.getNestedValue(chemical, propertyPath.split('.')));
    }

    // Function to flatten range values (mp_lower_bound and mp_upper_bound)
    flattenRangeValues(lowerBoundPath, upperBoundPath) {
        return this.chemicalData.reduce((acc, chemical) => {
            const lowerBound = this.getNestedValue(chemical, lowerBoundPath.split('.'));
            const upperBound = this.getNestedValue(chemical, upperBoundPath.split('.'));    
        
            // Flatten: Push only non-null values into the array
            if (lowerBound != null) acc.push(lowerBound);
            if (upperBound != null) acc.push(upperBound); 
            return acc;
        }, []); // Start with an empty array
    }

    // Function to navigate nested objects
    getNestedValue(obj, pathArray) {
        return pathArray.reduce((acc, key) => acc && acc[key], obj);
    }
}
  