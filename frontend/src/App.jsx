import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { MachineProvider } from './contexts/MachineContext';
import Layout from './components/common/Layout';
import Dashboard from './components/dashboard/Dashboard';
import OperatorPanel from './components/operator/OperatorPanel';
import Login from './components/auth/Login';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <MachineProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/" element={<Layout />}>
                <Route index element={<Dashboard />} />
                <Route path="/operator/:machineId" element={<OperatorPanel />} />
              </Route>
            </Routes>
          </div>
        </Router>
      </MachineProvider>
    </AuthProvider>
  );
}

export default App;
