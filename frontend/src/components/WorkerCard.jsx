function WorkerCard({ name, status }) {
    return (
        <div className="worker-card">

            <h3>{name}</h3>

            <p>{status}</p>

        </div>
    );
}

export default WorkerCard;