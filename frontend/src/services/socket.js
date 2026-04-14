import { io } from 'socket.io-client';

// Connect to the Flask backend URL
const socket = io('http://127.0.0.1:5000');

export default socket;