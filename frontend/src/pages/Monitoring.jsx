import { useEffect, useState } from "react";
import { getMetrics, getEvents, getRetries, getFailedJobs} from "../api/schedulerApi";

import "../styles/monitoring.css";


function Monitoring() {


    const [metrics, setMetrics] = useState(null);
    const [events, setEvents] = useState([]);
    const [retries, setRetries] = useState([]);
    const [failedJobs, setFailedJobs] = useState([]);


    useEffect(() => {


        const fetchMetrics = () => {


            getMetrics()

                .then(response => {

                    setMetrics(response.data);

                    getEvents()
                        .then(response => {
                            setEvents(response.data);
                        });


                    getRetries()
                        .then(response => {
                            setRetries(response.data);
                        });


                    getFailedJobs()
                        .then(response => {
                            setFailedJobs(response.data);
                        });

                })

                .catch(error => {

                    console.error(
                        "Failed to load monitoring:",
                        error
                    );

                });


        };



        fetchMetrics();



        const interval = setInterval(
            fetchMetrics,
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
            : Math.round(
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
                        🟢 OPERATIONAL
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
                        Completed Jobs:
                        {" "}
                        {successfulJobs}
                    </p>


                </div>



            </div>







            <h2>
                Queue Metrics
            </h2>



            <div className="queue-grid">


                <div className="queue-card high">

                    HIGH

                    <strong>
                        {metrics.queue_sizes.high}
                    </strong>

                    waiting

                </div>



                <div className="queue-card medium">

                    MEDIUM

                    <strong>
                        {metrics.queue_sizes.medium}
                    </strong>

                    waiting

                </div>




                <div className="queue-card low">

                    LOW

                    <strong>
                        {metrics.queue_sizes.low}
                    </strong>

                    waiting

                </div>


            </div>







            <h2>
                Worker Cluster
            </h2>



            <div className="worker-grid">


                {Object.entries(metrics.workers).map(
                    ([worker, jobs]) => (


                        <div
                            className="worker-monitor-card"
                            key={worker}
                        >


                            <h3>
                                {worker}
                            </h3>


                            <p>
                                Status:
                                {" "}

                                {jobs > 0
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


                    )
                )}


            </div>





            <h2>
                Runtime Statistics
            </h2>



            <div className="runtime-card">


                <p>
                    Total Jobs:
                    {" "}
                    {metrics.monitor.total_jobs}
                </p>


                <p>
                    Successful:
                    {" "}
                    {metrics.monitor.success_jobs}
                </p>


                <p>
                    Failed:
                    {" "}
                    {metrics.monitor.failed_jobs}
                </p>


            </div>


                <h2>
                    Live Events
                </h2>


                <div className="monitor-card">

                    {events.length === 0 ? (

                        <p>
                            No events available
                        </p>

                    ) : (

                        events.map((event, index) => (

                            <p key={index}>

                                {event.level === "SUCCESS" && "🟢"}

                                {event.level === "FAILED" && "🔴"}

                                {event.level === "RUNNING" && "🔵"}

                                {" "}

                                {event.message}

                            </p>

                        ))

                    )}

                </div>





                <h2>
                    Retry History
                </h2>


                <div className="monitor-card">


                    {retries.length === 0 ? (

                        <p>
                            No retries
                        </p>

                    ) : (

                        retries.map((retry, index) => (

                            <p key={index}>

                                Job:
                                {" "}
                                {retry.job_id.substring(0,6)}

                                {" | "}

                                Attempt:
                                {" "}
                                {retry.attempt}/
                                {retry.max_retries}

                            </p>

                        ))

                    )}


                </div>





                <h2>
                    Failed Jobs
                </h2>


                <div className="monitor-card">


                    {failedJobs.length === 0 ? (

                        <p>
                            No failed jobs
                        </p>

                    ) : (

                        failedJobs.map((job,index)=>(

                            <p key={index}>

                                {job.type}

                                {" | "}

                                Error:
                                {" "}
                                {job.error}

                                {" | Retries: "}

                                {job.retries}

                            </p>

                        ))

                    )}


                </div>

        </div>


    );

}


export default Monitoring;