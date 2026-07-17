import { useState } from "react";
import axios from "axios";
import "../styles/submitJob.css";


function SubmitJob() {

    const [type, setType] = useState("math");
    const [priority, setPriority] = useState("MEDIUM");

    const [numbers, setNumbers] = useState("");
    const [duration, setDuration] = useState(1);
    const [text, setText] = useState("");

    const [message, setMessage] = useState("");



    const submitJob = async () => {


        let payload = {};



        if (type === "math") {


            payload = {

                data: numbers
                    .split(",")
                    .map(number => Number(number.trim()))
                    .filter(number => !isNaN(number))

            };


        }


        else if (type === "sleep") {


            payload = {

                duration: Number(duration)

            };


        }


        else if (type === "text") {


            payload = {

                text: text

            };


        }





        try {


            const response = await axios.post(

                "http://localhost:8000/submit-job",

                {
                    type,
                    priority,
                    payload
                }

            );



            setMessage(
                `Job submitted: ${response.data.job_id}`
            );


        }


        catch (error) {


            console.error(error);


            setMessage(
                "Failed to submit job"
            );


        }


    };





    return (


        <div className="submit-page">



            <h1>
                Submit Job
            </h1>





            <div className="submit-card">





                <div className="form-group">


                    <label>
                        Job Type
                    </label>



                    <select

                        value={type}

                        onChange={(e)=>setType(e.target.value)}

                    >


                        <option value="math">
                            Math
                        </option>


                        <option value="text">
                            Text
                        </option>


                        <option value="sleep">
                            Sleep
                        </option>


                    </select>


                </div>







                <div className="form-group">


                    <label>
                        Priority
                    </label>



                    <select

                        value={priority}

                        onChange={(e)=>setPriority(e.target.value)}

                    >


                        <option value="HIGH">
                            HIGH
                        </option>


                        <option value="MEDIUM">
                            MEDIUM
                        </option>


                        <option value="LOW">
                            LOW
                        </option>


                    </select>


                </div>







                <div className="form-group">


                    <label>
                        Payload
                    </label>





                    {type === "math" && (


                        <input

                            type="text"

                            value={numbers}

                            onChange={
                                (e)=>setNumbers(e.target.value)
                            }

                            placeholder="Example: 10,20,30"

                        />


                    )}






                    {type === "sleep" && (


                        <input

                            type="number"

                            value={duration}

                            onChange={
                                (e)=>setDuration(e.target.value)
                            }

                            placeholder="Duration"

                        />


                    )}






                    {type === "text" && (


                        <textarea

                            value={text}

                            onChange={
                                (e)=>setText(e.target.value)
                            }

                            placeholder="Enter text"

                        />


                    )}



                </div>







                <button

                    onClick={submitJob}

                >

                    Submit Job

                </button>





                {message && (


                    <p className="submit-message">

                        {message}

                    </p>


                )}




            </div>



        </div>


    );

}


export default SubmitJob;