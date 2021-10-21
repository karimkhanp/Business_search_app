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
    keywords: [],
    loader: false
});

export const getters = {
    categories: (state) => {
        return state.categories;
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
    },
    getLoaderState: (state) => {
        return state.loader
    },
    getPriorityName: (state) => {
        return state.priorityName
    }
}

export const mutations = {
    'set-categories'(state, categories) {
      state.categories = categories;
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
    },
    'setLoaderState' (state, value) {
        state.loader = value
    },
    'setPriorityName' (state, value) {
        state.priorityName = value
    }
}

export const actions = {
    'load-categories'({commit}) {
        return this.$axios.$get("/category").then((response)=> {
            commit('set-categories', response.Categories);
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
        let formData = new FormData();
        Object.keys(parameters.params).forEach((key) => {
            formData.append(key, parameters.params[key]);
        });
        return this.$axios.$post("/search?limit=" + parameters.rpp + "&page=" + parameters.page + "&search_for=" + parameters.priority, formData, {'Content-Type': 'multipart/form-data'}).then((response)=> {
            commit('set-companies', response.data);
            commit('setPriorityName', response.next_search_for);
        });
    },
    'load-popular'({commit}, params) {
        return this.$axios.$get("/popular", { params }).then((response)=> {
            commit('set-popular', response.data);
        });
    },
    'post-states'({commit}, params=undefined) {
        if(!params) return this.$axios.$post("/states").then((response)=> commit('set-states', response.data));
        return this.$axios.$post("/states", params).then((response)=> commit('set-states', response.data));
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
