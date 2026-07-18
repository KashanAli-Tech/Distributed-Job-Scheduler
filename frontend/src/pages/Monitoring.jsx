import { useEffect, useState } from "react";
import {getMetrics, getEvents, getRetries, getFailedJobs} from "../api/schedulerApi";

import "../styles/monitoring.css";


function Monitoring() {


    const [metrics, setMetrics] = useState(null);
    const [events, setEvents] = useState([]);
    const [retries, setRetries] = useState([]);
    const [failedJobs, setFailedJobs] = useState([]);


    useEffect(() => {


        const fetchMonitoring = async () => {


            try {


                const [
                    metricsResponse,
                    eventsResponse,
                    retriesResponse,
                    failedResponse

                ] = await Promise.all([

                    getMetrics(),
                    getEvents(),
                    getRetries(),
                    getFailedJobs()

                ]);



                setMetrics(metricsResponse.data);

                setEvents(eventsResponse.data);

                setRetries(retriesResponse.data);

                setFailedJobs(failedResponse.data);



            }

            catch(error) {

                console.error(
                    "Failed to load monitoring:",
                    error
                );

            }


        };



        fetchMonitoring();



        const interval = setInterval(
            fetchMonitoring,
            5000
        );



        return () => clearInterval(interval);



    }, []);




    if (!metrics) {

        return (

            <h1>
                Loading monitoring...
            </h1>

        );

    }




    const totalJobs =
        metrics.monitor.total_jobs;


    const successfulJobs =
        metrics.monitor.success_jobs;



    const successRate =
        totalJobs === 0
        ? 0
        :
        Math.round(
            (successfulJobs / totalJobs) * 100
        );




    return (


        <div className="monitoring">


            <h1>
                System Monitoring
            </h1>



            <div className="health-grid">


                <div className="monitor-card">

                    <h2>
                        System Health
                    </h2>


                    <p className="online">
                        OPERATIONAL
                    </p>


                    <p>
                        API: Online
                    </p>


                    <p>
                        Workers:
                        {" "}
                        {Object.keys(metrics.workers).length}
                    </p>


                </div>





                <div className="monitor-card">

                    <h2>
                        Success Rate
                    </h2>


                    <p className="metric-number">
                        {successRate}%
                    </p>


                    <p>
                        Completed:
                        {" "}
                        {successfulJobs}
                    </p>


                </div>



            </div>







            <h2>
                Queue Metrics
            </h2>



            <div className="queue-grid">


                {
                    Object.entries(metrics.queue_sizes)
                    .map(([queue,value]) => (


                        <div
                            className={`queue-card ${queue}`}
                            key={queue}
                        >


                            <span>
                                {queue.toUpperCase()}
                            </span>


                            <strong>
                                {value}
                            </strong>


                            <small>
                                waiting
                            </small>


                        </div>


                    ))
                }


            </div>







            <h2>
                Worker Cluster
            </h2>



            <div className="worker-grid">


                {
                    Object.entries(metrics.workers)
                    .map(([worker,jobs]) => (


                        <div
                            className="worker-monitor-card"
                            key={worker}
                        >


                            <h3>
                                {worker}
                            </h3>

                            <p>

                                {
                                    jobs > 0
                                    ? "🟢 ACTIVE"
                                    : "⚪ IDLE"
                                }

                            </p>



                            <p>
                                Jobs Processed:
                                {" "}
                                {jobs}
                            </p>


                        </div>


                    ))
                }


            </div>





            <h2>
                Runtime Statistics
            </h2>

            <div className="runtime-grid">


                <div className="runtime-card">

                    <span>
                        Total Jobs
                    </span>

                    <strong>
                        {metrics.monitor.total_jobs}
                    </strong>

                </div>




                <div className="runtime-card">

                    <span>
                        Successful
                    </span>

                    <strong>
                        {metrics.monitor.success_jobs}
                    </strong>

                </div>




                <div className="runtime-card">

                    <span>
                        Failed
                    </span>

                    <strong>
                        {metrics.monitor.failed_jobs}
                    </strong>

                </div>


            </div>


            <h2>
                Live Events
            </h2>


            <div className="event-list">


                {
                    events.length === 0

                    ?

                    <p>
                        No events available
                    </p>

                    :

                    events
                    .slice()
                    .reverse()
                    .map((event,index)=>(


                        <div
                            className={`event-card ${event.level.toLowerCase()}`}
                            key={index}
                        >


                            <div className="event-header">


                                <strong>
                                    {event.level}
                                </strong>


                                <span>
                                    {event.timestamp}
                                </span>


                            </div>


                            <p>
                                {event.message}
                            </p>


                        </div>


                    ))
                }


            </div>





            <h2>
                Retry History
            </h2>


            <div className="retry-grid">


                {
                    retries.length === 0

                    ?

                    <p>
                        No retries
                    </p>

                    :

                    retries.map((retry,index)=>(


                        <div
                            className="retry-card"
                            key={index}
                        >

                            <h3>
                                {retry.job_id.substring(0,6)}
                            </h3>


                            <p>
                                Attempt:
                                {" "}
                                {retry.attempt}/
                                {retry.max_retries}
                            </p>


                        </div>


                    ))
                }


            </div>





            <h2>
                Failed Jobs
            </h2>



            <div className="failed-grid">


                {
                    failedJobs.length === 0

                    ?

                    <p>
                        No failed jobs
                    </p>


                    :

                    failedJobs.map((job,index)=>(


                        <div
                            className="failed-card"
                            key={index}
                        >

                            <h3>
                                {job.type}
                            </h3>


                            <p>
                                {job.error}
                            </p>


                            <span>
                                Retries:
                                {" "}
                                {job.retries}
                            </span>


                        </div>


                    ))
                }


            </div>

        </div>


    );

}


export default Monitoring;