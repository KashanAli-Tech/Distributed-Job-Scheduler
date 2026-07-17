function PriorityBadge({ priority }) {

    return (

        <span className={`priority-badge ${priority.toLowerCase()}`}>

            {priority}

        </span>

    );

}


export default PriorityBadge;