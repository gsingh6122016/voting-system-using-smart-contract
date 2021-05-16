import React from 'react'
import { Button } from 'antd';
import { useHistory } from "react-router-dom";
import {url} from '../globalUrl'
import { message } from 'antd';
import './AdminDashboard.css'
import logoutIcon from '../images/logout.png'
import stop from '../images/stop.png'
import result from '../images/result.png'
export default function AdminDashboard() {

    let history = useHistory();

    function logout () {
    history.replace('/');
    }

    function endHandle () {
        fetch( url + '/end', {
            method: 'POST',
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8',

            }
        })
        .then((response)=> {
            console.log('response', response)
            if (response['status'] === 201 || response['status'] === 200) {
                message.success('Election Ended!');
                return response.json()
            }
            else{
                message.error('Something went wrong!');
            }
        })
    }

    function viewResults() {
        history.push('/results')
    }

    


    return (
        <>
            <div className='candidates__ctr ' >

            <div className='candidates__header top__fix' >
                    <h1>Admin Dashboard</h1>
                </div>
       
                <div className='center_row' >
                <div className='dashboard_card' >
                <div className="_center">
                    <img className='right' src={result} alt='logo' ></img>
                    </div>
                    <h2>Show Results</h2>
                    <br/>
                <Button onClick={viewResults} type="primary">View </Button>
                  

                </div>
                <div className='dashboard_card' >
                <div className="_center">
                    <img className='right' src={stop} alt='logo' ></img>
                    </div>
                    <h2>End Election</h2>
                    <br/>
                <Button onClick={endHandle} type="primary">End </Button>
                  

                </div>
                <div className='dashboard_card' >
                <div className="_center">
                    <img className='right' src={logoutIcon} alt='logo' ></img>
                    </div>
                    <h2>Logout</h2>
                    <br/>
                <Button onClick={logout} type="primary">Logout </Button>
                  

                </div>
                </div>




            </div>
        </>
    )
}
