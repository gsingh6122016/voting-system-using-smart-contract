import React, { useEffect, useState } from 'react'
import './Candidates.css'
import bjpIcon from '../images/bjp.png'
import incIcon from '../images/congress.png'
import cpimIcon from '../images/cpim.png'
import aapIcon from '../images/aap.png'
import notaIcon from '../images/nota.png'
import ssIcon from '../images/shivsenajpg.jpg'
import tmcIcon from '../images/tmc.png'
import 'antd/dist/antd.css';
import { Popconfirm, message } from 'antd';
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


export default function Candidates() {

    const [candidates, setCandidates] = useState([]);

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
                    setCandidates(result)
                }
            )

    }, [])


    function confirm(can_id) {

        let aid = localStorage.getItem('aid')
        let cid = can_id + 1

        const data = {
            "aadhaarID": parseInt(aid),
            "candidateID": cid
        }
        console.log('data', data)

        fetch(  url + '/vote', {
            method: 'POST',
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8',

            },
            body: JSON.stringify(data)
        })
            .then((response) => {
                console.log('response', response)
                if (response['status'] === 201 || response['status'] === 200) {
                    message.success('Vote Submitted Successfully!');
                    return response.json()
                }
                else {
                    message.error('Already Voted!');
                }
            })
            .then((result) => {
                console.log('result', result)

            })


    }

    function cancel(e) {
        console.log(e);
        message.error('Cancled by User');
    }

    return (
        <>
            <div className='candidates__ctr' >
                <div className='candidates__header' >
                    <h1>List of Candidates</h1>
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
                            <div className='row_3' style={{justifyContent:"flex-end"}} >
                                <h4>Action</h4>
                            </div>

                        </div>

                        {
                            candidates.map((result, index) => (
                                <div className='candidates__card' key={index} >

                                <div className='row_3' >
                                    <img className='party__icon' src={party_icons[result?.[2]]} alt='logo' ></img>
                                </div>

                                <div className='row_3'  >
                                    <h5>{result?.[1]}</h5>
                                </div>
                                <div className='row_3'  >
                                    <h5>{party_names[result?.[2]]}</h5>
                                </div>
                                <div className='row_3' style={{justifyContent:"flex-end"}} >
                                    <Popconfirm
                                        title="Are you sure to vote this candidate?"
                                        onConfirm={()=>confirm(index)}
                                        onCancel={cancel}
                                        okText="Yes"
                                        cancelText="No"
                                        placement="left"
                                    >
                                        <button className='btn btn-primary' > VOTE </button>
                                    </Popconfirm>
    
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
