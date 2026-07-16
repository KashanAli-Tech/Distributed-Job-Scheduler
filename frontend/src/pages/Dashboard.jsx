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
                    value={metrics?.monitor?.total_jobs ?? 0}                />


                <StatCard 
                    title="Completed Jobs"
                    value={metrics?.monitor?.success_jobs ?? 0}
                />


                <StatCard 
                    title="Failed Jobs"
                    value={metrics?.monitor?.failed_jobs ?? 0}
                />


                <StatCard 
                    title="Running Jobs"
                    value="N/A"
                />

            </div>


            <h2>
                Worker Activity
            </h2>


            <WorkerCard
                name="Worker-1"
                status="RUNNING"
            />


            <WorkerCard
                name="Worker-2"
                status="IDLE"
            />


            <WorkerCard
                name="Worker-3"
                status="RUNNING"
            />

            <Charts metrics={metrics}/>

        </div>

    );

}


export default Dashboard;