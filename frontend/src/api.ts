import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const generateReport = async (query: string) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate`, { query });
    return response.data;
  } catch (error) {
    console.error('Error generating report:', error);
    throw error;
  }
};
