import { createStore } from 'vuex';

const store = createStore({
  state: {
    isLoggedIn: false,
    id: null,
    user: null,
    role: null,
    errorMessage: null
  },
  mutations: {
    SET_AUTH(state, { isLoggedIn, id, user, role }) {
      state.isLoggedIn = isLoggedIn;
      state.id = id;
      state.user = user;
      state.role = role;
      state.errorMessage = null; // Сброс ошибки при успешной аутентификации
    },
    LOGOUT(state) {
      state.isLoggedIn = false;
      state.id = null;
      state.user = null;
      state.role = null;
      state.errorMessage = null; // Сброс ошибки при выходе
    },
    SET_ERROR(state, errorMessage) {
      state.errorMessage = errorMessage; // Установка сообщения об ошибке
    }
  },
  actions: {
    async checkAuthStatus({ dispatch }) {
      // Проверяем статус авторизации при загрузке приложения
      await dispatch('fetchCurrentUser');
    },
    async fetchCurrentUser({ commit }) {
      try {
        const response = await fetch('/api/current_user', {
          credentials: 'include'
        });

        if (response.ok) {
          const data = await response.json();
          commit('SET_AUTH', { isLoggedIn: true, id: data.id, user: data.user, role: data.role });
        } else if (response.status === 401) {
          commit('SET_AUTH', { isLoggedIn: false, id: null, user: null, role: null });
        } else {
          const errorData = await response.json();
          commit('SET_ERROR', errorData.error || 'Unexpected error occurred');
        }
      } catch (error) {
        commit('SET_ERROR', 'Network error during login');
      }
    },
    async login({ commit }, { username, password }) {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password }),
          credentials: 'include'
        });

        if (response.ok) {
          const data = await response.json();
          commit('SET_AUTH', { isLoggedIn: true, id: data.id, user: data.user, role: data.role });
          return { success: true };
        } else {
          const errorData = await response.json();
          commit('SET_ERROR', errorData.error || 'Failed to login');
          return { success: false, error: errorData.error || 'Failed to login' };
        }
      } catch (error) {
        commit('SET_ERROR', 'Network error during login');
        return { success: false, error: 'Network error during login' };
      }
    },
    async logout({ commit }) {
      try {
        await fetch('/api/logout', {
          method: 'POST',
          credentials: 'include'
        });
        commit('LOGOUT');
      } catch (error) {
        commit('SET_ERROR', 'Network error during logout');
      }
    }
  },
  getters: {
    user(state) {
      return {
        isLoggedIn: state.isLoggedIn,
        id: state.id,
        user: state.user,
        role: state.role,
        isAdmin: state.role === 'admin'
      }
    },
    errorMessage(state) {
      return state.errorMessage;
    }
  }
});

export default store;
