import React from 'react';
import { Redirect } from 'react-router-dom';
import Header from '../components/Header';
import GetSecretFormStyles from '../styles/GetSecretForm.module.css';
import InfoField from '../components/InfoField';

class GetSecretForm extends React.Component {

    constructor(props) {
        super(props);
        this.secret_key = this.props.match.params.secret_key;
        this.state = {
            errors: null,
            phrase: '',
            text: '',
        };
        this.SetPhrase = this.SetPhrase.bind(this);
        this.GetSecret = this.GetSecret.bind(this);
    }

    componentDidMount() {
        fetch(`http://localhost:8000/secret/check/${this.secret_key}/`)
            .then(response => {
                const status_code = response.status;
                response.json()
                    .then(data => {
                        console.log(data)
                        if (status_code !== 200){
                            this.setState({errors: {
                                status: status_code,
                                error: data['errors'],
                            }}, () => {
                                console.log(this.state)
                            })
                        }
                    })
            })
    }

    SetPhrase(parametr, value) {
        switch(parametr) {
            case 'phrase':
                this.setState({phrase: value});
                break;
            default:
                break;
        }   
    }

    GetSecret(){
        fetch(`http://localhost:8000/secret/${this.secret_key}/`, {
            method: "POST",
            // credentials: "include",
            headers: {
                "Content-Type": "application/vnd.api+json",
            },
            body: JSON.stringify(
                {
                    "data": {
                        "type": "Secret",
                        "attributes": {
                            "secret_word": this.state.phrase.trim() || ''
                        }
                    }
                })
        })
        .then(response => {
            const status_code = response.status;
            response.json()
            .then(data=> {
                console.log(data);
                if (status_code !== 200) {
                    this.setState({errors: {
                        status: status_code,
                        error: data['errors']
                    }})
                } else {
                    this.setState({errors: null})
                    this.setState({text: data['data']})
                }
            })
        })
        .catch((err) => {
            console.log(err);
        })
    }

    render() {
        let description = null;

        if(this.state.text) {
            return <Redirect to={{
                pathname: '/success_get_secret',
                state: { secret: this.state.text }
            }}/>
        }

        if (this.state.errors !== null) {
            description = <div className={GetSecretFormStyles.errorform}>
                    {this.state.errors.status}! {this.state.errors.error}
                </div>
        } else {
            description = <React.Fragment>
                    <div className={GetSecretFormStyles.notation}> ENTER VALID CODE PHRASE BELOW:</div>
                    <InfoField name="phrase" length="128" rows="3" description="Enter your Check Phrase(max 128 symbols)" placeholder="Type your code phrase here.." ChangeVal={this.SetPhrase}/>
            </React.Fragment>

        }

        return (
            <React.Fragment>
                <Header/>
                <div className={GetSecretFormStyles.container}>
                    {description}
                    <div className={GetSecretFormStyles.sendbutton} onClick={this.GetSecret}>
                            Get Secret!
                    </div>
                </div>    
            </React.Fragment>
        );
    }

}

export default GetSecretForm;