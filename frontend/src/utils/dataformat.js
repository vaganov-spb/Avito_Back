function dataformat(obj) {

    let seconds = (parseInt(obj['hours'], 10) || 0 )* 3600 + (parseInt(obj['minutes'], 10) || 0 ) * 60 + (parseInt(obj['seconds'], 10) || 0 );
    let days = parseInt(obj['days'], 10);

    return {
        "data": {
            "type": "Secret",
            "attributes": {
                "timedelta":{
                    "microseconds": 0,
                    "seconds": seconds ||  0,
                    "days": days || 0
                },
                "secret_text": obj['text'].trim() || '',
                "secret_word": obj['phrase'] || ''
            }
        }
    }
}

export default dataformat;