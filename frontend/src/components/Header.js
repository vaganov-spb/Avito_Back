import React from 'react';
import HeaderStyles from '../styles/Header.module.css';

function Header(props) {
    return (
        <div className={HeaderStyles.header}>
            <div className={HeaderStyles.title}>
                OneTimeSecret
            </div>
            <img className={HeaderStyles.logo} src='https://www.t-barcyprus.com/wp-content/uploads/2018/01/TBC201700990A.svg' alt=''/>
        </div>
    );
}

export default Header