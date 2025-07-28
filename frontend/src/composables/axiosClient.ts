import axios from 'axios';

const API_URL = import.meta.env.VITE_BASE_URL;

const apiClient = axios.create({
    baseURL: API_URL,
    withCredentials: true,
});

apiClient.interceptors.request.use(
    async (config) => {
        // Получение CSRF токена перед каждым запросом
        const response = await axios.get(API_URL + 'generate-key/', { withCredentials: true });
        const csrfToken = response.data.csrf_token;
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default apiClient;
