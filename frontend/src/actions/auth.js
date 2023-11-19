import Cookies from 'js-cookie';
import axios from 'axios';
import {
    REGISTER_SUCCESS,
    REGISTER_FAIL,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT_SUCCESS,
    LOGOUT_FAIL,
} from './types';

export const login = (username, password) => async dispatch => {
    const csrfToken = Cookies.get('csrftoken');

    if (!csrfToken) {
        // Handle the scenario where the CSRF token is missing
        dispatch({
            type: REGISTER_FAIL,
        });
        return;
    }

    const config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        withCredentials: true,
    };

}

export const register = (username, password, re_password) => async dispatch => {
    const csrfToken = Cookies.get('csrftoken');

    if (!csrfToken) {
        // Handle the scenario where the CSRF token is missing
        dispatch({
            type: REGISTER_FAIL,
        });
        return;
    }

    const config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        withCredentials: true,
    };

    const body = JSON.stringify({ username, password, re_password });

    try {
        const res = await axios.post(`${process.env.REACT_APP_API_URL}/accounts/register`, body, config);

        if (res.data.error) {
            dispatch({
                type: REGISTER_FAIL
            });
        } else {
            dispatch({
                type: REGISTER_SUCCESS
            });
        }
    } catch (err) {
        dispatch({
            type: REGISTER_FAIL
        });
    }
};