import { useEffect, useState } from "react";
import { getMetrics } from "../api/schedulerApi";

import StatCard from "../components/StatCard";
import WorkerCard from "../components/WorkerCard";
import Charts from "../components/Charts";


function Dashboard() {

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


        const interval = setInterval(fetchMetrics, 5000);


        return () => clearInterval(interval);


    }, []);



    if (!metrics) {

        return (
            <h1>
                Loading dashboard...
            </h1>
        );

    }



    const queueSize =
        metrics.queue_sizes.high +
        metrics.queue_sizes.medium +
        metrics.queue_sizes.low;



    return (

        <div>


            <h1>
                Dashboard
            </h1>



            <h2>
                Scheduler Status: ONLINE 🟢
            </h2>




            <div>


                <StatCard
                    title="Total Jobs"
                    value={metrics.monitor.total_jobs}
                />


                <StatCard
                    title="Completed Jobs"
                    value={metrics.monitor.success_jobs}
                />


                <StatCard
                    title="Failed Jobs"
                    value={metrics.monitor.failed_jobs}
                />


                <StatCard
                    title="Queue Size"
                    value={queueSize}
                />


            </div>





            <h2>
                Worker Activity
            </h2>




            <div>


                {Object.entries(metrics.workers).map(
                    ([worker, jobs]) => (

                        <WorkerCard
                            key={worker}
                            name={worker}
                            status={
                                jobs > 0
                                    ? "RUNNING"
                                    : "IDLE"
                            }
                        />

                    )
                )}


            </div>




            <Charts metrics={metrics}/>



        </div>

    );

}


export default Dashboard;