/* eslint-disable default-case */
import React from 'react';
import Header from '../components/Header'

class RenderSecretUrl extends React.Component{ 

    constructor(props) {
        super(props);
        this.secret_url = props.location.state.secret_url;
    }

    render(){
        return (
            <React.Fragment>
                <Header/>
                <div>
                    Use this url {this.secret_url} to get your secret and don't forget your secret phrase!
                </div>
            </React.Fragment>
        )
    }
}

export default RenderSecretUrl;