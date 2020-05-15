/* eslint-disable default-case */
import React from 'react';
import Header from '../components/Header'
import RenderSecretUrlStyles from '../styles/RenderSecretUrl.module.css'

class RenderSecretUrl extends React.Component{ 

    constructor(props) {
        super(props);
        this.secret_url = props.location.state.secret_url;
    }

    render(){
        console.log(this.props.location)
        return (
            <React.Fragment>
                <Header/>
                <div className={RenderSecretUrlStyles.container}>
                    <span className={RenderSecretUrlStyles.link}> Use this <a href={this.secret_url}> link </a> to get your secret and don't forget your secret phrase! </span>
                </div>
            </React.Fragment>
        )
    }
}

export default RenderSecretUrl;