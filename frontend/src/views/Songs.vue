<template>
  <Header />
  <v-container>
    <v-row>
      <v-col
        v-for="song in songs"
        :key="song.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card
          class="mx-auto"
          max-width="400"
          @click="goToSong(song.id)"
        >
          <v-card-title>{{ song.title }}</v-card-title>
          <v-card-subtitle>{{ song.artist }}</v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Header from '@/components/Header.vue';

export default {
  name: 'Songs',
  components: {Header},
  data() {
    return {
      songs: []
    };
  },
  async created() {
    await this.fetchSongs();
  },
  methods: {
    async fetchSongs() {
      try {
        const response = await fetch('/api/songs');
        if (!response.ok) {
          throw new Error('Failed to fetch songs');
        }
        this.songs = await response.json();
      } catch (error) {
        console.error('Error fetching songs:', error);
      }
    },
    goToSong(songId) {
      this.$router.push(`/songs/${songId}`);
    }
  }
};
</script>

<style scoped>
.v-card {
  cursor: pointer;
}
</style>
