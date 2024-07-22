import { createContext, useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import swal from 'sweetalert2';

// Create a new context for authentication
const AuthContext = createContext();
export default AuthContext;

// Create a new provider for authentication
export const AuthProvider = ({ children }) => {
    // Navigation and loading state
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);

    // State to store authentication tokens, initially tries to load from localStorage
    const [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem("authTokens")
            ? JSON.parse(localStorage.getItem("authTokens"))
            : null
    );

    // State to store user details, initially decoded from JWT token in localStorage if present
    const [user, setUser] = useState(() =>
        localStorage.getItem("authTokens")
            ? jwtDecode(localStorage.getItem("authTokens"))
            : null
    );

    // Function to handle user login
    const loginUser = async (email, password) => {
        // Perform POST request to login endpoint with user credentials
        const response = await fetch(import.meta.env.VITE_TOKEN_URL, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, password }),
        });

        // Parse response data as JSON
        const data = await response.json();
        console.log(data);

        // If response status is 200, login is successful, store the access token in localStorage and navigate to home page
        // Else, display an error message
        if(response.status === 200 && typeof data.access === 'string'){
            console.log("Login successful");
            setAuthTokens(data.access);
            setUser(jwtDecode(data.access));
            localStorage.setItem("authTokens", JSON.stringify(data));
            navigate("/");
            await swal.fire({
                title: "Login Successful",
                icon: "success",
                toast: true,
                timer: 2000,
                position: 'top-right',
                timerProgressBar: true,
                showConfirmButton: false,
            })
        } else {
            console.log(response.status);
            console.log("Server error");
            await swal.fire({
                title: "Username or password does not exists",
                icon: "error",
                toast: true,
                timer: 2000,
                position: 'top-right',
                timerProgressBar: true,
                showConfirmButton: false,
            })

        }
    }

    // Function to handle user registration
    const registerUser = async (email, username, password, password2) => {
        // Perform POST request to register endpoint with user details
        const response = await fetch(import.meta.env.VITE_REGISTER_URL, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, username, password, password2 }),
        });

        // If response status is 201, registration is successful else display an error message
        if(response.status === 201){
            console.log("Register successful");
            await swal.fire({
                title: "Registration Successful, Login Now",
                icon: "success",
                toast: true,
                timer: 2000,
                position: 'top-right',
                timerProgressBar: true,
                showConfirmButton: false,
            })
        } else {
            console.log(response.status);
            console.log("Server error");
            await swal.fire({
                title: "Username or email already exists",
                icon: "error",
                toast: true,
                timer: 2000,
                position: 'top-right',
                timerProgressBar: true,
                showConfirmButton: false,
            })
        }
    }

    // Function to handle user logout
    const logoutUser = () => {
        // Clear authTokens and user state, remove authTokens from localStorage and navigate to login page
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem("authTokens")
        swal.fire({
            title: "You have been logged out...",
            icon: "success",
            toast: true,
            timer: 2000,
            position: 'top-right',
            timerProgressBar: true,
            showConfirmButton: false,
        }).then(r => r.dismiss === swal.DismissReason.timer && window.location.reload())
    }

    // Context data to be passed to consumers
    const contextData = {
        user,
        setUser,
        authTokens,
        setAuthTokens,
        registerUser,
        loginUser,
        logoutUser,
    }

    // Load user details from JWT token in authTokens
    useEffect(() => {
        if (authTokens && typeof authTokens.access === 'string') {
            setUser(jwtDecode(authTokens.access))
        }
        setLoading(false)
    }, [authTokens, loading])

    // Return provider
    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    )

};
