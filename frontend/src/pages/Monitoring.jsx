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

                    console.error(error);

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



    const total =
        metrics.monitor.total_jobs;


    const success =
        metrics.monitor.success_jobs;


    const successRate =
        total === 0
            ? 0
            : Math.round(
                (success / total) * 100
            );



    return (

        <div className="monitoring">


            <h1>
                System Monitoring
            </h1>



            <div className="monitor-card">

                <h2>
                    Queue Breakdown
                </h2>


                <p>
                    High Priority:
                    {" "}
                    {metrics.queue_sizes.high}
                </p>


                <p>
                    Medium Priority:
                    {" "}
                    {metrics.queue_sizes.medium}
                </p>


                <p>
                    Low Priority:
                    {" "}
                    {metrics.queue_sizes.low}
                </p>

            </div>




            <div className="monitor-card">

                <h2>
                    Worker Metrics
                </h2>


                {Object.entries(metrics.workers).map(
                    ([worker, jobs]) => (

                        <p key={worker}>

                            {worker}:

                            {" "}

                            {jobs} jobs processed

                        </p>

                    )
                )}

            </div>





            <div className="monitor-card">

                <h2>
                    System Health
                </h2>


                <p>
                    API Status:
                    🟢 ONLINE
                </p>


                <p>
                    Workers:
                    🟢 {Object.keys(metrics.workers).length}/
                    {Object.keys(metrics.workers).length}
                </p>


                <p>
                    Success Rate:
                    {successRate}%
                </p>


            </div>



        </div>

    );

}


export default Monitoring;