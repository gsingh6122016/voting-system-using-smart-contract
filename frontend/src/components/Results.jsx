import React, { useEffect, useState } from 'react'
import bjpIcon from '../images/bjp.png'
import { url } from '../globalUrl';

export default function Results() {

    const [results, setResults] = useState([]);

    useEffect(() => {

        fetch(url + '/results', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then(res => res.json())
            .then(
                (result) => {
                    console.log('result', result)
                    setResults(result)
                }
            )

    }, [])

    return (
        <>
             <div className='candidates__ctr' >
                <div className='candidates__header' >
                    <h1>Election Results</h1>
                </div>
                <div className='candidates__body' >



                    <div className='candidates__cards' >

                        <div className='candidates__card__head' >

                            <div >
                                <h4>Symbol</h4>
                            </div>
                            <div  >
                                <h4>Candidate Name</h4>
                            </div>
                            <div  >
                                <h4>Party Name</h4>
                            </div>
                            <div >
                                <h4>Votes</h4>
                            </div>

                        </div>

                        {
                            results.map(result=>(
                                <div className='candidates__card' >

                                <div >
                                    <img className='party__icon' src={bjpIcon} alt='logo' ></img>
                                </div>
                                <div  >
                                    <h5>{result?.[1]}</h5>
                                </div>
                                <div  >
                                    <h5>Bharatiya Janta Party</h5>
                                </div>
                                <div >
                                <h5>{result?.[2]}</h5>
                                </div>
    
                            </div>
                            ))
                        }




                    </div>
                </div>
            </div>
        </>
    )
}
