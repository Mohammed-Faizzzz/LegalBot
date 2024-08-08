import React from 'react';
import './styles/Footer.css';
import FacebookIcon from '@mui/icons-material/Facebook';
import TwitterIcon from '@mui/icons-material/Twitter';
import LinkedInIcon from '@mui/icons-material/LinkedIn';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="footer-section">
                    <h3>Let's Connect</h3>
                    <div className="social-icons">
                        <FacebookIcon className="icon" />
                        <TwitterIcon className="icon" />
                        <LinkedInIcon className="icon" />
                    </div>
                    <p>By continuing past this page, you agree to our <a href="#" sx={{color: '#61dafb'}}>terms of use</a></p>
                </div>
                <div className="footer-section">
                    <h3>Resources</h3>
                    <ul>
                        <li><a href="#">Case Studies</a></li>
                        <li><a href="#">Blog</a></li>
                        <li><a href="#">Webinars</a></li>
                        <li><a href="#">Whitepapers</a></li>
                    </ul>
                </div>
                <div className="footer-section">
                    <h3>Support</h3>
                    <ul>
                        <li><a href="#">FAQs</a></li>
                        <li><a href="#">Contact Us</a></li>
                        <li><a href="#">User Guides</a></li>
                        <li><a href="#">Customer Support</a></li>
                    </ul>
                </div>
                <div className="footer-section">
                    <h3>Company</h3>
                    <ul>
                        <li><a href="#">About Us</a></li>
                        <li><a href="#">Careers</a></li>
                        <li><a href="#">News</a></li>
                        <li><a href="#">Privacy Policy</a></li>
                    </ul>
                </div>
            </div>
            <div className="footer-bottom">
                <ul>
                    <li><a href="#">Terms of Use</a></li>
                    <li><a href="#">Privacy Policy</a></li>
                    <li><a href="#">Cookies Policy</a></li>
                    <li><a href="#">Manage Cookies</a></li>
                </ul>
                <p>© 2024 LexCelerate. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;
