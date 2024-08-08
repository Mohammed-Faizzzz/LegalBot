import React from 'react';
import AccountCircle from '@mui/icons-material/AccountCircle';

const Login_button = () => {
    return (
        <div className="login_button" style={{ display: 'flex', flexDirection: 'row', flex: 1, alignContent: 'center'}}>
            <AccountCircle style={{alignSelf: 'center'}}/>
            <p style={{ fontSize: 14, alignSelf: 'center', marginLeft: 8 }}>Login/Sign Up</p>
        </div>
    );
}

export default Login_button;