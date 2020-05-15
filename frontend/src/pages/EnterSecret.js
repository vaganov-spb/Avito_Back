/* eslint-disable default-case */
import React from 'react';
import { Redirect } from 'react-router-dom';
import Header from '../components/Header'
import InfoField from '../components/InfoField'
import EnterSecretStyles from '../styles/EnterSecret.module.css'
import Lifetime from '../components/Lifetime'
import dataformat from '../utils/dataformat'

class EnterSecret extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
            days: null,
            hours: null,
            minutes: null,
            seconds: null,
            text: null,
            phrase: null,
            errors: null,
            secret_url: null,
        };
        this.SetParam  = this.SetParam.bind(this);
        this.SendToBackend  = this.SendToBackend.bind(this);
    }

    SetParam(parametr, value){
        switch(parametr) {
            case 'days':
                this.setState({days: value});
                break;
            case 'hours':
                this.setState({hours: value});
                break;
            case 'minutes':
                this.setState({minutes: value});
                break;
            case 'seconds':
                this.setState({seconds: value});
                break;
            case 'text':
                this.setState({text: value});
                break;
            case 'phrase':
                this.setState({phrase: value});
                break;
        }   
    }

    async SendToBackend(){
        const data = dataformat(this.state);
        console.log(data)
        await fetch("http://localhost:8000/generate/", {
            method: "POST",
            // credentials: "include",
            headers: {
                "Content-Type": "application/vnd.api+json",
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            const status_code = response.status;
            response.json()
            .then(data=> {
                if (status_code !== 201) {
                    this.setState({errors: {
                        status: status_code,
                        error: data['errors']
                    }})
                } else {
                    this.setState({errors: null})
                    this.setState({secret_url: `http://127.0.0.1:3000/secret/${data['data']['attributes']['secret_key']}`})
                }
            })
        })
        .catch((err) => {
            console.log(err);
        })
    }

    render(){

        if (this.state.secret_url) {
            return <Redirect to={{
                pathname: '/success_creation',
                state: { secret_url: this.state.secret_url }
            }}/>
        }

        let error = null
        let description = null;

        if (this.state.errors !== null) {

            if(this.state.errors.error['secret_text']){
                description = `Secret Text: ${this.state.errors.error['secret_text']}`;
            } else if(this.state.errors.error['secret_word']){
                description = `Secret Word: ${this.state.errors.error['secret_word']}`;
            }  else if(this.state.errors.error['__all__']){
                description = `Time to Live: ${this.state.errors.error['__all__']}`;
            }

            error = <div className={EnterSecretStyles.errorform}> 
                        {this.state.errors.status}!  {description}
                    </div>
        }

        return (
            <React.Fragment>
                <Header/>
                <div className={EnterSecretStyles.container}>
                    {error}
                    <InfoField name="text" length="1000" rows="8" description="Enter your Secret(max 1000 symbols)" ChangeVal={this.SetParam}/>
                    <InfoField name="phrase" length="128" rows="3" description="Enter your Check Phrase(max 128 symbols)" ChangeVal={this.SetParam}/>
                    <Lifetime ChangeVal={this.SetParam}/>
                    <div className={EnterSecretStyles.sendbutton} onClick={this.SendToBackend}>
                        Send Secret!
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default EnterSecret