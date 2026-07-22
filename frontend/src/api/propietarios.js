import axiosClient from './axiosClient';

export async function buscarPropietarioPorDni(dni) {
  const response = await axiosClient.get('/propietarios', {
    params: { dni },
  });
  return response.data;
}

export async function obtenerFichaCliente(idPropietario) {
  const response = await axiosClient.get(`/propietarios/${idPropietario}`);
  return response.data;
}