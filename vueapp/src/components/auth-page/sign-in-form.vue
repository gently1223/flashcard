<template>
  <div class="form-container sign-in-container mt-12">
    <v-form
      action="#"
      :class="{
        'px-2': $vuetify.breakpoint.smAndDown,
        'px-8': $vuetify.breakpoint.mdAndUp,
      }"
    >
      <img src="../../assets/img/team.png" class="team-img pt-8" />
      <h1 class="pb-8 font-weight-bold">Sign in</h1>
      <v-text-field
        prepend-inner-icon="mdi-account"
        placeholder="Username"
        v-model="username"
        filled
      ></v-text-field>
      <v-text-field
        prepend-inner-icon="mdi-lock"
        placeholder="Password"
        type="password"
        v-model="password"
        filled
      ></v-text-field>
      <v-btn
        color="info"
        block
        dark
        tile
        class="pa-6 font-weight-bold"
        elevation="0"
        @click="login()"
        >Sign In</v-btn
      >
      <v-row class="justify-center py-10">
        <span
          :class="{
            'text-secondary forgot-password-sm': $vuetify.breakpoint.smAndDown,
            'text-secondary forgot-password-md': $vuetify.breakpoint.mdAndUp,
          }"
          >Forgot your password?</span
        >
      </v-row>
    </v-form>
  </div>
</template>
<script>
import axios from 'axios'
import Vue from 'vue'
import VueToast from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css';
import VueSession from 'vue-session'
Vue.use(VueSession)
Vue.use(VueToast, {
  position: 'top'
});
export default {
  data: () => {
    return {
      username: null,
      password: null,
    };
  },
  methods: {
    login() {
        axios.get('http://localhost:8000/api/user_info/?user_id='+this.username+'&password='+this.password)
        .then( response => {
            this.subscriptions = response.data
            console.log(this.subscriptions)
            if (this.subscriptions.length != 0){
              this.$session.start()
              this.$session.set('username', this.username)
              Vue.$toast.open('Success Login');
              setTimeout(() => {                  
                this.$store.dispatch("authPageModule/loginAndSaveToken", {
                username: this.username,
                asswor: this.password,
                }); 
              
              }, 3000);
            }
            else {
              Vue.$toast.error('Invalid Member');
            }

        });

    },
  },
};
</script>
<style scoped>
.sign-in-container {
  left: 0;
  width: 50%;
  z-index: 2;
}
.team-img {
  width: 50%;
}

.container.right-panel-active .sign-in-container {
  transform: translateX(100%);
}

.container.right-panel-active .overlay-container {
  transform: translateX(-100%);
}
.forgot-password-sm {
  font-size: 12px;
}
.forgot-password-md {
  font-size: 15px;
}
</style>