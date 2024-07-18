<template>
  <v-container>
    <v-form @submit.prevent="register">
      <v-text-field
        v-model="username"
        label="Username"
        required
      ></v-text-field>
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
      <v-btn type="submit" color="primary">Register</v-btn>

      <v-alert v-if="alertMessage" :value="true" type="error" dismissible>
        {{ alertMessage }}
      </v-alert>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      alertMessage: ''
    };
  },
  methods: {
    async register() {
      try {
        const response = await fetch('/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password
          })
        });
        const data = await response.json();
        if (response.ok) {
          console.log('Registered:', data);
          this.alertMessage = data.message; // Регистрация успешна
          this.redirectToPreviousPage();
        } else {
          console.error('Failed to register:', data.error);
          this.alertMessage = data.error; // Устанавливаем сообщение об ошибке
        }
      } catch (error) {
        console.error('Failed to register:', error);
        this.alertMessage = 'Failed to register'; // Устанавливаем общее сообщение об ошибке
      }
    },
    redirectToPreviousPage() {
      // Получаем предыдущий путь из хранилища сессии
      const previousPath = sessionStorage.getItem('previousPath');
      if (previousPath) {
        this.$router.push(previousPath); // Перенаправляем на предыдущую страницу
      } else {
        this.$router.push('/'); // Если предыдущий путь не найден, перенаправляем на главную страницу
      }
    }
  }
};
</script>
