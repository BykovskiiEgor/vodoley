<script setup>
import Navbar from '../components/Navbar.vue'
import MobileMenu from '../components/MobileMenu.vue'
import Footer from '../components/Footer.vue';
import IconPhone from '@/components/icons/IconPhone.vue';
import IconAdress from '@/components/icons/IconAdress.vue';
</script>

<template>
  <div class="page-container">
    <header>
      <Navbar />
    </header>
    <main class="content-wrap">
      <div class="container py-5">
        <div class="row gx-5 align-items-center">
          <div class="col-lg-6">
            <div class="p-3">
              <h1 class="display-4">Добро пожаловать в Водолей</h1>
              <p>Мы занимаемся розничными продажами с 2009 года и имеем большой опыт в сфере сантехники и не только. На сайте вы можете ознакомиться с частью нашего ассортимента и осуществить заказ понравившихся товаров.</p>
              <h2 class="mt-4">Условия заказов:</h2>
              <ul class="conditions-list">
                <li>Оформление заказов временно недоступно, все товары вы можете приобрести в магазине</li>
                <!-- <li>При заказе на сумму менее 5 тысяч рублей доступен только самовывоз или платная доставка.</li>
                <li>При заказе на сумму от 5 тысяч рублей доставка по г. Белебей осуществляется бесплатно.</li> -->
              </ul>
              <h2 class="mt-4">Контакты:</h2>
              <div class="contact-info">
                <p>
                  <IconPhone />
                  +7 (927) 940-2532                                                
                </p>
                <p>
                  <IconAdress />
                  г. Белебей, ул. Интернациональная, д. 116
                </p>
              </div>
            </div>
          </div>
          <div class="col-lg-6 text-center">
            <div class="p-3">
              <iframe
                src="https://yandex.ru/map-widget/v1/?um=constructor%3Abdc45f3933bcfc3db9dca2eddd8e0efd867ed5b081ecb0eaefa6d8094c8760c0&amp;source=constructor"
                width="100%"
                height="300"
                frameborder="0"
                style="border:0;"
                allowfullscreen=""
                aria-hidden="false"
                tabindex="0">
              </iframe>
            </div>
          </div>
        </div>
      </div>
    </main>
    <footer>
      <MobileMenu />
      <Footer/>
    </footer>
  </div>
</template>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-wrap {
  flex: 1;
}

.container {
  max-width: 1200px;
}

@media (min-width: 1024px) {
  .container {
    display: flex;
    align-items: center;
  }
}

h1.display-4, h2 {
  font-family: 'Roboto', sans-serif;
  font-weight: 300;
  margin-bottom: 1rem;
}

h1.display-4 {
  font-size: 2.5rem;
}

h2 {
  font-size: 2rem;
  margin-top: 2rem;
}

p, ul.conditions-list li {
  font-family: 'Roboto', sans-serif;
  font-size: 1rem;
  font-weight: 300;
  margin-bottom: 0.5rem;
}

ul.conditions-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.contact-info p {
  display: flex;
  align-items: center;
}

.contact-info p svg {
  margin-right: 0.5rem;
}
</style>
