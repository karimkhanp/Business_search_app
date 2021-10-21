<template>
  <div>
    <div class="main-slider custom-bg">
      <div class="gradient-bg w-100">
        <div class="container header-text-fix">
          <div class="row justify-content-between align-items-center">
            <div class="col-md-7 my-2">
              <h1 class="header-title text-left text-white">
                Leading experts to
                find Organisations that<br>
                suits works
              </h1>
              <p class="text-white text-left sub-text">
                Logipsum provide affordable, high-quality organisation to suit your work and gives you boost to expand your wings.
              </p>
            </div>
            <div class="col-md-5 my-2">
                <AppSearchCard
                    :countryGroups="countryGroups"
                    :jobTitles="jobTitles"
                    @removeCountry="RemoveCountry"
                    @search="SearchSubmitted"
                />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="isSearchDone" class="bottom-section">
      <div class="filter-section mb-4">
        <FilterSection
                :cities="cities"
                :states="states"
                :recordOptions="recordOptions"
                @searchByCity="searchByCity"
                @searchByState="searchByState"
                @searchOnFilter="searchOnFilter"
                @exportToFile="exportToFile"
            />
      </div>
          <KeywordCards
             :items="[{key: 'Category', value: category.join(', ')},
                      {key: 'Job Title', value: jobTitle},
                      {key: 'Country', value: country.join(', ')},
                      {key: 'City', value: city},
                      {key: 'Employee', value: employee.join(', ')}]"
             @remove="remove"/>
             <div v-if="getLoaderState" class="loader">
                <img :src="loader" alt="loader">
             </div>
      <div v-if="getLoaderState === false" class="filter-cards-section regular" >
        <div class="container"><div class="result-found"> About {{companies.length}} results found</div></div>
        <Filtercards :companies="companies"/>
      </div>
      <div v-if="!showMoreLoader">
        <button v-if="isSearchDone && companies && companies.length > 0 && !getLoaderState"  @click="fetchMore" class="btn-show-more text-white">Show more</button>
        <div class="text-center text-white" v-else-if="!getLoaderState">No Records found</div>
      </div>
      <div v-else-if="showMoreLoader" class="loader"> 
        <img :src="loader" alt="loader">
      </div>
      <div v-if="isSearchDone" class="most-viewed-organisation">
        <div class="container mt-5 mb-4">
          <p class="most-viewed-heading mb-0 text-white">Most viewed organisation for </p>
          <p class="most-viewed-term mb-0 text-white">
            {{ keyword }}
          </p>
        </div>
        <div  v-if="isSearchDone" class="filter-cards-section">
          <Filtercards :companies="popular"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Homeslider from '../components/homeSlider'
  import Filtercards from '../components/Filtercards'
  import { mapGetters } from "vuex";
  import constants from "../api/constants"
  import Multiselect from 'vue-multiselect'
  import KeywordCards from '../../FrontEnd/components/keyword-cards.vue';
  import FilterSection from '../components/Filtersection.vue';
  import { fas } from '@fortawesome/free-solid-svg-icons'
  import AppSearchCard from "../components/AppSearchCard.vue";
  import loader from  '../../FrontEnd/static/loader.svg'

  // var VueScrollTo = require("vue-scrollto");

  export default {
    layout: 'default',
    computed: {
       fas () {
         return fas
        },
      ...mapGetters({
        getCompanies: 'index-module/companies',
        getPopular : 'index-module/popular',
        getStates: 'index-module/states',
        getCities: 'index-module/cities',
        getKeywordsFromStore: 'index-module/keywords',
        getCategories: 'index-module/categories',
        getJobTitlesFromStore: 'index-module/job-titles',
        getCategories: 'index-module/categories',
        getJobTitles: 'index-module/job-titles',
        getLoaderState: 'index-module/getLoaderState',
        getPriorityName: 'index-module/getPriorityName'
      })
    },
    components: {
      Homeslider,
      FilterSection,
      Filtercards,
      Multiselect,
      KeywordCards,
      AppSearchCard
    },
    data() {
      return {
        loader,
        categories: [],
        countryGroups:  constants.COUNTRY_GROUPS,
        jobTitles: [],
        companies: constants.EMPTY_STRING,
        category : constants.EMPTY_STRING,
        jobTitle: constants.EMPTY_STRING,
        revenue: [],
        showModal: false,
        isSearching: false,
        countryList: [],
        countrySelected: [],
        selectedCountryGroup: [],
        page:1,
        scrollPosition: 0,
        view: constants.LIST,
        sliderMin: 0,
        sliderMax: 100,
        sliderVal: 80,
        sliderPos: null,
        isSearchDone: false,
        hasEqualSize: false,
        isSubscribed: false,
        isStateSelected: false,
        states: [],
        cities: [],
        emps: [constants.ANY_SMALLA],
        companies: [],
        popular: [],
        keywords: [],
        flips: [],
        popflips: [],
        lastId: null,
        type: constants.KEYWORD,
        rpp:15,
        country: [],
        newCountryL:[],
        state: constants.ALL,
        city: constants.ALL,
        keyword: constants.EMPTY_STRING,
        employee: [],
        companyValues:[],
        recordOptions: constants.RECORD_OPTIONS,
        showMoreLoader: false
      };
    },
    created() {
      this.getKeywords();
      this.updateValues();
      this.loadJobTitles();
    },
    watch: {
      sliderVal(newVal) {
        const chngedVal = Number(
          ((newVal - this.sliderMin) * 100) / (this.sliderMax - this.sliderMin)
        );
        this.sliderPos =
          this.sliderVal == 0
            ? `0px`
            : `calc(${chngedVal}% + (${3 - chngedVal * 0.15}px))`;
      },
    },
    mounted() {
      window.addEventListener("scroll", this.updateScroll);
    },
    methods: {
      SearchSubmitted(params) {
        this.isSearchDone = true;
        this.$store.commit('index-module/setLoaderState', true)
        const { industry, country, jobTitle, keyword, companies, countryList, employee, revenue} = params;
        this.category = [...industry];
        this.country = [ ...country, ...countryList];
        this.jobTitle = jobTitle;
        this.keyword = keyword;
        this.revenue = revenue;
        this.companies = companies ? companies.split(',') : [];
        this.employee = employee;
        this.countryList = countryList;
        this.search();
      },
      RemoveCountry(countrySelected) {
         this.countrySelected = countrySelected;
      },
      exportToFile() {
         const csvContent = "data:text/csv;charset=utf-8," + this.companies.map(company => JSON.stringify(company)).join(constants.NEW_LINE);
         window.open(encodeURI(csvContent));
      },
      remove(item) {
           switch(item) {
             case 'Category': {
               this.category = [];
               break;
             }
             case 'Job Title': {
               this.jobTitle = constants.EMPTY_STRING;
               break;
             }
             case 'Country': {
               this.country = [];
               break;
             }
             case 'City': {
               this.city = constants.EMPTY_STRING;
               break;
             }
             case 'Employee': {
               this.employee = [];
               break;
             }
             default: {
                this.resetAll();
             }
           }
           this.search();
      },
      resetAll() {
        this.category = [];
        this.jobTitle = constants.EMPTY_STRING;
        this.country = [];
        this.city = constants.EMPTY_STRING;
        this.employee = [];
      },
      updateScroll() {
        this.scrollPosition = window.scrollY;
      },
      searchOnFilter(rpp) {
        this.rpp = rpp;
        this.search();
      },
      removeFromSearch(){
        const filteredCountry = this.countryList.length > 0 ? this.countryList.filter((item)=> !this.countrySelected.includes(item)): [];
        this.country = [...this.country, ...filteredCountry];
      },
      scrollToTop() {
        window.scrollTo(0, 0);
      },
      toogleMenu() {
        var menu = document.getElementById("main-navbar");
        menu.classList.toggle("is-active");
      },

      toggleFlip(i) {
        if (this.flips.includes(i)) {
          this.flips.splice(this.flips.indexOf(i), 1);
          } else {
          this.flips.push(i);
          this.addPopularity(this.companies[i].id);
        }
      },

      togglePopFlip(i) {
        if (this.popflips.includes(i)) {
          this.popflips.splice(this.popflips.indexOf(i), 1);
          } else {
          this.popflips.push(i);
        }
      },

      SearchKeyword(keyword) {
        this.keyword = keyword;
        this.search_type = constants.KEYWORD;
        this.search();
      },

      compare(a, b) {
         return a.score > b.score ? -1: 1;
      },

      applyFilter() {
        this.isSearching = true;
        this.showModal = false;
        this.searchBySize();
      },

      updateValues() {
        const changedVal = Number(
          ((this.sliderVal - this.sliderMin) * 100) /
          (this.sliderMax - this.sliderMin)
        );
        this.sliderPos = this.sliderVal == 0 ? `0px` : `calc(${changedVal}% + (${3 - changedVal * 0.15}px))`;
      },

      addPopularity(id) {
          this.$store.dispatch("index-module/add-popularity", {id});
      },

      async search() {
        const employees = Object.values(this.employee).map((item)=> item);
        if(employees.includes(constants.ANY) && employees.length > 1) {
            const index = employees.indexOf(constants.ANY);
            employees.splice(index, 1);
        }
        this.employee = employees;
          if(this.country.length > 0) {
              this.newCountryL = [...this.country];
          }
          if(this.selectedCountryGroup.length > 0) {
              const loadedCountryL = this.selectedCountryGroup.reduce(async (newCountryL, selectedCountryGroup)=> {
                 await this.$store.dispatch("index-module/load-country-group", selectedCountryGroup);
                 newCountryL = [...newCountryL, ...this.getCountryList];
              }, []);
              this.newCountryL = [...this.newCountryL, ...loadedCountryL];
            }
            this.page = 1;
            this.performSearch();
            this.populatePopular();
            const parameters = this.country[0] !== constants.ANY_SMALLA?  { country: this.country }: {};
            this.postStates(parameters);
            this.postCities(parameters);
            this.hasEqualSize = this.newCountryL.length == this.rpp ? true : false;
      },
      performSearch(params=undefined) {
        const minMax = this.findMinMax(this.employee);
        const minMaxRevenue = this.findMinMax(this.revenue);
        if(!params) {
          this.$store.commit('index-module/setPriorityName', 'AssetName')
          params = {
            score: this.sliderVal,
            keyword: this.keyword,
            company_name: this.companies,
            Max_Revenue: isFinite(minMaxRevenue.max) ? minMaxRevenue.max : 0,
            Min_Revenue: isFinite(minMaxRevenue.min) ? minMaxRevenue.min : 0,
            employee: this.employee,
            Min_Num_Of_Employees: isNaN(minMax.min) ? 0 : minMax.min,
            Max_Num_Of_Employees: isNaN(minMax.max) ? 0 : minMax.max,
            search_type: this.type,
            country: this.newCountryL.length > 0 ? this.newCountryL:constants.EMPTY_STRING,
            state:  this.state !== constants.ALL ? this.state : constants.EMPTY_STRING,
            city: this.city !== constants.ALL ? this.city : constants.EMPTY_STRING,
            employee: !this.employee.includes(constants.ANY) ? this.employee : "1-10000000",
            category: this.category,
            jobtitle: this.jobTitle,
          };
        }
        this.isSearching = true; 
        const searchParameters = {
          rpp: this.rpp,
          page: this.page,
          params: params,
          priority: this.getPriorityName
        }
        this.$store.dispatch('index-module/search', searchParameters).then(()=> {
            this.getCompanies.forEach(company => this.companies.push(company));
            if(this.companies.length>0) {
              this.lastId = this.companies[this.companies.length - 1];
            }
            this.isSearching = false;
            this.$store.commit('index-module/setLoaderState', false)
            this.showMoreLoader = false
        });
      }, 

      populatePopular() {
        const params = {
          keyword: this.keyword,
          search_type: this.type,
          Country: this.country.join(constants.COMMA),
          Industry: this.category.join(constants.COMMA),
          JobTitle: this.jobTitle
        };
        this.$store.dispatch('index-module/load-popular', params).then(()=> {
             this.popular = this.getPopular;
        });
      },

      postStates(params) {
          this.$store.dispatch("index-module/post-states",  params ).then(()=>{
            this.states = this.getStates;
          });
      },
      postCities(params, all=constants.EMPTY_STRING) {
          this.$store.dispatch("index-module/post-cities", params ).then(()=> {
            this.cities = [...this.getCities];
            if(all) this.cities.push(all);
          });
      },
      loadJobTitles() {
        this.$store.dispatch('index-module/load-job-titles').then(()=> {
           this.jobTitles = this.getJobTitlesFromStore;
        });
      },
      findMinMax(employee) {
          const min =  Math.min(...employee.reduce((values, size)=> { values = [...values, parseInt(size.split("-")[0])]; return values;}, []));
          const max =  Math.max(...employee.reduce((values, size)=> { values = [...values, parseInt(size.split("-")[1])]; return values;}, []));
          return { min, max};
      },
      async searchByState(state) {
        this.state = state;
        this.removeFromSearch();
        this.page = 1;
        this.performSearch();
        let params = { state: this.state !== constants.ANY ? this.state : constants.EMPTY_STRING, country :this.newCountryL};
        this.postCities(params, constants.ALL); 
        this.city = constants.ALL;
      },

      async searchByCity(city) {
        this.city = city;
        this.removeFromSearch();
        this.page = 1;
        this.performSearch();
      },

      async fetchMore() {
        this.showMoreLoader = true
        this.removeFromSearch();
        this.page = this.page + 1;
        const params = {
            score: this.sliderVal,
            keyword: this.keyword,
            search_type: this.type,
            country: this.country !== constants.ANY_SMALLA ? this.country : constants.EMPTY_STRING,
            state:  this.state !== constants.ALL ? this.state : constants.EMPTY_STRING,
            city: this.city !== constants.ALL  ? this.city : constants.EMPTY_STRING,
            employee: !this.employee.includes(constants.ANY) ? this.employee : "1-10000000",
            category: this.category,
            jobtitle: this.jobTitle,
          }
        this.performSearch(params);
      },
      getKeywords() {
        this.$store.dispatch("index-module/load-keywords").then(()=> {
            this.keywords = this.getKeywordsFromStore;
        });
      },
      getClass(score){
        return score <=35?'is-critical': (score >35 && score <= 60)? 'is-good': constants.EMPTY_STRING;
      }
    },
  }
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
  .most-viewed-organisation {
    display: none;
  }

  .filter-cards-section.regular {
    margin-top: 50px;
  }

  .result-found {
    text-align: left;
    padding-left: 0;
    width: fit-content;
    color: #94999e;
    margin: 0;
  }

  .main-header nav.navbar{
    position: absolute;
    width: 100%;
  }
  .main-slider{
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .main-slider.custom-bg {
    background: url(./../assets/img/bg-image.jpg);
    background-size: cover;
    background-position: top;
  }
  .gradient-bg{
    background: linear-gradient(246.04deg, #031C32 22.45%, rgba(255, 0, 0, 0.3) 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-size: cover;
    background-position: 100% 100%;
  }
  .keep-walking{
    font-size: 24px;
    font-style: normal;
    font-weight: 700;
    line-height: 30px;
    letter-spacing: 0em;
    text-align: left;
  }
  .you-are-gem{
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: 20px;
    letter-spacing: 0em;
    text-align: left;
  }

  .btn-show-more{
    background: #B3365B;
    border-radius: 8px;
    padding: 10px 60px;
    border: 0;
    font-size: 18px;
    font-weight: 700;
    line-height: 23px;
  }
  .most-viewed-heading{
    font-size: 24px;
    font-style: normal;
    font-weight: 700;
    line-height: 30px;
    text-align: center;
  }
  .most-viewed-term{
    font-size: 24px;
    font-style: normal;
    font-weight: 700;
    line-height: 30px;
    text-align: center;
    color: #EBCACA !important;
  }
  .bottom-section{
    padding-top: 80px;
    padding-bottom: 80px;
  }
  .header-title{
    font-size: 48px;
    font-family: 'Mulish';
    font-style: normal;
    font-weight: 800;
    line-height: 58px;
    letter-spacing: 0em;
    text-align: left;
  }
  .sub-text{
    font-size: 20px;
    font-style: normal;
    font-weight: 400;
    line-height: 30px;
    letter-spacing: 0em;
    text-align: left;
  }

  body {
    font-family: Mulish;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    background: #031C32;
  }

  .card-tab-btn{
    display: inline-block;
    border: 1px solid #C6C6C6;
    box-sizing: border-box;
    border-radius: 8px;
    padding: 10px 20px;
    color: #374958;
    text-decoration: none;
    cursor: pointer;
  }
  .card-tab-btn:hover{
    text-decoration: none;
    color: #374958;
  }
  .card-tab-btn.active{
    border: 1px solid #B3365B;
    background: #B3365B;
    color: #fff;
  }

  .country-buttons a{
    border-radius: 6px;
    margin-right: 2px;
    padding: 8px 12px;
    font-weight: 600;
    font-size: 12px;
    line-height: 15px;
    display: inline-block;
  }

  .country-buttons a.active{
    background: rgba(179, 54, 91, 0.1);
    border: 1px solid rgba(179, 54, 91, 0.5);
    color: #B3365B;
  }
  .hr-seperator{
    border: 1px solid #C6C6C6;
    margin-top: 20px;
    margin-bottom: 15px;
  }
  .score-number{
    color: #B3365B;
  }
  .score-section{
    font-weight: 600;
    font-size: 14px;
    line-height: 18px;
  }

  .btn-search-lg{
    background: #B3365B;
    border-radius: 8px;
    padding: 0.75rem 60px;
    border: 0;
    line-height: 23px;
    width: 100%;
    font-size: 18px;
    font-style: normal;
    font-weight: 600;
    color: #E7E7E7;
  }

  .btn-search-lg:active{
      transform: scale(0.98);
      box-shadow: 3px 2px 22px 1px rgba(0, 0, 0, 0.24);
  }

  .vue-slider.vue-slider-ltr{
      margin-top: 35px;
  }

  .popular-heading,
  .popular-item{
    font-size: 14px;
    line-height: 18px;
    color: #374958;
  }
  .popular-heading{
    font-weight: 600;
  }
  .popular-item{
    font-weight: 700;
    cursor: pointer;
  }
  .popular-item a{
    border-bottom: 1px solid #C6C6C6;
  }

  .navbar-brand{
    font-size: 32px;
    font-weight: 700;
    line-height: 38px;
    text-align: left;
  }
  .nav-item a{
    font-size: 16px;
    font-weight: 600;
    line-height: 20px;
    text-align: left;
    color: #fff;
  }
 
  nav.navbar{
    position: absolute;
    width: 100%;
  }

  .bottom-section{
    text-align: center;
  }

  .vue-slider-process {
    background-color: #B3365B !important;
  }
  .vue-slider-dot-handle {
    border: 2px solid #B3365B;
    transition: box-shadow 0.3s, border-color 0.3s;
  }
  .vue-slider-dot-handle:hover,
  .vue-slider:hover .vue-slider-dot-handle,
  .vue-slider:hover .vue-slider-dot-handle:hover,
  .vue-slider:hover .vue-slider-process{
    border-color: #B3365B !important;
  }
  .vue-slider-dot-handle-focus{
    box-shadow: 0 0 0 0 !important;
  }
  .vue-slider-dot{
    width: 11px !important;
    height: 11px !important;
    cursor: pointer;
  }
  .vue-slider-dot-tooltip-inner {
    border-radius: 16px 16px;
    border-color: #B3365B !important;
    background-color: #B3365B !important;
    font-size: 12px;
    width: 30px;
    height: 26px;
    padding: 4px 0 0 0;
  }
  .vue-slider-dot-tooltip-inner-top::after {
    top: 89%;
    left: 50.4%;
    border-width: 10px;
  }

  .multiselect__element:hover{
    background-color: #EBCACA !important;
    color: #B3365B  !important;
  }

  .multiselect__option--highlight {
    background: #EBCACA  !important;
    outline: none;
    color: #B3365B  !important;
  }

  .multiselect__option--highlight::after {
    background: #EBCACA  !important;
    content: none;
    color: #B3365B  !important;
  }
  .multiselect__option--selected{
    content: none;
    background: #EBCACA;
    color: #B3365B;
  }

  .multiselect__input::before{
    background: olivedrab;
  }

  ::-webkit-scrollbar{
    width: 5px;
    height: 5px;
    border-radius: 8px;
  }

  ::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  } 

  ::-webkit-scrollbar-thumb {
    background: #ff3377;
    width: 5px;
    height: 45px;
    -webkit-box-shadow: inset 0 0 3px rgba(0,0,0,0.5);
  }

  input[type=checkbox] {
    border: 1px solid #B3365B;
    outline: 1px solid #B3365B;
    box-sizing: border-box;
    border-radius: 2px;
    background: #B3365B;
    outline-style: auto;
  }

  input:checked{
    color: #B3365B;
    background-color: green !important;
    background: green !important;
    background: #B3365B;
  }

  .multiselect__tags {
    padding: 10px 40px 3px 12px !important;
    min-height: 48px;
    border-radius: 8px !important;
    border: 1px solid #ced4da !important;
  }
  .multiselect__input, .multiselect__single{
    border-radius: 8px !important;
    line-height: 24px;
    font-size: 14px;
    font-weight: 600;
  }
  .country .multiselect__input,.country .multiselect__single{
    border-radius: 8px !important;
    line-height: 24px;
    padding: 0 0 0 32px;
  }
  .multiselect__content-wrapper{
    border-radius: 8px !important;
    margin-top: 10px;
    border: 1px solid #e8e8e8 !important;
    max-height: 220px !important;
  }
  .multiselect__content-wrapper .multiselect__element .option__desc > span input[type=checkbox]{
    top: 1px;
    position: relative;
  }
  .multiselect__content-wrapper .multiselect__element .option__desc span.option__small{
    margin-left: 12px;
    font-weight: 600;
  }

  .multiselect__content-wrapper .multiselect__element .option__desc span.option__small:nth-of-type(2) {
    margin-left: 36px;
  }

  .multiselect__select{
    height: 48px;
  }
  .multiselect__option{
    min-height: 44px;
  }
  
  .multiselect {
    min-height: 48px;
  }
  .multiselect__spinner {
    height: 46px;
    border-radius: 8px;
  }
  .multiselect--active .multiselect__tags {
    border-color: #B3365B !important;
  }

  .form-control:disabled{
     background: #EBCACA !important;
  }
  .multiselect__option--selected.multiselect__option--highlight:after,
  .multiselect__option--selected:after{
    content: '' !important;
  }
  .multiselect--active .icon {
    transform: rotate(180deg);
  }
  .country .multiselect::before{
    content: "\F07D9";
    z-index: 1;
  }
  .multiselect::before,
  .multiselect--active::after{
    display: inline-block;
    font: normal normal normal 24px/1 "Material Design Icons";
    text-rendering: auto;
    line-height: inherit;
    -webkit-font-smoothing: antialiased;
    position: absolute;
    top: 5px;
    left: 12px;
    font-size: 26px;
  }

.header-text-fix{
  margin-top:70px
}
.loader {
  position: relative;
  top: 20px;
}
</style>
