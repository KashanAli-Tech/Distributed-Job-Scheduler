import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import StatusBadge from "../components/StatusBadge";
import PriorityBadge from "../components/PriorityBadge";


function JobDetails() {

    const { id } = useParams();
    const [job, setJob] = useState(null);


    useEffect(() => {

        const fetchJob = async () => {

            try {

                const response = await fetch(
                    `http://localhost:8000/job/${id}`
                );

                const data = await response.json();
                setJob(data);


            } catch (error) {

                console.error(
                    "Failed to fetch job:",
                    error
                );

            }

        };


        fetchJob();


    }, [id]);



    if (!job) {

        return (
            <h2>
                Loading job details...
            </h2>
        );

    }



    return (

        <div className="job-details">


            <h1>
                Job Details
            </h1>



            <div className="details-card">


                <p>
                    ID: {job.id}
                </p>


                <p>
                    Type: {job.type}
                </p>


                <p>
                    Priority: {" "}
                    <PriorityBadge
                        priority={job.priority}
                    />
                </p>


                <p>
                    Status: {" "}
                    <StatusBadge
                        status={job.status}
                    />
                </p>


                <p>
                    Retries: {job.retries}
                </p>


            </div>




            <div className="details-section">

                <h2>
                    Payload
                </h2>


                <div className="details-card">

                    {Object.entries(job.payload || {}).map(([key, value]) => (

                        <p key={key}>
                            {key}: {Array.isArray(value)
                                ? value.join(", ")
                                : value
                            }
                        </p>

                    ))}

                </div>

            </div>





            <div className="details-section">

                <h2>
                    Result
                </h2>


                <div className="details-card">

                    {Object.entries(job.result || {}).map(([key, value]) => (

                        <p key={key}>
                            {key}: {Array.isArray(value)
                                ? value.join(", ")
                                : value
                            }
                        </p>

                    ))}

                </div>

            </div>



        </div>

    );

}


export default JobDetails;