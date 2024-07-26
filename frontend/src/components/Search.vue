<template>

  <v-menu
      :model-value="menuOpen"
      transition="scale-transition"
      close-on-back
    >
      <template v-slot:activator="{ props }">
        <v-text-field
          v-bind="props"
          v-model="searchQuery"
          @update:modelValue="debouncedSearch"
          append-inner-icon="mdi-magnify"
          placeholder="Search here"
          density="compact"
          variant="solo"
          hide-details
          single-line
          :loading="isLoading"
        ></v-text-field>
      </template>


      <v-list
        v-if="searchResults.authors.length > 0"
        density="compact"
        tile
      >
        <v-list-subheader>Authors</v-list-subheader>
        <v-list-item
          v-for="author in searchResults.authors"
          :key="author.id"
          :prepend-avatar="author.image"
          @click="$router.push(`/authors/${author.id}`)"
          link
        >
          <v-list-item-title>{{ author.name }}</v-list-item-title>
        </v-list-item>
      </v-list>

      <v-list
        v-if="searchResults.songs.length > 0"
        density="compact"
        tile
      >
        <v-list-subheader>Songs</v-list-subheader>
        <v-list-item
          v-for="song in searchResults.songs"
          :key="song.id"
          :title="song.title"
          :subtitle="song.author.name"
          @click="$router.push(`/authors/${song.author.id}/songs/${song.id}`)"
          density="compact"
          link
        >
        </v-list-item>
      </v-list>

      <v-list v-if="errorMessage" density="compact" tile>
        <v-list-item subtitle="Hmm... There is no results"></v-list-item>
      </v-list>

    </v-menu>
</template>

<script>

function debounce(callee, timeoutMs) {
  let lastCallTimer;
  return function perform(...args) {
    const context = this;
    if (lastCallTimer) {
      clearTimeout(lastCallTimer);
    }
    lastCallTimer = setTimeout(() => {
      callee.apply(context, args);
    }, timeoutMs);
  };
}


export default {
  name: 'Search',
  data() {
    return {
      searchQuery: '',
      searchResults: {
        authors: [],
        songs: []
      },
      isLoading: false,
      menuOpen: false,
      errorMessage: null
    };
  },
  methods: {
    debouncedSearch: debounce(function () {
      this.performSearch(this.searchQuery);
    }, 300),
    async performSearch(query) {
      if (query.length < 3) {
        this.errorMessage = null;
        return;
      }
      this.isLoading = true;
      try {
        const response = await fetch(`/api/search/${query}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.searchResults = await response.json();
        this.menuOpen = true;
      } catch (error) {
        console.error('Error fetching authors:', error);
      } finally {
        this.errorMessage = (this.searchResults.authors.length === 0 && this.searchResults.songs.length === 0) ? 'No results found' : null
        this.isLoading = false;
      }
    }
  }
};
</script>

<style>
.v-card {
  cursor: pointer;
}
</style>
