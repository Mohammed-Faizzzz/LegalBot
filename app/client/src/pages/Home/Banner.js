import React from 'react';
import './styles/Banner.css';
import CustomListItem from './CustomListItem';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import AccountCircleIcon from '@mui/icons-material/AccountCircle'; // Used if needed
import LiveHelpIcon from '@mui/icons-material/LiveHelp';
import { useNavigate } from 'react-router-dom';

const Banner = () => {

    const navigate = useNavigate();

    const handleHomeClick = () => {
        console.log('Home clicked');
        navigate('/');
    }

    const handleLoginLogout = () => {
        if (isLoggedIn) {
        // Logic for logging out
        } else {
        navigate('/login');
        }
    };
    const logo = process.env.PUBLIC_URL + '/logo_full.png';

    const isLoggedIn = false; // This should ideally come from a global state or context

    return (
        <Box>
            <div className='banner'>
                <Toolbar />
                <div className='banner-content'>
                    <div className='logo-container'>
                        <img src={logo} alt='logo' className='logo' onClick={handleHomeClick} />
                    </div>
                    <Box className='drawer-content'>
                        <List className='drawer-list'>
                            <CustomListItem IconComponent={AccountCircleIcon} primary="Try It" />
                            <CustomListItem IconComponent={LiveHelpIcon} primary="Help" />
                            <CustomListItem
                                IconComponent={AccountCircleIcon}
                                primary={isLoggedIn ? 'Logout' : 'Login'}
                                onClick={handleLoginLogout}
                            />
                        </List>
                    </Box>
                </div>
            </div>
        </Box>
    );
};

export default Banner;
