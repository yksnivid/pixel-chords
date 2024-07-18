<template>
  <v-container class="fill-height">
    <v-responsive
      class="align-centerfill-height mx-auto"
      max-width="900"
    >
      <v-img
        class="mb-4"
        height="300"
        src="@/assets/logo.png"
      />

      <div class="text-center">
        <h1 class="text-h2 font-weight-bold">Chords</h1>
      </div>

      <div class="py-4" />

      <v-row>
        <v-col>
          <v-card
            class="mx-auto"
            max-width="300"
            title="Random"
            subtitle="Get a random song"
            link
            @click="goToRandomSong"
          ></v-card>
        </v-col>

        <v-col>
          <v-card
            class="mx-auto"
            max-width="300"
            title="Authors"
            subtitle="Discover authors"
            link
            @click="goToAuthors"
          ></v-card>
        </v-col>

        <v-col>
          <v-card
            class="mx-auto"
            max-width="300"
            title="Recent"
            subtitle="Check out recent songs"
            link
            disabled
          ></v-card>
        </v-col>

      </v-row>
    </v-responsive>
  </v-container>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    async goToRandomSong() {
      try {
        const response = await fetch('/api/songs/random');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const song = await response.json();
        this.$router.push(`/songs/${song.author}/${song.title}`);
      } catch (error) {
        console.error('Error fetching random song:', error);
      }
    },
    goToAuthors() {
      this.$router.push({ name: 'authors' });
    }
  }
}
</script>
