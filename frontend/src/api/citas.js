import axiosClient from './axiosClient';

export async function getCitas(pagina = 1) {
  const response = await axiosClient.get('/citas', {
    params: { pagina },
  });
  return response.data;
}

export async function crearCita(datos) {
  const response = await axiosClient.post('/citas', datos);
  return response.data;
}

export async function cancelarCita(idCita) {
  const response = await axiosClient.post(`/citas/${idCita}/cancelar`);
  return response.data;
}