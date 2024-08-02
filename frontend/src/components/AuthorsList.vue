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
          <v-card-title class="text-white" v-text="author.name"></v-card-title>
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
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import {mapGetters} from "vuex";
import DeleteAuthorDialog from "@/components/authors/DeleteAuthorDialog.vue";

export default {
  name: "AuthorsList",
  components: {DeleteAuthorDialog},
  props: {
    authors: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      deleteDialog: false,
      authorToDelete: {
        type: Object,
        default: undefined
      }
    };
  },
  computed: {
    ...mapGetters(['user'])
  }
}
</script>

<style scoped>

</style>
