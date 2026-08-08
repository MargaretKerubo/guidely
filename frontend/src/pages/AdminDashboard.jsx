import { useState } from 'react';
import Notification from '../components/Notification';
import UploadDocument from '../components/UploadDocument';
import IndexManager from '../components/IndexManager';

export default function AdminDashboard() {
  const [notification, setNotification] = useState({ type: '', message: '' });

  const showNotification = (type, message) => {
    setNotification({ type, message });
    setTimeout(() => setNotification({ type: '', message: '' }), 5000);
  };

  return (
    <div className="max-w-4xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
      <div className="mb-10 text-center animate-fade-in-up">
        <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight sm:text-5xl mb-4">
          Admin Dashboard
        </h1>
        <p className="text-xl text-gray-500">
          Manage your knowledge base documents and search index.
        </p>
      </div>

      <Notification
        type={notification.type}
        message={notification.message}
        onClose={() => setNotification({ type: '', message: '' })}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
        <UploadDocument showNotification={showNotification} />
        <IndexManager showNotification={showNotification} />
      </div>
    </div>
  );
}
