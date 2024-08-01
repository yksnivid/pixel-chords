<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title class="headline">Sign Up</v-card-title>
      <v-card-text>
        <v-form v-model="isValid" @submit.prevent="submitRegister" validate-on="input lazy">
          <v-text-field
            v-model="registerData.username"
            label="Username"
            :rules="[value => value.length >= 1 || 'Too short']"
            required
          ></v-text-field>
          <v-text-field
            v-model="registerData.email"
            label="Email"
            required
            :rules="[v => /^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(v) || 'Invalid Email address']"
          ></v-text-field>
          <v-text-field
            v-model="registerData.password"
            label="Password"
            :rules="[value => value.length >= 6 || 'Password is too short']"
            required
            :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
            :type="visible ? 'text' : 'password'"
            @click:append-inner="visible = !visible"
          ></v-text-field>
          <v-text-field
            v-if="!visible"
            v-model="confirmPassword"
            label="Confirm Password"
            :rules="[value => value === registerData.password || 'Passwords do not match']"
            required
            :type="visible ? 'text' : 'password'"
          ></v-text-field>
          <v-btn type="submit" color="primary">Submit</v-btn>
        </v-form>
      </v-card-text>
      <v-card-text v-if="message">
        <v-alert type="error">{{ message }}</v-alert>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="closeDialog">Cancel</v-btn>
      </v-card-actions>
    </v-card>

  </v-dialog>
</template>

<script>
import {mapActions} from "vuex";

export default {
  name: 'RegisterDialog',
  props: {
    modelValue: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      dialog: false,
      registerData: {
        username: '',
        email: '',
        password: '',
      },
      isValid: false,
      confirmPassword: '',
      message: null,
      visible: false
    };
  },
  watch: {
    modelValue(val) {
      this.dialog = val;
    },
    dialog(val) {
      this.$emit('update:modelValue', val);
    },
  },
  methods: {
    ...mapActions(['login']),
    async submitRegister() {
      if (!this.isValid) {
        this.message = 'Check your registration form';
        return;
      }
      try {
        const response = await fetch('/api/users', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.registerData)
        });
        const data = await response.json();
        if (response.ok) {
          this.dialog = false;
          this.message = null;
          await this.login(this.registerData);
        } else {
          this.message = data.message;
        }
      } catch (error) {
        this.message = 'Failed to register';
      }
    },
    closeDialog() {
      this.dialog = false;
    },
  },
};
</script>

<style scoped>
</style>
