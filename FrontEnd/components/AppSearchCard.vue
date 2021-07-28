<template>
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
                  <span v-if="product && product.includes(props.option)">
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
                <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
              </template>
              <template
                slot="option"
                slot-scope="props">
                <div class="option__desc">
                  <span v-if="country.includes(props.option)">
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
            <a class="card-tab-btn" v-on:click="showCountry(selectedCountry)" :class="selectedCountryGroup.includes(selectedCountry) ? 'active' : ''" :key="index" v-for="selectedCountry, index in countryGroups">{{selectedCountry}}</a>
            <div class="show-city mt-3" v-if="!isHidden">
                <div class="close-city">
                    <a class="btn-dark " v-on:click="isHidden = true">x</a>
                </div>
                <div class="city-list">
                    <a class="card-tab-btn " @click="removeCountry(city)" :key="index" v-for="city, index in countryList">
                      {{city}}
                      <span v-if="!countrySelected.includes(city)" class="mdi mdi-check-bold ml-2"></span>
                    </a>
                </div>
          </div>
          </div>
          <button class="btn-search-lg text-white my-4" type="button" data-toggle="button" @click="$emit('search', {product, category, country, jobTitle, keyword, countryList})"  :disabled="keyword.trim() == ''" title="Search" >Search</button>
        </div>
</template>

<script>
import constants from "../api/constants"
import { mapGetters } from "vuex";
import Multiselect from 'vue-multiselect'

export default {
  name: "SearchCard",
    props: {
      countryGroups: Array
  },
  data () {
    return {
      product:[],
      products: constants.PRODUCTS,
      category : constants.EMPTY_STRING,
      jobTitle: constants.EMPTY_STRING,
      country: [],
      countryList: [],
      countries: constants.COUNTRIES,
      isHidden: true,
      jobSearchSlotText: constants.LOADING,
      selectedCountryGroup: [],
      keyword: constants.EMPTY_STRING,
      countrySelected: [],
      categories: [],
      jobTitles: [],
      constJobTitles: []
    }
  },
  created() {
      this.loadCategories();
      this.loadJobTitles();
  },
  computed: {
      ...mapGetters({
        getCountryList: 'index-module/country-list',
        getCategories: 'index-module/categories',
        getJobTitlesFromStore: 'index-module/job-titles',
      })
  },
  components: {
    Multiselect
  },
  methods: {
      async asyncFindCategories(query) {
        if(query!=constants.EMPTY_STRING) {
          this.categories= this.constCategories.filter(industry=> this.notEmptyAndNull(industry) && industry.toLowerCase().startsWith(query.toLowerCase()));
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
      notEmptyAndNull(item) {
         return item!=null && item!= constants.EMPTY_STRING;
      },
      showCountry(selectedCountry) {
        if(this.selectedCountryGroup.includes(selectedCountry)) {
          var index = this.selectedCountryGroup.indexOf(selectedCountry);
          this.selectedCountryGroup.splice(index, 1);
          this.$store.dispatch('index-module/load-country-group', selectedCountry).then(()=> {
              this.countryList = this.countryList.filter((country)=> !this.getCountryList.includes(country));
          });
          if(this.selectedCountryGroup.length==0) {
            this.isHidden = true;
          }
        }  else  {
          this.selectedCountryGroup.push(selectedCountry);
          this.isHidden = false;
          this.$store.dispatch('index-module/load-country-group', selectedCountry).then(()=> {
              this.countryList = [...this.countryList, ...this.getCountryList];
          });
        }
      },
      removeCountry(country){
          const index = this.countrySelected.indexOf(country);
          if (index > -1) {
            this.countrySelected.splice(index, 1);
          } else {
            this.countrySelected.push(country);
          }
          this.$emit('removeCountry', this.countrySelected);
      },
      loadCategories() {
        this.$store.dispatch('index-module/load-categories').then(()=> {
            let categories = this.getCategories;
            this.categories =  categories.filter((category)=> category!=null && (/[a-zA-Z]/).test(category.charAt(0)));
            this.constCategories = categories;
        });
      },
      loadJobTitles() {
        this.$store.dispatch('index-module/load-job-titles').then(()=> {
              this.jobTitles= this.getJobTitlesFromStore;
              this.constJobTitles = this.getJobTitlesFromStore;
        });
      },
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
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
  border: 1px solid #C6C6C6;
  box-sizing: border-box;
  border-radius: 8px;
  padding: 10px 20px;
  color: #374958;
  text-decoration: none;
  cursor: pointer;
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

.search-card .input-group.custom-input-group .input-group-prepend{
  position: absolute;
  z-index: 5;
}
.search-card .input-group.custom-input-group .form-control:focus{
  border-color: #B3365B !important;
}

.hr-seperator{
  border: 1px solid #C6C6C6;
  margin-top: 25px;
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

.show-city {
  height: 110px;
  display: flex;
  flex-direction: column;
}

.close-city {
  display: flex;
  justify-content: flex-end;
}

.close-city a.btn-dark{
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
  border-bottom: 1px solid #C6C6C6;
  cursor: pointer;
}
</style>
