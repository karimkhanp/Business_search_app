export const state = () => ({
    counter: 0,
    categories: [],
    countryGroups: [],
    countryList: [],
    jobTitles: [],
    companies: [],
    popular: [],
    states: [],
    cities: [],
    keywords: []
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
    },
    companies: (state)=> {
        return state.companies;
    },
    popular: (state) => {
        return state.popular;
    },
    states: (state) => {
        return state.states;
    },
    cities: (state) => {
        return state.cities;
    },
    keywords: (state) => {
        return state.keywords;
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
    },
    'set-companies'(state, companies) {
        companies = companies.sort(compare);
        state.companies = companies;
    },
    'set-popular'(state, popular) {
        state.popular = popular;
    },
    'set-states'(state, states) {
        state.states = states;
    },
    'set-cities'(state, cities) {
        state.cities = cities;
    },
    'set-keywords'(state, keywords) {
        state.keywords = keywords;
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
    },
    'add-popularity'(id) {
        return this.$axios.$post("/add_popularity", {id});
    },
    search({commit}, parameters) {
        return this.$axios.$post("/search?limit="+parameters.rpp+"&page="+parameters.page, parameters.params).then((response)=> {
            commit('set-companies', response.data);
        });
    },
    'load-popular'({commit}, params) {
        return this.$axios.$get("/popular", { params }).then((response)=> {
            commit('set-popular', response.data);
        });
    },
    'post-states'({commit}, params={}) {
        return this.$axios.$post("/states", params).then((response)=> {
           commit('set-states', response.data);
        });
    }, 
    'post-cities'({commit}, params={}) {
        return this.$axios.$post("/cities", params).then((response)=> {
            commit('set-cities', response.data);
        });
    },
    'load-keywords'({commit}) {
        return this.$axios.$get("/keywords").then((response)=> {
            commit('set-keywords', response.data);
        });
    }

}

export const compare=(a,b)=> a.score > b.score ? -1: 1;
