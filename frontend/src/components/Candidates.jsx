import React from 'react'
import './Candidates.css'
import bjpIcon from '../images/bjp.png'
import 'antd/dist/antd.css';
import { Popconfirm, message } from 'antd';

function confirm(e) {
    console.log(e);
    message.success('Vote Submitted Successfully!');
}

function cancel(e) {
    console.log(e);
    message.error('Cancled by User');
}

export default function Candidates() {
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

                        <div className='candidates__card' >

                            <div >
                                <img className='party__icon' src={bjpIcon} alt='logo' ></img>
                            </div>
                            <div  >
                                <h5>Dr. Ramesh Saxena</h5>
                            </div>
                            <div  >
                                <h5>Bharatiya Janta Party</h5>
                            </div>
                            <div >
                                <Popconfirm
                                    title="Are you sure to vote this candidate?"
                                    onConfirm={confirm}
                                    onCancel={cancel}
                                    okText="Yes"
                                    cancelText="No"
                                    placement="left"
                                >
                                    <button className='btn btn-primary' > VOTE </button>
                                </Popconfirm>
                                
                            </div>

                        </div>
                        <div className='candidates__card' >

                            <div >
                                <img className='party__icon' src={bjpIcon} alt='logo' ></img>
                            </div>
                            <div  >
                                <h5>Dr. Ramesh Saxena</h5>
                            </div>
                            <div  >
                                <h5>Bharatiya Janta Party</h5>
                            </div>
                            <div >
                                <button className='btn btn-primary' > VOTE </button>
                            </div>

                        </div>

                        <div className='candidates__card' >

                            <div >
                                <img className='party__icon' src={bjpIcon} alt='logo' ></img>
                            </div>
                            <div  >
                                <h5>Dr. Ramesh Saxena</h5>
                            </div>
                            <div  >
                                <h5>Bharatiya Janta Party</h5>
                            </div>
                            <div >
                                <button className='btn btn-primary' > VOTE </button>
                            </div>

                        </div>
                        <div className='candidates__card' >

                            <div >
                                <img className='party__icon' src={bjpIcon} alt='logo' ></img>
                            </div>
                            <div  >
                                <h5>Dr. Ramesh Saxena</h5>
                            </div>
                            <div  >
                                <h5>Bharatiya Janta Party</h5>
                            </div>
                            <div >
                                <button className='btn btn-primary' > VOTE </button>
                            </div>

                        </div>
                        <div className='candidates__card' >

                            <div >
                                <img className='party__icon' src={bjpIcon} alt='logo' ></img>
                            </div>
                            <div  >
                                <h5>Dr. Ramesh Saxena</h5>
                            </div>
                            <div  >
                                <h5>Bharatiya Janta Party</h5>
                            </div>
                            <div >
                                <button className='btn btn-primary' > VOTE </button>
                            </div>

                        </div>

                    </div>
                </div>
            </div>
        </>
    )
}
