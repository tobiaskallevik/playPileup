import React, {useState} from "react";
import '/src/App.css';
import '../styles/auth.css';
import Login from '../components/Login.jsx';
import Register from '../components/Register.jsx';
import {Card, Divider, Space, Typography} from "antd";
const { Text, Link } = Typography;


export default function AuthPage() {

  const [isRegister, setIsRegister] = useState(false);
  const toggleRegister = () => setIsRegister(prev => !prev);

  const handleClick = () => {
    setIsRegister((previousValue) => !previousValue);
    console.log('Register clicked')
  }

  return (
    <div className="authContainer">
      <Card className="authForm">
        <Typography.Title level={1} style={{ margin: 0 }}>
          Welcome To PlayPileup
        </Typography.Title>
        {isRegister ? (
          <>
            <Register onToggleRegister={toggleRegister} />
            <Divider>Or</Divider>
            <Text className="clickable-text" onClick={handleClick}>Already Registered? Login instead.</Text>
          </>
        ) : (
          <>
            <Login />
            <Divider>Or</Divider>
            <Text className="clickable-text" onClick={handleClick}>Register Now!</Text>
          </>
        )}
      </Card>
    </div>
  );
}
