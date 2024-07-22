import React, { useContext } from 'react';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
import { jwtDecode } from "jwt-decode"
import AuthContext from '../../auth/context/AuthContext';
import { Button, Dropdown, Space } from 'antd';
import { DownOutlined, SmileOutlined } from '@ant-design/icons';
const { Header, Content, Footer } = Layout;


const MainLayout = ({ children }) => {

  // User context
  const {user, logoutUser} = useContext(AuthContext)
  const token = localStorage.getItem("authTokens")

  // Get user id from token
  if (token){
    const decoded = jwtDecode(token)
    var user_id = decoded.user_id
  }

  // Items for profile dropdown
  const items = [
    {
      label: 'Profile',
      key: '1',
    },
    {
      label: 'Settings',
      key: '2',
    },
    {
      type: 'divider',
    },
    {
      label: 'Logout',
      key: '3',
      danger: true,
      onClick: () => {
        logoutUser();
      },
    },
  ];



  return (
    <div>
      <Header style={styles.header}>
        <div style={styles.userDropdown}>
          <Dropdown menu={{items}} trigger={['click']} >
            <a style={{color: 'white'}} onClick={(e) => e.preventDefault()}>
              <Space>
                {user.username}
                <DownOutlined />
              </Space>
            </a>
          </Dropdown>
        </div>
      </Header>
      <Content style={styles.content}>
        {children}
      </Content>

    </div>
  );
};

export default MainLayout;

const styles = {
  header: {
    position: 'sticky',
    top: 0,
    display: 'flex',
    zIndex: 1,
    marginBottom: '1rem',
  },
  content: {
      
  },
  footer: {
    textAlign: 'center',
   
    bottom: 0,
  },
  userDropdown: {
    marginLeft: 'auto',
    paddingRight: '1rem',
  },


};