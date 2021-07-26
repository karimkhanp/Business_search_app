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
              <div class="search-card">
                <h3 class="card-title mb-4">Search Organisations</h3>
                <div class="input-group custom-input-group mb-3">
                 <multiselect v-model="product" :options="products"
                    :multiple="false"
                    :close-on-select="true"
                    :clear-on-select="false"
                    :hideSelected="false"
                    :taggable="false"
                    placeholder="Product being promoted"
                    :preserve-search="true"
                    :internal-search="false"
                    @search-change="asyncFindProducts" >
                    <template slot="selection" slot-scope="{ values }">
                      <span class="multiselect__single" v-if="values.length">{{values[0]}}</span>
                    </template>
                    <template slot="option" slot-scope="props">
                      <div class="option__desc">
                        <span v-if="countryValues.includes(props.option)">
                          <input type="checkbox" value="" checked>
                        </span>
                        <span v-else> <input type="checkbox" value=""></span>
                        <span class="option__small">{{ props.option }}</span>
                      </div>
                    </template>
                    <template slot="selection">
                      <span class="mdi mdi-magnify"></span>
                    </template>
                  </multiselect>
                </div>
                <div class="input-group custom-input-group mb-3">
                  <div class="input-group-prepend">
                    <span class="input-group-text-custom" id="basic-addon1">
                      <span class="mdi mdi-magnify"></span>
                    </span>
                  </div>
                  <input type="text" class="form-control" placeholder="e.g Ux Designer" aria-label="Username" v-model="keyword" aria-describedby="basic-addon1" required>
                </div>
                <div class="input-group custom-input-group mb-3 mag-icon-search">
                  <multiselect
                    v-model="category"
                    :options="categories"
                    :multiple="false"
                    :close-on-select="true"
                    :clear-on-select="false"
                    :hideSelected="false"
                    :taggable="false"
                    placeholder="Category"
                    :preserve-search="true"
                    :internal-search="false"
                    @search-change="asyncFindCategories" >
                    <template slot="selection" slot-scope="{ values, search, isOpen }">
                      <span class="multiselect__single" style="padding-left: 0px;" v-if="values.length">{{values[0]}}</span>
                    </template>
                    <span class="arrow" style="position: absolute; right: 0;margin:7px; font-size: 1.4rem;" slot="caret"><i class="mdi mdi-chevron-down"></i></span>
                  </multiselect>
                </div>
                <div class="input-group custom-input-group mb-3 mag-icon-search">
                <multiselect
                    v-model="jobTitle"
                    
                    @search-change="asyncFindJobTitles" 
                    :options="jobTitles"
                    :multiple="false"
                    :close-on-select="true"
                    :clear-on-select="true"
                    :hideSelected="false"
                    :taggable="false"
                    placeholder="Job Title"
                    :internal-search="false"
                    :preserve-search="true"
                     >
                    <template slot="selection" slot-scope="{ values, search, isOpen }">
                      <span class="multiselect__single" style="padding-left: 0px;" v-if="values.length">{{values[0]}}</span>
                    </template>
                    <template slot="noOptions">{{jobSearchSlotText}}</template>
                    <template slot="noResult">{{jobSearchSlotText}}</template>
                    <template slot="spinner">Searching Please Wait...</template>
                    <span class="arrow" style="position: absolute; right: 0;margin:7px; font-size: 1.4rem;" slot="caret"><i class="mdi mdi-chevron-down"></i></span>
                  </multiselect>
                </div>
                <div class="country">
                 <multiselect
                    v-model="country"
                    :options="countries"
                    :multiple="true"
                    :internal-search="false"
                    :close-on-select="false"
                    :clear-on-select="false"
                    :hideSelected="false"
                    :taggable="false"
                    placeholder="Any Country"
                    :preserve-search="true"
                    @search-change="asyncFindCountries">
                    <template slot="selection" slot-scope="{ values }">
                      <span class="multiselect__single" v-if="values.length">{{values[0]}}</span>
                    </template>
                    <template
                      slot="option"
                      slot-scope="props">
                      <div class="option__desc">
                        <span v-if="countryValues.includes(props.option)">
                          <input type="checkbox" value="" checked>
                        </span>
                        <span v-else>
                          <input type="checkbox" value="">
                        </span>
                        <span class="option__small">{{ props.option }}</span>
                      </div>
                    </template>
                    <template slot="selection">
                      <span class="mdi mdi-magnify"></span>
                    </template>
                  </multiselect>
                </div>

                <div class="country-buttons text-left my-4" >
                  <a class="card-tab-btn" v-on:click="showCountry(selectedCountry)" :class="selectedCountryGroup == selectedCountry ? 'active' : ''" :key="index" v-for="selectedCountry, index in countryGroups">{{selectedCountry}}</a>
                 <div class="show-city mt-3" v-if="isHidden == true">
                      <div class="close-city">
                          <a class="btn-dark " v-on:click="isHidden = false">x</a>
                      </div>
                      <div class="city-list">
                          <a class="card-tab-btn " @click="removeCountry(city)" :key="index" v-for="city, index in countryList">
                            {{city}} 
                            <span v-if="!countrySelected.includes(city)" class="mdi mdi-check-bold ml-2"></span>
                          </a>
                      </div>
                </div>
                </div>
                <button class="btn-search-lg text-white my-4" type="button" data-toggle="button" @click="search"  :disabled="keyword.trim() == ''" title="Search" >Search</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isSearchDone" class="bottom-section">
      <div class="filter-section mb-4">
        <div class="container">
          <div class="main-filter-section">
            <div class="form-row">
              <div class="form-group col-md-2 text-left">
                <label class="typo__label">State</label>
                <multiselect
                  v-model="state"
                  :options="states"
                  :multiple="false"
                  :preselect-first="true"
                  placeholder="Any"
                  :close-on-select="true"
                  @input="searchByState"

                  :clear-on-select="false"
                  :preserve-search="true" >

                  <template slot="selection"
                            slot-scope="{ values, search, isOpen }">
                    <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
                  </template>
                  <template slot="option" slot-scope="props">
                    <div class="option__desc">
                      <span class="option__small" v-html="props.option"></span>
                    </div>
                  </template>
                </multiselect>
              </div>
              <div class="form-group col-md-3 text-left">
                <label class="typo__label">City</label>
                <multiselect
                  v-model="city"
                  :options="cities"
                  :multiple="false"
                  :preselect-first="true"
                  placeholder="Any"
                  :close-on-select="true"
                  @input="searchByCity"
                  :clear-on-select="false"
                  :preserve-search="true" >

                  <template slot="selection"
                            slot-scope="{ values, search, isOpen }">
                    <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
                  </template>
                  <template slot="option" slot-scope="props">
                    <div class="option__desc">
                      <span class="option__small" v-html="props.option"></span>
                    </div>
                  </template>
                </multiselect>
              </div>

              <div class="form-group col-md-3 text-left">
                <label class="typo__label">Company Size</label>
                <multiselect
                  v-model="employee"
                  :options="companySizes"
                  :multiple="true"
                  :preselect-first="true"
                  placeholder="Any"
                  :close-on-select="false"
                  @input="searchBySize"
                  :clear-on-select="false"
                  :preserve-search="true" >

                  <template slot="selection"
                            slot-scope="{ values, search, isOpen }">
                    <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
                  </template>
                  <template slot="option" slot-scope="props">
                    <div class="option__desc">
                      <span v-if="companyValues.includes(props.option)">
                        <input type="checkbox" value="" checked>
                      </span>
                      <span v-else>
                        <input type="checkbox" value="">
                      </span>
                      <span class="option__small" v-html="props.option"></span>
                    </div>
                  </template>
                </multiselect>
              </div>
              <div class="form-group col-md-2 text-left">
                <label for="inputPages">Records</label>
                <multiselect
                  v-model="rpp"
                  :options="recordOptions"
                  :multiple="false"
                  :preselect-first="true"
                  placeholder="Any"
                  :close-on-select="true"
                  @input="search"
                  :clear-on-select="false"
                  :preserve-search="true" >
                  <template slot="selection" slot-scope="{ values, search, isOpen }">
                    <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
                  </template>
                  <template slot="option" slot-scope="props">
                  </template>
                </multiselect>
              </div>
              <div class="file-export form-groupp col-md-2 text-left">
                  <button class="btn btn-primary" v-on:click="exportToFile"> <font-awesome-icon :icon="fas.faFileExport" /></button>
              </div> 
            </div> 
          </div>
        </div>
      </div>

      <div class="container">
           <KeywordCards
             :category="category"
             :jobTitle="jobTitle"
             :country="country"
             :city="city"
             :employee="employee"
             v-on:remove="remove" />
      </div>

      <div v-if="isSearchDone" class="keep-walking-section mb-4">
        <div class="container">
          <p class="keep-walking mb-0 text-white">Keep Walking</p>
          <p class="you-are-gem mb-0 text-white">You are the Gem</p>
        </div>
      </div>

      <div v-if="isSearchDone" class="filter-cards-section" >
        <Filtercards  :companies="companies"/>
      </div>

      <button v-if="isSearchDone && companies && companies.length > 0 "  @click="fetchMore" class="btn-show-more text-white">Show more</button>
      <div class="text-center text-white" v-else>No Records found</div>
      <div v-if="isSearchDone" class="most-viewed-organisation">
        <div class="container mt-5 mb-4">
          <p class="most-viewed-heading mb-0 text-white">Most viewed organisation for </p>
          <p class="most-viewed-term mb-0 text-white">
            {{ keyword }}
          </p>
        </div>
        <div  v-if="isSearchDone" class="filter-cards-section">
          <Filtercards  :companies="popular"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Homeslider from '../components/homeSlider'
  import Filtersection from '../components/Filtersection'
  import Filtercards from '../components/Filtercards'
  import { mapGetters } from "vuex";
  import constants from "../api/constants"
  import Multiselect from 'vue-multiselect'
  import { fas } from '@fortawesome/free-solid-svg-icons'
  import { KeywordCards } from '../../FrontEnd/components/keyword-cards.vue';

  var VueScrollTo = require("vue-scrollto");

  export default {
    layout: 'default',
    computed: {
       fas () {
         return fas
        },
      ...mapGetters({
        getCategories: 'index-module/categories',
        getCountryGroups: 'index-module/country-groups',
        getCountryList: 'index-module/country-list',
        getJobTitlesFromStore: 'index-module/job-titles',
        getCompanies: 'index-module/companies',
        getPopular : 'index-module/popular',
        getStates: 'index-module/states',
        getCities: 'index-module/cities',
        getKeywordsFromStore: 'index-module/keywords'
      })
    },
    components: {
      Homeslider,
      Filtersection,
      Filtercards,
      Multiselect
    },
    data() {
      return {
        category : constants.EMPTY_STRING,
        categories : [],
        constCategories:[],
        jobTitle: constants.EMPTY_STRING,
        jobTitles: [],
        constJobTitles:[],
        jobSearchSlotText: constants.LOADING,
        showModal: false,
        isSearching: false,
        countryList: [],
        countryGroups:[],
        countrySelected: [],
        selectedCountryGroup: [],
        isHidden: false,
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
        countries: constants.COUNTRIES,
        states: [],
        cities: [],
        emps: [constants.ANY_SMALLA],
        companies: [],
        products:constants.PRODUCTS,
        popular: [],
        keywords: [],
        flips: [],
        popflips: [],
        lastId: null,
        type: constants.KEYWORD,
        rpp:15,
        country: [],
        product:[],
        newCountryL:[],
        state: constants.ALL,
        city: constants.ALL,
        keyword: constants.EMPTY_STRING,
        employee: constants.ANY,
        countryValues:[],
        companyValues:[],
        companySizes: [
          'Any', '1-99', '100-249', '250-499', '500-999', '1000-4999', '5000-9999', '10000+'
        ],
        recordOptions: [
          '15', '50', '80', '100'
        ]
      };
    },
    created() {
      this.getKeywords();
      this.updateValues();
      this.loadCountryGroups();
      this.loadCategories();
      this.getJobTitles();
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
      exportToFile() {
         const csvContent = "data:text/csv;charset=utf-8," + this.companies.map(company => company.join(constants.COMMA)).join(constants.NEW_LINE);
         window.open(encodeURI(csvContent));
      },
      remove(item) {
           switch(item) {
             case 'category': {
               this.category = constants.EMPTY_STRING;
               break;
             }
             case 'jobTitle': {
               this.jobTitle = constants.EMPTY_STRING;
               break;
             }
             case 'country': {
               this.country = [];
               break;
             }
             case 'city': {
               this.city = constants.EMPTY_STRING;
               break;
             }
             default: this.employee = constants.EMPTY_STRING
           }
           this.search();
      },
      updateScroll() {
        this.scrollPosition = window.scrollY;
      },
      notEmptyAndNull(item) {
         return item!=null && item!= constants.EMPTY_STRING;
      },
      async asyncFindCategories(query) {
        if(query!=constants.EMPTY_STRING) {
          this.categories = this.constCategories.filter(industry=> this.notEmptyAndNull(industry) && industry.toLowerCase().startsWith(query.toLowerCase()));
        }
      },
      async asyncFindJobTitles(query) {
        this.jobTitles = this.constJobTitles.filter(job => job.toLowerCase().startsWith(query.toLowerCase()));
      },
      async asyncFindProducts(query) {
        this.products = constants.PRODUCTS.filter((product) =>product.toLowerCase().startsWith(query.toLowerCase()));
      },
      async asyncFindCountries(query) {
        this.countries = constants.COUNTRIES.filter((country)=> country.toLowerCase().startsWith(query.toLowerCase()));
      },
      showCountry(selectedCountry) {
        if(this.selectedCountryGroup.includes(selectedCountry)) {
          var index = this.selectedCountryGroup.indexOf(selectedCountry);
          this.selectedCountryGroup.splice(index, 1);
          this.isHidden = false;
        }  else  {
          this.selectedCountryGroup.push(selectedCountry);
          this.isHidden = true;
          this.$store.dispatch('index-module/load-country-group', selectedCountry).then(()=> {
              this.countryList = this.getCountryList;
          });
        }
      },
      getJobTitles() {
        this.$store.dispatch('index-module/load-job-titles').then(()=> {
              this.jobTitles= this.getJobTitlesFromStore;
              this.constJobTitles = this.getJobTitlesFromStore;
        });
      },

      loadCountryGroups() {
        this.$store.dispatch('index-module/load-country-groups').then(()=> {
            this.countryGroups = this.getCountryGroups;
        });
      },
      loadCategories() {
        this.$store.dispatch('index-module/load-categories').then(()=> {
            let categories = this.getCategories;
            this.categories =  categories.filter((category)=> category!=null && (/[a-zA-Z]/).test(category.charAt(0)));
            this.constCategories = categories;
        });
      },
      removeCountry(city){
          const index = this.countrySelected.indexOf(city);
          if (index > -1) {
            this.countrySelected.splice(index, 1);
          } else {
            this.countrySelected.push(city);
          }
      },

      removeFromSearch(){
        this.country = this.countryList.filter((item)=> !this.countrySelected.includes(item));
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

      search() {
        this.state = constants.ALL;
        if(this.country.length > 0) {
          this.newCountryL = [...this.country];
        }
        if(this.selectedCountryGroup.length > 0) {
                   this.$store.dispatch("index-module/load-country-group", this.selectedCountryGroup[0]).then(()=> {
                   this.newCountryL = [...this.newCountryL, ...this.getCountryList];
                   this.page = 1;
                   this.performSearch();
                   this.populatePopular();
                   const parameters = this.country[0] !== constants.ANY_SMALLA?  { country: this.country }: {};
                   this.postStates(parameters);
                   this.postCities(parameters);
                   this.hasEqualSize = this.newCountryL.length == this.rpp ? true : false;
        });
        }
      },
      performSearch(params=undefined) {
        if(!params) {
            params = {
                  score: this.sliderVal,
                  keyword: this.keyword,
                  search_type: this.type,
                  country: this.newCountryL.length > 0 ? this.newCountryL:constants.EMPTY_STRING,
                  state:  this.state !== constants.ALL ? this.state : constants.EMPTY_STRING,
                  city: this.city !== constants.ALL ? this.city : constants.EMPTY_STRING,
                  employee: !this.employee.includes(constants.ANY) ? this.employee : "1-10000000",
                  category: this.category,
                  jobtitle: this.jobTitle,
              };
        }
        this.isSearchDone = true;
        this.isSearching = true; 
        const searchParameters = {
          rpp: this.rpp,
          page: this.page,
          params: params
        }
        this.$store.dispatch('index-module/search', searchParameters).then(()=> {
            this.companies = this.getCompanies;
            if(this.companies.length>0) {
              this.lastId = this.companies(this.companies.length - 1);
            }
            this.isSearching = false;
            VueScrollTo.scrollTo("#results", 200, { offset: -50 });
        });
      }, 

      populatePopular() {
        const params = {
          keyword: this.keyword,
          search_type: this.type,
          Country: this.country.join(constants.COMMA),
          Industry: this.category,
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

      async searchBySize() {
        this.removeFromSearch();
        this.page = 1;
        const params = {
             score: this.sliderVal,
             keyword: this.keyword,
             search_type: this.type,
             country: this.country !== constants.ANY_SMALLA ? this.country : constants.EMPTY_STRING,
             state:  this.state !== constants.ALL ? this.state : constants.EMPTY_STRING,
             city: this.city !== constants.ALL ? this.city : constants.EMPTY_STRING,
             employee: !this.employee.includes(constants.ANY) ? this.employee : "1-10000000",
             category: this.category,
             jobtitle: this.jobTitle,
         }
        this.performSearch(params);
      },

      async searchByState() {
        this.removeFromSearch();
        this.page = 1;
        this.performSearch();
        let params = { state: this.state !== constants.ANY ? this.state : constants.EMPTY_STRING, country :this.newCountryL};
        this.postCities(params, constants.ALL); 
        this.city = constants.ALL;
      },

      async searchByCity() {
        this.removeFromSearch();
        this.page = 1;
        this.performSearch();
      },

      async fetchMore() {
        this.removeFromSearch();
        this.page = this.page + 1;
        const params = {
            lId: this.lastId,
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
  .file-export {
     display:flex;
     align-items: center;
     justify-content: flex-end;
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

  .search-card{
    background: #FFFFFF;
    border-radius: 8px;
    padding: 40px;
  }
  .search-card .card-title{
    font-size: 20px;
    font-weight: 600;
    line-height: 25px;
    text-align: left;
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
  .input-group-text-custom{
    display: flex;
    align-items: center;
    padding: 5px 0 0 12px;
    margin-bottom: 0;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: #495057;
    text-align: center;
    white-space: nowrap;
    border-radius: 0.25rem;
  }
  .input-group-text-custom .mdi.mdi-magnify{
    font-size: 26px;
  }
  .custom-input-group{
    border-radius: 8px;
  }
  .custom-input-group .form-control{
    border-radius: 8px !important;
    padding: 1.5rem 0.75rem;
    padding-left: 45px;
    color: #374958 !important;
  }
  .custom-input-group .form-control:focus {
    box-shadow: none;
  }
  .country-buttons a{
    border-radius: 10px;
    margin-right: 4px;
    padding: 8px 16px;
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

  .main-filter-section{
    background: #B3365B;
    border-radius: 8px;
    padding: 32px;
  }
  .main-filter-section select{
    background: #EBCACA;
    border-radius: 8px;
    padding: 5px;
    height: 45px;
  }

  .main-filter-section .form-group label{
    font-size: 16px;
    font-weight: 600;
    line-height: 20px;
    color: #C6C6C6 !important;
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
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.5);
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

  .search-card .input-group.custom-input-group .input-group-prepend{
    position: absolute;
    z-index: 5;
  }
  .search-card .input-group.custom-input-group .form-control:focus{
    border-color: #B3365B !important;
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
    margin-left: 10px;
  }
  .multiselect__select{
    height: 48px;
  }
  .multiselect__option{
    min-height: 44px;
  }
  
  .country .multiselect__placeholder {
    padding: 0 0 0 32px !important;
    font-size: 16px !important;
    color: #495057 !important;
    margin-bottom: 8px !important;
  }
  .multiselect__placeholder {
    /* padding: 0 0 0 32px !important; */
    font-size: 16px !important;
    color: #495057 !important;
    margin-bottom: 8px !important;
  }
  .multiselect {
    min-height: 48px;
  }
  .multiselect__spinner {
    height: 46px;
    border-radius: 8px;
  }
  .multiselect--active .multiselect__tags{
    border-color: #B3365B !important;
  }
  .main-filter-section .multiselect__single{
    /* display: none !important; */
    background: #EBCACA !important;
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
  .main-filter-section .multiselect{
    background: #EBCACA;
    border-radius: 8px;
  }
  .main-filter-section .multiselect__tags {
    background: #EBCACA;
  }
  .main-filter-section .multiselect--active .multiselect__tags {
    background: #fff;
  }

.show-city{
    height: 110px;
    display: flex;
    flex-direction: column;
}

.close-city {
  display: flex;
  justify-content: flex-end;
}

.close-city a{
    border-radius: 50%;
    padding: 2px 7px;
    margin-bottom: 3px;
}

.city-list{
    height: 110px;
    padding: 10px 10px;
    overflow-y : scroll;
    overflow-x : hidden;
    box-shadow: 0px 2px 8px rgba(40, 41, 61, 0.08), 0px 20px 32px rgba(96, 97, 112, 0.24);
}
.city-list a{
padding: 1px 6px !important;
}

.mdi-check-bold{
    color: rgb(255, 255, 255);
    background: #B3365B;
    border-radius: 100%;
    height: 36px;
    width: 36px;
    padding: 3px 4px;
    font-size: 7px;
}


/* header text */
.header-text-fix{
  margin-top:70px
}

</style>