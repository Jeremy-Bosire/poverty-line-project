import { Link } from 'react-router-dom';
import '../styles/Navbar.css'; 

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-logo">PovAware</Link>

      <div className="navbar-links">
        <Link to="/home" className="navbar-logo">🏠</Link>
        <Link to="/about" className="navbar-link">About</Link>
        <Link to="/features" className="navbar-link">Features</Link>
        <Link to="http://localhost:5000/login" className="navbar-cta">
            SignIn/SignUp
        </Link>
      </div>
    </nav>
  );
}
