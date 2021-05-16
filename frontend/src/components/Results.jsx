import React, { useEffect, useState } from 'react'
import bjpIcon from '../images/bjp.png'
import incIcon from '../images/congress.png'
import cpimIcon from '../images/cpim.png'
import aapIcon from '../images/aap.png'
import notaIcon from '../images/nota.png'
import ssIcon from '../images/shivsenajpg.jpg'
import tmcIcon from '../images/tmc.png'
import { url } from '../globalUrl';



let party_icons = {
    bjp: bjpIcon,
    inc: incIcon,
    cpi: cpimIcon,
    aap: aapIcon,
    nota: notaIcon,
    ss: ssIcon,
    aitc: tmcIcon,
  };

  let party_names = {
    bjp: "Bharatiya janta Party",
    inc: "Indian National Congress",
    cpi: "communist Party of India",
    aap: "Aam Aadmi Party",
    nota: "NOTA",
    ss: "Shiv Shena",
    aitc: "All India Trinamool Congress",
  };

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

                            <div className='row_3' >
                                <h4>Symbol</h4>
                            </div>
                            <div className='row_3' >
                                <h4>Candidate Name</h4>
                            </div>
                            <div className='row_3' >
                                <h4>Party Name</h4>
                            </div>
                            <div className='row_3' style={{justifyContent:"center"}} >
                                <h4>Votes</h4>
                            </div>

                        </div>

                        {
                            results.map(result=>(
                                <div className='candidates__card' >

                                <div className='row_3' >
                                    <img className='party__icon' src={party_icons[result?.[2]]} alt='logo' ></img>
                                </div>
                                <div className='row_3'  >
                                    <h5>{result?.[1]}</h5>
                                </div>
                                <div className='row_3' >
                                    <h5>{party_names[result?.[2]]}</h5>
                                </div>
                                <div className='row_3' style={{justifyContent:"center"}}  >
                                <h5>{result?.[3]}</h5>
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
