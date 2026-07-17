import axios from "axios";


const API = axios.create({

    baseURL: "http://localhost:8000"

});


export const getMetrics = () => {

    return API.get("/metrics");

};

export const getJobs = () => {

    return API.get("/jobs");

};

export const getEvents = () => {

    return API.get("/events");

};


export const getRetries = () => {

    return API.get("/retries");

};


export const getFailedJobs = () => {

    return API.get("/failed-jobs");

};