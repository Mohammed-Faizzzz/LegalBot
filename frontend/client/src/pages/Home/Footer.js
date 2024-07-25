import React from 'react';
import './styles/Footer.css';
import FacebookIcon from '@mui/icons-material/Facebook';
import TwitterIcon from '@mui/icons-material/Twitter';
import InstagramIcon from '@mui/icons-material/Instagram';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="footer-section">
                    <h3>Let's Connect</h3>
                    <div className="social-icons">
                        <FacebookIcon className="icon" />
                        <TwitterIcon className="icon" />
                        <InstagramIcon className="icon" />
                    </div>
                    <p>By continuing past this page, you agree to our <a href="#" sx={{color: '#61dafb'}}>terms of use</a></p>
                </div>
                <div className="footer-section">
                    <h3>Categories</h3>
                    <ul>
                        <li><a href="#">Concerts</a></li>
                        <li><a href="#">Sports</a></li>
                        <li><a href="#">Arts, Theatre & Comedy</a></li>
                        <li><a href="#">Family Entertainment</a></li>
                    </ul>
                </div>
                <div className="footer-section">
                    <h3>Customer Care</h3>
                    <ul>
                        <li><a href="#">FAQs</a></li>
                        <li><a href="#">Contact Us</a></li>
                        <li><a href="#">Terms of Use</a></li>
                        <li><a href="#">News</a></li>
                    </ul>
                </div>
                <div className="footer-section">
                    <h3>Be Part Of It</h3>
                    <ul>
                        <li><a href="#">Ticket Your Event</a></li>
                    </ul>
                </div>
                <div className="footer-section">
                    <h3>Corporate</h3>
                    <ul>
                        <li><a href="#">Who We Are</a></li>
                        <li><a href="#">Careers</a></li>
                        <li><a href="#">Across The Globe</a></li>
                    </ul>
                </div>
            </div>
            <div className="footer-bottom">
                <ul>
                    <li><a href="#">Purchase Policy</a></li>
                    <li><a href="#">Privacy Policy</a></li>
                    <li><a href="#">Cookies</a></li>
                    <li><a href="#">Manage my cookies</a></li>
                </ul>
                <p>© 2024 SmarTix. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;
