<template>  
    <header>
      <Navbar />
    </header>                    
      <div class="container" v-for="product in products" :key="product.id">
        <Breadcrumbs :product="product"/>         
        <div class="product-card">
          <div class="product-card-images">
            <div class="thumbnails">   
              <button
                v-if="product.images.length > 5"
                @click="showMoreImages(-1, product.id)"
                class="show-more-button">
                <span class="up">
                  <IconUp/>
                </span>
              </button>             
              <img 
                v-for="(image, index) in product.images.slice(startIndex, startIndex + 5)"
                :key="index"
                :src="image.image"
                :class="['thumbnail', { active: index + startIndex === currentIndex[product.id] }]"
                @click="changeImage(product.id, index + startIndex)"/> 
              <button
                v-if="product.images.length > 5"
                @click="showMoreImages(1, product.id)"
                class="show-more-button">
                <span class="down">
                  <IconDown/>
                </span>
              </button>
            </div>                           
            <div class="indicators">
              <span 
                v-for="(image, index) in product.images"
                :key="index"
                :class="['indicator', { active: index === currentIndex[product.id] }]"
                @click="changeImage(product.id, index)"
              ></span>
            </div> 
            <div class="main-image" @mousemove="(e) => handleMouseMove(e, product)" @mouseleave="handleMouseLeave">
              <img :src="currentImage(product)" class="zoom-image" :style="imageStyle">
              <button v-if="!scaleImage && product.images.length > 1" class="b-prev" @click="scrollImages(product.id, -1)">
                <IconLeft/>
              </button>
              <button v-if="!scaleImage && product.images.length > 1" class="b-next" @click="scrollImages(product.id, 1)">
                <IconRight/>
              </button> 
            </div>   
          </div>
          <div class="scale-button-container">
              <button v-if="!scaleImage" class="scale-button" @click="scaleImage = !scaleImage">
                <span class="tooltiptext">При нажатии вы сможете<br>увеличить изображение</span>
                <ScaleIcon/>
              </button>
              <button v-if="scaleImage" class="scale-button" @click="scaleImage = !scaleImage">
                <span class="tooltiptext">При нажатии вы сможете<br>увеличить изображение</span>
                <ScaleMIcon/>
              </button>
          </div>           
          <div class="product-info-box" :class="{ 'sticky': isSticky }">
            <div class="item-article">                
              <span ref="textToCopy">{{ product.article }}</span>
              <button class="copy-button" @click="copyText(product.article)">
                <IconCopy/>
                {{ isCopied ? 'Скопировано!' : 'Копировать' }}
              </button>
            </div>
            <div class="item-name">{{ product.name }}</div>            
            <span class="star-rating" v-if="parseFloat(product.avg_rating ?? '0') > 0">                
              <star-rating :rating="parseFloat(product.avg_rating ?? '0')" :read-only="true" :star-size="15" />                
            </span>
            <span class="item-price-container" v-if="product.discount_price ?? 0 > 0">
                <div class="text-muted text-decoration-line-through">{{ product.price }}₽</div>
                <div class="text-success">{{ product.discount_price }}₽</div>
            </span>
            <span class="item-price-container" v-else>
                <div>{{ product.price }}₽</div>
            </span> 
            <div v-if="!product.available || product.quantity === 0">
              <button class="not-available" @click="showRequestForm">Оставить заявку</button>
            </div>  
            <div v-else class="buttons-cintainer"> 
              <button v-if="!cart[product.id]" @click="addToCart(product)" class="add-to-cart">                               
                  В корзину
              </button>
              <div v-else class="quantity-control">
                  <button @click="decrement(product)"><IconMinus/></button>
                  <span>{{ cart[product.id].quantity }}</span>
                  <button @click="increment(product)"><IconPlus/></button>
              </div>               
            </div>         
          </div>  
          <div class="sticky-sentinel"></div>            
        </div>                         
        <div class="description-attribute-container">
          <div v-if="product.attributes.length > 0" class="attributes-section">
            <span class="border-line"></span>
            <span class="dac-names">Характеристики</span>
            <div class="attributes-container" :class="{expanded: isExpanded}">
              <div class="attribute-item" v-for="(attribute, index) in product.attributes" :key="index">
                <span class="attribute-name">{{ attribute.attribute.name }}</span>
                <span class="attribute-dots"></span>
                <span class="attribute-value">{{ attribute.value }}</span>
              </div>
            </div>
            <button class="button-full-att" @click="showFullAtt">
              <component :is="isExpanded ? IconUp : IconDown" />    
            </button> 
          </div>
          <div v-if="product.description && product.description.length > 0" class="description-section">
            <span class="border-line"></span>
            <span class="dac-names" >Описание</span>
            <div class="description-container">
              <span class="description" v-html="product.description"></span>
            </div>        
          </div>                    
        </div>
        <div v-if="isUser" class="rate-item-container">
          <span class="border-line"></span>
          <span v-if="!product.user_rating">
            <span  class="dac-names" >Оцените товар</span>
            <star-rating             
              :star-size="40" 
              @update:rating="handleRatingSelected"              
            />   
          </span>
          <span v-if="product.user_rating">
            <span  class="dac-names" >Ваша оценка</span>
            <star-rating             
              :star-size="40"             
              :rating="product.user_rating"
              :read-only="true"
            />     
          </span>                     
        </div>                                                               
        <ModalWindow :visible="isRequestFormVisible" :product="product" :hide="hideRequestForm"/>                
    </div> 
    <MobileMenu/>
    <Footer/>   
</template>

<script setup lang="ts">
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import MobileMenu from '../components/MobileMenu.vue';
import { useItem } from '../composables/useItem';
import ModalWindow from '../components/ModalWindow.vue'
// @ts-ignore
import StarRating from 'vue-star-rating';
import IconCopy from '@/components/icons/IconCopy.vue';
import IconLeft from '@/components/icons/IconLeft.vue';
import IconRight from '@/components/icons/IconRight.vue';
import IconUp from '@/components/icons/IconUp.vue';
import IconPlus from '@/components/icons/IconPlus.vue';
import IconMinus from '@/components/icons/IconMinus.vue';
import ScaleIcon from '@/components/icons/ScaleIcon.vue';
import ScaleMIcon from '@/components/icons/ScaleMIcon.vue';
import IconDown from '@/components/icons/IconDown.vue';
import Breadcrumbs from '@/components/Breadcrumbs.vue';

const {
  products,
  addToCart,
  cart,
  increment,
  decrement,    
  isRequestFormVisible, 
  showRequestForm, 
  hideRequestForm,
  currentImage,
  changeImage,
  currentIndex,
  copyText,
  isCopied,
  scrollImages,
  showMoreImages,
  startIndex,
  handleMouseMove,
  handleMouseLeave,
  imageStyle,
  ScaleImage,
  scaleImage,
  isSticky,
  showFullAtt,
  isExpanded,
  isUser,
  handleRatingSelected,
} = useItem();
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
  display: flex;
  flex-direction: column;  
  position: relative;
}

.product-card{
  position: relative;
  display: flex;
  gap: 15px;
  justify-content: space-between;
  margin-bottom: 40px;
}

.product-card-images{
  display: flex;
  align-items: center;  
  gap: 40px;  
}

.main-image{
  display: flex;
  align-items: start;
  justify-content: start;
  width: min-content;
  margin-left: 50px;
  position: relative;
  height: 100%;
  overflow: hidden;
}


.main-image img{ 
  width: 520px;
  height: 520px;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.b-next,.b-prev{  
  display: flex;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: #F5F5F5;;
  border: none;
  padding: 8px;
  cursor: pointer;
  z-index: 10; 
  border-radius: 90px;  
}

.b-prev{
  left: 0; 
}

.b-prev svg{
  transform: translateX(-10%);
}

.b-next svg{
  transform: translateX(5%);
}

.b-next {
    right: 0; 
  }

.scale-button{
  background-color: transparent;
  border: none;
  display: flex;
  align-items: center;
  
}

.tooltiptext{
  visibility: hidden;
  position: absolute;
  z-index: 1;  
  background-color: #F5F5F5;  
  padding: 5px 10px;
  border-radius: 4px 4px 0px 4px;  
  right: 125%;
  top: -25px;
  white-space: nowrap;
  font-size: 10px;
}

.scale-button-container:hover .tooltiptext{
  visibility: visible;
}

.scale-button-container{
  position: relative;
  display: inline-block;
  height: fit-content;
}

.scale-button-container .tooltiptext::after {
  content: " ";
  position: absolute;
  top: 80%;
  border-width: 8px 8px 0 8px;
  border-style: solid;
  border-color: transparent transparent transparent #F5F5F5;
  left: 100%;

}

.thumbnails{ 
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px; 
  width: min-content;
  overflow-y: auto;
  max-height: 600px;
}

.thumbnails img{
  width: 88px; 
  height: 88px;
  object-fit: cover; 
  cursor: pointer;
  border: 1px solid #bbbdbe;
  border-radius: 4px;
  transition: border-color 0.3s ease;
}

.thumbnails img:hover{
  border: 1px solid #003464;
}

.thumbnail.active{
  border-color: #003464;
}

.show-more-button{
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background-color: #F5F5F5;

  border-radius: 100vmin;
}

.up,.down{
  background-color: transparent;
}

.up svg{
  transform: translateY(-5%);  
}

.down svg{
  transform: translateY(-6%) translateX(-1%);
}

.indicators{
  display: flex;
  justify-content: center;
  gap: 8px;  
}

.indicator{
  width: 7px;
  height: 7px;
  background-color: #ccc; 
  border-radius: 50%; 
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.indicator.active {
  background-color: #003464; 
}

.product-info-box{
  display: flex;
  flex-direction: column;
  align-items: start;  
  border-radius: 8px;
  box-shadow: 0px 0px 8px 0px  rgba(0, 0, 0, 0.2);
  padding: 24px;
  width: 100%;
  margin-left: 50px;
  height: 100%;
  /* transition: all 0.3s ease; */
}

.product-info-box.sticky {
  position: fixed;
  max-width: 343px;
  width: 30%;
  z-index: 100;
  transition: top 0.2s ease-out;
  height: max-content; 
  padding-right: 24px;
  margin-right: 15px;
  visibility: hidden;
}


.item-article{
  opacity: 60%;
  font-size: 14px;
  margin-bottom: 12px;
}

.copy-button{
  background-color: transparent;
  border: none;
  font-weight: 350;
  font-size: 14px;
}
.copy-button svg{
  padding-bottom: 3px;
}

.item-name{
  font-size: 16px;
  font-weight: 550;
  margin-bottom: 12px;
}

.star-rating{
  margin-bottom: 12px;
}

::v-deep(.star-rating svg) {  
  display: flex;
}

.item-price-container{
  margin-bottom: 12px;
}

.item-price-container div{
  font-weight: 650;
  font-size: 24px;
}

.buttons-cintainer{
  display: flex;
  width: 100%;
}

.add-to-cart{
  background-color: #003464;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;  
  margin-top: auto;
  width: 100%;
}

.not-available{
  background-color: #003464;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;  
}

.quantity-control{
  background-color: #003464;
  color: #fff;
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  margin-top: auto;
  display: flex;
  justify-content: space-around; 
  align-items: center; 
  margin-top: auto; 
  height: 40px;   
  width: 100%;
}

.quantity-control button{
  background-color: #003464;
  color: #fff;
  border: none; 
  display: flex; 
}

.quantity-control span{
  display: flex; 
}

.description-attribute-container{
  display: flex;
  align-items: start;
  flex-direction: column;
  gap: 20px;
  width: 60%;
  margin-bottom: 40px;
}

.attributes-section, .description-section{
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 16px;
}

.border-line{
  width: 100%;
  background-color: #003464;
  height: 2px; 
}

.dac-names{
  font-size: 20px;
  font-weight: 700;
}

.attributes-container {
  display: flex;
  flex-direction: column;  
  gap: 8px;              
  width: 100%;
  max-height: 198px;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.attributes-container.expanded {
  max-height: none;
}

.button-full-att{
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background-color: #F5F5F5;
  width: 112px;
  height: 40px;
  border-radius: 120px;
}

.attribute-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: last baseline;        
}

.attribute-name {  
  max-width: 200px;   
  text-align: start;  
}

.attribute-dots {
  border-bottom: 1px dotted #e8e7e7;  

}

.attribute-value {  
  max-width: 200px; 
  text-align: end;     
}
  
.description-container{
  display: flex;
  flex-direction: column;  
  gap: 8px;              
  width: 100%;
}

.rate-item-container{
  display: flex;
  align-items: start;
  flex-direction: column;
  gap: 20px;
  width: 60%;
  margin-bottom: 40px;
}

.sticky-sentinel {
  position: absolute;
  bottom: 300px;
  right: 0;

}

@media (min-width: 1024px) {
  .indicators{
    display: none;
  }
}



@media (max-width: 1024px) {
  .product-card {
    flex-direction: column;
  }

  .product-card-images{
    flex-direction: column;
    align-self: center;
  }

  .thumbnails{
    flex-direction: row;
    order: 2;
  }

  .main-image{
    order: 1;
    margin-left: 0;
  }

  .main-image img{
    width: 420px;
    height: 420px;
  }

  .down svg{
    transform: rotate(-90deg) translateX(6%) translateY(5%)
  }

  .up svg{
    transform: rotate(270deg) translateX(5%);
  }

  .product-info-box{
    margin-left: 0px;
  }

  .b-next{
    display: none;
  }

  .b-prev{
    display: none;
  }

  .indicators{
    display: none;
  }
  .scale-button-container{
    display: none;
  }
  .attributes-container {    
    gap: 4px;              
    width: 100%;
  }

  .attribute-item {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: last baseline;        
  }

  .attribute-name {  
    width: min-content;    
    text-align: start;
    min-width: 100px;  
  }

  .attribute-dots {
    border-bottom: 1px dotted #e8e7e7;  

  }

  .attribute-value {  
    width: min-content; 
    min-width: 50px;
    text-align: end;     
  }

  .description-attribute-container{
    width: 100%;
  }

    
  .description-container{
    display: flex;
    flex-direction: column;  
    gap: 4px;              
    width: 100%;
  }

  .border-line{
    width: 100%;
  }

  .product-info-box.sticky {
    display: none;
   
  }

  .rate-item-container
  {
    display: flex;
    flex-direction: column;  
    gap: 16px;              
    width: 100%;
  }

  
}

@media (max-width: 440px) { 
  .product-card-images{
    gap: 0;
  }

  .main-image img{
    order: 1;
    width: 380px;
    height: 380px;
  }

  .thumbnails{
    display: none;
    order: unset;
  } 

  .indicators{  
    order: 2;
    display: inherit;
  }

  .b-next,.b-prev{
    display: flex;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    border: none;
    padding: 8px;
    cursor: pointer;
    z-index: 10;       
  }

  .attributes-container {    
    gap: 4px;              
    width: 100%;
  }

  .attribute-item {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: last baseline;        
  }

  .attribute-name {  
    width: min-content;    
    text-align: start;
    min-width: 100px;  
  }

  .attribute-dots {
    border-bottom: 1px dotted #e8e7e7;  

  }

  .attribute-value {  
    width: min-content; 
    min-width: 50px;
    text-align: end;     
  }
    
  .description-container{
    display: flex;
    flex-direction: column;  
    gap: 4px;              
    width: 100%;
  }

  .border-line{
    width: 100%;
  }
}

</style>
