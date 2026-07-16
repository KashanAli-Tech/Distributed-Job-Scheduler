import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Jobs from "./pages/Jobs";
import SubmitJob from "./pages/SubmitJob";
import Monitoring from "./pages/Monitoring";
import JobDetails from "./pages/JobDetails";


function App() {
    return (
        <BrowserRouter>

            <Routes>

                <Route path="/" element={<Dashboard />} />

                <Route path="/jobs" element={<Jobs />} />

                <Route path="/submit" element={<SubmitJob />} />

                <Route path="/monitoring" element={<Monitoring />} />

                <Route path="/jobs/:id" element={<JobDetails />} />

            </Routes>

        </BrowserRouter>
    );
}

export default App;