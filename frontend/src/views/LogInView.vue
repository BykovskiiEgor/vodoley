<script setup lang="ts">
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import MobileMenu from '../components/MobileMenu.vue';
import {useLogin} from '../composables/useLogin'


const{
  email,
  password,
  passwordReceived,
  handleFormSubmit  
}=useLogin();
</script>

   
<template>
    <div class="vh-100 d-flex flex-column">
      <header>
        <Navbar />
      </header>
      <section class="flex-grow-1 d-flex align-items-center justify-content-center">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-md-6 col-lg-5">
              <div class="card p-4 shadow-sm">
                <div class="text-center mb-4">
                  <heroIcon />
                </div>
                <form @submit.prevent="handleFormSubmit">
                  <div class="mb-3" v-if="!passwordReceived">
                    <label for="email" class="form-label">Почтовый адрес</label>
                    <input
                      type="email"
                      name="email"
                      class="form-control"
                      id="email"
                      placeholder="name@example.com"
                      v-model="email"
                    />
                  </div>
                  <div class="mb-3" v-if="passwordReceived">
                    <label for="password" class="form-label">Пароль</label>
                    <input
                      type="password"
                      name="password"
                      class="form-control"
                      id="password"
                      placeholder="Введите временный пароль"
                      v-model="password"
                    />
                  </div>
                  <div class="mb-3">
                    <button type="submit" class="enter-button">
                      {{ passwordReceived ? 'Войти' : 'Получить код' }}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>
      <MobileMenu />
      <Footer />
    </div>
</template>
  

<style scoped>
.h-custom {
  height: calc(100% - 73px);
}

@media (max-width: 450px) {
  .h-custom {
    height: 100%;
  }
}

.card {
  border: none;
  border-radius: 0.75rem;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #1a48732e;
  border-color: #0056b3;
}
.enter-button{
  background-color: #003464;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: auto;
}
</style>
