import { Route, Navigate } from 'react-router-dom';
import { useContext } from "react";
import AuthContext from "../context/AuthContext.jsx";

// Create private route component
const PrivateRoute = ({ children }) => {
    const { user } = useContext(AuthContext);
    return user ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
