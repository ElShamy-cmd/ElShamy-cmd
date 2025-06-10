import React from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

const ThreeDScene = () => {
    return (
        <Canvas>
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} />
            {/* Add your 3D models or elements here */}
            <OrbitControls />
        </Canvas>
    );
};

export default ThreeDScene;