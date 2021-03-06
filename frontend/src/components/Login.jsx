import React, {useState} from 'react'
import { useHistory } from "react-router-dom";
import { Input } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { Button } from 'antd';
import {url} from '../globalUrl'
import './Login.css'
import adr from '../images/adr.png'
import { message } from 'antd';

export default function Login() {

    const[adno, setAdno] = useState('');

    let history = useHistory();

    function submitHandle () {

        const data = {
            "aadhaarNo":adno,
            }
        console.log('data', data)

        fetch( url + '/login', {
            method: 'POST',
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8',

            },
            body: JSON.stringify(data)
        })
        .then((response)=> {
            console.log('response', response)
            if (response['status'] === 201 || response['status'] === 200) {
                message.success('Login Successfully!');
                return response.json()
            }
            else if (response['status'] === 401) {
                message.error('Already Voted!');
            }
            else{
                message.error('Election Ended!');
            }
        })
        .then((result) => {
            console.log('result', result)
            if(result) {
                localStorage.setItem('aid', result);
                   history.push('/candidates')
            }

        })

      
    }

    return (
        <>
            <div className='candidates__ctr place__center' >

            <div className='candidates__header top__fix' >
                    <h1>Welcome to Decentralized Voting System</h1>
                </div>
       
                <div className='_center' >
                <div className='form__ctr' style={{height:'370px'}} >
                <div className="_center">
                    <img className='right' src={adr} alt='logo' ></img>
                    </div>
                    <h2>Biometric Verification</h2>
           
                    <Input type='number' value={adno} onChange={(e)=>setAdno(e.target.value)} size="large" placeholder="Enter Your Adhaar Number" prefix={<UserOutlined />} />
                    <br/>
                <Button onClick={submitHandle} type="primary">Submit</Button>
                  

                </div>
                </div>



            </div>
        </>
    )
}
