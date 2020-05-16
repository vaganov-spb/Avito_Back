import React from 'react';
import Header from '../components/Header';
import RenderSecretStyles from '../styles/RenderSecret.module.css';

class RenderSecretUrl extends React.Component{ 

    constructor(props) {
        super(props);
        this.secret = props.location.state.secret;
    }

    render(){
        console.log(this.props.location)
        return (
            <React.Fragment>
                <Header/>
                <div className={RenderSecretStyles.container}>
                    <div className={RenderSecretStyles.congrats}> Your Secret Text: </div>
                    <div className={RenderSecretStyles.text}>
                        {this.secret}
                    </div>
                </div>
            </React.Fragment>
        )
    }
}

export default RenderSecretUrl;