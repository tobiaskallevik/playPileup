import React, {useContext} from "react";
import '../../shared/styles/global.css';
import '../styles/auth.css';
import {Button, Form, Input, Typography} from "antd";
import {LockOutlined, MailOutlined, UserOutlined} from "@ant-design/icons";
import AuthContext from "../context/AuthContext.jsx";

export default function Register({ onToggleRegister }){

  const {registerUser} = useContext(AuthContext)

  const handleSubmit = (values) => {
    const { email, username, password, password2 } = values;
    registerUser(email, username, password, password2);
    console.log("User registered with email: ", email, " username: ", username, " password: ", password, " password2: ", password2);
    onToggleRegister(); // Toggle back to login
  }

  return (
    <div className="authItem">
      <Typography.Title level={3} style={{margin: 10}}>
        Please Register to Continue
      </Typography.Title>
      <Form
        name="normal_login"
        className="login-form"
        initialValues={{
          remember: true,
        }}
        style={{ margin: 'auto'}}
        onFinish={handleSubmit}
      >
        <Form.Item
          name="email"
          type="email"
          rules={[
            {
              required: true,
              message: 'Please input your Email!',
            },
          ]}
        >
          <Input prefix={<MailOutlined className="site-form-item-icon"/>} placeholder="Email"/>
        </Form.Item>

        <Form.Item
          name="username"
          type="username"
          rules={[
            {
              required: true,
              message: 'Please input your Username!',
            },
          ]}
        >
          <Input prefix={<UserOutlined className="site-form-item-icon"/>} placeholder="Username"/>
        </Form.Item>

        <Form.Item
          name="password"
          type="password"
          rules={[
            {
              required: true,
              message: 'Please input your Password!',
            },
          ]}
        >
          <Input
            prefix={<LockOutlined className="site-form-item-icon"/>}
            type="password"
            placeholder="Password"
          />
        </Form.Item>

        <Form.Item
          name="password2"
          type="password2"
          rules={[
            {
              required: true,
              message: 'Please re-enter your Password!',
            },
          ]}
        >
          <Input
            prefix={<LockOutlined className="site-form-item-icon"/>}
            type="password"
            placeholder="Re-enter password"
          />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" className="login-form-button">
            Register
          </Button>
        </Form.Item>
      </Form>
    </div>
  )
}
