import axiosClient from './axiosClient';

export async function getCitas(pagina = 1) {
  const response = await axiosClient.get('/citas', {
    params: { pagina },
  });
  return response.data;
}