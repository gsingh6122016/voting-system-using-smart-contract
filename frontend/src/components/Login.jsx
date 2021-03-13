import React from 'react'
import { useHistory } from "react-router-dom";
import { Input } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { Button } from 'antd';
import './Login.css'

export default function Login() {

    let history = useHistory();

    function submitHandle () {
        history.push('/candidates')
    }

    return (
        <>
            <div className='candidates__ctr place__center' >

            <div className='candidates__header top__fix' >
                    <h1>Welcome to Blockchain based Voting App</h1>
                </div>
       
                <div className='_center' >
                <div className='form__ctr' >
                    <h2>Adhaar Verification</h2>
           
                    <Input type='number' size="large" placeholder="Enter Your Adhaar Number" prefix={<UserOutlined />} />
                    <br/>
                <Button onClick={submitHandle} type="primary">Submit</Button>
                  

                </div>
                </div>



            </div>
        </>
    )
}
