import axiosClient from './axiosClient';

export async function obtenerFichaMascota(idMascota) {
  const response = await axiosClient.get(`/mascotas/${idMascota}`);
  return response.data;
}