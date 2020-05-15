import React from 'react';
import InfoFields from '../styles/InfoFields.module.css';

function InfoField(props) {
    function onChange(event) {
        props.ChangeVal(props.name, event.target.value)
    }

    return (
        <div className={InfoFields.wrapper}>
            <textarea 
                className={InfoFields.name} 
                onChange={(e) => onChange(e)} 
                placeholder="Write here...."  
                maxLength={props.length}
                rows={props.rows}
            />
            <div className={InfoFields.userlen}> {props.description} </div>
        </div>
    );
}

export default InfoField