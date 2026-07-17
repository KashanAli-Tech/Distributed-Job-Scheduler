import { useEffect, useState } from "react";
import { getJobs } from "../api/schedulerApi";
import { useNavigate } from "react-router-dom";
import StatusBadge from "../components/StatusBadge";
import PriorityBadge from "../components/PriorityBadge";


function Jobs() {

    const [jobs, setJobs] = useState([]);

    const [search, setSearch] = useState("");

    const [statusFilter, setStatusFilter] = useState("ALL");

    const [priorityFilter, setPriorityFilter] = useState("ALL");


    const navigate = useNavigate();



    useEffect(() => {


        const fetchJobs = async () => {

            try {

                const response = await getJobs();

                setJobs(response.data);

            } catch (error) {

                console.error(
                    "Failed to fetch jobs:",
                    error
                );

            }

        };


        fetchJobs();


        const interval = setInterval(
            fetchJobs,
            3000
        );


        return () => clearInterval(interval);


    }, []);




    const filteredJobs = jobs.filter((job) => {


        const matchesSearch =
            job.id.includes(search) ||
            job.type.includes(search);



        const matchesStatus =
            statusFilter === "ALL" ||
            job.status === statusFilter;



        const matchesPriority =
            priorityFilter === "ALL" ||
            job.priority === priorityFilter;



        return (
            matchesSearch &&
            matchesStatus &&
            matchesPriority
        );

    });





    return (

        <div>


            <h1>
                Jobs
            </h1>



            <div>


                <input

                    type="text"

                    placeholder="Search jobs..."

                    value={search}

                    onChange={(e) =>
                        setSearch(e.target.value)
                    }

                />



                <select

                    value={statusFilter}

                    onChange={(e) =>
                        setStatusFilter(e.target.value)
                    }

                >

                    <option value="ALL">
                        All Status
                    </option>

                    <option value="SUCCESS">
                        Success
                    </option>

                    <option value="FAILED">
                        Failed
                    </option>

                    <option value="RUNNING">
                        Running
                    </option>

                    <option value="QUEUED">
                        Queued
                    </option>


                </select>




                <select

                    value={priorityFilter}

                    onChange={(e) =>
                        setPriorityFilter(e.target.value)
                    }

                >

                    <option value="ALL">
                        All Priority
                    </option>

                    <option value="HIGH">
                        High
                    </option>

                    <option value="MEDIUM">
                        Medium
                    </option>

                    <option value="LOW">
                        Low
                    </option>


                </select>


            </div>





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


                    {filteredJobs.map((job) => (


                        <tr

                            key={job.id}

                            onClick={() =>
                                navigate(`/jobs/${job.id}`)
                            }

                            style={{
                                cursor: "pointer"
                            }}

                        >


                            <td>
                                {job.id.substring(0, 6)}
                            </td>


                            <td>
                                {job.type}
                            </td>


                            <td>
                                <PriorityBadge priority={job.priority} />
                            </td>


                            <td>
                                <StatusBadge status={job.status} />

                            </td>


                            <td>
                                {job.retries}
                            </td>


                        </tr>


                    ))}



                </tbody>



            </table>



            {filteredJobs.length === 0 && (

                <p>
                    No jobs found
                </p>

            )}



        </div>

    );

}


export default Jobs;