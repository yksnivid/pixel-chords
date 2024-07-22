<template>
  <div>
    <v-btn
      :color="song.isFavorite ? 'red' : 'medium-emphasis'"
      icon="mdi-heart"
      size="small"
      variant="plain"
      @click.stop="toggleFavorite"
    ></v-btn>
    <v-btn
      icon="mdi-share-variant"
      size="small"
      variant="plain"
      @click.stop="shareSong"
    ></v-btn>
  </div>
  <LoginDialog v-model="loginDialog" />
</template>

<script>
import LoginDialog from "@/components/LoginDialog.vue";
import { mapGetters } from 'vuex';

export default {
  name: "SongButtons",
  components: {LoginDialog},
  props: {
    song: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      loginDialog: false
    }
  },
  computed: {
   ...mapGetters(['user'])
  },
  methods: {
    async toggleFavorite() {
      if (!this.user.isLoggedIn) {
        this.loginDialog = true;
        return;
      }
      try {
        this.song.isFavorite = !this.song.isFavorite;

        const method = this.song.isFavorite ? 'POST' : 'DELETE';

        const response = await fetch(`/api/users/${this.user.id}/favorites`, {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ item_type: 'song', item_id: this.song.id })
        });

        if (!response.ok) {
          throw new Error('Failed to toggle favorite');
        }
        const data = await response.json();
        console.log(`${data.message}, song id: ${this.song.id}`);
      } catch (error) {
        console.error('Error toggling favorite:', error);
        // Revert the isFavorite status in case of an error
        this.song.isFavorite = !this.song.isFavorite;
      }
    },
    shareSong() {
      console.log('Shared song:', this.song.id);
    }
  }
};
</script>

<style scoped>
</style>
