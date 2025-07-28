<template>
    <div class="mobile-gallery" >
        <div class="mobile-gallery-item">
            <router-link :to="`/products/${235}`">
                <img src="../assets/mix.jpg" alt="Mix">
            </router-link>
        </div>
        <div class="mobile-gallery-item">
            <router-link :to="`/products/${238}`">
                <img src="../assets/shower.jpg" alt="Shower">
            </router-link>
        </div>
        <div class="mobile-gallery-item">
            <router-link :to="`/products/${168}`" >
                <img src="../assets/wash.jpg" alt="Wash">
            </router-link>            
        </div>
        <div class="mobile-gallery-item">
            <router-link :to="`/products/${243}`">
                <img src="../assets/toilet.jpg" alt="Toilet">
            </router-link>
        </div>
        <div class="mobile-gallery-item">
            <router-link :to="`/products/${247}`">
                <img src="../assets/install.jpg" alt="Install">
            </router-link>            
        </div>
        <div class="mobile-gallery-item">
            <router-link :to="`/products/${44}`">
                <img src="../assets/pp.jpg" alt="PP">
            </router-link>            
        </div>
        <div class="mobile-gallery-item">
            <router-link :to="`/products/${88}`">
                <img src="../assets/plumb.jpg" alt="Plumb">
            </router-link>
        </div>
        <div class="mobile-gallery-item">
            <router-link :to="`/products/${243}`">
                <img src="../assets/toilet.jpg" alt="Toilet">
            </router-link>
        </div>
    </div>
  </template>

<style scoped>
    .mobile-gallery {
        display: none; 
        padding-top: 20px;
    }

    @media (max-width: 767.98px) {
        .mobile-gallery {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 10px; 
        }

        .mobile-gallery-item {
            width: calc(50% - 5px); 
            margin-bottom: 10px; 
        }

        .mobile-gallery-item img {
            width: 100%; 
            height: auto; 
           
        }
    }
</style>

