<template>
    <div v-if="localShowModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-container">
            <button class="close-btn" @click="closeModal">&times;</button>
            <div class="file-container">
                <form>
                    <input type="file" id="media" accept="image/*" @change="handleFileUpload" />                    
                </form>
            </div>
            <div class="images" v-if="imageSrc">
                <div class="images-lists">
                    <div class="image-container">
                        <img :src="imageSrc" class="image-style" />
                    </div>
                    <div class="cross-icon" @click="removeImage">
                        &times;
                    </div>
                    <p class="text-center">{{ selectedFile?.name }}</p>
                </div>
            </div>
            <button class="search-by-image" @click="searchByImage" :disabled="!imageBase64">
                Найти по фото 
            </button> 
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from "vue";
import { requestSearchImage } from "@/composables/useAPI";
import { useRouter } from "vue-router";
import { useProductsStore } from "@/stores/productsByImage";

const props = defineProps({
    showModal: Boolean
});

const localShowModal = ref(props.showModal);
const emit = defineEmits(["update:showModal"]);

watch(() => props.showModal, (newValue) => {
    localShowModal.value = newValue;
});

const closeModal = () => {
    localShowModal.value = false;
    emit("update:showModal", false); 
};

const removeImage = () => {
    imageSrc.value = null;
    selectedFile.value = null;
    imageBase64.value = null;
};

const router = useRouter();
const productsStore = useProductsStore();

const selectedFile = ref<File | null>(null);
const imageSrc = ref<string | null>(null);
const imageBase64 = ref<string | ArrayBuffer | null>(null);


const handleFileUpload = (e: Event): void => {
    const input = e.target as HTMLInputElement;
    const file = input.files?.[0];
    
    selectedFile.value = null;
    imageSrc.value = null;
    imageBase64.value = null;

    if (!file) {
        console.error('No file selected');
        return;
    }

    const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
    const MAX_FILE_SIZE = 5 * 1024 * 1024;

    if (!ALLOWED_TYPES.includes(file.type)) {
        alert(`Неподдерживаемый формат файла. Разрешены: ${ALLOWED_TYPES.join(', ')}`);
        input.value = '';
        return;
    }

    if (file.size > MAX_FILE_SIZE) {
        alert(`Файл слишком большой. Максимальный размер: ${MAX_FILE_SIZE / 1024 / 1024}MB`);
        input.value = '';
        return;
    }

    selectedFile.value = file;
    imageSrc.value = URL.createObjectURL(file);

    const reader = new FileReader();

    reader.onload = (event: ProgressEvent<FileReader>) => {
        if (!event.target?.result) {
            console.error('File reading error');
            return;
        }
        imageBase64.value = event.target.result;
    };

    reader.onerror = () => {
        console.error('Error reading file');
        input.value = '';
    };

    reader.readAsDataURL(file);
};

const searchByImage = async () => {
    if (imageBase64.value) {
        try {
            const response = await requestSearchImage(imageBase64.value as string);
            productsStore.setProducts(response);

            router.push({ 
                name: 'search-by-image',
            });

        } catch (error) {
            console.error("Error searching by image:", error);
        }
    } else {
        console.log("No image selected");
    }
};

</script>


  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1001;
  }
  
  .modal-container {
    background: white;
    padding: 20px;
    border-radius: 10px;
    width: 500px;
    position: relative;
  }
  
  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    border: none;
    background: transparent;
    font-size: 24px;
    cursor: pointer;
  }
  
  .file-container {
    margin-bottom: 20px;
  }
  
  .images {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
  }
  
  .images-lists {
    position: relative;
  }
  
  .image-container {
    padding: 4px;
    border: 0.5px solid #a0a0a0;
    border-radius: 10px;
  }
  
  .image-style {
    height: 100px;
    width: 100px;
    object-fit: cover;
  }
  
  .cross-icon {
    position: absolute;
    top: 0;
    right: 0;
    cursor: pointer;
  }

  .search-by-image{
    background-color: #003464;
    color: #fff;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: auto;

  }
  </style>
  