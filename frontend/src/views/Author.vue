<template>
  <Header />
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card v-if="!loading && !error">
          <v-img
            class="align-end text-white mb-3"
            height="200"
            :src="authorInformation.coverImage"
            cover
          >
            <v-card-title>{{ authorInformation.author }}</v-card-title>
          </v-img>

          <div v-if="authorInformation.about">
            <v-card-subtitle>About</v-card-subtitle>
            <v-card-text>{{ authorInformation.about }}</v-card-text>
          </div>

          <v-card-subtitle>
            Number of songs: {{ authorInformation.numberOfSongs }}
          </v-card-subtitle>

          <v-list>
            <v-list-item
              v-for="song in authorInformation.songs"
              :key="song.id"
              :title="song.title"
              @click="$router.push(`/songs/${authorInformation.author}/${song.title}`)"
            >
              <template v-slot:append>
                <v-btn
                  :color="isLoggedIn && song.isFavorite ? 'red' : 'medium-emphasis'"
                  icon="mdi-heart"
                  size="small"
                  variant="plain"
                  @click.stop="toggleFavorite(song)"
                ></v-btn>
                <v-btn
                  icon="mdi-share-variant"
                  size="small"
                  variant="plain"
                  @click.stop="shareSong(song.id)"
                ></v-btn>
              </template>
            </v-list-item>
          </v-list>

        </v-card>

        <v-alert v-else-if="error" type="error">
          {{ error }}
        </v-alert>

        <v-progress-circular
          v-else
          indeterminate
          color="primary"
        ></v-progress-circular>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Header from "@/components/Header.vue";
export default {
  name: "Author",
  data() {
    return {
      authorInformation: {
        about: null,
        author: null,
        coverImage: null,
        numberOfSongs: null
      },
      error: null,
      loading: true
    };
  },
  async created() {
    await this.fetchAuthorData();
  },
  beforeRouteUpdate(to, from, next) {
    this.fetchAuthorData(to.params.author);
    next();
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.isLoggedIn;
    }
  },
  methods: {
    async fetchAuthorData(authorName = this.$route.params.author) {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch(`/api/author/${authorName}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.authorInformation = await response.json();
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
    async toggleFavorite(song) {
      if (!this.isLoggedIn) {
        // this.$router.push('/login');
        return;
      }
      try {
        song.isFavorite = !song.isFavorite;
        const response = await fetch('/api/toggle_favorite_song', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ song_id: song.id })
        });
        if (!response.ok) {
          throw new Error('Failed to toggle favorite');
        }
        // Обработка успешного добавления/удаления из избранного
        console.log('Toggled favorite song');
      } catch (error) {
        console.error('Error toggling favorite:', error);
      }
    },
    shareSong(songId) {
      // Логика для поделиться песней
      console.log('Shared song:', songId);
    }
  }
};
</script>

<style scoped>
</style>
