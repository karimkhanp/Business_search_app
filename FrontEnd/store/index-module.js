export const state = () => ({
    counter: 0,
    categories: [],
    countryGroups: [],
    countryList: [],
    jobTitles: []
});

export const getters = {
    categories: (state) => {
        return state.categories;
    },
    'country-groups': (state)=> {
        return state.countryGroups;
    },
    'country-list': (state)=> {
        return state.countryList;
    },
    'job-titles': (state)=> {
        return state.jobTitles;
    }
}
  
export const mutations = {
    'set-categories'(state, categories) {
      state.categories = categories;
    },
    'set-country-groups'(state, countryGroups) {
        state.countryGroups = countryGroups;
    },
    'set-country-list'(state, countryList) {
        state.countryList = countryList;
    },
    'set-job-titles'(state, jobTitles) {
        state.jobTitles = jobTitles;
    }

}

export const actions = {
    'load-categories'({commit}) {
        return this.$axios.$get("/category").then((response)=> {
            commit('set-categories', response.Categories);
        });
    },
    'load-country-groups'({commit}) {
        return this.$axios.$get("/listgroups").then((response)=> {
            commit('set-country-groups', response.data);
        })
    },
    'load-country-group'({commit}, selectedCountry) {
        return this.$axios.$get("/group?country_group=" + selectedCountry).then((response)=> {
             commit('set-country-list', response.Countries);
        });
    },
    'load-job-titles'({commit}) {
        return this.$axios.$get("/jobtitle").then((response)=> {
             commit('set-job-titles', response.Titles);
        });
    }
}
