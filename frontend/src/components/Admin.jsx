import React, {useState} from 'react'
import { useHistory } from "react-router-dom";
import { Input } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { Button } from 'antd';
import {url} from '../globalUrl'
import './Login.css'
import { message } from 'antd';
import admin from '../images/admin.jpg'

export default function Admin() {

    const[username, setUsername] = useState('');
    const[password, setPassword] = useState('');

    let history = useHistory();


    function submitHandle () {

        const data = {
            "username":username,
            "password":password
            }
        console.log('data', data)

        fetch( url + '/admin-login', {
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
                history.push('/admin-dashboard')
                return response.json()
            }
            else{
                message.error('Wrong Username or Password!');
            }
        })


      
    }

    return (
        <>
            <div className='candidates__ctr place__center' >

            <div className='candidates__header top__fix' >
                    <h1>Voting App Admin Panel</h1>
                </div>
       
                <div className='_center' >
                <div className='form__ctr' style={{height:'430px'}} >
                <div className="_center">
                    <img className='right' src={admin} alt='logo' ></img>
                    </div>
                    <h2>Admin Verification</h2>
           
                    <Input type='text' value={username} onChange={(e)=>setUsername(e.target.value)} size="large" placeholder="Enter Your Username" prefix={<UserOutlined />} />
                    <br/>
                               
                    <Input type='password' value={password} onChange={(e)=>setPassword(e.target.value)} size="large" placeholder="Enter Your Password" prefix={<UserOutlined />} />
                    <br/>
                <Button onClick={submitHandle} type="primary">Submit</Button>
                  

                </div>
                </div>



            </div>
        </>
    )
}
