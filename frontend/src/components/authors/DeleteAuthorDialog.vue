<template>
  <v-dialog
    :model-value="modelValue"
    max-width="600"
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
          @click="$emit('update:modelValue', false)"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "DeleteAuthorDialog",
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    author: {
      type: Object,
      required: true
    }
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
        this.$emit('update:modelValue', false);
        this.$router.go();
      } catch (error) {
        console.error('Error while deleting song:', error);
      }
    }
  }
}
</script>

<style scoped>

</style>
