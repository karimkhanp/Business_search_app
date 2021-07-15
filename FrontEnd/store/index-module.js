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
    'set-categories'(state, categories) {
      state.categories = categories;
    },
    'set-country-groups'(state, countryGroups) {
        state.countryGroups = countryGroups;
    }

}

export const actions = {
    'load-categories'({commit}) {
        console.log(commit);
        return this.$axios.$get("/category").then((response)=> {
            commit('set-categories', response.Categories);
        });
    },
    'load-countrygroups'({commit}) {
        return this.$axios.$get("/listgroups").then((response)=> {
            commit('set-country-groups', response.data);
        })
    },
}
