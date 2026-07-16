import Sidebar from "./Sidebar";


function Layout({ children }) {

    return (

        <div className="app-container">

            <Sidebar />

            <main className="content">

                {children}

            </main>

        </div>

    );

}


export default Layout;