import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import {requestLogin, requestPassword} from './useAPI'


interface User {
  email: string;
  password: string;
}

export function useLogin(){
    const router = useRouter();
    const password = ref('');
    const email = ref('');
    const passwordReceived = ref(false);
    const user: User = {
        email: email.value,
        password: password.value,
    };
  

    async function handleFormSubmit() {
    if (!passwordReceived.value) {
        await tempPasswordGet();
    } else {
        await logIn();
    }
    }

    async function tempPasswordGet() {
    try {
        const response = await requestPassword(email.value)    
        passwordReceived.value = true;
    } catch (error) {
        console.error('Error requesting password:', error);    
    }
    }

    async function logIn() {
        const user: User = {
          email: email.value,
          password: password.value,
        };
      
        try {
          const response = await requestLogin(user);
          console.log('User logged in successfully:', response.data);
          alert('Вы успешно авторизировались');
          localStorage.setItem('user', JSON.stringify(response.data));
          localStorage.setItem('access_token', response.data.tokens.access);
          localStorage.setItem('refresh_token', response.data.tokens.refresh);
          router.push('/profile'); 
        } catch (error) {
          console.error('Error logging in:', error);
          alert('Что-то пошло не так, попробуйте позже.');
        }
      }

    return{
        email,
        password,
        passwordReceived,
        handleFormSubmit,        
    }
}

