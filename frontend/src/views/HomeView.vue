<template>
  <header>
    <Navbar/>
  </header> 
  <main>
    <div class="container">  
      <div id="carouselExampleControls" class="carousel slide" data-ride="carousel">
        <div class="carousel-inner" style="border-radius: 10px;" >
          <div class="carousel-item active">
            <router-link :to="{ name: 'discounts' }">
              <img loading="lazy" class="d-block w-100" src="/images/disc.jpg" alt="First slide">
            </router-link>
          </div>
          <div class="carousel-item">
            <router-link :to="{ name: 'recommendations' }" >
              <img loading="lazy" class="d-block w-100" src="/images/rec.jpg" alt="Second slide">
            </router-link>
          </div>
          <div class="carousel-item">
            <router-link :to="`/products/${268}`">
              <img loading="lazy" class="d-block w-100" src="/images/new.jpg" alt="Third slide">
            </router-link>
          </div>
        </div>
        <button class="carousel-control-prev rounded-button" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
          <span><prevIcon/></span>         
        </button>
        <button class="carousel-control-next rounded-button" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
          <span><nextIcon/></span>          
        </button>
      </div>
      <MobileBanners/>
      <div class="container-carousel2 text-center my-3">
        <div id="recipeCarousel" class="carousel slide" data-bs-ride="carousel">
          <div class="carousel-inner w-100" role="listbox">
            <div class="carousel-item active">
              <div class="row flex-nowrap">
                <div class="col-md-3">
                  <div class="card card-body">
                    <router-link :to="`/products/${235}`">
                      <img loading="lazy" class="d-block w-100" src="/images/mix.jpg" alt="...">
                    </router-link>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="card card-body">
                    <router-link :to="`/products/${238}`">
                      <img loading="lazy" class="d-block w-100" src="/images/shower.jpg" alt="...">
                    </router-link>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="card card-body">
                    <router-link :to="`/products/${168}`">
                      <img loading="lazy" class="d-block w-100" src="/images/wash.jpg" alt="...">
                    </router-link>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="card card-body">
                    <router-link :to="`/products/${303}`">
                      <img loading="lazy" class="d-block w-100" src="/images/toilet.jpg" alt="...">
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
            <div class="carousel-item">
              <div class="row flex-nowrap">
                <div class="col-md-3">
                  <div class="card card-body"  >
                    <router-link :to="`/products/${247}`">
                      <img loading="lazy" class="d-block w-100" src="/images/install.jpg" alt="...">
                    </router-link>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="card card-body" >
                    <router-link :to="`/products/${44}`">
                      <img loading="lazy" class="d-block w-100" src="/images/pp.jpg" alt="...">
                    </router-link>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="card card-body" >
                    <router-link :to="`/products/${88}`">
                      <img loading="lazy" class="d-block w-100" src="/images/plumb.jpg" alt="...">
                    </router-link>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="card card-body">
                    <router-link :to="`/products/${243}`">
                      <img loading="lazy" class="d-block w-100" src="/images/toilet.jpg" alt="...">
                    </router-link>
                  </div>
                </div>
              </div>
            </div>           
          </div>
          <button class="carousel-control-prev rounded-button" type="button" data-bs-target="#recipeCarousel" data-bs-slide="prev">
            <span><prevIcon/></span>  
          </button>
          <button class="carousel-control-next rounded-button" type="button" data-bs-target="#recipeCarousel" data-bs-slide="next">
            <span><nextIcon/></span>  
          </button>
        </div>               
      </div>
    </div>    
  </main> 
  <MobileMenu/> 
  <Footer/>
</template>

<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const Navbar = defineAsyncComponent(() => import('../components/Navbar.vue'));
const Footer = defineAsyncComponent(() => import('../components/Footer.vue'));
const MobileMenu = defineAsyncComponent(() => import('../components/MobileMenu.vue'));
const MobileBanners = defineAsyncComponent(() => import('@/components/MobileBanners.vue'));
import prevIcon from '@/components/icons/prevIcon.vue';
import nextIcon from '@/components/icons/nextIcon.vue';

</script>  

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.carousel-item {
  border-radius: 10px;
}

.card-body {
  border-color: transparent;
  padding: 0;
  border-radius: 10px;
  
}

.carousel-control-prev, .carousel-control-next {
  top: 50%; 
  transform: translateY(-50%);
}

.carousel-control-prev {
  left: -20px;
}

.carousel-control-next {
  right: -20px;
}

.rounded-button {
  width: 40px;
  height: 40px; 
  border-radius: 50%; 
  background-color: white !important; 
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index:  1000;
  opacity: 1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;  
}

.rounded-button span {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

@media (max-width: 767.98px) {
  #recipeCarousel {
    display: none;
  }
}

.container-carousel2{
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;  
  padding-top: 10px;
}
</style>