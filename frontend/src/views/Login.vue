<template>
  <v-container>
    <v-form @submit.prevent="login">
      <v-text-field
        v-model="email"
        label="Email"
        required
      ></v-text-field>
      <v-text-field
        v-model="password"
        label="Password"
        type="password"
        required
      ></v-text-field>
      <v-btn type="submit" color="primary">Login</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });
        const data = await response.json();
        if (response.ok) {
          console.log('Logged in!', data);
        } else {
          console.error('Failed to login:', data.error);
        }
      } catch (error) {
        console.error('Failed to login:', error);
      }
    }
  }
};
</script>
