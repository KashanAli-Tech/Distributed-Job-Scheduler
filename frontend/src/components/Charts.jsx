import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer
} from "recharts";


function Charts({ metrics }) {


    const queueData = [
        {
            name: "High",
            jobs: metrics?.queue_sizes?.high ?? 0
        },
        {
            name: "Medium",
            jobs: metrics?.queue_sizes?.medium ?? 0
        },
        {
            name: "Low",
            jobs: metrics?.queue_sizes?.low ?? 0
        }
    ];


    const resultData = [
        {
            name: "Success",
            jobs: metrics?.monitor?.success_jobs ?? 0
        },
        {
            name: "Failed",
            jobs: metrics?.monitor?.failed_jobs ?? 0
        }
    ];


    return (

        <div>


            <h2>
                Queue Status
            </h2>


            <ResponsiveContainer width="100%" height={300}>

                <BarChart data={queueData}>

                    <XAxis dataKey="name" />

                    <YAxis />

                    <Tooltip />

                    <Bar dataKey="jobs" />

                </BarChart>

            </ResponsiveContainer>



            <h2>
                Job Results
            </h2>


            <ResponsiveContainer width="100%" height={300}>

                <BarChart data={resultData}>

                    <XAxis dataKey="name" />

                    <YAxis />

                    <Tooltip />

                    <Bar dataKey="jobs" />

                </BarChart>

            </ResponsiveContainer>


        </div>

    );

}


export default Charts;