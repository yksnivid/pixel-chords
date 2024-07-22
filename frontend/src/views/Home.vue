<template>
  <Header />
  <v-container fluid>
    <v-row>
      <v-col class="v-col-12 v-col-md-6">
        <v-card
          class="mx-auto"
          @click="goToRandomSong"
        >
          <v-row justify="space-between">
            <v-col class="v-col-6" cols="auto">
              <v-card-title class="text-h5">
                Random
              </v-card-title>
              <v-card-subtitle>One random song of all our chords collection</v-card-subtitle>
              <v-card-actions>
                <v-btn
                  class="ms-2"
                  size="small"
                  text="Go to random"
                  variant="outlined"
                ></v-btn>
              </v-card-actions>
            </v-col>
            <v-col cols="auto">
              <v-avatar
                class="ma-3"
                rounded="0"
                size="125"
              >
                <v-img src="https://img.freepik.com/premium-photo/pair-pink-glossy-dice-pink-background-dice-are-resting-flat-surface-image-is-welllit-colors-are-vibrant_14117-289917.jpg"></v-img>
              </v-avatar>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
      <v-col class="v-col-12 v-col-md-6">
        <v-card
            class="mx-auto"
            @click="$router.push('/authors')"
          >
            <v-row justify="space-between">
              <v-col class="v-col-6">
                <v-card-title class="text-h5">
                  Authors library
                </v-card-title>

                <v-card-subtitle class="flex-wrap">Explore over 9000 authors presented in our library</v-card-subtitle>

                <v-card-actions>
                  <v-btn
                    class="ms-2"
                    size="small"
                    text="Go to authors"
                    variant="outlined"
                  ></v-btn>
                </v-card-actions>
              </v-col>
              <v-col cols="auto">
                <v-avatar
                  class="ma-3"
                  rounded="0"
                  size="125"
                >
                  <v-img src="https://hips.hearstapps.com/hmg-prod/images/mh-indie-workout-1-1562856859.jpg?crop=0.6666666666666666xw:1xh;center,top&resize=1200:*"></v-img>
                </v-avatar>
              </v-col>
            </v-row>
          </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h5">
            Last updates
          </v-card-title>
          <v-list>
            <v-list-item
              v-for="song in songs"
              :key="song.id"
              :title="`${song.author.name} - ${song.title}`"
              :prepend-avatar="song.author.image"
              @click="$router.push(`/authors/${song.author.id}/songs/${song.id}`)"
            >
              <template v-slot:append>
                <SongButtons
                  :song="song"
                />
              </template>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import SongButtons from "@/components/SongButtons.vue";
import {mapGetters} from "vuex";

export default {
  name: 'Home',
  components: {SongButtons},
  data() {
    return {
      songs: []
    }
  },
  methods: {
    async goToRandomSong() {
      try {
        const response = await fetch('/api/songs/random');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const song = await response.json();
        this.$router.push(`/authors/${song.author.id}/songs/${song.id}`);
      } catch (error) {
        console.error('Error fetching random song:', error);
      }
    },
    async fetchRecentSongs() {
      try {
        const response = await fetch('/api/songs/recent');
        if (!response.ok) {
          throw new Error('Failed to fetch songs');
        }
        this.songs = await response.json();
      } catch (error) {
        console.error('Error fetching songs:', error);
      }
    },
  },
  async created() {
    await this.fetchRecentSongs();
  }
}
</script>
