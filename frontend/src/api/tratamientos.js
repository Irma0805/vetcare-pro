import axiosClient from './axiosClient';

export async function getTratamientos() {
  const response = await axiosClient.get('/tratamientos');
  return response.data;
}