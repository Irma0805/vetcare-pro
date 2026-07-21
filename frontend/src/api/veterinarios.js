import axiosClient from './axiosClient';

export async function getVeterinarios(pagina = 1) {
  const response = await axiosClient.get('/veterinarios', {
    params: { pagina },
  });
  return response.data;
}

export async function createVeterinario(datos) {
  const response = await axiosClient.post('/veterinarios', datos);
  return response.data;
}