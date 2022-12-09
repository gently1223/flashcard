<template>
  <div class="form-container sign-up-container">
    <v-form
      action="#"
      :class="{
        'px-2 mt-12': $vuetify.breakpoint.smAndDown,
        'px-8': $vuetify.breakpoint.mdAndUp,
      }"
    >
      <img src="../../assets/img/team.png" class="team-img pt-10" />
      <h1 class="pb-12 font-weight-bold">Create Account</h1>
      <v-text-field
        placeholder="Username"
        prepend-inner-icon="mdi-account"
        filled
        v-model="formData.username"
      ></v-text-field>
      <v-text-field
        placeholder="Password"
        prepend-inner-icon="mdi-lock"
        filled
        v-model="formData.password"
        type="password"
      ></v-text-field>
      <v-text-field
        placeholder="Password(repeat)"
        prepend-inner-icon="mdi-lock"
        filled
        v-model="formData.repeat_password"
        type="password"
      ></v-text-field>
      <v-btn
        color="info"
        block
        dark
        tile
        class="pa-6 font-weight-bold"
        elevation="0"
        @click="saveformData()"
        >Sign Up</v-btn
      >
    </v-form>
  </div>
</template>
<script>
import axios from 'axios'
import Vue from 'vue'
import VueToast from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css';
export default {
  computed: {
    isSignInPanelActive: {
      get: function () {
        return this.$store.getters["authPageModule/getIsSignInPanelActive"];
      },
      set: function (newVal) {
        this.$store.commit("authPageModule/setIsSignInPanelActive", newVal);
      },
    },
    currentSignUpStep: {
      get: function () {
        return this.$store.getters["authPageModule/getCurrentSignUpStep"];
      },
      set: function (newVal) {
        this.$store.commit("authPageModule/setCurrentSignUpStep", newVal);
      },
    },
    formData: {
      get: function () {
        return this.$store.getters["authPageModule/getFormData"];
      },
      set: function () {
        this.$store.commit("authPageModule/setFormData", this.formData);
      },
    },
  },
  methods: {
    saveformData() {
      console.log(this.formData)
      
      if (this.formData.password == this.formData.repeat_password){

        var sumbit_form = {"user_id":this.formData.username, "password":this.formData.password}
        axios.post('http://localhost:8000/api/user_info/', sumbit_form)
        .then( response=>{
                Vue.$toast.open('Success Register');
                setTimeout(() => {   
                  this.$store.commit("authPageModule/setFormData", this.formData);
                  this.isSignInPanelActive = false;               
                }, 1000);
          }
        )
      }
      else{
        Vue.$toast.error('Invalid data');
      }

    },
  },
};
</script>
<style scoped>
.sign-up-container {
  left: 0;
  width: 50%;
  opacity: 0;
  z-index: 1;
}
.team-img {
  width: 50%;
}

.container.right-panel-active .sign-up-container {
  transform: translateX(100%);
  opacity: 1;
  z-index: 5;
  animation: show 0s;
}

@keyframes show {
  0%,
  49.99% {
    opacity: 0;
    z-index: 1;
  }

  50%,
  100% {
    opacity: 1;
    z-index: 5;
  }
}
</style>