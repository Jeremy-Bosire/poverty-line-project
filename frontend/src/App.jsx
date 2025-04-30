import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import UserPage from './components/UserForm.jsx'
import OrganisationPage from './components/OrganisationPage.jsx'
import HomePage from './components/HomePage.jsx'
import FeaturesPage from './components/FeaturesPage.jsx'
import AboutPage from './components/AboutPage.jsx'
import Navbar from './components/Navbar.jsx'
import Footer from './components/Footer.jsx'

function App() {
  return (
    <Router>
    <Navbar />
  <main className="p-4">
    <Routes>
      <Route path="/" element={<h1>Welcome to PovAware</h1>} />
      <Route path="/userpage" element={<UserPage/>} />
      <Route path="/organisationpage" element={<OrganisationPage/>} />
      <Route path="/home" element={<HomePage/>} />
      <Route path="/features" element={<FeaturesPage/>} />
      <Route path="/about" element={<AboutPage/>} />
    </Routes>
  </main>
  <Footer/>
</Router>

  );
}


export default App
