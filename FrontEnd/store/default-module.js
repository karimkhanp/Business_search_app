export const state = () => ({
    counter: 0,
    categories: [],
    countryGroups: [],
});

export const getters = {
    categories: (state) => {
        return state.categories;
    },
    'country-groups': (state)=> {
        return state.countryGroups;
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
    'load-categories'({commit}) {
        console.log(commit);
        return this.$axios.$get("/category").then((response)=> {
            commit('setCategories', response.Categories);
        });
    },
    'load-countrygroups'({commit}) {
        return this.$axios.$get("/listgroups").then((response)=> {
            commit('setCountryGroups', response.data);
        })
    },
}
