import { Link } from "react-router-dom";


function Sidebar() {
    return (
        <aside className="sidebar">

            <h2>
                Distributed Job Scheduler
            </h2>


            <nav>

                <Link to="/">
                    Dashboard
                </Link>


                <Link to="/jobs">
                    Jobs
                </Link>


                <Link to="/submit">
                    Submit Job
                </Link>


                <Link to="/monitoring">
                    Monitoring
                </Link>

            </nav>

        </aside>
    );
}


export default Sidebar;