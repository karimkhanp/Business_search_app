export const state = () => ({
    counter: 0,
    categories: [],
    countryGroups: [],
});

export const getters = {
    categories: (state)=> {
        return state.categories;
    }
}
  
export const mutations = {
    setCategories(state, categories) {
      state.categories = categories;
    },
    setCountryGroups(state, countryGroups) {
        state.countryGroups = countryGroups;
    }

}

export const actions = {
    'load-categories'() {
        return this.$axios.$get("/category").then((categories)=> {
            commit('setCategories', categories);
        });
    },
    'load-countrygroups'() {
        return this.$axios.$get("/listgroups").then((countryGroups)=> {
            commit('setCountryGroups', countryGroups);
        })
    },
    
}
