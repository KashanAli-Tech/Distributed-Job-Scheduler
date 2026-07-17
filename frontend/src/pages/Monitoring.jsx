import { useEffect, useState } from "react";
import { getMetrics } from "../api/schedulerApi";

import "../styles/monitoring.css";


function Monitoring() {


    const [metrics, setMetrics] = useState(null);



    useEffect(() => {


        const fetchMetrics = () => {


            getMetrics()

                .then(response => {

                    setMetrics(response.data);

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



        </div>


    );

}


export default Monitoring;