<template>
  <Header />
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card v-if="!loading && !error">
          <v-img
            class="align-end text-white"
            height="200"
            :src="authorInformation.coverImage"
            cover
          >
            <v-card-title>{{ authorInformation.author }}</v-card-title>
          </v-img>

          <v-card-text v-if="authorInformation.about">
            <span>About:</span>
            <p>{{ authorInformation.about }}</p>
          </v-card-text>

          <v-card-subtitle class="pt-4">
            Number of songs: {{ authorInformation.numberOfSongs }}
          </v-card-subtitle>

          <v-list>
            <v-list-item
              v-for="song in authorInformation.songs"
              :key="song.title"
              :title="song.title"
              @click="$router.push(`/songs/${authorInformation.author}/${song.title}`)"
            ></v-list-item>
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
    const { author } = this.$route.params;
    try {
      const response = await fetch(`/api/author/${author}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      this.authorInformation = await response.json();
      console.log(this.authorInformation);
    } catch (error) {
      this.error = error.message;
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style scoped>
</style>
