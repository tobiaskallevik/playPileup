import React, {useEffect, useState} from 'react'
import {ConfigProvider, theme, Button, Card, Result} from "antd";
import './App.css'
import './index.css'
import AuthPage from "./modules/auth/pages/AuthPage.jsx";
import {BulbFilled, BulbOutlined} from "@ant-design/icons";
import {AuthProvider} from "./modules/auth/context/AuthContext.jsx";
import {BrowserRouter, Route, Router, Routes} from "react-router-dom";
import Home from "./modules/core/pages/Home.jsx";
import PrivateRoute from "./modules/auth/utils/PrivateRoutes.jsx";


function App() {
  const { defaultAlgorithm, darkAlgorithm } = theme;

  // Get the saved theme from local storage
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme ? savedTheme === 'dark' : true;
  });

  useEffect(() => {
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    document.body.style.backgroundColor = isDarkMode ? '#242424' : '#f0f2f5'; // Update body background color
  }, [isDarkMode]);

  const handleClick = () => {
    setIsDarkMode((previousValue) => !previousValue);
    document.body.style.backgroundColor = isDarkMode ? '#f0f2f5' : '#242424';
  };

  return (
    <ConfigProvider
      theme={{
      algorithm: isDarkMode ? darkAlgorithm : defaultAlgorithm,
    }}>
      <Button onClick={handleClick} style={styles.themeBtn} icon={isDarkMode ? <BulbFilled /> : <BulbOutlined />}></Button>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<AuthPage />} />
            <Route path="/" element={<PrivateRoute><Home /></PrivateRoute>} />
            <Route path="*" element={
              <Result
                status="404"
                title="404"
                subTitle="Sorry, the page you visited does not exist."
              />
            } />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </ConfigProvider>
  );
}

export default App

const styles = {
  themeBtn: {
    position: 'fixed',
    top: '1rem',
    right: '1rem',
    zIndex: 999,
  },
};
