import axios from "axios";
import { jwtDecode } from "jwt-decode";
import dayjs from "dayjs";
import { useContext } from "react";
import AuthContext from "../context/AuthContext.jsx";

const baseURL = import.meta.env.VITE_AUTHENTICATION_URL;

const useAxios = () => {
    const { authTokens, setUser, setAuthTokens } = useContext(AuthContext);

    // Create an axios instance with the base URL and authorization headers
    const axiosInstance = axios.create({
        baseURL,
        headers: { Authorization: `Bearer ${authTokens?.access}` }
    });

    // Add a request interceptor to the axios instance
    axiosInstance.interceptors.request.use(async req => {
        // Decode the JWT access token to get the user information and check if it is expired
        const user = jwtDecode(authTokens.access);
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;

        // If the token is not expired, proceed with the request as is
        if(isExpired) return req;

        // If the token is expired, perform a POST request to the refresh token endpoint with the refresh token
        const response = await axios.post(`${baseURL}/token/refresh/`, {
            refresh: authTokens.refresh
        });

        // Store the new access token in localStorage and set the new access token in the axios instance headers
        localStorage.setItem("authTokens", JSON.stringify(response.data));
        localStorage.setItem("authTokens", JSON.stringify(response.data));

        setAuthTokens(response.data);
        setUser(jwtDecode(response.data.access));

        req.headers.Authorization = `Bearer ${response.data.access}`;
        return req;
    });

    return axiosInstance;
};

export default useAxios;
