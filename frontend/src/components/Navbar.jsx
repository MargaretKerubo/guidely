import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();
  const isSearch = location.pathname === '/';
  const isAdmin = location.pathname === '/admin';

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center">
              <span className="text-2xl font-bold text-indigo-600">Guidely</span>
            </Link>
            <nav className="ml-10 flex space-x-8">
              <Link
                to="/"
                className={`${
                  isSearch
                    ? 'border-indigo-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
              >
                Search Dashboard
              </Link>
              <Link
                to="/admin"
                className={`${
                  isAdmin
                    ? 'border-indigo-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
              >
                Admin Management
              </Link>
            </nav>
          </div>
        </div>
      </div>
    </header>
  );
}
