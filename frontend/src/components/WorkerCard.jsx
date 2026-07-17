function WorkerCard({ name, status, jobs }) {

    return (

        <div className="worker-card">


            <h3>
                {name}
            </h3>


            <p className={
                status === "RUNNING"
                    ? "worker-status active"
                    : "worker-status idle"
            }>

                ● {status}

            </p>



            <div className="worker-info">

                <span>
                    Jobs processed
                </span>


                <strong>
                    {jobs ?? 0}
                </strong>

            </div>


        </div>

    );

}


export default WorkerCard;