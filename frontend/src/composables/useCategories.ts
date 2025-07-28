import { ref, onMounted } from 'vue';
import { fetchCategory } from './useAPI';


interface Category {
  id: number;
  name: string;
  parent: string | null;
  children: Category[];
  image: string | null;
}

export function useCategories(){
    const categories = ref<Category[]>([]);
    const collapsedCategories = ref<number[]>([]);

    onMounted(() => {
        fetchCategories();
        localStorage.removeItem("savedFilters")
        localStorage.removeItem("scrollY")
    });
    
    const fetchCategories = async () => {
      try {
        fetchCategory()
        .then(data => {
          categories.value = data;
          initializeCollapsedCategories(data);
        });                    
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
 
    const initializeCollapsedCategories = (categories: Category[]) => {
      const collapseAllNested = (category: Category) => {
        if (category.children && category.children.length) {
          category.children.forEach(child => {
            collapsedCategories.value.push(child.id); 
            collapseAllNested(child); 
          });
        }
      };

      categories.forEach(category => {
        collapseAllNested(category); 
      });
    };

      const toggleCollapse = (categoryId: number) => {
        if (collapsedCategories.value.includes(categoryId)) {
          collapsedCategories.value = collapsedCategories.value.filter(id => id !== categoryId);
        } else {
          collapsedCategories.value.push(categoryId);
        }
      };

      return {
        categories,
        collapsedCategories,
        toggleCollapse,        
      };
}