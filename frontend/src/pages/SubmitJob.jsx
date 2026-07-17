import { useState } from "react";
import axios from "axios";

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

            setMessage(`✅ Job submitted: ${response.data.job_id}`);

        }

        catch (error) {

            console.error(error);

            setMessage("❌ Failed to submit job");

        }

    };



    return (

        <div>

            <h1>Submit Job</h1>

            <label>Job Type: </label>

            <select
                value={type}
                onChange={(e) => setType(e.target.value)}
            >
                <option value="math">Math</option>
                <option value="sleep">Sleep</option>
                <option value="text">Text</option>
            </select>


            <br /><br />


            {type === "math" && (

                <>
                    <label>Numbers (comma separated): </label>

                    <input
                        type="text"
                        placeholder="10,20,30"
                        value={numbers}
                        onChange={(e) => setNumbers(e.target.value)}
                    />
                </>

            )}


            {type === "sleep" && (

                <>
                    <label>Duration (seconds): </label>

                    <input
                        type="number"
                        min="1"
                        value={duration}
                        onChange={(e) => setDuration(e.target.value)}
                    />
                </>

            )}


            {type === "text" && (

                <>
                    <label>Text</label>

                    <textarea
                        rows="4"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                    />
                </>

            )}


            <br /><br />


            <label>Priority: </label>

            <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
            >
                <option value="HIGH">HIGH</option>
                <option value="MEDIUM">MEDIUM</option>
                <option value="LOW">LOW</option>
            </select>


            <br /><br />


            <button onClick={submitJob}>

                Submit Job

            </button>


            <br /><br />


            <strong>{message}</strong>

        </div>

    );

}

export default SubmitJob;