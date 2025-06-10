import React from 'react';
import ThreeDScene from './components/ThreeDScene';
import './styles/main.css';

const App = () => {
    return (
        <div className="App">
            <h1>Welcome to the 3D Web Application</h1>
            <ThreeDScene />
        </div>
    );
};

export default App;