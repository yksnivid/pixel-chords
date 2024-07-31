<template>
  <v-row dense>
    <v-col
      v-for="author in authors"
      :key="author.id"
      cols="12"
      sm="6"
      md="4"
    >
      <v-card @click="$router.push(`/authors/${author.id}`)">
        <v-img
          :src="author.image"
          class="align-end"
          gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
          height="200px"
          cover
        >
          <v-card-title class="text-white py-0" v-text="author.name"></v-card-title>
          <v-card-subtitle class="text-white my-2" v-text="'Songs: ' + author.numberOfSongs"></v-card-subtitle>
        </v-img>
        <v-card-actions >
          <v-btn
            class="ms-2"
            size="small"
            text="Go to author"
            variant="outlined"
          ></v-btn>
          <v-spacer></v-spacer>
          <AuthorButtons :author="author" />
          <v-btn
            v-if="user.isAdmin"
            icon="mdi-delete"
            size="small"
            variant="plain"
            @click.stop="deleteDialog = true"
          ></v-btn>
          <v-dialog
            v-model="deleteDialog"
          >
            <v-card
              :text='`Are you sure you want to delete author "${author.name}"?`'
              title="Delete song"
            >
              <template v-slot:actions>
                <v-btn
                  text="Yes, delete"
                  @click="deleteAuthor(author)"
                  color="error"
                ></v-btn>
                <v-btn
                  text="No"
                  @click="deleteDialog = false"
                ></v-btn>
              </template>
            </v-card>
          </v-dialog>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "AuthorsList",
  props: {
    authors: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      deleteDialog: false,
    };
  },
  computed: {
    ...mapGetters(['user'])
  },
  methods: {
    async deleteAuthor(author) {
      try {
        const response = await fetch(`/api/authors/${author.id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) {
          throw new Error('Failed to delete author');
        }
        console.log('Deleted author:', author.id);
        this.deleteDialog = false;
      } catch (error) {
        console.error('Error while deleting song:', error);
      }
    }
  }
}
</script>

<style scoped>

</style>
