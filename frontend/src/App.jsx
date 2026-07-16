import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Jobs from "./pages/Jobs";
import SubmitJob from "./pages/SubmitJob";
import Monitoring from "./pages/Monitoring";
import JobDetails from "./pages/JobDetails";

import Layout from "./components/Layout";


function App() {
    return (
        <BrowserRouter>

            <Layout>

                <Routes>

                    <Route path="/" element={<Dashboard />} />

                    <Route path="/jobs" element={<Jobs />} />

                    <Route path="/submit" element={<SubmitJob />} />

                    <Route path="/monitoring" element={<Monitoring />} />

                    <Route path="/jobs/:id" element={<JobDetails />} />

                </Routes>

            </Layout>

        </BrowserRouter>
    );
}

export default App;