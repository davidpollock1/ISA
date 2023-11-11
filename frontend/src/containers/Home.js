import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => (
    <div className='container'>
        <div className='mt-5 p-5 bg-light'>
            <h1 className='display-4'>Welcome to ThreePar</h1>
            <p className='lead'>
                The perfect way to schedule and manage your golf lessons!
            </p>
            <hr className='my-4'/>
            <p>Click the button below to log in.</p>
            <Link className='btn btn-primary btn-lg' to='/login'>Login</Link>
        </div>
    </div>
)

export default Home;