import { useEffect, useState } from "react";
import { getJobs } from "../api/schedulerApi";


function Jobs() {

    const [jobs, setJobs] = useState([]);


    useEffect(() => {

        const fetchJobs = async () => {

            try {

                const response = await getJobs();

                setJobs(response.data);

            } catch (error) {

                console.error("Failed to fetch jobs:", error);

            }

        };


        fetchJobs();


        const interval = setInterval(fetchJobs, 3000);


        return () => clearInterval(interval);


    }, []);



    return (

        <div>

            <h1>
                Jobs
            </h1>


            <table>

                <thead>

                    <tr>

                        <th>ID</th>
                        <th>Type</th>
                        <th>Priority</th>
                        <th>Status</th>
                        <th>Retries</th>

                    </tr>

                </thead>


                <tbody>


                    {jobs.map((job) => (

                        <tr key={job.id}>

                            <td>
                                {job.id.substring(0, 6)}
                            </td>


                            <td>
                                {job.type}
                            </td>


                            <td>
                                {job.priority}
                            </td>


                            <td>
                                {job.status}
                            </td>


                            <td>
                                {job.retries}
                            </td>


                        </tr>

                    ))}


                </tbody>


            </table>


        </div>

    );

}


export default Jobs;