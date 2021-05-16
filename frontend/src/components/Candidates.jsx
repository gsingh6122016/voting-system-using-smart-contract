import React, { useEffect, useState } from 'react'
import './Candidates.css'
import bjpIcon from '../images/bjp.png'
import 'antd/dist/antd.css';
import { Popconfirm, message } from 'antd';
import { url } from '../globalUrl';



export default function Candidates() {

    const [candidates, setCandidates] = useState([]);

    useEffect(() => {

        fetch(url + '/candidates_list', {
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
                                <h4>Action</h4>
                            </div>

                        </div>

                        {
                            candidates.map((candidate, index) => (
                                <div className='candidates__card' key={index} >

                                <div >
                                    <img className='party__icon' src={bjpIcon} alt='logo' ></img>
                                </div>
                                <div  >
                                    <h5>{candidate}</h5>
                                </div>
                                <div  >
                                    <h5>Bharatiya Janta Party</h5>
                                </div>
                                <div >
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
