import React, {useContext} from "react";
import '../../shared/styles/global.css';
import '../styles/auth.css';
import {Button, Form, Input, Typography} from "antd";
import {LockOutlined, MailOutlined, UserOutlined} from "@ant-design/icons";
import AuthContext from "../context/AuthContext.jsx";

export default function Login(){

  const {loginUser} = useContext(AuthContext)

  const handleSubmit = (values) => {
    const { email, password } = values;
    email.length > 0 && loginUser(email, password)
    console.log(email)
    console.log(password)
  }

  return (
    <div className="authItem">
      <Typography.Title level={3} style={{margin: 10}}>
        Please Login to Continue
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
              message: 'Please input your Username!',
            },
          ]}
        >
          <Input prefix={<MailOutlined className="site-form-item-icon"/>} placeholder="Email"/>
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
        <Form.Item>
          <Button type="primary" htmlType="submit" className="login-form-button">
            Log in
          </Button>
        </Form.Item>
      </Form>
    </div>
  )
}
